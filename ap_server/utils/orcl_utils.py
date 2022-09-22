# -*- coding:utf-8 -*-
import os
import logging
import cx_Oracle
from configs import (ORCL_HOST, ORCL_PASSWD, ORCL_PORT, ORCL_SERVICE_NAME,
                    ORCL_USER)

logger = logging.getLogger(__name__)


class OracleAccess(object):     # 設定 Oracle DB 的初始化
    arraysize = None
    pool = None

    @staticmethod        # 静态方法无需实例化           
    def initialise(min=1, max=2, increment=1, encoding="UTF-8", ):
        os.environ['NLS_LANG'] = 'TRADITIONAL CHINESE_TAIWAN.AL32UTF8'
        # os.environ['PATH'] = 'C:\Users\learn\Desktop\instantclient_21_6' + ";" + os.environ["PATH"]
        OracleAccess.arraysize = 100
        try:
            OracleAccess.pool = cx_Oracle.SessionPool(
                ORCL_USER,
                ORCL_PASSWD,
                "%s:%s/%s" % (ORCL_HOST, ORCL_PORT, ORCL_SERVICE_NAME),
                min=min,
                max=max,
                increment=increment,
                encoding=encoding
            )
        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            logger.error("%s: %s" % (error_obj.code, error_obj.message))
    
    @staticmethod
    def _get_conn():
        return OracleAccess.pool.acquire()  #???非同步執行??
    
    @staticmethod
    def _get_cursor(conn, arraysize=None):
        cursor = conn.cursor()
        cursor.arraysize = arraysize if arraysize else OracleAccess.arraysize
        return cursor
    
    @staticmethod
    def query(sql, args=[], arraysize=None):
        """
        Args:
            sql(string)
        """
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.execute(sql, args)
            return cursor.fetchall()
        finally:
            if conn:
                OracleAccess.pool.release(conn)

    @staticmethod
    def query_by_offset(sql, arraysize=None, offset=0, numrows=20):
        """
        Args:
            sql(string)
        """
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.execute(sql, offset=offset, numrows=numrows)
            return cursor.fetchall()    # 即返回多条记录(rows),如果没有结果,则返回 ()
        finally:
            if conn:
                OracleAccess.pool.release(conn)

    @staticmethod      
    def insert(sql, rows, arraysize=None):
        """
        Args:
            sql(string)
            rows(list)
        """
        
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.prepare(sql)     # test
            cursor.executemany(sql, rows)  
            conn.commit()   #提交事务，要不然不能真正的插入数据
        finally:
            if conn:
                OracleAccess.pool.release(conn)

    @staticmethod
    def execute(sql, args=None, arraysize=None):
        """
        Args:
            sql(string)
        """
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.execute(sql, args)
            conn.commit()
        finally:
            if conn:
                OracleAccess.pool.release(conn)
                
    @staticmethod
    def update(sql, arraysize=None):
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.execute(sql)
            conn.commit()
        finally:
            if conn:
                OracleAccess.pool.release(conn)

    @staticmethod
    def get(sql, arraysize=None):
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            if conn:
                OracleAccess.pool.release(conn)