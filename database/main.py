import psycopg2 as pg
import os


def querySet(query, values = ()):
    try:
        conn = pg.connect(
            dbname="stocksim", password=os.environ["DATABASE_PASSWORD"], user="postgres", host="localhost"
        )
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        raise Exception("Internal error")


def queryGet(query, values=()):
    try:
        conn = pg.connect(
            dbname="stocksim", password=os.environ["DATABASE_PASSWORD"], user="postgres", host="localhost"
        )
        cur = conn.cursor()
        cur.execute(query, values)
        cols = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        result = []
        for i in data:
            result.append(dict(zip(cols , i)))
        cur.close()
        conn.close()
        return result
    except Exception  as e:
        print(e)
        raise Exception("Internal error")
