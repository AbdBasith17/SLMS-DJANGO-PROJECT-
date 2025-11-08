from django import forms
from students.models import StudentProfile, Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'notion_link']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notion_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Paste Notion lesson link'}),
        }

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
             'phone', 'address', 'profile_pic',
            'institution', 'pass_out_year', 'guardian_name', 'guardian_contact',
            'linkedin_url', 'github_url', 'leetcode_url'
        ]



from django.contrib.auth import get_user_model
User = get_user_model()



class AdminForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Set password only when creating a new admin."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'Admin'
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
