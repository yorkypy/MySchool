from django import forms
from django.db.models import fields 
from django.forms import Form, ModelForm
from .models import AssignSection, Section, AcademicYear


class DateInput(forms.DateInput):
    input_type = "date"



class AddStudentForm(forms.Form):
    first_name    = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name     = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username      = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    index_number  = forms.CharField(label="Index Number", max_length=10, widget=forms.TextInput(attrs={"class":"form-control"}))
    email         = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    address       = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    parent_number = forms.CharField(label="Parent's Number", widget=forms.TextInput(attrs={"class":"form-control"}))
    dob           = forms.DateField(label="Date of Birth", widget=DateInput(attrs={"class":"form-control"}))
    password      = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))

    
    #For Displaying Section
    try:
        Section = Section.objects.all()
        course_list = []
        for course in Section:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []
    
    #For Displaying academic_year Years
    try:
        academic_years = AcademicYear.objects.all()
        academic_year_year_list = []
        for academic_year_year in academic_years:
            single_academic_year_year = (academic_year_year.id, str(academic_year_year.academic_year_start_year)+" to "+str(academic_year_year.academic_year_end_year))
            academic_year_year_list.append(single_academic_year_year)
            
    except:
        academic_year_year_list = []
    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    course_id = forms.ChoiceField(label="Class/Section", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    academic_year_year_id = forms.ChoiceField(label="academic_year Year", choices=academic_year_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # academic_year_start_year = forms.DateField(label="academic_year Start", widget=DateInput(attrs={"class":"form-control"}))
    # academic_year_end_year = forms.DateField(label="academic_year End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))



class EditStudentForm(forms.Form):
    #For Displaying Section
    try:
        Section = Section.objects.all()
        course_list = []
        for course in Section:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    #For Displaying academic_year Years
    try:
        academic_years = AcademicYear.objects.all()
        academic_year_year_list = []
        for academic_year_year in academic_years:
            single_academic_year_year = (academic_year_year.id, str(academic_year_year.academic_year_start_year)+" to "+str(academic_year_year.academic_year_end_year))
            academic_year_year_list.append(single_academic_year_year)
            
    except:
        academic_year_year_list = []

    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    academic_year_year_id = forms.ChoiceField(label="academic_year Year", choices=academic_year_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))



""" #Staff Form

class AddStaffForm(forms.Form):
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    first_name   = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name    = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username     = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email        = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password     = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    staff_number = forms.CharField(label="Parent's Number", widget=forms.TextInput(attrs={"class":"form-control"}))
    address      = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))    
    gender       = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    dob          = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={"class":"form-control"}))
    profile_pic  = forms.FileField(label="Passport", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
"""




class AssignSectionForm(ModelForm):
    class Meta:
        model = AssignSection
        fields = '__all__'