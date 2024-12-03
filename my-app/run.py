from flask import Flask, render_template

app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('public/index.html')  # Se busca en templates/public/index.html

if __name__ == '__main__':
    app.run(debug=True)
