import mariadb
import dbcreds

def signUp(username, password):
    conn = None
    cursor = None
    row = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()       
        cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", [username, password])
        conn.commit()
        row = cursor.rowcount
    except mariadb.ProgrammingError:
        print("program error...")
    except mariadb.DataError:
        print("Data error...")
    except mariadb.DatabaseError:
        print("Database error...")
    except mariadb.OperationalError:
        print("connect error...")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        print(cursor.rowcount)
        if row == 1:
            return True
        else:
            return False
        
def login(username,password):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()       
        cursor.execute("SELECT * FROM users WHERE username=? and password=?", [username, password])
        user = cursor.fetchone()
        print(user)
    except mariadb.ProgrammingError:
        print("program error...")
    except mariadb.DataError:
        print("Data error...")
    except mariadb.DatabaseError:
        print("Database error...")
    except mariadb.OperationalError:
        print("connect error...")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        print(cursor.rowcount)
        return user
    
def token(token, user_id, date):
    conn = None
    cursor = None
    row = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()       
        print(token)
        # cursor.execute("DELETE FROM login WHERE user_id=?", [user_id,])
        # conn.commit()
        cursor.execute("INSERT INTO login(token, user_id, date) VALUES (?, ?, ?)", [token, user_id, date])
        conn.commit()
        row = cursor.rowcount
    except mariadb.ProgrammingError:
        print("program error...")
    except mariadb.DataError:
        print("Data error...")
    except mariadb.DatabaseError:
        print("Database error...")
    except mariadb.OperationalError:
        print("connect error...")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        print(cursor.rowcount)
        if row == 1:
            return True
        else:
            return False
        
def getUser():
    conn = None
    cursor = None
    users = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(users)
        for user in users:
            col_name_list = [tuple[0] for tuple in res.description]
            print(col_name_list)
    except mariadb.ProgrammingError:
        print("program error...")
    except mariadb.DataError:
        print("Data error...")
    except mariadb.DatabaseError:
        print("Database error...")
    except mariadb.OperationalError:
        print("connect error...")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        return users