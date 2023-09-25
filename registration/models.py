from django.db import models
from django.contrib.auth.models import User


class EmploymentDetails(models.Model):

    models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_details")

    is_ten_ten = models.BooleanField()

    is_vtc_coach = models.BooleanField()



class Employee(models.Model):

    wage = models.FloatField()

    is_contract = models.BooleanField()

    class Meta:
        abstract = True


class VTCEmployee(Employee):

    details = models.ForeignKey(EmploymentDetails, on_delete=models.CASCADE, related_name="vtc_details")

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'


class TenTenEmployee(Employee):

    details = models.ForeignKey(EmploymentDetails, on_delete=models.CASCADE, related_name="ten_ten_details")

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    

# class Coach(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_info")
#     wage = models.FloatField()

#     def __str__(self) -> str:
#         return f'{self.user.first_name} makes {self.wage}$ an hour'