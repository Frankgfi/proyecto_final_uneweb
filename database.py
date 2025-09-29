import mysql.connector

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306
}

DB_NAME = 'proyecto_inv'

def main():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"Base de datos '{DB_NAME}' creada o ya existe.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()