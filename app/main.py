# Server related
from flask import Flask, request, render_template, make_response
from flask_moment import Moment

# Data parse
from bson import json_util
import json

# DB connectivity
from flask_pymongo import pymongo
import dotenv
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"
dotenv.load_dotenv(ENV_FILE_PATH)

client = pymongo.MongoClient(os.environ.get("DB_URI"))
db = client.get_database('flask_mongodb_atlas')

app = Flask(__name__)
moment = Moment(app)


@app.route('/', methods=['GET', ])
def home():
    records = db['slots'].find().sort([("building", pymongo.ASCENDING), ("slot", pymongo.ASCENDING)])
    data = json.loads(json_util.dumps(records))

    result = {}
    for item in data:
        if item["building"] not in result:
            result[item["building"]] = []
        result[item["building"]].append(
            {"slot": item["slot"], "status": item["status"]})

    return render_template('index.html', result=result)


@app.route('/api/slots', methods=['GET', 'POST', 'DELETE'])
@app.route("/api/slots/<building>/<slot>", methods=['GET', 'POST', 'DELETE'])
def slots_manager(building=None, slot=None):
    if request.method == 'GET':
        # Get all slots. If no data return 404, normal: 200

        records = db['slots'].find().sort([("building", pymongo.ASCENDING), ("slot", pymongo.ASCENDING)])
        records = json_util.dumps(records)
        
        if len(json.loads(records)):
            return make_response(records, 200)
        else:
            return {"error": "Records not found"}, 404

    elif request.method == 'POST':
        # Add new slot. If any errors: 400, normal: 201

        data = {'building': building, 'slot': slot}
        
        if db['slots'].count_documents(data):
            return {'error': 'Record with same building and slots exists'}, 400
        else:
            db['slots'].insert_one(data | {'status': 0})

        return data | {'status': 0}, 201

    elif request.method == 'DELETE':
        # Delete slot. If record not found return 404, error: 400, normal: 200

        data = {'building': building, 'slot': slot}

        if db['slots'].count_documents(data):
            records = db['slots'].delete_one(data)
            if records.deleted_count > 0:
                return data, 200
            else:
                return {"error": "Deletion error"}, 400
        else:
            return {"error": "Records not found"}, 404


@app.route("/api/slots/status/<building>/<slot>", methods=['POST', 'DELETE'])
def status_manager(building=None, slot=None):
    if request.method == 'POST':
        # Set slot as parked. If record not found return 404, normal: 200

        data = {'building': building, 'slot': slot}
        
        if db['slots'].count_documents(data):
            records = db['slots'].update_one(data, {"$set": {"status": 1}})
            if records.modified_count > 0:
                return data, 200
            else:
                return {"error": "Updation error"}, 400
        else:
            return {"error": "Records not found"}, 404

    elif request.method == 'DELETE':
        # Set slot as unparked. If record not found return 404, If any errors: 400, normal: 200

        data = {'building': building, 'slot': slot}

        if db['slots'].count_documents(data):
            records = db['slots'].update_one(data, {"$set": {"status": 0}})
            if records.modified_count > 0:
                return data, 200
            else:
                return {"error": "Updation error"}, 400
        else:
            return {"error": "Records not found"}, 404
