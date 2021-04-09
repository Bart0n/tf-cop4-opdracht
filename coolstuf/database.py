import sqlite3
import os
from coolstuf import color as c


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print("DB Error - Create Connection")
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
                                            open_port text,
                                            closed_port text
                                        ); """
        conn.execute(create_table_scanner)
    except sqlite3.Error as e:
        print("DB Error - Create Table")
        print(e)


def insert_data(conn, date, ip, scan_type, port_range, open_port, closed_port):
    try:
        # Insert the data into the table
        sql = '''
        INSERT INTO scanner(date, ip, type, port_range, open_port, closed_port)
        VALUES (?,?,?,?,?,?)
        '''
        cur = conn.cursor()
        data_for_db = date, ip, scan_type, port_range, open_port, closed_port
        cur.execute(sql, data_for_db)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print("DB Error - Insert Data")
        print(e)


def delete_db(database_file):
    # Check if the database exist
    if os.path.exists(database_file):
        try:
            os.remove(database_file)
            print(f"\n{c.C.YELLOW}[✓]{c.C.END} Database removed!\n")
        except:
            print(f"\n{c.C.RED}[✖]{c.C.END} Cannot delete database file, maybe it is in use?")
            exit()
    else:
        print(f"\n{c.C.RED}[✖]{c.C.END} Requested to delete the database, but database does not exist yet.")
        exit()
