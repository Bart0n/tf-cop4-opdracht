import sqlite3
import os


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn):
    try:
        # Create table 'scanner' if it does not exist.
        conn.cursor()
        create_table_scanner = """ CREATE TABLE IF NOT EXISTS scanner (
                                            date text,
                                            ip text,
                                            type text,
                                            port_range text,
                                            result text
                                        ); """
        conn.execute(create_table_scanner)
    except sqlite3.Error as e:
        print(e)


def insert_data(conn, data):
    try:
        # Insert the data into the table
        sql = '''
        INSERT INTO scanner(date, ip, type, port_range, result)
        VALUES (?,?,?,?,?)
        '''
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(e)


def delete_db(database_file):
    # Check if the database exist
    if os.path.exists(database_file):
        try:
            os.remove(database_file)
        except:
            print("Cannot delete database file, maybe it is in use?")
            exit()
    else:
        print("Requested to delete the database, but database does not exist yet.")
        exit()
