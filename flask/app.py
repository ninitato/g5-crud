from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path

app = Flask(__name__, instance_relative_config=True)

# Get the current directory (flask folder)
BASE_DIR = Path(__file__).resolve().parent

# Create instance folder inside flask directory
os.makedirs(BASE_DIR / "instance", exist_ok=True)

# Update database path to be inside flask folder
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR}/instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Item {self.name}>'

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)