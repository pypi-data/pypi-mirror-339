""" """
from snowflake.snowpark import Session
import pandas as pd


def sql_append_with_drop_duplicates(
        session: Session,
        df: pd.DataFrame,
        table_name: str,
        cols: list | set | tuple,
        delete_stage: bool = True):
    """
    Append to Snowflake Table using Snowpark while Dropping Duplicates.

    Approach:
    1. Upload the DataFrame to a staging table.
    2. Remove duplicates from the original table based on the specified columns.
    3. Append the new DataFrame to the original table.

    """
    assert isinstance(cols, (list, set, tuple)), f"cols must be list|set|tuple, but got {type(cols)}"

    # Convert DataFrame to Snowpark DataFrame
    snowpark_df = session.create_dataframe(df)

    # Define staging table name
    staging_table_name = f"{table_name}_STAGE"

    # Create or replace the staging table
    snowpark_df.write.save_as_table(staging_table_name, mode="overwrite")

    # Generate the DELETE query to remove duplicates from the original table
    cols_str = ", ".join(f'"{col}"' for col in cols)
    query_delete = f"""
        DELETE FROM {table_name}
        WHERE ({cols_str}) 
        IN (SELECT {cols_str} FROM {staging_table_name})"""
    session.sql(query_delete).collect()

    # Append the new data to the original table using SQL
    query_insert = f"""
        INSERT INTO {table_name}
        SELECT * 
        FROM {staging_table_name}"""
    session.sql(query_insert).collect()

    # Optionally drop the staging table
    if delete_stage:
        session.sql(f"DROP TABLE {staging_table_name}").collect()

    return True
