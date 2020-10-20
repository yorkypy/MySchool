from django.http import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from core_app.models import AssignSection, CustomUser, FeedBackTeacher, LeaveReportTeacher, Principal, Section, StudentUpload, Subject, Student, AcademicYear, FeedBackStudent, LeaveReportStudent, LeaveReportTeacher, Attendance, AttendanceReport, Teacher
from core_app.forms import AddStudentForm, AssignSectionForm, EditStudentForm


def principal_home(request):
    total_students = Student.objects.all().count()
    total_subjects = Subject.objects.all().count()
    total_sections = Section.objects.all().count()
    total_teachers = Teacher.objects.all().count()
    principal      = Principal.objects.all()
    
    """
    #Total Subjects and Student in each Section
    Section = Section.objects.all()
    section_name_list = []
    subject_count_list = []
    student_count_list_in_section = []

    for section in Section:
        subjects = Subjects.objects.filter(section=section.id).count()
        Student = Student.objects.filter(section=section.id).count()
        section_name_list.append(section.section_name)
        subject_count_list.append(subjects)
        student_count_list_in_section.append(Student)
    
    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        section = Section.objects.get(id=subject.section.id)
        student_count = Student.objects.filter(section=section.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)
    
    # For Teacher
    teacher_attendance_present_list=[]
    teacher_attendance_leave_list=[]
    teacher_name_list=[]

    Teacher= Teacher.objects.all()
    for teacher in Teacher:
        subjects = Subjects.objects.filter(teacher=teacher.admin.id)
        attendance = Attendance.objects.filter(subject__in=Section).count()
        leaves = LeaveReportTeacher.objects.filter(teacher=teacher.id, leave_status=1).count()
        teacher_attendance_present_list.append(attendance)
        teacher_attendance_leave_list.append(leaves)
        teacher_name_list.append(teacher.admin.first_name)


    # For Student
    student_attendance_present_list=[]
    student_attendance_leave_list=[]
    student_name_list=[]

    Student = Student.objects.all()
    for student in Student:
        attendance = AttendanceReport.objects.filter(student=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)
    """
    context = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_sections': total_sections,
        'total_teachers': total_teachers,
        'principal': principal

    }
    return render(request, 'principal/principal_dashboard.html', context)


def add_assign_section(request):
    form = AssignSectionForm()
    context = {
        'form': form
    }
    return render(request, 'principal/add_assign_section.html', context)

