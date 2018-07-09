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

VERSION = '1.2'


class UserNotFoundException(object):
    pass


class TrojanDatabase:

    def __init__(self, db_user, db_pass, db):
        self.dbpass = db_user
        self.db_pass = db_pass
        self.db = db
        self.table = 'trojan'
        self.connection = MySQLdb.connect('localhost', self.db_user, self.db_pass, self.db)
        self.cursor = self.connection.cursor()

    def add_user(self, username, password):
        hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        fullhash = hashlib.sha224('{}:{}'.format(username, password).encode('utf-8')).hexdigest()
        self.cursor.execute("INSERT INTO {} (username, password, fullhash) VALUES ({}, {}, {})".format(self.table, username, hashed_password, fullhash))
        self.connection.commit()

    def del_user(self, username):
        self.cursor.execute("DELETE FROM {} WHERE username = '{}'".format(self.table, username))
        if self.cursor.rowcount == 0:
            raise UserNotFoundException()
            return
        self.connection.commit()

    def user_exists(self, username):
        self.cursor.execute("SELECT * FROM {} WHERE username = '{}'".format(self.table, username))
        user_id = self.cursor.fetchone()
        if user_id is not None:
            return True
        return False

    def verify(self, fullhash):
        valid_hashes = []
        self.cursor.execute("SELECT * FROM {}".format(self.table))
        all_users = self.cursor.fetchall()
        for user in all_users:
            valid_hashes.append(user[2])
        if fullhash in valid_hashes:
            print('Accept')
            return True
        print('Decline')
        return False


def main():
    trojan_db = TrojanDatabase('trojan', 'trojan_password')
    try:
        if sys.argv[1] == 'verify':
            trojan_db.verify(sys.argv[2])
        elif sys.argv[1] == 'add':
            trojan_db.add_user(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'delete':
            trojan_db.del_user(sys.argv[2])
        else:
            print('Invalid command')
    except IndexError:
        print('No commands specified')
        exit(0)


if __name__ == '__main__':
    main()
