from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator



class CustomUser(AbstractUser):
    user_type_data = ((1, "Principal"), (2, "Teacher"), (3, "Student"))
    user_type      = models.CharField(default=1, choices=user_type_data, max_length=10)


class Principal(models.Model):
    user        = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    profile_pic = models.FileField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class Teachers(models.Model):
    user             = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address          = models.TextField()
    my_classes       = models.ManyToManyField('Sections')
    is_class_teacher = models.BooleanField(default=False)
    num_regex        = RegexValidator(regex="^[0-9]{10,15}$", message="Example: 17882282")
    teacher_number   = models.CharField(validators=[num_regex], max_length=13, blank=True)
    gender           = models.CharField(max_length=10)
    dob              = models.DateField(default=timezone.now)
    profile_pic      = models.FileField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def date_of_birth(self):
        return self.dob.strftime('%D-%M-%Y')
    
    def students_under_teacher(self):
        students = self.students_set.all().count()
        return students


class Students(models.Model):
    user          = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender        = models.CharField(max_length=10)
    profile_pic   = models.FileField()
    address       = models.TextField()
    session_year  = models.ForeignKey('AcademicYear', on_delete=models.CASCADE)
    num_regex     = RegexValidator(regex="^[0-9]{10,15}$", message="Example: 17882282")
    parent_number = models.CharField(validators=[num_regex], max_length=13, blank=True)
    dob           = models.DateField(default=timezone.now)
    profile_pic   = models.FileField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)


class AcademicYear(models.Model):
    start_year = models.DateField()
    end_year   = models.DateField()

    def start_year(self):
        return self.start_year.strftime('%Y')
    
    def end_year(self):
        return self.end_year.strftime('%Y')


class Sections(models.Model):
    section_name  = models.CharField(max_length=255)
    student       = models.ForeignKey(Students, on_delete=models.CASCADE)
    updated_at    = models.DateTimeField(auto_now=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
	    return self.course_name

    def student_count(self):
        count = self.students_set.all().count()
        return count


class Subjects(models.Model):
    subject_name = models.CharField(max_length=255)
    section      = models.ManyToManyField(Sections)
    teacher      = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name


class Attendance(models.Model):
    subject         = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year    = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    student    = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status     = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStudent(models.Model):
    student       = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date    = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status  = models.IntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)


class LeaveReportTeacher(models.Model):
    teacher       = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    leave_date    = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status  = models.IntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)


class FeedBackStudent(models.Model):
    student        = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback       = models.TextField()
    feedback_reply = models.TextField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)


class FeedBackTeachers(models.Model):
    teacher        = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    feedback       = models.TextField()
    feedback_reply = models.TextField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)


class NotificationStudent(models.Model):
    student    = models.ForeignKey(Students, on_delete=models.CASCADE)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationTeacher(models.Model):
    teacher    = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Result(models.Model):
    student    = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject    = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    exam_marks = models.FloatField(default=0)
    ia_marks   = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




'''Receiver'''
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:     
        if instance.user_type == 1:
            Principal.objects.create(user=instance)
        if instance.user_type == 2:
            Teachers.objects.create(user=instance)
        if instance.user_type == 3:
            Students.objects.create(
                admin=instance, 
                course_id=Sections.objects.get(id=1), 
                session_year_id=AcademicYear.objects.get(id=1), 
                address='', 
                profile_pic='', 
                gender=''
            )

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.principal.save()
    if instance.user_type == 2:
        instance.teachers.save()
    if instance.user_type == 3:
        instance.students.save()
    
