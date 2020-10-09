from core_app.forms import AddStudentForm, EditStudentForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from core_app.models import CustomUser, LeaveReportTeacher, Principal, Teacher, Section, Subject, Student, AcademicYear, Attendance, AttendanceReport, FeedBackTeacher, Result


def teacher_home(request):
    # Fetching All Student under Staff

    subjects = Subject.objects.filter(teacher=request.admin.id)
    section_list = []
    for subject in subjects:
        section = Section.objects.get(id=subject.section.id)
        section_list.append(section.id)
    
    final_section = []
    # Removing Duplicate section Id
    for section in section_list:
        if section not in final_section:
            final_section.append(section)
    
    Student_count = Student.objects.filter(section__in=final_section).count()
    subject_count = subjects.count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(subject__in=subjects).count()
    # Fetch All Approve Leave
    staff = Teacher.objects.get(admin=request.admin.id)
    leave_count = LeaveReportTeacher.objects.filter(teacher=staff.id, leave_status=1).count()

    #Fetch Attendance Data by Subjects
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    student_attendance = Student.objects.filter(section__in=final_section)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in student_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student=student.id).count()
        student_list.append(student.admin.first_name+" "+ student.admin.last_name)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    context={
        "Student_count": Student_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "student_list": student_list,
        "attendance_present_list": student_list_attendance_present,
        "attendance_absent_list": student_list_attendance_absent
    }
    return render(request, "teacher/teacher_home_template.html", context)



def teacher_take_attendance(request):
    subjects = Subject.objects.filter(teacher=request.admin.id)
    academic_years = AcademicYear.objects.all()
    context = {
        "subjects": subjects,
        "academic_years": academic_years
    }
    return render(request, "teacher/take_attendance_template.html", context)


def teacher_apply_leave(request):
    teacher_obj = Teacher.objects.get(admin=request.admin.id)
    leave_data = LeaveReportTeacher.objects.filter(teacher=teacher_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "teacher/teacher_apply_leave_template.html", context)


