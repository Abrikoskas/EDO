import utils
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from main_view import docs_set


class UploadForm(FlaskForm):
    doc = FileField(validators=[FileAllowed(docs_set, 'Docs only!'),
                      FileRequired('File was empty!')])
    submit = SubmitField('Upload')


class File:
    def __init__(self, url, filename):
        self.url = url
        self.name = filename


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

def email_send_file(file):
 pass
