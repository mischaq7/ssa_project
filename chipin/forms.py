from django import forms
from .models import Group  # Adjust the model name if it's different
from .models import Comment

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']  # Replace with relevant fields


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your comment...'})
        }

    # Clean the content to sanitise input
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if "<script>" in content.lower():  # Prevent XSS by checking for script tags
            raise forms.ValidationError("Invalid content.")
        return content