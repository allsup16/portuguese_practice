import sqlite3
#statement building
#table = str
#primary = list
#columns = dict
#unique = list
def create(table, primary=None, columns=None, unique=None):
    parts = [f'CREATE TABLE IF NOT EXISTS {table} (']
    if isinstance(primary, list) and primary:
        pk = f"PRIMARY KEY ({', '.join(primary)})"
    else:
        pk = "ID INTEGER PRIMARY KEY AUTOINCREMENT"
    col_defs = []
    col_defs.append(pk)
    if isinstance(columns, dict):
        for col, dtype in columns.items():
            col_defs.append(f"{col} {dtype}")
    if isinstance(unique, list) and unique:
        col_defs.append(f"UNIQUE ({', '.join(unique)})")
    parts.append(", ".join(col_defs))
    parts.append(")")
    query = " ".join(parts)
    return query
#table=str #to be deleted
def drop(table):
    return f'DROP TABLE {table}'
#altering a table
#table = string
#add = dict (what is)
def alter(table,add=None,rename=None):
    query = [f"ALTER TABLE {table}"]
    if add:
        addittion = [f"ADD COLUMN {col} {dtype}" for col,dtype in add.items()]
        query.append(", ".join(addittion))
    elif rename:
        for old,new in rename.items():
            query.append(f"RENAME COLUMN {old} TO {new}")
    return " ".join(query)+';'
#specify the table and what it is know as
def from_(table,alias=None):
    if alias:
        return f""" FROM {table} AS {alias}"""
    return f""" FROM {table}"""
#general select
#all strings are associated with column names
#default,count,sum_,avg,min_,max_ = string
def select(default=None,count=None,sum_=None,avg=None,min_=None,max_=None):
    part = []
    if default != None:
        part.append(f'{default} ')
    if count != None:
        part.append(f'COUNT({count})')
    if sum_ != None:
        part.append(f'SUM({sum_})')
    if avg != None:
        part.append(f'AVG({avg})')
    if min_ != None:
        part.append(f'MIN({min_})')
    if max_ != None:
        part.append(f'MAX({max_})')
    query = "SELECT " + ", ".join(part)
    return query
#full written out expression as list, handles more advances features of select like aliasing and arethmetic.
def select_advanced(*expression):
    return "SELECT " + ", ".join(expression)
#full where statements are written out as a string.
def where(condition):
    return f" WHERE {condition}"
#given a column name, will order based on the column in ascending order(unless specifyed)
def order_by(column, descending=False):
    return f"ORDER BY {column} {'DESC' if descending else 'ASC'}"
#only n number of rows are shown.
def limit(n):
    return f"LIMIT {n}"
#table to get columns from
def PRAGMA(table):
    return f"PRAGMA table_info({table})"
#columns = dict   Keys:placeholder values
def insert(table, columns: dict):
    keys = list(columns.keys())
    values = list(columns.values())
    col_names = ', '.join(keys)
    placeholders = ', '.join(['?'] * len(keys))
    query = f"INSERT OR IGNORE INTO {table} ({col_names}) VALUES ({placeholders})"
    return query, values
#delete rows (can be paired with where function)
def delete(table):
    return f"DELETE FROM {table}"
#update = dict
def update(table,updates):
    set_clause = ', '.join(f"{k} = ?" for k in updates.keys())
    return f"UPDATE {table} SET {set_clause}"

#additional functionality
def data_type(column):
    if isinstance(column, str):
        return "TEXT"
    elif isinstance(column, int):
        return "INTEGER"
    elif isinstance(column, float):
        return "REAL"
    elif isinstance(column, bool):
        return "BOOLEAN"
    elif isinstance(column, list) or isinstance(column, dict):
        if column:
            return data_type(next(iter(column)))  # safely handles both lists and dicts
        else:
            return "TEXT"  # default if empty
    else:
        return "TEXT"  # fallback