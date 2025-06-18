from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/')
def home():
    return '<h1>Chatterbox API</h1>'

# GET /messages: returns all messages ordered by created_at ascending
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([msg.to_dict() for msg in messages]), 200

# POST /messages: create a new message from form data
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_msg = Message(
        body=data.get('body'),
        username=data.get('username')
    )
    db.session.add(new_msg)
    db.session.commit()
    return jsonify(new_msg.to_dict()), 201

# PATCH /messages/<int:id>: update the body of a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)
    if not message:
        return make_response({'error': 'Message not found'}, 404)
    
    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
        db.session.commit()

    return jsonify(message.to_dict()), 200

# DELETE /messages/<int:id>: delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return make_response({'error': 'Message not found'}, 404)

    db.session.delete(message)
    db.session.commit()

    return make_response({'message': 'Message deleted'}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

