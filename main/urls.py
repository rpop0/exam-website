from django.urls import path
from main.views import (
    DashboardView,
    AdminView,
    InviteListView,
    InviteCreateView,
    InviteDeleteView,
    ManageUsersListView
)

urlpatterns = [
    path('', DashboardView.as_view(), name="main-dashboard"),
    path('admin/', AdminView.as_view(), name="main-admin"),
    path('manage-users/', ManageUsersListView.as_view(), name="main-admin-manage-users"),
    path('admin/invite', InviteCreateView.as_view(), name="main-admin-invite"),
    path('admin/invite/list', InviteListView.as_view(), name="main-admin-invite-list"),
    path('admin/invite/list/<int:pk>/delete', InviteDeleteView.as_view(), name="main-admin-invite-delete"),
]