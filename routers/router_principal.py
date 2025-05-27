from app import app
from flask import Flask, render_template



@app.route('/public')
def indexPrincipal():
    return render_template('public/index.html')
