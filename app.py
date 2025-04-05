from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS books ('
                     'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                     'title TEXT NOT NULL, '
                     'category TEXT NOT NULL, '
                     'author TEXT NOT NULL, '
                     'image_url TEXT NOT NULL)')
        print('BOOKS table created successfully.')


init_db()


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/donate', methods=['POST'])
def donate_book():
    data = request.get_json()
    title = data.get('title')
    category = data.get('category')
    author = data.get('author')
    image_url = data.get('image_url')

    if not all([title, category, author, image_url]):
        return jsonify({'Error': 'All fields are required'}), 400

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, category, author, image_url) VALUES (?, ?, ?, ?)',
                       (title, category, author, image_url))
        conn.commit()

    return jsonify({'Message': 'Book successfully registered!'}), 201


@app.route('/donated-books', methods=['GET'])
def list_books():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()

    books_json = [{'id': book[0], 'title': book[1], 'category': book[2],
                   'author': book[3], 'image_url': book[4]} for book in books]

    return jsonify({'books': books_json}), 200


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (id,))
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({'Error': 'Book not found'}), 404

    return jsonify({'Message': 'Book successfully deleted!'}), 200


if __name__ == "__main__":
    app.run(debug=True)
