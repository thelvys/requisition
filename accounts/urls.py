from django.urls import path
from . import views

urlpatterns = [
    # URLs pour CustomUser
    path('users/', views.CustomUserListView.as_view(), name='customuser_list'),
    path('users/<int:pk>/', views.CustomUserDetailView.as_view(), name='customuser_detail'),
    path('users/create/', views.CustomUserCreateView.as_view(), name='customuser_create'),
    path('users/<int:pk>/update/', views.CustomUserUpdateView.as_view(), name='customuser_update'),
    path('users/<int:pk>/delete/', views.CustomUserDeleteView.as_view(), name='customuser_delete'),

    # URLs pour Department
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('departments/create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),

    # URLs pour Profile
    path('profiles/', views.ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profiles/create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('profiles/<int:pk>/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profiles/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
]