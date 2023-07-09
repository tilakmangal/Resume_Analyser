import fitz
import pandas as pd
from resumepars import Resumepars

doc = fitz.open(r'assets/resumes/<filename>.pdf')
text = ""
for page in doc:
    text += page.get_text()

# Reading csv file with the help of python pandas
df = pd.read_csv('assets/resume_parser.csv')

# Converting dataframe object to dictionary
dfd = df.to_dict()

resume_info = Resumepars(text=text, dfd=dfd)
print(resume_info.name())
print(resume_info.phone())
print(resume_info.email())
print(resume_info.final_job_scores())