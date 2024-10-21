from django import forms
from django.contrib.auth.models import User
from .models import Profile
class LoginUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']



    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("كلمات المرور لا تتطابق.")
        

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']       

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model =  Profile
        fields = ['image']        
