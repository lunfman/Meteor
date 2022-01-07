from . import dashboard
from .logic import make_dashboard_logic

@dashboard.route('/')
def home_page():
    return make_dashboard_logic()
