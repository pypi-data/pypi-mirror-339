import os
import sys
import sqlite3

from datetime import datetime
from pathlib import Path

tablename = "sessions"

sql = f"""
CREATE TABLE IF NOT EXISTS {tablename} (
    uuid TEXT PRIMARY KEY,
    datetime TEXT NOT NULL,
    user TEXT NOT NULL,
    workdir TEXT NOT NULL,
    pid INTEGER NOT NULL,
    ppid INTEGER NOT NULL,
    args TEXT NOT NULL
);
"""

sql_op = """
CREATE TABLE IF NOT EXISTS op (
    session TEXT NOT NULL,
    timedate TEXT NOT NULL,
    pathtype TEXT NOT NULL,
    path TEXT NOT NULL,
    status TEXT NOT NULL,
    errmsg TEXT
);
"""

sql_insert = f"""
INSERT INTO {tablename} (uuid, datetime, user, workdir, pid, ppid, args)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

sql_insert_op = """
INSERT INTO op (session, timedate, pathtype, path, status, errmsg)
VALUES (?, ?, ?, ?, ?, ?);
"""


class DB:
    def __init__(self, uuid):
        self.uuid = str(uuid)

        home = Path.home()
        dbdir = os.path.join(home, ".local", "state", "ngm", "logs")
        dbpath = os.path.join(dbdir, "remove.db")

        os.makedirs(dbdir, exist_ok=True)

        self.conn = sqlite3.connect(dbpath)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.execute(sql_op)
        self.conn.commit()
        self.init()

    def __del__(self):
        # print(f"Session: {self.uuid}")
        self.conn.close()

    def init(self):
        # Get current datetime
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        args = " ".join(sys.argv)

        pid = os.getpid()
        ppid = os.getppid()
        user = os.getlogin()
        workdir = os.getcwd()

        # Execute the SQL query with the provided parameters
        self.conn.execute(sql_insert, (self.uuid, dt, user, workdir, pid, ppid, args))
        self.conn.commit()

    def insert(self, pathtype, path, status, errmsg=None):
        # Get current datetime
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.conn.execute(
            sql_insert_op, (self.uuid, dt, pathtype, path, status, errmsg)
        )
        self.conn.commit()
