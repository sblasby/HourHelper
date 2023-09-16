from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.FloatField()
    coach = models.CharField(max_length=100)
    student = models.CharField(max_length=100, blank=True)
    lesson_type = models.CharField(max_length=200)
    wage = models.FloatField()
    submitted = models.BooleanField(default=False)
    earning = models.FloatField(blank=True, null=True)

    def __str__(self):
        student_field = ""
        if not self.student == "":
            student_field = f"({self.student})"
        return f"{self.coach} - {self.lesson_type} {student_field} - {self.date}"

    def save(self, *args, **kwargs):
        # Calculate earning before saving the object
        self.earning = float(self.duration) * float(self.wage)
        super().save(*args, **kwargs)
