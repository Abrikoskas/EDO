import os
import utils
from flask import Flask, render_template, send_from_directory, redirect, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT, DOCUMENTS, patch_request_class
import Server as srvr

# ------------Configs------------
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'

docs_dir = os.path.join(basedir, 'Docs')
app.config['UPLOADED_DOCS_DEST'] = docs_dir

docs_set = UploadSet('docs', TEXT+IMAGES+DOCUMENTS)
configure_uploads(app, docs_set)

patch_request_class(app)

contragents = ['iii']

# ------------Main page------------
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = srvr.UploadForm()
    if form.validate_on_submit():
        _ = docs_set.save(form.doc.data)
    docs = srvr.Docs(docs_dir)
    return render_template('index.html', form=form, docs=docs)


# Download file enpoint
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOADED_DOCS_DEST'],
                               filename, as_attachment=True)


@app.route('/delete/<path:filename>')
def delete_file(filename):
    print("delete")
    utils.delete_file(docs_dir, filename)
    return redirect('/')


# ------------Email form------------
@app.route('/SendEmail/<path:filename>', methods=['GET', 'POST'])
def email_send_file(filename):
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным input
        password = request.form.get('password')
        to = request.form.get('to')
        subject = request.form.get('subject')
        text = request.form.get('text')

    if "submit" in request.form:  # если нажата кнопка добавить
        files = os.path.join(docs_dir, filename)
        utils.send_mail(send_from=username, send_to=to, subject= subject, text=text,
                        gmail_user=username, gmail_password=password,
                        files=files)
        return redirect('/')
    return render_template('email_form.html', filename=filename, contragents=contragents)


@app.route('/contragents', methods=['GET', 'POST'])
def contragents_view():
    print(contragents)
    if request.method == 'POST':
        email = request.form.get('email')
    # if "submit" in request.form:  # если нажата кнопка добавить
        contragents.append(email)
        print(f"after submit{contragents}")
        return redirect('/contragents')
    return render_template('contragents.html', contragents=contragents)


@app.route('/delete_contragent/<email>', methods=['GET', 'POST'])
def delete_contragent(email):
    contragents.remove(email)
    return redirect('/contragents')


if __name__ == '__main__':
    app.run()

