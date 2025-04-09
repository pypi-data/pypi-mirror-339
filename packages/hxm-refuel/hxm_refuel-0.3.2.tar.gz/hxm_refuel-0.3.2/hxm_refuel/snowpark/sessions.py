""" Collection of functions related to instantiating a Snowpark Session """
import os
import toml
from snowflake.snowpark.session import Session
from .rsa import rsa_token_stuff


def secrets_from_toml(path: str=".streamlit/secrets.toml"):
    """
    Create a Secrets Dictionary from a toml file.

    :param path: The path to the toml file.
    :returns: Dictionary object of secrets.

    Assumption is the file structure will look something like this:
        [snowflake_rsa_user_details]
        user = "SNOWFLAKE_USER"
        password = ""
        account = "SNOWFLAKE_ACCOUNT"
        region = "eu-west-1"
        warehouse = "LAB_SOMETHING_WH"
        database = "LAB_SOMETHING"
        schema = ""
        private_key_password = "THE_PASSWORD_STRING"
    """
    return toml.load(path)


def create_session_dynamic_spcs(
        secrets_path: str = ".streamlit/secrets.toml",
        secrets_key: str = "snowflake_rsa_user_details",
        private_key: str = "private_key_password",
        private_key_path: str = '.streamlit/snowflake_rsa_key.p8'):
    """
    """

    # fetch secrets from file
    secrets = secrets_from_toml(secrets_path)

    # next step is a bit of a cludge
    # a container will contain 'SNOWFLAKE_ACCOUNT' in the os.environ & we assume it won't be there otherwise
    # so we use that to route to a session builder function
    if 'SNOWFLAKE_ACCOUNT' in os.environ.keys():
        print("'SNOWFLAKE_ACCOUNT in `os.environ`; logging in with OAuth")
        return create_container_oauth_session(
            secrets=secrets,
            secrets_key=secrets_key,
        )
    else:
        print("'SNOWFLAKE_ACCOUNT' not in `os.environ`; assume local env & logging in with RSA" )
        return create_rsa_session(
            secrets=secrets,
            secrets_key=secrets_key,
            private_key_path=private_key_path,
        )


def create_rsa_session(
        secrets,
        password: str = None,
        secrets_key: str = "snowflake_rsa_user_details",
        private_key_path: str = '.streamlit/snowflake_rsa_key.p8',
        private_password_key: str = 'private_key_password'):
    """
    Create snowpark session from RSA key

    :param secrets (dict): generally from secrets.toml file
    :param password (str): password for the RSA key
    :param secrets_key (str): key within dict to access secrets like user, database etc...
    :param private_key_path (str): path to private key for the RSA key

    """
    pkb = rsa_token_stuff(
        password=secrets[secrets_key][private_password_key],
        private_key_file=private_key_path,
    )

    # append private key to secrets to create credentials
    credentials = dict(secrets[secrets_key]) | {'private_key': pkb}
    session = Session.builder.configs(credentials).create()
    return session

def get_login_token():
    """  Get OAuth Token from Streamlit Container
    SPCS creates a file at /snowflake/session/token with an authorisation token
    https://docs.snowflake.com/en/developer-guide/snowpark-container-services/additional-considerations-services-jobs
    """
    with open('/snowflake/session/token', 'r') as f:
        return f.read()

def create_container_oauth_session(
        secrets,
        secrets_key: str = 'snowflake_rsa_user_details'):
    """
    Create a Snowpark Session using OAuth credentials.

    Required when connecting to a Snowflake Database with a Snowflake Container Service.
    Snowflake restrict use of RSA etc. within the container and force use of an OAuth token.
    The OAuth token can be found within the container itself, but changes frequently.
    The container also contains details in the environment variables like SNOWFLAKE_ACCOUNT.

    :param: secrets_path (str): path to toml secrets file structured as a toml
    :param: toml_key (str): key within the secrets file
    """

    # Build the configuration dictionary for OAuth authentication.
    # within a container many details are provided as environment variables
    config = {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "region": secrets[secrets_key].get("region", "eu-west-1"),
        "authenticator": "oauth",
        "token": get_login_token(),
        "warehouse": secrets[secrets_key]["warehouse"],
        "database": secrets[secrets_key]["database"],
        "schema": secrets[secrets_key].get("schema", ""),
        "client_session_keep_alive": True,
    }

    # Create and return the Snowpark Session.
    return Session.builder.configs(config).create()
