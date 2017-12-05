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

    patent_abs = TextAreaField('New Patent Claim Text (for example <strong>A new and distinct cultivar of ornamental  Hosta  plant named Beckoning; as herein described and illustrated, with yellowish leaf center and blue-green margin, suitable as a potted plant, for the garden, and for cut flower arrangements.</strong>)',
                        validators=[DataRequired()])

    patent_cosine_sim_threshold = TextField('Patent Claim Match Threshold %, Scale 0-100%. (for example <strong> 30</strong> no need to enter unit)',
                        validators=[DataRequired()])

    patent_result_top = TextField('Patent Result Get Top X (for example <strong> 5</strong>)',
                        validators=[DataRequired()])

    submit = SubmitField()
