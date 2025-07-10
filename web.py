from flask import Flask
from flask import render_template
from flask import request
from main import send_mail

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/send', methods=['POST'])
def send():
    to = request.form['recipient']
    template = request.form['template']
    send_mail(template, to)
    return f"<p>Send to: {to} <br> Use template: {template}</p>"
