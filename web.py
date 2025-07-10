from flask import Flask
from flask import render_template
from flask import request
from main import send_mail
from PyPDF2 import PdfReader
import os

app = Flask(__name__)


def getTemplates():
    templates = []
    for name in os.listdir('files/'):
        templates.append(os.path.splitext(name)[0])
    return(templates)

@app.route("/", methods=['POST', 'GET'])
def home():
    templates = getTemplates()
    if request.method == 'POST':
        to = request.form['recipient']
        template = request.form['template']
        send_mail(template, to)
        return render_template("index.html", popup=True, temps=templates)

    return render_template("index.html", popup=False, temps=templates)