from django import forms
from .models import Group  # Adjust the model name if it's different

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']  # Replace with relevant fields
