import psycopg2
import os
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

db_user = os.getenv('USER_DB')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
db = os.getenv('DB')

def db_connect():
	conn = psycopg2.connect(user=db_user, password=password, host=host, port=port, database=db)
	return conn

@app.route("/Result")
def Result(text):
    print(text)
    return text
    
@app.route("/", methods=['GET','POST'])
def main():
	
	conn = db_connect()
	cur = conn.cursor()
	
	if request.method == 'POST':
		number = request.form.get("number")
		result = check(int(number), cur, conn)
		if result == 1:
		    return Result("Already in DB")
		elif result == 2:
		    return Result("Your number + 1 Already in DB")
		elif result == 0:
		    return Result(str(int(number) + 1))
		
		print(number)

	return '''
            <form method="POST">
                <div><label>Введите число: <input type="int" name="number"></label></div>
                <input type="submit" value="Submit">
           	</form>'''
		
def check(number, cur, conn):
    cur.execute("SELECT number FROM numbers WHERE number=%s", (number,))
    res = cur.fetchone()
    if res:      #Если число уже поступало
        return 1
    else:
        cur.execute("SELECT number FROM numbers WHERE number=%s", (number + 1,))
        res = cur.fetchone()
        if res:       #Если число на 1 больше уже поступало
            return 2
        else:         #Если все четко
            cur.execute("INSERT INTO numbers VALUES (%s)", (number,))
            conn.commit()
            print(cur)
            return 0    
    		

if __name__ == "__main__":
    app.run()
