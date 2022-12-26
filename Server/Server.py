from flask import Flask, flash, redirect, url_for, render_template, request
import sys
app = Flask(__name__)

class File:
    def __init__(self, url, name):
        self.url = url
        self.name = name

class Context:
    def __init__(self, template, **variables):
        self.variables = variables
        self.template = template


file1 = File(url="",
             name="Отчёт1")

context = Context('main.html', files = [file1])


@app.route('/')
def hello_world():
    return render_template('main.html', files = [file1])



if __name__ == "__main__":
    app.run(debug=True)