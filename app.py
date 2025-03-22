from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS livros ('
                     'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                     'titulo TEXT NOT NULL, '
                     'categoria TEXT NOT NULL, '
                     'autor TEXT NOT NULL, '
                     'imagem_url TEXT NOT NULL)')
        print('Tabela LIVROS criada com sucesso.')


init_db()


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/doar', methods=['POST'])
def doar_livro():
    dados = request.get_json()
    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')

    if not all([titulo, categoria, autor, imagem_url]):
        return jsonify({'Erro': 'Todos os campos são obrigatórios'}), 400

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO livros (titulo, categoria, autor, imagem_url) VALUES (?, ?, ?, ?)',
                       (titulo, categoria, autor, imagem_url))
        conn.commit()

    return jsonify({'Mensagem': 'Livro cadastrado com sucesso!'}), 201


@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM livros')
        livros = cursor.fetchall()

    livros_json = [{'id': livro[0], 'titulo': livro[1], 'categoria': livro[2],
                    'autor': livro[3], 'imagem_url': livro[4]} for livro in livros]

    return jsonify({'livros': livros_json}), 200


@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM livros WHERE id = ?', (id,))
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({'Erro': 'Livro não encontrado'}), 404

    return jsonify({'Mensagem': 'Livro deletado com sucesso!'}), 200


if __name__ == "__main__":
    app.run(debug=True)
