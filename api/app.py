from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://solidguy7:15072001@mysql:3306/0'
db = SQLAlchemy(app)

class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation

    def __repr__(self):
        return '<Author %d>' % self.id

class AuthorsSchema(Schema):
    class Meta(Schema.Meta):
        model = Authors
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)

@app.route('/authors', methods=['GET'])
def index():
    get_authors = Authors.query.all()
    authors_schema = AuthorsSchema(many=True)
    authors = authors_schema.dump(get_authors)
    return make_response(jsonify({'authors': authors}))

@app.route('/authors/<id>', methods=['GET'])
def get_author_by_id(id):
    get_author = Authors.query.get(id)
    author_schema = AuthorsSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({'author': author}))

@app.route('/authors', methods=['POST'])
def create_author():
    name = request.json['name']
    specialisation = request.json['specialisation']
    new_author = Authors(name, specialisation)
    new_author.create()
    author_schema = AuthorsSchema()
    return make_response(jsonify({'author': author_schema.dump(new_author)}), 200)

@app.route('/authors/<id>', methods=['PUT'])
def update_author_by_id(id):
    data = request.get_json()
    get_author = Authors.query.get(id)
    if data.get('name'):
        get_author.name = data['name']
    if data.get('specialisation'):
        get_author.specialisation = data['specialisation']
    get_author.create()
    author_schema = AuthorsSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({'author': author}))

@app.route('/authors/<id>', methods=['DELETE'])
def delete_author_by_id(id):
    get_author = Authors.query.get(id)
    get_author.delete()
    return make_response('', 204)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
