from . import dashboard
from .logic import return_dashboard_logic

@dashboard.route('/')
def home_page():
    return return_dashboard_logic()
