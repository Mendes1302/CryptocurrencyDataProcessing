import sqlite3
from typing import Optional
import pandas as pd

class Sqlite():
    """
    A class to interact with an SQLite database, supporting basic operations
    such as querying, inserting, updating, and closing the connection.
    """
    def __init__(self, database: str) -> None:
        """
        Initializes the Sqlite class with the given database path.

        Args:
            database (str): The path to the SQLite database file.
        """
        self.database = database
        self.conn = None
        self.cur = None
        self.__connect()

    def __connect(self) -> None:
        """
        Establishes the connection to the SQLite database and creates a cursor.
        """
        try:
            self.conn = sqlite3.connect(self.database)
            self.cur = self.conn.cursor()
        except sqlite3.Error as error:
            print(f"Failed to connect to database {self.database}: {error}")

    def get(self, query: str) -> Optional[pd.DataFrame]:
        """
        Executes a SELECT query and returns the results as a pandas DataFrame.

        Args:
            query (str): The SQL SELECT query to execute.

        Returns:
            Optional[pd.DataFrame]: A pandas DataFrame containing the query results, or None if an error occurs.

        Raises:
            sqlite3.Error: If there is an error executing the query.
        """
        try:
            self.cur.execute(query)
            columns = [desc[0] for desc in self.cur.description]
            rows = self.cur.fetchall()
            return pd.DataFrame(rows, columns=columns)
        except sqlite3.Error as error:
            print(f"Error executing query: {query}. {error}")
            return None

    def insert(self, query: str) -> None:
        """
        Executes an INSERT query.

        Args:
            query (str): The SQL INSERT query to execute.

        Returns:
            None

        Raises:
            sqlite3.Error: If there is an error executing the insert query.
        """
        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as error:
            print(f"Error executing insert query: {query}. {error}")

    def update(self, query: str) -> None:
        """
        Executes an UPDATE query.

        Args:
            query (str): The SQL UPDATE query to execute.

        Returns:
            None

        Raises:
            sqlite3.Error: If there is an error executing the update query.
        """
        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as error:
            print(f"Error executing update query: {query}. {error}")

    def close(self) -> None:
        """
        Closes the connection to the SQLite database.

        Returns:
            None
        """
        if self.conn:
            self.conn.close()