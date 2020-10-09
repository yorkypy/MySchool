
from os import name
from django.urls import path
from core_app.views import views, principal, teacher, student 


urlpatterns = [
    #Authentication
    path('', views.home, name='home'),
    path('login/', views.loginPage, name="login"),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('principal_home/', principal.principal_home, name="principal_home"),

    #Principal
    path('add_teacher/', principal.add_teacher, name="add_teacher"),
    path('add_teacher_save/', principal.add_teacher_save, name="add_teacher_save"),
    path('manage_teacher/', principal.manage_teacher, name="manage-teacher"),
    path('edit_teacher/<teacher_id>/', principal.edit_teacher, name="edit-teacher"),
    path('edit_teacher_save/', principal.edit_teacher_save, name="edit-teacher-save"),
    path('delete_teacher/<teacher_id>/', principal.delete_teacher, name="delete-teacher"),
    path('teacher_detail/<teacher_id>', principal.teacher_detail, name='teacher-detail'),
    path('add_assign_section/', principal.add_assign_section, name='add-assign-section'),

    path('add_section/', principal.add_section, name="add-section"),
    path('add_section_save/', principal.add_section_save, name="add-section-save"),
    path('manage_section/', principal.manage_section, name="manage-section"),
    path('edit_section/<section_id>/', principal.edit_section, name="edit-section"),
    path('edit_section_save/', principal.edit_section_save, name="edit-section-save"),
    path('delete_section/<section_id>/', principal.delete_section, name="delete-section"),

    path('manage_academic_year/', principal.manage_academic_year, name="manage_academic_year"),
    path('add_academic_year/', principal.add_academic_year, name="add_academic_year"),
    path('add_academic_year_save/', principal.add_academic_year_save, name="add_academic_year_save"),
    path('edit_academic_year/<academic_year_id>', principal.edit_academic_year, name="edit_academic_year"),
    path('edit_academic_year_save/', principal.edit_academic_year_save, name="edit_academic_year_save"),
    path('delete_academic_year/<academic_year_id>/', principal.delete_academic_year, name="delete_academic_year"),

    path('add_student/', principal.add_student, name="add_student"),
    path('add_student_save/', principal.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', principal.edit_student, name="edit_student"),
    path('edit_student_save/', principal.edit_student_save, name="edit_student_save"),
    path('manage_student/', principal.manage_student, name="manage_student"),
    path('student_detail/<student_id>', principal.student_detail, name='student_detail'),
    path('delete_student/<student_id>/', principal.delete_student, name="delete_student"),

    path('add_subject/', principal.add_subject, name="add_subject"),
    path('add_subject_save/', principal.add_subject_save, name="add_subject_save"),
    path('manage_subject/', principal.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>/', principal.edit_subject, name="edit_subject"),
    path('edit_subject_save/', principal.edit_subject_save, name="edit_subject_save"),
    path('delete_subject/<subject_id>/', principal.delete_subject, name="delete_subject"),
    
    path('check_email_exist/', principal.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', principal.check_username_exist, name="check_username_exist"),
    path('student_feedback_message/', principal.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_reply/', principal.student_feedback_message_reply, name="student_feedback_message_reply"),
    path('teacher_feedback_message/', principal.teacher_feedback_message, name="teacher_feedback_message"),
    path('teacher_feedback_message_reply/', principal.teacher_feedback_message_reply, name="teacher_feedback_message_reply"),
    path('student_leave_view/', principal.student_leave_view, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', principal.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', principal.student_leave_reject, name="student_leave_reject"),
    path('teacher_leave_view/', principal.teacher_leave_view, name="teacher_leave_view"),
    path('teacher_leave_approve/<leave_id>/', principal.teacher_leave_approve, name="teacher_leave_approve"),
    path('teacher_leave_reject/<leave_id>/', principal.teacher_leave_reject, name="teacher_leave_reject"),
    path('principal_view_attendance/', principal.principal_view_attendance, name="principal_view_attendance"),
    path('principal_get_attendance_dates/', principal.principal_get_attendance_dates, name="principal_get_attendance_dates"),
    path('principal_get_attendance_student/', principal.principal_get_attendance_student, name="principal_get_attendance_student"),
    path('principal_profile/', principal.principal_profile, name="principal-profile"),
    path('principal_profile_update/', principal.principal_profile_update, name="principal-profile-update"),
    


    # URLS for teacher
    path('teacher_home/', teacher.teacher_home, name="teacher_home"),
    path('teacher_take_attendance/', teacher.teacher_take_attendance, name="teacher_take_attendance"),
    path('get_Student/', teacher.get_Student, name="get_Student"),
    path('save_attendance_data/', teacher.save_attendance_data, name="save_attendance_data"),
    path('teacher_update_attendance/', teacher.teacher_update_attendance, name="teacher_update_attendance"),
    path('get_attendance_dates/', teacher.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', teacher.get_attendance_student, name="get_attendance_student"),
    path('update_attendance_data/', teacher.update_attendance_data, name="update_attendance_data"),
    path('teacher_apply_leave/', teacher.teacher_apply_leave, name="teacher_apply_leave"),
    path('teacher_apply_leave_save/', teacher.teacher_apply_leave_save, name="teacher_apply_leave_save"),
    path('teacher_feedback/', teacher.teacher_feedback, name="teacher_feedback"),
    path('teacher_feedback_save/', teacher.teacher_feedback_save, name="teacher_feedback_save"),
    path('teacher_profile/', teacher.teacher_profile, name="teacher_profile"),
    path('teacher_profile_update/', teacher.teacher_profile_update, name="teacher_profile_update"),
    path('teacher_add_result/', teacher.teacher_add_result, name="teacher_add_result"),
    path('teacher_add_result_save/', teacher.teacher_add_result_save, name="teacher_add_result_save"),
    path('manage_result/', teacher.manage_result, name="manage_result"),


    path('teacher_add_student/', teacher.teacher_add_student, name="teacher_add_student"),
    path('teacher_add_student_save/', teacher.teacher_add_student_save, name="teacher_add_student_save"),
    path('teacher_edit_student/<student_id>', teacher.teacher_edit_student, name="teacher_edit_student"),
    path('teacher_edit_student_save/', teacher.teacher_edit_student_save, name="teacher_edit_student_save"),
    path('teacher_manage_student/', teacher.teacher_manage_student, name="teacher_manage_student"),
    path('teacher_delete_student/<student_id>/', teacher.teacher_delete_student, name="teacher_delete_student"),

    # URSL for Student
    path('student_home/', student.student_home, name="student_home"),
    path('student_view_attendance/', student.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', student.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave/', student.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save/', student.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback/', student.student_feedback, name="student_feedback"),
    path('student_feedback_save/', student.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', student.student_profile, name="student_profile"),
    path('student_profile_update/', student.student_profile_update, name="student_profile_update"),
    path('student_view_result/', student.student_view_result, name="student_view_result"),
]
