import os
import sys
import sqlite3
import sql_custom

def create_table_statement(database_name,table_name,primary=None,columns=None,unique=None):
    conn = sqlite3.connect(f'{database_name}.db')
    cursor = conn.cursor()
    query = sql_custom.create(table_name,primary,columns,unique)
    cursor.execute(query)
    conn.commit()
    conn.close()
    return query

def insert(database_name,table_name,rows):
    conn = sqlite3.connect(f'{database_name}.db')
    cursor = conn.cursor()
    query,values = sql_custom.insert(table_name,rows)
    cursor.execute(query,values)
    conn.commit()
    conn.close()
    return query

def all_column_names(database_name,table_name):
    conn = sqlite3.connect(f'{database_name}.db') 
    cursor = conn.cursor()
    query = sql_custom.PRAGMA(table_name)
    cursor.execute(query)
    result=cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def all_column_names_stripped(dic):
    names = []
    for x in dic:
        if x[1] != 'ID':
            names.append(x[1])
    return names

def all_rows(database_name,table_name):
    conn = sqlite3.connect(f'{database_name}.db') 
    cursor = conn.cursor()
    query = sql_custom.select('*')+sql_custom.from_(table_name)
    cursor.execute(query)
    result=cursor.fetchall()
    conn.commit()
    conn.close()
    return result