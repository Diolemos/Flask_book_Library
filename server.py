from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#hey, flask. I will be using sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"

db = SQLAlchemy()

db.init_app(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    
with app.app_context():
    db.create_all()
    
@app.route('/')
def home():
    all_books = db.session.execute(db.select(Book)).scalars().all()
    print(all_books)
    return render_template('index.html',books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route('/edit', methods=["GET","POST"])
def edit():
    if request.method == 'POST':
        #UPDATE RECORD
        book_id = request.form['id']
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html",book=book_selected)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)    