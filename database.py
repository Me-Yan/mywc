#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
import traceback


class Database:

    def __init__(self):

        self.host = "localhost"
        self.user = "root"
        self.password = "123456"
        self.database = "mywc"
        self.port = 3306

    def create_db_connection(self):

        db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)

        return db

    def insert_goods_data(self, sql):

        # print(sql)

        db = self.create_db_connection()

        cursor = db.cursor()

        try:
            cursor.execute(sql)
            db.commit()
        except Exception:
            db.rollback()
            print(traceback.print_exc())
            print("-------插入记录失败。。。%s" % (sql))

        db.close()

    def insert_users_data(self, sql):

        db = self.create_db_connection()

        cursor = db.cursor()

        try:
            cursor.execute(sql)
            db.commit()
        except Exception:
            db.rollback()
            print(traceback.print_exc())
            print("---------插入记录失败。。。%s" % (sql))

        db.close()



