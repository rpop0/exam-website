from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class UserIsSeniorMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_staff: #If user is not staff
            if not self.request.user.staff and not self.request.user.admin and not self.request.user.senior:
                return False
        return True #Gets here if user is either staff or has rank greater than six

    def handle_no_permission(self):
        return redirect('main-dashboard')

class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_staff:
            if not self.request.user.admin: #If user is not staff
                return False
        return True #Gets here if user is either staff or has rank greater than six

    def handle_no_permission(self):
        return redirect('main-dashboard')

class UserIsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_staff: #If user is not staff
            if not self.request.user.staff and not self.request.user.admin:
                return False
        return True #Gets here if user is either staff or has rank greater than six

    def handle_no_permission(self):
        return redirect('main-dashboard')

