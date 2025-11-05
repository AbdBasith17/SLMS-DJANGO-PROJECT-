from django import forms
from .models import StudentProfile, Enrollment,Course

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['bio', 'phone', 'address', 'profile_pic']

class EnrollForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']
class Course(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']


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
            'profile_pic': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'guardian_contact': forms.TextInput(attrs={'placeholder': 'Guardian contact'}),
            'address': forms.Textarea(attrs={'maxlength': 200, 'rows': 3}),
            'pass_out_year': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
        }
