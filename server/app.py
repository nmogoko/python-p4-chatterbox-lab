from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.all()
        return jsonify([message_item.message_serializer() for message_item in messages]), 200
    else:
        data = request.get_json()
        body = data.get("body")
        username = data.get("username")
        message = Message(body=body, username=username)

        db.session.add(message)
        db.session.commit()
        return jsonify(message.message_serializer()), 201  # 201 Created status




@app.route('/messages/<int:id>', methods=["DELETE", "PATCH"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if not message:
        return jsonify({"error": "message not found"}), 404
    
    if request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 204
    else:
        data = request.get_json()
        if "body" in data:
            message.body = data["body"]
        if "username" in data:
            message.username = data["username"]
        message.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify(message.message_serializer()), 200

if __name__ == '__main__':
    app.run(debug=True, port=5555)
