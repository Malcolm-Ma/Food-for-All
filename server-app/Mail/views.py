from django.core.mail import send_mail
from FoodForAll.settings import EMAIL_HOST_USER
from DataBase import models

# Create your views here.
class Mail(object):
    @staticmethod
    def regis_verify(mail, code, fail_silently=True):
        send_mail("Thank you for signing up to FoodForAll", "Your verification code is " + code, EMAIL_HOST_USER, [mail], fail_silently=fail_silently)

    @staticmethod
    def welcome(mail, fail_silently=True):
        send_mail("Welcome to FoodForAll", "Welcome to FoodForAll", EMAIL_HOST_USER, [mail], fail_silently=fail_silently)