from django.urls import path
from .views import RegisterView, LoginView, AdminDashboardView, DeveloperView, SalesView, ClientView, RoleListView, AssignRoleView, UserRoleView, DashboardView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='Register'),
    path('auth/login', LoginView.as_view(), name='Login'),
    path("admin/dashboard/", AdminDashboardView.as_view()),
    path("developer/dashboard/", DeveloperView.as_view()),
    path("sales/dashboard/", SalesView.as_view()),
    path("client/dashboard/", ClientView.as_view()),
    path("roles/", RoleListView.as_view(), name="roles-list"),
    path("users/<int:user_id>/assign-role/", AssignRoleView.as_view(), name="assign-role"),
    path("users/<int:user_id>/role/", UserRoleView.as_view(), name="user-role"),
    path("users/me/role/", UserRoleView.as_view(), name="my-role"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]