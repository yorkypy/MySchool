from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime # To Parse input DateTime into Python Date Time Object

from core_app.models import CustomUser, Teacher, Section, Subject, Student, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, Result


def student_home(request):
    student_obj = Student.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(student=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student=student_obj, status=False).count()

    section_obj = Section.objects.get(id=student_obj.section.id)
    total_subjects = Subject.objects.filter(section=section_obj).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subject.objects.filter(section=student_obj.section)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance__in=attendance, status=True, student=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance__in=attendance, status=False, student=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    
    context={
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "student/student_dashboard.html", context)


def student_view_attendance(request):
    student = Student.objects.get(admin=request.user.id) # Getting Logged in Student Data
    section = student.section # Getting section Enrolled of LoggedIn Student
    # section = Section.objects.get(id=student.section.id) # Getting section Enrolled of LoggedIn Student
    subjects = Subject.objects.filter(section=section) # Getting the Subjects of section Enrolled
    context = {
        "subjects": subjects
    }
    return render(request, "student/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subject.objects.get(id=subject)
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        # Getting Student Data Based on Logged in Data
        stud_obj = Student.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject=subject_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance__in=attendance, student=stud_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student/student_attendance_data.html', context)
       

def student_apply_leave(request):
    student_obj = Student.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'student/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Student.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student=student_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


def student_feedback(request):
    student_obj = Student.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Student.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Student.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Student.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):
    student = Student.objects.get(admin=request.user.id)
    student_result = Result.objects.filter(student=student.id)
    context = {
        "student_result": student_result,
    }
    return render(request, "student/student_view_result.html", context)





