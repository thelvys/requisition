from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import CustomUser, Department, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm, DepartmentForm, ProfileForm

class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'customuser_list.html'

class CustomUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'customuser_detail.html'

class CustomUserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'customuser_form.html'
    permission_required = 'yourapp.add_customuser'  # Remplacez 'yourapp' par le nom de votre application

class CustomUserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'customuser_form.html'
    permission_required = 'yourapp.change_customuser'

class CustomUserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'customuser_confirm_delete.html'
    success_url = '/'  # Rediriger vers la page d'accueil après la suppression
    permission_required = 'yourapp.delete_customuser'


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'department_list.html'

class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    template_name= 'department_detail.html'

class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'
    permission_required = 'yourapp.add_department'

class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'
    permission_required = 'yourapp.change_department'

class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Department
    template_name = 'department_confirm_delete.html'
    success_url = reverse_lazy('department_list')  # Utilisez reverse_lazy pour générer l'URL après la suppression
    permission_required = 'yourapp.delete_department' 

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profile_list.html'

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile_detail.html'

class ProfileCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_form.html'
    permission_required = 'yourapp.add_profile'

class ProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_form.html'
    permission_required = 'yourapp.change_profile'

class ProfileDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Profile
    template_name = 'profile_confirm_delete.html'
    success_url = reverse_lazy('profile_list')
    permission_required = 'yourapp.delete_profile'
