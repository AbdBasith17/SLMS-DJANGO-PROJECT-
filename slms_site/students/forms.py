from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'profile_pic', 
            'phone',
            'address',
            'institution',
            'pass_out_year',
            'guardian_name',
            'guardian_contact',
            'linkedin_url',
            'github_url',
            'leetcode_url', 
        ]
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept':'image/*'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone number'}),
            'address': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'maxlength':200}),
            'linkedin_url': forms.TextInput(attrs={'class':'form-control'}),
            'github_url': forms.TextInput(attrs={'class':'form-control'}),
            'leetcode_url': forms.TextInput(attrs={'class':'form-control'}),
        }
