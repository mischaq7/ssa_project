from django import forms
from .models import Group, Comment

# CommentForm with custom validation and widget
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Use 'content', which matches your model
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write a comment...'}),  # Add placeholder
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if "<script>" in content.lower():  # Prevent XSS by checking for script tags
            raise forms.ValidationError("Invalid content.")
        return content

# GroupCreationForm for group creation
class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']  # Relevant fields for group creation

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Set the user as a member of the group automatically
            self.instance.admin = user  # Set the user as the group admin
            self.fields['name'].initial = f"Group for {user.username}"  # Set initial name for the group
