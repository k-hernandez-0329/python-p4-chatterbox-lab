from crypt import methods
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = []
        for message in Message.query.all():
            message_dict = message.to_dict()
            messages.append(message_dict)
        return jsonify(messages), 200

    elif request.method == "POST":
        data = request.json
        new_message = Message(body=data.get("body"), username=data.get("username"))
        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()
        return jsonify(message_dict), 201


@app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    # if message:
    #     new_body = request.json.get("body")
    #     if new_body:
    #         message.body = new_body
    #         db.session.commit()

    #         updated_message = message.to_dict()

    if request.method == "PATCH":
        data = request.json
        new_body = data.get("body")

        if new_body:
            message.body = new_body
            db.session.commit()
            return jsonify(message.to_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        return jsonify({"message": "Message was successfully deleted"})


if __name__ == "__main__":
    app.run(port=5555)
