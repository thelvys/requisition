from django import forms
from .models import CustomUser
from .models import Requisition

class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['details', 'amount']


class ShareRequisitionForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )