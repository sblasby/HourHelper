from django.db import models
from django.contrib.auth.models import User
from registration import models as rmodels

# Create your models here.


class Hour(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.FloatField()
    employee = models.CharField(max_length=100)
    # student = models.CharField(max_length=100, blank=True)
    class_type = models.CharField(max_length=100)
    wage = models.FloatField()
    submitted = models.BooleanField(default=False)
    earning = models.FloatField(blank=True, null=True)

    # def __str__(self):
    #     student_field = ""
    #     if not self.student == "":
    #         student_field = f"({self.student})"
    #     return f"{self.coach} - {self.lesson_type} {student_field} - {self.date}"

    def save(self, *args, **kwargs):
        # Calculate earning before saving the object
        self.earning = float(self.duration) * float(self.wage)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class TenTenHour(Hour):

    ten_ten_details = models.ForeignKey(rmodels.TenTenEmployee, on_delete=models.CASCADE)

    school = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        
        school_field = ""

        if self.school != "":
            school_field = f'({self.school})'
        
        return f'{self.employee} - {self.class_type} {school_field} - {self.date}'

class VtcHour(Hour):

    vtc_details = models.ForeignKey(rmodels.VTCEmployee, on_delete=models.CASCADE)

    student = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        
        student_field = ""

        if self.student != "":
            student_field = f'({self.student})'
        
        return f'{self.employee} - {self.class_type} {student_field} - {self.date}'
