from datetime import datetime


def sidebar_context_data(request):
    if request.user.is_authenticated:
        points = 0
        month = datetime.now().strftime("%B").lower()
        kwargs = {
            'current_year': datetime.now().year,
            'current_month': datetime.now().strftime("%B"),
            'total_points': 0
        }
        return kwargs
    kwargs = dict()
    return kwargs
