import psycopg2
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_USER = os.getenv("USER_DB")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")


def connect_to_postgres():
    conn = psycopg2.connect(
        user=DB_USER, 
        password=PASSWORD, 
        host=HOST, 
        port=PORT, 
        database=DB
        )
    return conn


def check(cur, num):
    cur.execute("SELECT num FROM nums WHERE num=%s", (num,))
    res = cur.fetchone()
    if res:
        return False
    return True


@app.route("/", methods=["GET", "POST"])
def main():
    conn = connect_to_postgres()
    cur = conn.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS nums (num INT);")
    
    num = int(request.json["num"])

    if not check(cur, num):
        return jsonify({"Error 1":"This number is already in DB."})
    
    if not check(cur, num + 1):
        return jsonify({"Error 2":"This number is one less than number in DB."})

    cur.execute("INSERT INTO nums VALUES (%s)", (num,))
    conn.commit()

    return jsonify({"next_number": num + 1})


if __name__ == "__main__":
    app.run()

