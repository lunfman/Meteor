import re
from . import help
from flask import render_template

@help.route('/help')
def help():
    return render_template('help.html')