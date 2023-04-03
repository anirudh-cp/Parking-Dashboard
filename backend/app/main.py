
from flask import Flask, request
import sqlite3
import json

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('./app/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/slots')
@app.route("/api/slots/<building>/<slot>", methods = ['GET', 'POST', 'DELETE'])
def slots_manager(building=None, slot=None):
    if request.method == 'GET':
        conn = get_db_connection()
        data = conn.execute('SELECT * FROM slots').fetchall()
        conn.close()
        return json.dumps([dict(x) for x in data]), 200
    elif request.method == 'POST':
        conn = get_db_connection()
        conn.execute("INSERT INTO slots VALUES (?, ?, ?)", (building, slot, 0))
        conn.commit()
        conn.close()
        return 200
    elif request.method == 'DELETE':
        conn = get_db_connection()
        conn.execute("DELETE slots WHERE building=? AND slot=?)", (building, slot))
        conn.commit()
        conn.close()
        return 200
   
    
    
@app.route("/api/slots/status/<building>/<slot>", methods = ['POST', 'DELETE'])
def status_manager(building=None, slot=None):
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute("UPDATE slots VALUES SET status=? WHERE building=? AND slot=?)", (1, building, slot))
        conn.commit()
        conn.close()
        return 200
    elif request.method == 'DELETE':
        conn = get_db_connection()
        conn.execute("UPDATE slots VALUES SET status=? WHERE building=? AND slot=?)", (0, building, slot))
        conn.commit()
        conn.close()
        return 200
