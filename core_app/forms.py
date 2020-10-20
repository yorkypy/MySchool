from os import execl
from django import forms
from django.db.models import fields 
from django.forms import Form, ModelForm
from django.forms import widgets
from .models import AssignSection, Section, AcademicYear, Student


class DateInput(forms.DateInput):
    input_type = "date"



class AddStudentForm(forms.Form):

    data = forms.TextInput(
        attrs={"class":"form-control"}
    )
    
    first_name   = forms.CharField(label="First Name", max_length=50,widget=data)
    last_name    = forms.CharField(label="Last Name", max_length=50, widget=data)
    email        = forms.EmailField(label="Email", max_length=50, widget=data)
    index_number = forms.CharField(label="Index Number", max_length=10, widget=data)
    address      = forms.CharField(label="Address", max_length=50, widget=data)
    
     #For Displaying Section
    try:
        sections = Section.objects.all()
        section_list = []
        for section in sections:
            single_section = (section.id, section.section_name)
            section_list.append(single_section)
    except:
        section_list = []
    
    #For Displaying Academic Years
    try:
        aca_years = AcademicYear.objects.all()
        year_list = []
        for year in aca_years:
            single_year = (year.id, str(year.aca_start_year)+" to "+str(year.aca_end_year))
            year_list.append(single_year)
    except:
        year_list = []
    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    dob           = forms.DateField(label="Date of Birth", widget=DateInput(attrs={"class":"form-control"}))
    parent_number = forms.CharField(label="Parent's Number", widget=forms.TextInput(attrs={"class":"form-control"}))
    gender        = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    section       = forms.ChoiceField(label="Class/Section", choices=section_list, widget=forms.Select(attrs={"class":"form-control"}))
    aca_year      = forms.ChoiceField(label="Academic Year", choices=year_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic   = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))


""" class AddStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'
        execlude = ('admin', 'created_at', 'updated_at')
        widgets = {
            "class":"form-control"
        } """

class EditStudentForm(forms.Form):

    data = forms.TextInput(
        attrs={"class":"form-control"}
    )
    
    first_name   = forms.CharField(label="First Name", max_length=50,widget=data)
    last_name    = forms.CharField(label="Last Name", max_length=50, widget=data)
    index_number = forms.CharField(label="Index Number", max_length=10, widget=data)
    email        = forms.EmailField(label="Email", max_length=50, widget=data)
    address      = forms.CharField(label="Address", max_length=50, widget=data)
    
    #For Displaying Section
    try:
        sections = Section.objects.all()
        section_list = []
        for section in sections:
            single_section = (section.id, section.section_name)
            section_list.append(single_section)
    except:
        section_list = []
    
    #For Displaying Academic Years
    try:
        aca_years = AcademicYear.objects.all()
        year_list = []
        for year in aca_years:
            single_year = (year.id, str(year.aca_start_year)+" to "+str(year.aca_end_year))
            year_list.append(single_year)
    except:
        year_list = []
    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    parent_number = forms.CharField(label="Parent's Number", widget=data)
    dob           = forms.DateField(label="Date of Birth", widget=data)
    gender        = forms.ChoiceField(label="Gender", choices=gender_list, widget=data)
    my_section    = forms.ChoiceField(label="Section", choices=section_list,widget=data)
    aca_year      = forms.ChoiceField(label="Academic Year", choices=year_list, widget=data)
    profile_pic   = forms.FileField(label="Profile Pic", required=False, widget=data)


class AssignSectionForm(ModelForm):
    class Meta:
        model = AssignSection
        fields = '__all__'