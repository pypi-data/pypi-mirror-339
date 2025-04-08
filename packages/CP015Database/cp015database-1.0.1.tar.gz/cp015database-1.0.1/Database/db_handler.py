import mysql.connector
import csv


class DBdata:
    """
    A generic database handler for CRUD operations.
    Supports dynamic tables and simple CSV import.
    """

    def __init__(self):
        """
        Prompt user for database connection details.
        """
        host = input("Enter database host (default: localhost): ") or "localhost"
        user = input("Enter database user (default: root): ") or "root"
        password = input("Enter database password (default: admin): ") or "admin"
        database = input("Enter database name (default: agro): ") or "agro"

        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            exit(1)

    def insert_csv(self, filename):
        """
        Insert data from a CSV file into a table.
        The filename (without extension) is used as the table name.
        The first column is the primary key.
        """
        table_name = filename.split('.')[0]

        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Get column names

            primary_key = headers[0]  # First column is the primary key
            columns = ', '.join(headers)
            placeholders = ', '.join(['%s'] * len(headers))

            # Create table if not exists
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {primary_key} VARCHAR(255) PRIMARY KEY,
                {', '.join(f'{col} TEXT' for col in headers[1:])}
            )
            """
            self.cursor.execute(create_table_sql)

            # Insert data with error handling
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            for row in reader:
                try:
                    self.cursor.execute(insert_sql, row)
                except mysql.connector.IntegrityError as err:
                    print(f"Duplicate entry error in {table_name}: {err}")
                except mysql.connector.Error as err:
                    print(f"Error inserting into {table_name}: {err}")

            self.conn.commit()
            print(f"Data inserted into {table_name} successfully.")

    def insert_data(self, table_name, data_obj):
        """
        Insert data into any specified table using a generic object.
        :param table_name: Name of the table to insert into.
        :param data_obj: Instance of TableData containing column values.
        """
        if not hasattr(data_obj, "__dict__"):
            print("Error: Data must be an object with attributes.")
            return

        try:
            data_dict = vars(data_obj)
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join(['%s'] * len(data_dict))
            values = tuple(data_dict.values())

            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"Data inserted successfully into {table_name}.")

        except mysql.connector.IntegrityError as err:
            print(f"Duplicate entry error in {table_name}: {err}")
        except mysql.connector.Error as err:
            print(f"Error inserting into {table_name}: {err}")

    def execute_sql(self, sql, params=None):
        """
        Execute any SQL query passed as a parameter.
        :param sql: The SQL query to execute.
        :param params: Tuple of parameters if needed.
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)

            if sql.strip().upper().startswith("SELECT"):
                results = self.cursor.fetchall()
                for row in results:
                    print(row)
                return results

            self.conn.commit()
            print("SQL executed successfully.")

        except mysql.connector.Error as err:
            print(f"Error executing SQL: {err}")

    def close_connection(self):
        """ Close the database connection. """
        self.cursor.close()
        self.conn.close()


class TableData:
    """
    Generic class to represent any table data.
    Attributes are set dynamically using keyword arguments.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)



