from django import forms
from .models import Comment, Blog

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'message']  # Default fields for anonymous users
        widgets = {  
                'name': forms.TextInput(attrs={'placeholder':'Name', 'class':'form-control'}),
                'email': forms.EmailInput(attrs={'placeholder':'Email','class':'form-control'}),
                'message': forms.Textarea(attrs={'placeholder':'Message','class':'form-control'}),
            }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated: 
            del self.fields['name']  
            del self.fields['email']  

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'publish','image','category'] 
        widgets = {
            'title': forms.TextInput(attrs={ 'class':'form-control'}),
            'description': forms.Textarea(attrs={ 'class':'form-control'}),
            'image': forms.FileInput(attrs={ 'class':'form-control'}),
            'category': forms.Select(attrs={ 'class':'form-control'}),
            
        }