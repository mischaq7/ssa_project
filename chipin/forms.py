from django import forms
from .models import Group  # Adjust the model name if it's different
from .models import Comment

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']  # Replace with relevant fields



class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']  # Add other fields as needed

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Set the user as a member of the group automatically
            self.instance.admin = user  # Set the user as the group admin
            self.fields['name'].initial = f"Group for {user.username}"  
    # Clean the content to sanitise input
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if "<script>" in content.lower():  # Prevent XSS by checking for script tags
            raise forms.ValidationError("Invalid content.")
        return content