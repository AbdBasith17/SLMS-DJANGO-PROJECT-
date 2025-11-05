from django import forms
from students.models import StudentProfile, Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'student_id', 'user', 'phone', 'address', 'profile_pic',
            'institution', 'pass_out_year', 'guardian_name', 'guardian_contact',
            'linkedin_url', 'github_url', 'leetcode_url'
        ]
