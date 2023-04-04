
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
        # Get all slots. If no data return 404, any errors: 400, normal: 200
        conn = get_db_connection()
        data = None
        status = 200
        
        if conn.execute("SELECT * from slots").fetchall() == []:
            conn.commit()
            conn.close()
            
            return {"error": "Records not found"}, 404
        
        try:
            data = conn.execute('SELECT * FROM slots').fetchall()
            data = [dict(x) for x in data]
        except sqlite3.Error as e:
             data, status = {"error": str(e)}, 400


        conn.close()
        return json.dumps(data), status

    elif request.method == 'POST':
        # Add new slot. If any errors: 400, normal: 201
        conn = get_db_connection()
        data = {'building': building, 'slot': slot}
        status = 201
        
        try:
            conn.execute("INSERT INTO slots VALUES (?, ?, ?)", (building, slot, 0))
        except sqlite3.Error as e:
            data, status = {"error": str(e)}, 400
        
        conn.commit()
        conn.close()
        
        return json.dumps(data), status

    elif request.method == 'DELETE':
        # Delete slot. If record not found return 404, If any errors: 400, normal: 200
        
        conn = get_db_connection()
        data = {'building': building, 'slot': slot}
        status = 200
        
        if conn.execute("SELECT * from slots WHERE building=? AND slot=?", (building, slot)).fetchall() == []:
            conn.commit()
            conn.close()
            
            return {"error": "Record not found"}, 404

        try:
            conn.execute("DELETE FROM slots WHERE building=? AND slot=?", (building, slot))
        except sqlite3.Error as e:
            data, status = {"error": str(e)}, 400

        conn.commit()
        conn.close()
        return json.dumps(data), status
   
    
    
@app.route("/api/slots/status/<building>/<slot>", methods = ['POST', 'DELETE'])
def status_manager(building=None, slot=None):
    if request.method == 'POST':
        # Set slot as parked. If record not found return 404, If any errors: 400, normal: 200
        
        conn = get_db_connection()
        data = {'building': building, 'slot': slot, "status": 1}
        status = 200
        
        if conn.execute("SELECT * from slots WHERE building=? AND slot=?", (building, slot)).fetchall() == []:
            conn.commit()
            conn.close()
            
            return {"error": "Record not found"}, 404

        
        try:
            conn.execute("UPDATE slots SET status=? WHERE building=? AND slot=?", (1, building, slot))
        except sqlite3.Error as e:
            data, status = {"error": str(e)}, 400
    
        conn.commit()
        conn.close()

        return json.dumps(data), status

    elif request.method == 'DELETE':
        # Set slot as unparked. If record not found return 404, If any errors: 400, normal: 200
        
        conn = get_db_connection()
        data = {'building': building, 'slot': slot}
        status = 200
        
        if conn.execute("SELECT * from slots WHERE building=? AND slot=?", (building, slot)).fetchall() == []:
            conn.commit()
            conn.close()
            
            return {"error": "Record not found"}, 404

        try:
            conn.execute("UPDATE slots VALUES SET status=? WHERE building=? AND slot=?", (0, building, slot))
        except sqlite3.Error as e:
            data, status = {"error": str(e)}, 400

        conn.commit()
        conn.close()
        return json.dumps(data), status
   
