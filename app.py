from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define model
class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

# Create database
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    items = GroceryItem.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = request.form['quantity']
    new_item = GroceryItem(name=name, quantity=quantity)
    db.session.add(new_item)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

