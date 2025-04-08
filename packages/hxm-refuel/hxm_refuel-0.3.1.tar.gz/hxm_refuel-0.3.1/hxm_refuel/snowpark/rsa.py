""" """
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def rsa_token_stuff(password: str, private_key_file="rsa_key.p8"):
    """ Create RSA Tokens

    For RSA we require 2 things:
        1. a password, which is a string and should be private saved in os.env or whatever
        2. a private key, which is a .p8 file and wil have a form like below

            -----BEGIN ENCRYPTED PRIVATE KEY-----
            MIIFHzBJBgkqhkiG9w0BBQ0wPDAbBgkqhkiG9w0BBQwwDgQIxIoCnzcfizcCAggA
            BUTthisLINEwillGOonFOR20or30linesOFnonsense!Basdgers&WeaselsROCK
            -----END ENCRYPTED PRIVATE KEY-----

    INPUTS:
        password: str: something of the form "pleasechangemepassphraseZXCs1234"
        private_key_file: str: file path to "rsa_key.p8" file
    """

    assert isinstance(private_key_file, str), f"private key file needs to be a string: {type(private_key_file)}"

    with open(private_key_file, "rb") as key:
        p_key = serialization.load_pem_private_key(
            key.read(),
            password=password.encode('utf-8'),
            backend=default_backend(),
        )

        pkb = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

    return pkb
