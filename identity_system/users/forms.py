from django import forms
from .models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 
                  'date_of_birth', 'address', 'gender', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        date_of_birth = cleaned_data.get('date_of_birth')
        gender = cleaned_data.get('gender')
        
        if first_name and last_name and date_of_birth and gender:
            import hashlib
            hash_input = first_name + last_name + str(date_of_birth) + gender
            check_hash = hashlib.sha256(hash_input.encode()).hexdigest()
            
            if User.objects.filter(unique_hash=check_hash).exists():
                raise ValidationError('A user with this name, date of birth, and gender already exists!')
        
        return cleaned_data

class UserSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Search by name, email, phone, or ID...'
        })
    )