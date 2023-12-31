from django.db import models
from django.contrib.auth.models import User


class EmploymentDetails(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_details")

    is_ten_ten_employee = models.BooleanField()

    is_vtc_coach = models.BooleanField()

    first_login = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'Employment Details for {self.user.first_name} {self.user.last_name}'



class Employee(models.Model):

    wage = models.FloatField()

    is_contract = models.BooleanField()

    class Meta:
        abstract = True


class VTCEmployee(Employee):

    details = models.OneToOneField(EmploymentDetails, on_delete=models.CASCADE, related_name="vtc_details")

    def __str__(self) -> str:
        return f'{self.details.user.first_name} {self.details.user.last_name}'


class TenTenEmployee(Employee):

    details = models.OneToOneField(EmploymentDetails, on_delete=models.CASCADE, related_name="ten_ten_details")

    def __str__(self) -> str:
        return f'{self.details.user.first_name} {self.details.user.last_name}'

    

# class Coach(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_info")
#     wage = models.FloatField()

#     def __str__(self) -> str:
#         return f'{self.user.first_name} makes {self.wage}$ an hour'