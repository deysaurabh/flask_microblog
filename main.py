from flask import Flask
from flask import render_template, request
import datetime
from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())
    app.db = client.microblog

    @app.route("/", methods=["GET","POST"])
    def home():
        if request.method =="POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            print(entry_content, formatted_date)
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries = [(entry["content"], entry["date"],
                       datetime.datetime.strptime(entry["date"],'%Y-%m-%d').strftime('%b %d'))
                       for entry in app.db.entries.find({})]

        return render_template("index.html", entries=entries)

    return app

