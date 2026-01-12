from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import RolePermission
from rest_framework.permissions import IsAuthenticated
from .models import User

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Account created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class AdminDashboardView(APIView):
    permission_classes = [RolePermission]
    RolePermission.allowed_roles = ["admin"]

    def get(self, request):
        return Response({"message": f"Hello Admin {request.user.email}"})


class DeveloperView(APIView):
    permission_classes = [RolePermission]
    RolePermission.allowed_roles = ["developer"]

    def get(self, request):
        return Response({"message": f"Hello Developer {request.user.email}"})


class SalesView(APIView):
    permission_classes = [RolePermission]
    RolePermission.allowed_roles = ["sales"]

    def get(self, request):
        return Response({"message": f"Hello Sales {request.user.email}"})


class ClientView(APIView):
    permission_classes = [RolePermission]
    RolePermission.allowed_roles = ["client"]

    def get(self, request):
        return Response({"message": f"Hello Client {request.user.email}"})
    
class RoleListView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Any logged-in user

    def get(self, request):
        roles = [role.value for role in User.Roles]
        return Response({"roles": roles})
    
class AssignRoleView(APIView):
    permission_classes = [IsAuthenticated]  # We’ll enforce admin inside

    def post(self, request, user_id):
        # Only admins can assign roles
        if request.user.role != "admin":
            return Response({"detail": "Only admins can assign roles."}, status=status.HTTP_403_FORBIDDEN)

        role = request.data.get("role")
        if role not in [r.value for r in User.Roles]:
            return Response({"detail": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            user.role = role
            user.save()
            return Response({"message": f"{user.email} is now a {role}"})
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class UserRoleView(APIView):
    permission_classes = [IsAuthenticated]  # Admin can view anyone, others see self

    def get(self, request, user_id=None):
        # If user_id not provided, return own role
        if not user_id:
            return Response({"id": request.user.id, "email": request.user.email, "role": request.user.role})

        # Only admin can view other users
        if request.user.role != "admin" and int(user_id) != request.user.id:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            return Response({"id": user.id, "email": user.email, "role": user.role})
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

# system dashboard
        
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.user.role

        if role == "admin":
            data = self.admin_dashboard(request)
        elif role == "developer":
            data = self.developer_dashboard(request)
        elif role == "sales":
            data = self.sales_dashboard(request)
        elif role == "client":
            data = self.client_dashboard(request)
        else:
            data = {"message": "No dashboard for this role"}

        return Response(data)

    # Example dashboard data
    def admin_dashboard(self, request):
        from .models import User
        users_count = User.objects.count()
        roles_count = {
            "admin": User.objects.filter(role="admin").count(),
            "developer": User.objects.filter(role="developer").count(),
            "sales": User.objects.filter(role="sales").count(),
            "client": User.objects.filter(role="client").count(),
        }
        return {
            "message": f"Welcome Admin {request.user.email}",
            "total_users": users_count,
            "roles_count": roles_count,
        }

    def developer_dashboard(self, request):
        return {
            "message": f"Welcome Developer {request.user.email}",
        }

    def sales_dashboard(self, request):
        return {
            "message": f"Welcome Sales {request.user.email}",
        }

    def client_dashboard(self, request):
        return {
            "message": f"Welcome Client {request.user.email}",
            "account_info": {"email": request.user.email, "role": request.user.role},
        }

    

    



