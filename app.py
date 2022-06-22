import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("entry")

            # add hover element to show time
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": date})

        entries = [entry for entry in app.db.entries.find({})]

        entry_with_date = []
        for entry in entries:
            entry_with_date.append(
                (
                    entry["content"],
                    entry["date"],
                    datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime(
                        "%b %d"
                    ),
                )
            )

        return render_template("home.html", entries=entry_with_date)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
