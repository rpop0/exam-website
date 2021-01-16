from ..templatetags.custom_filters import position_id_to_string
from datetime import datetime
from users.models import User
from datetime import datetime, timedelta

def get_monthly_data():
    # month = datetime.now().strftime("%B").lower()
    # year = datetime.now().strftime("%Y")
    # total_points = 0
    # total_diipt = 0
    # total_exams = 0
    # total_approved = 0
    # total_denied = 0
    # total_ridealong = 0
    # total_users = len(User.objects.all())
    # total_tracker_entries = 0
    # tracker = PointTracker.objects.filter(month=month, year=year)
    # for entry in tracker:
    #     total_points += entry.points
    #     total_tracker_entries += 1
    #     if "Conducting" in entry.name and ("Interview" in entry.name or "Physical" in entry.name):
    #         total_diipt += 1
    #     if "Issuing Examination" in entry.name:
    #         total_exams += 1
    #     if "Approving Preliminary" in entry.name:
    #         total_approved += 1
    #     if "Accepting Police Ridealong" in entry.name:
    #         total_ridealong += 1
    #     if "Denying Preliminary" in entry.name:
    #         total_denied += 1

    monthly_data = {
        'points': 0,
        'users': 0,
        'tracker_entries': 0,
        'diipt': 0,
        'exams': 0,
        'approved': 0,
        'denied': 0,
        'ridealong': 0,
    }
    return monthly_data
