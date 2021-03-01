from django.db import models

# Create your models here.


class UserLoginHistory(models.Model):
    # Login Status
    SUCCESS = 'S'

    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),
                    (FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(
        max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'user_login_history'
        verbose_name_plural = 'user_login_histories'

class Profile(models.Model):
  #  id= models.ForeignKey('auth.user' , on_delete=models.CASCADE)
    company_name= models.CharField(max_length=100,blank=True)
    school_name = models.CharField(max_length=100,blank=True)
    Current_Location=models.CharField(max_length=100,blank=True)

