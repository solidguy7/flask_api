from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://solidguy7:15072001@mysql:3306/db'
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return 'Hello, from Flask!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
