from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator



class CustomUser(AbstractUser):
    user_type_data = ((1, 'Principal'), (2, 'Teacher'), (3, 'Student'))
    user_type      = models.CharField(default=1, choices=user_type_data, max_length=10)


class Principal(models.Model):
    admin       = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    profile_pic = models.FileField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class Teacher(models.Model):
    admin            = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address          = models.TextField()
    sections         = models.ManyToManyField('Section', through='AssignSection')    
    num_regex        = RegexValidator(regex='^[0-9]{10,15}$', message='Example: 17882282')
    teacher_number   = models.CharField(validators=[num_regex], max_length=13, blank=True)
    gender           = models.CharField(max_length=10)
    dob              = models.DateField(default=timezone.now)
    profile_pic      = models.FileField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.admin.first_name} {self.admin.last_name}'
    def date_of_birth(self):
        return self.dob.strftime('%D-%M-%Y')
    
    def student_under_teacher(self):
        student = self.student_set.all().count()
        return student


class AssignSection(models.Model):
    re_teacher       = models.ForeignKey(Teacher, verbose_name="Teacher", related_name='teacher_related', on_delete=models.CASCADE)
    re_section       = models.ForeignKey('Section', verbose_name="Section", related_name='subject_related', on_delete=models.CASCADE)
    is_class_teacher = models.BooleanField(default=False)

    class Meta:
        unique_together = [['re_teacher', 're_section']]


class Section(models.Model):
    section_name = models.CharField(max_length=255)
    teachers     = models.ManyToManyField(Teacher, through='AssignSection')
    subjects     = models.ManyToManyField('Subject', through='AssignSubject')
    updated_at   = models.DateTimeField(auto_now=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
	    return self.section_name

    def student_count(self):
        count = self.student_set.all().count()
        return count

class Student(models.Model):
    admin         = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    index_number  = models.CharField(max_length=10, unique=True)
    gender        = models.CharField(max_length=10)
    profile_pic   = models.FileField()
    address       = models.TextField()
    academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE)
    num_regex     = RegexValidator(regex="^[0-9]{10,15}$", message="Example: 17882282")
    parent_number = models.CharField(validators=[num_regex], max_length=13, blank=True)
    dob           = models.DateField(default=timezone.now)
    my_section    = models.ForeignKey(Section, on_delete=models.CASCADE)
    profile_pic   = models.FileField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)


class AssignSubject(models.Model):
    rel_section = models.ForeignKey(Section, verbose_name="Section", related_name='related_section', on_delete=models.CASCADE)
    rel_subject = models.ForeignKey('Subject', verbose_name="Subject", related_name='related_subject', on_delete=models.CASCADE)

    class Meta:
        unique_together = [['rel_section', 'rel_subject']]

class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    teacher      = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sections     = models.ManyToManyField(Section, through='AssignSubject')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name
















class AcademicYear(models.Model):
    start_year = models.DateField()
    end_year   = models.DateField()

    def start_year(self):
        return self.start_year.strftime('%Y')
    
    def end_year(self):
        return self.end_year.strftime('%Y')


class Attendance(models.Model):
    subject         = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    academic_year_year    = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    student    = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status     = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStudent(models.Model):
    student       = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_date    = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status  = models.IntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)


class LeaveReportTeacher(models.Model):
    teacher       = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_date    = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status  = models.IntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)


class FeedBackStudent(models.Model):
    student        = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback       = models.TextField()
    feedback_reply = models.TextField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)


class FeedBackTeacher(models.Model):
    teacher        = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    feedback       = models.TextField()
    feedback_reply = models.TextField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)


class NotificationStudent(models.Model):
    student    = models.ForeignKey(Student, on_delete=models.CASCADE)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationTeacher(models.Model):
    teacher    = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Result(models.Model):
    student    = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject    = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_marks = models.FloatField(default=0)
    ia_marks   = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




'''Receiver'''
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:     
        if instance.user_type == 1:
            Principal.objects.create(admin=instance)
        if instance.user_type == 2:
            Teacher.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(
                admin=instance, 
                course_id=Section.objects.get(id=1), 
                academic_year=AcademicYear.objects.get(id=1), 
                address='', 
                profile_pic='', 
                gender=''
            )

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.principal.save()
    if instance.user_type == 2:
        instance.teacher.save()
    if instance.user_type == 3:
        instance.student.save()
    
