import mariadb
import dbcreds

def getBlog(user_id):
    conn = None
    cursor = None
    blogs = None
    result = []
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        print(user_id) 
        if user_id != None:
            cursor.execute("SELECT b.title ,b.content ,b.created_at, b.id,u.username ,b.user_id FROM users u INNER JOIN blog b ON u.id = b.user_id WHERE b.user_id=? ORDER BY created_at DESC" , [user_id,])
            rows = cursor.fetchall()
        else:
            cursor.execute("SELECT b.title ,b.content ,b.created_at, b.id,u.username ,b.user_id FROM users u INNER JOIN blog b ON u.id = b.user_id ORDER BY created_at DESC")
            rows = cursor.fetchall()
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            result.append(dict(zip(headers,row)))

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
        return result
    
def newBlog(title, content, created_at, token):
    conn = None
    cursor = None
    row = None
    newblog = None
    user_id = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            print('2')
            cursor.execute("INSERT INTO blog(title, content, created_at, user_id) VALUES (?,?,?,?)", [title, content, created_at, user_id])
            conn.commit()
            row = cursor.rowcount
        if row == 1:
            cursor.execute("SELECT b.title ,b.content ,b.created_at, b.id,u.username ,b.user_id FROM users u INNER JOIN blog b ON u.id = b.user_id WHERE b.title=? and b.content=?", [title, content])
            rows = cursor.fetchone()
            print(rows)
            headers = [ i[0] for i in cursor.description]
            print(headers)
            newblog = dict(zip(headers,rows))
            print(newblog)
        print(newblog)
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
        return newblog
        
        
def editBlog(content, token, blog_id):
    conn = None
    cursor = None
    row = None
    newblog = None
    user_id = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            if content != None and content != "":
                cursor.execute("UPDATE blog SET content=? WHERE id=? and user_id=?", [content, blog_id, user_id])
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
        if row == 1:
            newBlog ={"content": content,
                      "user_id": user_id
                      }
            return newBlog
        
def deleteBlog(blog_id, token):
    conn = None
    cursor = None
    row = None
    newblog = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            cursor.execute("DELETE FROM blog WHERE id=? and user_id=?", [blog_id, user_id])
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
        if row == 1:
            return True
        else:
            return False
        
