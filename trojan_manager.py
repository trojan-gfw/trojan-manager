#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Radius MySQL Account Controller
Dev: K4YT3X
Date Created: July 8, 2018
Last Modified: July 8, 2018

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt
(C) 2018 K4YT3X
"""
import hashlib
import MySQLdb
import sys

VERSION = '1.2.1'


class TrojanDatabase:

    def __init__(self, db_user, db_pass, db, table):
        self.db_user = db_user
        self.db_pass = db_pass
        self.db = db
        self.table = table
        self.connection = MySQLdb.connect('localhost', self.db_user, self.db_pass, self.db)
        self.cursor = self.connection.cursor()

    def check_rows_affected(self):
        """
        Check how many rows are affected by
        the command executed by self.cursor
        """
        if self.cursor.rowcount == 0:
            print('No rows affected')
        else:
            print('{} row(s) affected'.format(self.cursor.rowcount))

    def add_user(self, username, password):
        """ Add new user into database
        """
        hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        fullhash = hashlib.sha224('{}:{}'.format(username, hashed_password).encode('utf-8')).hexdigest()
        self.cursor.execute("INSERT INTO {} (username, password) VALUES ('{}', '{}')".format(self.table, username, hashed_password, fullhash))
        self.connection.commit()
        return 0

    def del_user(self, username):
        """ Delete a user from the database
        """
        self.cursor.execute("DELETE FROM {} WHERE username = '{}'".format(self.table, username))
        if self.cursor.rowcount == 0:
            return 1
        self.connection.commit()

    def user_exists(self, username):
        """ Determines if a user exists in the database
        """
        self.cursor.execute("SELECT * FROM {} WHERE username = '{}'".format(self.table, username))
        user_id = self.cursor.fetchone()
        if user_id is not None:
            return True
        return False

    def set_quota(self, username, quota):
        try:
            self.cursor.execute("UPDATE users SET quota = {} WHERE username = '{}'".format(int(quota), username))
        except ValueError:
            print('Quota must be an integer')

    def add_quota(self, username, appended_quota):
        try:
            self.cursor.execute("UPDATE users SET quota = quota + {} WHERE username = '{}'".format(appended_quota, username))
        except ValueError:
            print('Quota must be an integer')

    def verify(self, fullhash):
        """ Verify if user credentials are valid
        """
        valid_hashes = []
        self.cursor.execute("SELECT * FROM {}".format(self.table))
        all_users = self.cursor.fetchall()
        for user in all_users:
            valid_hashes.append(user[2])
        if fullhash in valid_hashes:
            print(0)
            return 0
        print(1)
        return 1


def print_help():
    help_lines = [
        "Commands are not case-sensitive"
        "Verify [hash]",
        "Add [username] [password]",
        "Delete [username]",
        "SetQuota [quota]",
        "AddQuota [quota]",
    ]
    for line in help_lines:
        print(line)


def main():
    trojan_db = TrojanDatabase('trojan', 'thisisthetrojandbpassword', 'trojan', 'users')
    try:
        if sys.argv[1].lower() == 'help':
            print_help()
        elif sys.argv[1].lower() == 'verify':
            trojan_db.verify(sys.argv[2])
        elif sys.argv[1].lower() == 'add':
            trojan_db.add_user(sys.argv[2], sys.argv[3])
        elif sys.argv[1].lower() == 'delete':
            trojan_db.del_user(sys.argv[2])
        elif sys.argv[1].lower() == 'setquota':
            trojan_db.set_quota(sys.argv[2], sys.argv[3])
        elif sys.argv[1].lower() == 'addquota':
            trojan_db.add_quota(sys.argv[2], sys.argv[3])
        else:
            print('Invalid command')
        exit(0)
    except IndexError:
        print('No commands specified')
        exit(0)


if __name__ == '__main__':
    main()
