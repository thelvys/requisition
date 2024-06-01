from django import forms
from .models import CustomUser, Department, Profile

class CustomUserCreationForm(forms.ModelForm):
    """Formulaire pour la création d'un utilisateur personnalisé."""
    class Meta:
        model = CustomUser
        fields = ('email', 'password')  # Assurez-vous d'ajouter les champs nécessaires

class CustomUserChangeForm(forms.ModelForm):
    """Formulaire pour la modification d'un utilisateur personnalisé."""
    class Meta:
        model = CustomUser
        fields = ('email', 'is_active', 'is_staff', 'is_admin')

class DepartmentForm(forms.ModelForm):
    """Formulaire pour la création/modification d'un département."""
    class Meta:
        model = Department
        fields = ('dep_name', 'description', 'main_dep', 'supervisor')

class ProfileForm(forms.ModelForm):
    """Formulaire pour la création/modification d'un profil."""
    class Meta:
        model = Profile
        fields = ('user_dep',)