def add_assign_section_save(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid Method')
        return redirect('add-assign-section')
    else:
        form = AssignSectionForm(request.POST, request.FILES)

        if form.is_valid():
            re_teacher       = form.cleaned_data['re_teacher']
            re_section       = form.cleaned_data['re_section']
            is_class_teacher = form.cleaned_data['is_class_teacher']

            try:
                assign_section = AssignSection(
                    re_teacher=re_teacher,
                    re_section=re_section,
                    is_class_teacher=is_class_teacher
                )
                assign_section.save()
                             
                messages.success(request, 'Student Added Successfully!')
                return redirect('add-assign-section')
            except:
                messages.error(request, 'Failed to Add Student!')
                return redirect('add-assign-section')
        else:
            return redirect('add-assign-section')



def add_teacher(request):
    return render(request, 'principal/add_teacher.html')


def add_teacher_save(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid Method ')
        return redirect('add-teacher')
    else:
        first_name   = request.POST.get('first_name')
        last_name    = request.POST.get('last_name')
        username     = request.POST.get('username')
        email        = request.POST.get('email')
        password     = request.POST.get('password')
        address      = request.POST.get('address')
        dob          = request.POST.get('dob')
        teacher_number = request.POST.get('teacher_number')
        gender       = request.POST.get('gender')
        profile_pic  = request.POST.get('profile_pic')


        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.create_user(
                username=username, 
                password=password, 
                email=email, 
                first_name=first_name, 
                last_name=last_name, 
                user_type=2
            )
            user.teacher.dob=dob
            user.teacher.address = address
            user.teacher.teacher_number=teacher_number
            user.teacher.gender=gender
            user.teacher.profile_pic=profile_pic_url
            user.save()
            messages.success(request, 'Teacher Added Successfully!')
            return redirect('manage-teacher')
        except:
            messages.error(request, 'Failed to Add teacher!')
            return redirect('manage-teacher')
    

            
def manage_teacher(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers
    }
    return render(request, 'principal/manage_teacher.html', context)


def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.get(admin=teacher_id)
    context = {
        'teacher': teacher,
        'id': teacher
    }
    return render(request, 'principal/edit_teacher.html', context)


def edit_teacher_save(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        teacher        = request.POST.get('teacher')
        username       = request.POST.get('username')
        email          = request.POST.get('email')
        first_name     = request.POST.get('first_name')
        last_name      = request.POST.get('last_name')
        address        = request.POST.get('address')
        dob            = request.POST.get('dob')
        gender         = request.POST.get('gender')
        teacher_number = request.POST.get('teacher_number')
        teacher_id     = request.POST.get('teacher_id')

        

        try:
            # INSERTING into CustomUser Model
            user = CustomUser.objects.get(id=teacher_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Teacher Model
            teacher_obj=Teacher.objects.get(admin=teacher_id)
            teacher_obj.dob=dob
            teacher_obj.teacher_number=teacher_number
            teacher_obj.address=address
            teacher_obj.gender=gender
            teacher_obj.save()
            messages.success(request, 'Teacher Updated Successfully.')
            return redirect(reverse('manage-teacher'), {'teacher_id': teacher_id})

        except:
            messages.error(request, 'Failed to Update teacher.')
            return redirect(reverse('manage-teacher'), {'teacher_id': teacher})

def teacher_detail(request, teacher_id):
    teacher = Teacher.objects.get(admin=teacher_id)
    profile_image = Teacher.objects.all()
    context =  {
        'teacher': teacher,
        'profile_image': profile_image
    }
    return render(request, 'principal/teacher_detail.html',context)


def delete_teacher(request, teacher_id):
    teacher = Teacher.objects.get(admin=teacher_id)
    try:
        teacher.delete()
        messages.success(request, 'teacher Deleted Successfully.')
        return redirect('manage-teacher')
    except:
        messages.error(request, 'Failed to Delete teacher.')
        return redirect('manage-teacher')




# STUDENTS
def add_student(request):
    sections = Section.objects.all()
        
    context = {
        'sections': sections
    }
    return render(request, 'principal/add_student.html', context)


def add_student_save(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid Method')
        return redirect('add-student')
    else:
        first_name      = request.POST.get('first_name')
        last_name       = request.POST.get('last_name')
        email           = request.POST.get('email')
        index_number    = request.POST.get('index_number')
        address         = request.POST.get('address')
        dob             = request.POST.get('dob')
        parent_number   = request.POST.get('parent_number')
        gender          = request.POST.get('gender')
        section         = request.POST.get('section')
        profile_pic     = request.POST.get('profile_pic')


        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        
        my_sec = Section.objects.get(section_name=section)

        try:
            student = Student(
                first_name=first_name,
                last_name=last_name,
                email=email,
                index_number=index_number,
                address=address,
                parent_number=parent_number,
                profile_pic=profile_pic_url,
                gender=gender,
                dob=dob
            )
            student.my_section=my_sec
            student.save()
            messages.success(request, 'Student Added Successfully!')
            return redirect(reverse('manage-student'))
        except:
            messages.error(request, 'Failed to Add Student!')
            return redirect(reverse('manage-student'))
    

def manage_student(request):
    students = Student.objects.all()
    context = {
        'students': students
    }
    return render(request, 'principal/manage_student.html', context)


def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    context = {
        'student': student,
        'id': student
    }
    return render(request, 'principal/edit_student.html', context)


def edit_student_save(request):
    if request.method != 'POST':
        return HttpResponse('Invalid Method!')
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect(reverse('manage_student'))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email      = form.cleaned_data['email']
            index_number  = form.cleaned_data['index_number'] 
            parent_number = form.cleaned_data['parent_number']
            address     = form.cleaned_data['address']
            profile_pic = form.cleaned_data['profile_pic']
            gender      = form.cleaned_data['gender']
            aca_year    = form.cleaned_data['aca_year']
            section     = form.cleaned_data['my_section']
            dob         = form.cleaned_data['dob']  

            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
                               
            try:
                academic_year_obj = AcademicYear.objects.get(id=aca_year)            
                section_obj = Section.objects.get(id=section)
                student = Student(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    address=address,
                    dob=dob,
                    gender=gender,
                    parent_number=parent_number,
                    index_number=index_number,
                    profile_pic=profile_pic_url,
                )

                student.academic_year=academic_year_obj
                student.my_section=section_obj
                student.save()
                messages.success(request, 'Student Updated Successfully.')
                return redirect(reverse('manage-student'), {'student_id': student_id})
            except:
                messages.error(request, 'Failed to Update student.')
                return redirect(reverse('manage-student'), {'student_id': student_id})

        
def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    profile_pic = Student.objects.all()
    context = {
        'student': student,
        'profile_pic': profile_pic
    }
    return render(request, 'principal/student_detail.html', context)


def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    try:
        student.delete()
        messages.success(request, 'Student Deleted Successfully.')
        return redirect('manage-student')
    except:
        messages.error(request, 'Failed to Delete Student.')
        return redirect('manage-student')


class StudentUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentUpload
    template_name = 'principal/students_upload.html'
    fields = ['csv_file']
    success_url = 'manage-student'
    success_message = 'Successfully uploaded students'

@login_required
def downloadcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_template.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
        'firstname', 
        'last_name', 
        'email',
        'gender', 
        'parent_number', 
        'address', 
        'dob',
        'academic_year',
        'my_section',
        ]
    )
    return response




#SECTION/CLASS
def add_section(request):
    class_teacher = CustomUser.objects.filter(user_type='2')
    context = {
        'class_teacher': class_teacher
    }
    return render(request, 'principal/add_section.html', context)


def add_section_save(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid Method!')
        return redirect('add-section')
    else:
        section = request.POST.get('class')
        try:
            section_model = Section(
                section_name=section,
            )
            section_model.save()
            messages.success(request, 'Class added successfully!')
            return redirect('manage-section')
        except:
            messages.error(request, 'Failed to add class!')
            return redirect('manage-section')


def manage_section(request):
    sections = Section.objects.all()
    
    context = {
        'sections': sections,
    }
    return render(request, 'principal/manage_section.html', context)


def edit_section(request, section_id):
    section = Section.objects.get(id=section_id)
    context = {
        'section': section,
        'id': section_id
    }
    return render(request, 'principal/edit_section.html', context)


def edit_section_save(request):
    if request.method != 'POST':
        HttpResponse('Invalid Method')
    else:
        section = request.POST.get('section')
        section_id = request.POST.get('section_id')

        try:
            section_obj = Section.objects.get(id=section_id)
            section_obj.section_name = section
            section_obj.save()

            messages.success(request, 'Section Updated Successfully.')
            return redirect(reverse('manage-section'), {'section_id': section_id})
        except:
            messages.error(request, 'Failed to Update section.')
            return redirect(reverse('manage-section'), {'section_id': section_id})


def delete_section(request, section_id):
    section = Section.objects.get(id=section_id)
    try:
        section.delete()
        messages.success(request, 'section Deleted Successfully.')
        return redirect('manage-section')
    except:
        messages.error(request, 'Failed to Delete section.')
        return redirect('manage-section')




def add_academic_year(request):
    return render(request, 'principal/add_academic_year.html')


def manage_academic_year(request):
    academic_years = AcademicYear.objects.all()
    context = {
        'academic_years': academic_years
    }
    return render(request, 'principal/manage_academic_year.html', context)


def add_academic_year_save(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid Method')
        return redirect('add-academic')
    else:
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')

        #try:
        academic_year = AcademicYear(
            aca_start_year=start_year, 
            aca_end_year=end_year
        )
        academic_year.save()
        messages.success(request, 'Academic Year added Successfully!')
        return redirect('manage-academic-year')
        #except:
        #    messages.error(request, 'Failed to Add Academic Year')
        #    return redirect('manage-academic-year')


def edit_academic_year(request, academic_year_id):
    academic_year = AcademicYear.objects.get(id=academic_year_id)
    context = {
        'academic_year': academic_year
    }
    return render(request, 'principal/edit_academic_year.html', context)


def edit_academic_year_save(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid Method!')
        return redirect('manage-academic-year')
    else:
        academic_year = request.POST.get('academic_year')
        academic_year_start_year = request.POST.get('academic_year_start_year')
        academic_year_end_year = request.POST.get('academic_year_end_year')

        try:
            academic_year = AcademicYear.objects.get(id=academic_year)
            academic_year.academic_year_start_year = academic_year_start_year
            academic_year.academic_year_end_year = academic_year_end_year
            academic_year.save()

            messages.success(request, 'academic_year Year Updated Successfully.')
            return redirect('/edit-academic-year/'+academic_year)
        except:
            messages.error(request, 'Failed to Update academic_year Year.')
            return redirect('/edit-academic-year/'+academic_year)


def delete_academic_year(request, academic_year_id):
    academic_year = AcademicYear.objects.get(id=academic_year_id)
    try:
        academic_year.delete()
        messages.success(request, 'academic_year Deleted Successfully.')
        return redirect('manage-academic-year')
    except:
        messages.error(request, 'Failed to Delete academic_year.')
        return redirect('manage-academic-year')



def add_subject(request):
    teachers = CustomUser.objects.filter(user_type='2')
    context = {
        'teachers': teachers
    }
    return render(request, 'principal/add_subject.html', context)



def add_subject_save(request):
    if request.method != 'POST':
        messages.error(request, 'Method Not Allowed!')
        return redirect('add-subject')
    else:
        subject_name = request.POST.get('subject')

        teacher_id = request.POST.get('subject_t')
        teacher = CustomUser.objects.get(id=teacher_id)  

        try:
            subject = Subject(
                subject_name=subject_name, 
            )
            subject.subject_teacher=teacher
            subject.save()
            messages.success(request, 'Subject Added Successfully!')
            return redirect('manage-subject')
        except:
            messages.error(request, 'Failed to Add Subject!')
            return redirect('manage-subject')


def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects
    }
    return render(request, 'principal/manage_subject.html', context)


def edit_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    context = {
        'subject': subject,
        'id': subject
    }
    return render(request, 'principal/edit_subject.html', context)


def edit_subject_save(request):
    if request.method != 'POST':
        HttpResponse('Invalid Method.')
    else:
        subject = request.POST.get('subject')
        subject_name = request.POST.get('subject')
    
        try:
            subject = Subject.objects.get(id=subject)
            subject.subject_name = subject_name
            subject.save()

            messages.success(request, 'Subject Updated Successfully.')
            return HttpResponseRedirect(reverse('edit-subject', kwargs={'subject':subject}))

        except:
            messages.error(request, 'Failed to Update Subject.')
            return HttpResponseRedirect(reverse('edit-subject', kwargs={'subject':subject}))



def delete_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, 'Subject Deleted Successfully.')
        return redirect('manage-subject')
    except:
        messages.error(request, 'Failed to Delete Subject.')
        return redirect('manage-subject')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_section_exist(request):
    section = request.POST.get('class')
    section_obj = Section.objects.filter(section_name=section).exists()
    if section_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)



def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        'feedbacks': feedbacks
    }
    return render(request, 'principal/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse('True')

    except:
        return HttpResponse('False')


def teacher_feedback_message(request):
    feedbacks = FeedBackTeacher.objects.all()
    context = {
        'feedbacks': feedbacks
    }
    return render(request, 'principal/teacher_feedback_template.html', context)


@csrf_exempt
def teacher_feedback_message_reply(request):
    feedback = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackTeacher.objects.get(id=feedback)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse('True')

    except:
        return HttpResponse('False')


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        'leaves': leaves
    }
    return render(request, 'principal/student_leave_view.html', context)

def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def teacher_leave_view(request):
    leaves = LeaveReportTeacher.objects.all()
    context = {
        'leaves': leaves
    }
    return render(request, 'principal/teacher_leave_view.html', context)


def teacher_leave_approve(request, leave_id):
    leave = LeaveReportTeacher.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('teacher_leave_view')


def teacher_leave_reject(request, leave):
    leave = LeaveReportTeacher.objects.get(id=leave)
    leave.leave_status = 2
    leave.save()
    return redirect('teacher_leave_view')


def principal_view_attendance(request):
    subjects = Subject.objects.all()
    academic_years = AcademicYear.objects.all()
    context = {
        'subjects': subjects,
        'academic_years': academic_years
    }
    return render(request, 'principal/principal_view_attendance.html', context)


@csrf_exempt
def principal_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject = request.POST.get('subject')
    academic_year = request.POST.get('academic_year')

    # Student enroll to section, section has Subjects
    # Getting all data from subject model based on subject
    subject_model = Subject.objects.get(id=subject)

    academic_year_model = AcademicYear.objects.get(id=academic_year)

    # Student = Student.objects.filter(section=subject_model.section, academic_year=academic_year_model)
    attendance = Attendance.objects.filter(subject=subject_model, academic_year=academic_year_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={
            'id':attendance_single.id, 
            'attendance_date':str(attendance_single.attendance_date), 
            'academic_year':attendance_single.academic_year.id
        }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type='application/json', safe=False)


@csrf_exempt
def principal_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={
            'id':student.student.admin.id, 
            'name':student.student.admin.first_name+' '+student.student.admin.last_name, 
            'status':student.status
        }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type='application/json', safe=False)


def principal_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        'user': user
    }
    return render(request, 'principal/principal_profile.html', context)


def principal_profile_update(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid Method!')
        return redirect('principal-profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != '':
                customuser.set_password(password)
            customuser.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('principal-profile')
        except:
            messages.error(request, 'Failed to Update Profile')
            return redirect('principal-profile')
    


def teacher_profile(request):
    pass


def student_profile(requtest):
    pass



