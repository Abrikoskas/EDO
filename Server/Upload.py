# app-upload.py
import os
import utils
from flask import Flask, render_template, send_from_directory, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT, DOCUMENTS, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

# ------------Configs------------
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'

docs_dir = os.path.join(basedir, 'Docs')
app.config['UPLOADED_DOCS_DEST'] = docs_dir

docs_set = UploadSet('docs', TEXT+IMAGES+DOCUMENTS)
configure_uploads(app, docs_set)

patch_request_class(app)
# -------------------------------


class UploadForm(FlaskForm):
    doc = FileField(validators=[FileAllowed(docs_set, 'Docs only!'),
                      FileRequired('File was empty!')])
    submit = SubmitField('Upload')


class File:
    def __init__(self, url, filename):
        self.url = url
        self.name = filename

    def delete(self):
        print("Delete")
        utils.delete_file(docs_dir, self.name)


class Docs:
    def __init__(self, path_to_folder):
        self.files = []
        self.update_docs_list(path_to_folder)

    def update_docs_list(self, path_to_folder):
        for file in utils.get_files(path_to_folder):
            file_tmp = File(file, file.name)
            self.files.append(file_tmp)

    def get_docs(self):
        return self.files

# Main view
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = docs_set.save(form.doc.data)
        # file_url = docs.url(filename)
    else:
        file_url = None
    docs = Docs(docs_dir)
    return render_template('index.html', form=form, docs=docs)


# Download file enpoint
@app.route('/download/<path:filename>')
def download_file(filename):
    print("endpoint")
    print(filename)
    return send_from_directory(app.config['UPLOADED_DOCS_DEST'],
                               filename, as_attachment=True)


@app.route('/delete/<path:filename>')
def delete_file(filename):
    print("delete")
    utils.delete_file(docs_dir, filename)
    return redirect('/')



if __name__ == '__main__':
    app.run()