def teacher_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        teacher_obj = Teacher.objects.get(admin=request.admin.id)
        try:
            leave_report = LeaveReportTeacher(teacher=teacher_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('teacher_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('teacher_apply_leave')


def teacher_feedback(request):
    teacher_obj = Teacher.objects.get(admin=request.admin.id)
    feedback_data = FeedBackTeacher.objects.filter(teacher=teacher_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "teacher/teacher_feedback_template.html", context)


def teacher_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('teacher_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        teacher_obj = Teacher.objects.get(admin=request.admin.id)

        try:
            add_feedback = FeedBackTeacher(teacher=teacher_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('teacher_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('teacher_feedback')


# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_Student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject = request.POST.get("subject")
    academic_year = request.POST.get("academic_year")

    # Student enroll to section, section has Subjects
    # Getting all data from subject model based on subject
    subject_model = Subject.objects.get(id=subject)
    academic_year_model = AcademicYear.objects.get(id=academic_year)
    student = Student.objects.filter(
        section=subject_model.section, 
        academic_year=academic_year_model
    )

    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in Student:
        data_small={
            "id":student.admin.id, 
            "name":student.admin.first_name+" "+student.admin.last_name
        }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)




@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    Student = request.POST.get("Student")
    subject = request.POST.get("subject")
    attendance_date = request.POST.get("attendance_date")
    academic_year = request.POST.get("academic_year")

    subject_model = Subject.objects.get(id=subject)
    academic_year_model = AcademicYear.objects.get(id=academic_year)

    json_student = json.loads(Student)
    # print(dict_student[0]['id'])

    # print(Student)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(
            subject=subject_model, 
            attendance_date=attendance_date, 
            academic_year=academic_year_model
        )
        attendance.save()

        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Student.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(
                student=student, 
                attendance=attendance, 
                status=stud['status']
            )
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")




def teacher_update_attendance(request):
    subjects = Subject.objects.filter(teacher=request.admin.id)
    academic_years = AcademicYear.objects.all()
    context = {
        "subjects": subjects,
        "academic_years": academic_years
    }
    return render(request, "teacher/update_attendance_template.html", context)

@csrf_exempt
def get_attendance_dates(request):
    

    # Getting Values from Ajax POST 'Fetch Student'
    subject = request.POST.get("subject")
    academic_year = request.POST.get("academic_year")

    # Student enroll to section, section has Subjects
    # Getting all data from subject model based on subject
    subject_model = Subject.objects.get(id=subject)

    academic_year_model = AcademicYear.objects.get(id=academic_year)

    # Student = Student.objects.filter(section=subject_model.section, academic_year=academic_year_model)
    attendance = Attendance.objects.filter(subject=subject_model, academic_year=academic_year_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "academic_year":attendance_single.academic_year.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student.admin.id, "name":student.student.admin.first_name+" "+student.student.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def update_attendance_data(request):
    Student = request.POST.get("Student")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_student = json.loads(Student)

    try:
        
        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Student.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(student=student, attendance=attendance)
            attendance_report.status=stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def teacher_profile(request):
    admin = CustomUser.objects.get(id=request.admin.id)
    staff = Teacher.objects.get(admin=admin)

    context={
        "admin": admin,
        "staff": staff
    }
    return render(request, 'teacher/teacher_profile.html', context)


def teacher_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('teacher_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.admin.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Teacher.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('teacher_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('teacher_profile')



def teacher_add_result(request):
    subjects = Subject.objects.filter(teacher=request.admin.id)
    academic_years = AcademicYear.objects.all()
    context = {
        'subjects': subjects,
        'academic_years': academic_years,
    }
    return render(request, "teacher/add_result_template.html", context)


def teacher_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_add_result')
    else:
        student_admin = request.POST.get('student_list')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject = request.POST.get('subject')

        student_obj = Student.objects.get(admin=student_admin)
        subject_obj = Subject.objects.get(id=subject)

        try:
            # Check if Student Result Already Exists or not
            check_exist = Result.objects.filter(subject=subject_obj, student=student_obj).exists()
            if check_exist:
                result = Result.objects.get(subject=subject_obj, student=student_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
                messages.success(request, "Result Updated Successfully!")
                return redirect('teacher_add_result')
            else:
                result = Result(
                    student=student_obj, 
                    subject=subject_obj, 
                    subject_exam_marks=exam_marks, 
                    subject_assignment_marks=assignment_marks
                )
                result.save()
                messages.success(request, "Result Added Successfully!")
                return redirect('teacher_add_result')
        except:
            messages.error(request, "Failed to Add Result!")
            return redirect('teacher_add_result')


def manage_result(request):
    #subject_model = Subjects.objects.get(teacher=request.admin.id)
    #academic_year_model = AcademicYear.objects.get(id=academic_year)
    #Student = Student.objects.filter(
    #    section=subject_model.section, 
    #    #academic_year=academic_year_model
    #)
    Student = Result.objects.all()
    results = Result.objects.all()
    #Student_under_staff = Student_set.all()
    context = {
        "Student": Student,
        'results': results
    }
    return render(request, 'teacher/manage_result.html', context)



#staff add student
def teacher_add_student(request):
    form = AddStudentForm()
    context = {
        "form": form
    }
    return render(request, 'teacher/add_student.html', context)


def teacher_add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('teacher_add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name      = form.cleaned_data['first_name']
            last_name       = form.cleaned_data['last_name']
            adminname        = form.cleaned_data['adminname']
            email           = form.cleaned_data['email']
            password        = form.cleaned_data['password']
            address         = form.cleaned_data['address']
            academic_year = form.cleaned_data['academic_year']
            section       = form.cleaned_data['section']
            gender          = form.cleaned_data['gender']
            parent_number   = form.cleaned_data['parent_number']
            dob             = form.cleaned_data['dob']
            
            """ Getting Profile Pic first
            First Check whether the file is selected or not
            Upload only if file is selected  """
            

            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                admin = CustomUser.objects.create_admin(adminname=adminname, password=password, email=email, first_name=first_name, last_name=last_name, admin_type=3)
                admin.Student.address = address

                section_obj = Section.objects.get(id=section)
                admin.Student.section = section_obj

                academic_year_obj = AcademicYear.objects.get(id=academic_year)
                admin.Student.academic_year = academic_year_obj
                admin.Student.parent_number=parent_number
                admin.Student.dob=dob

                admin.Student.gender = gender
                admin.Student.profile_pic = profile_pic_url
                admin.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('teacher_add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('teacher_add_student')
        else:
            return redirect('teacher_add_student')


def teacher_manage_student(request):
    student = Student.objects.filter(subjects_set__teacher=2)
    context = {
        "Student": Student
    }
    return render(request, 'teacher/manage_student.html', context)


def teacher_edit_student(request, student):
    # Adding Student ID into academic_year Variable
    request.academic_year['student'] = student

    student = Student.objects.get(admin=student)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['adminname'].initial = student.admin.adminname
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['section'].initial = student.section.id
    form.fields['gender'].initial = student.gender
    form.fields['academic_year'].initial = student.academic_year.id

    context = {
        "id": student,
        "adminname": student.admin.adminname,
        "form": form
    }
    return render(request, "teacher/edit_student.html", context)


def teacher_edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student = request.academic_year.get('student')
        if student == None:
            return redirect('/teacher_manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            adminname = form.cleaned_data['adminname']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            section = form.cleaned_data['section']
            gender = form.cleaned_data['gender']
            academic_year = form.cleaned_data['academic_year']

            
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom Admin Model
                admin = CustomUser.objects.get(id=student)
                admin.first_name = first_name
                admin.last_name = last_name
                admin.email = email
                admin.adminname = adminname
                admin.save()

                # Then Update Student Table
                student_model = Student.objects.get(admin=student)
                student_model.address = address

                section = Section.objects.get(id=section)
                student_model.section = section

                academic_year_obj = AcademicYear.objects.get(id=academic_year)
                student_model.academic_year = academic_year_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student academic_year after the data is updated
                del request.academic_year['student']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/teacher_edit_student/'+student)
            except:
                messages.success(request, "Failed to Update Student.")
                return redirect('/teacher_edit_student/'+student)
        else:
            return redirect('/teacher_edit_student/'+student)


def teacher_delete_student(request, student):
    student = Student.objects.get(admin=student)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('teacher_manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('teacher_manage_student')


