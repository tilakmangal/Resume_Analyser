import fitz
import pandas as pd
from resumepars import Resumepars
from flask import Flask, render_template, request

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# class Upload(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(50))
#     data = db.Column(db.LargeBinary)
# db.create_all()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        file = request.files['resume']
        file.save(file.filename)
        # upload = Upload(filename=file.filename, data=file.read())
        # db.session.add(upload)
        # db.session.commit()
        text = convert_pdf_to_text(file.filename)

        # Reading csv file with the help of python pandas
        df = pd.read_csv('assets/parsingdata/resume_parser.csv')

        # Converting dataframe object to dictionary
        dfd = df.to_dict()

        resume_info = Resumepars(text=text, dfd=dfd)
        return render_template('index.html', ask=True, person=resume_info)
    return render_template('index.html', ask=False)


# Converting pdf to txt
def convert_pdf_to_text(f_name):
    doc = fitz.open(fr'{f_name}')
    text = ""
    for page in doc:
        text += page.get_text()
    return text


if __name__ == '__main__':
    app.run()
