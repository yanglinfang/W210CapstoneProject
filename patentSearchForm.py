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

    patent_abs = TextAreaField('New Patent Claim Text (for example <strong>A manipulation method of a telemeeting terminal device for performing communication between remote locations by a multiwindow function for displaying multiple media</strong>)',
                        validators=[DataRequired()])

    patent_cosine_sim_threshold = TextField('Patent Claim Match Threshold, Scale 0-1. (for example <strong> 0.5, 0.7</strong>)',
                        validators=[DataRequired()])

    patent_result_top = TextField('Patent Result Get Top X (for example <strong> 5, 10</strong>)',
                        validators=[DataRequired()])

    submit = SubmitField()
