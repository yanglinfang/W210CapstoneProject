#
# Data input form
# forms.py
#

# install: pip install Flask-WTF
from wtforms import TextField
from wtforms.fields import TextAreaField
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form

class PatentSearch(Form):

    patent_abs = TextAreaField('<b>Patent Abstract</b> (eg "A manipulation method of a telemeeting terminal device for performing communication between remote locations by a multiwindow function for displaying multiple media")',
                        validators=[DataRequired()])

    patent_cosine_sim_threshold = TextField('<b>Patent Similarity Threshold, Scale 0-1. </b> (eg 0.5, 0.7)',
                        validators=[DataRequired()])

    patent_result_top = TextField('<b>Patent Result Get Top X</b> (eg 5, 10)',
                        validators=[DataRequired()])

    submit = SubmitField()
