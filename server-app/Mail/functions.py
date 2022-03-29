from django.core.mail import send_mail
from FoodForAll.settings import EMAIL_HOST_USER


class Mail(object):
    @staticmethod
    def get_line(text, style=''):
        if style == 'code':
            return '<div style="text-align: center;"><b style="color: rgb(51, 51, 51);'\
                   + ' font-size: x-large;"><u>' + text + '</u></b></div>'
        else:
            return '<div style="text-align: center;"><span style="color: rgb(51, 51, 51);'\
                   + (' font-size: x-large;' if style == 'title' else '') + '">' + text + '</span></div>'

    @staticmethod
    def get_header():
        return '<br>'\
               + Mail.get_line('- Food For All by Apex08 -', 'title')\
               + '<br>'\
               + '<hr>'\
               + '<br>'

    @staticmethod
    def get_footer():
        return '<br>'\
               + '<hr>'\
               + Mail.get_line('© Food For All')\
               + '<br>'

    @staticmethod
    def regis_verify(mail, code, fail_silently=True):
        html_message = Mail.get_header()\
                       + Mail.get_line('Thank you for signing up to Food For All!', 'title')\
                       + Mail.get_line('Your verification code is:', 'title')\
                       + Mail.get_line(code, 'code')\
                       + '<br>'\
                       + Mail.get_line('Please complete verification before the code expires.')\
                       + Mail.get_footer()
        send_mail("Food For All - Verification code", "", EMAIL_HOST_USER, [mail], fail_silently=fail_silently, html_message=html_message)

    @staticmethod
    def welcome(mail, fail_silently=True):
        html_message = Mail.get_header()\
                       + Mail.get_line('Welcome to Food For All!', 'title')\
                       + '<br>'\
                       + Mail.get_line('Your registration is complete.')\
                       + Mail.get_line('Now you have full access to our best features!')\
                       + Mail.get_footer()
        send_mail("Welcome to Food For All!", "", EMAIL_HOST_USER, [mail], fail_silently=fail_silently, html_message=html_message)

    @staticmethod
    def reset_password_verify(mail, code, fail_silently=True):
        html_message = Mail.get_header()\
                       + Mail.get_line('You\'re trying to reset your password.', 'title')\
                       + Mail.get_line('Your verification code is:', 'title')\
                       + Mail.get_line(code, 'code')\
                       + '<br>'\
                       + Mail.get_line('Please complete verification before the code expires.')\
                       + Mail.get_line('If you didn\'t expect for this email,')\
                       + Mail.get_line('please reset your password ASAP.')\
                       + Mail.get_footer()
        send_mail("Food for All - Password reset", "", EMAIL_HOST_USER, [mail], fail_silently=fail_silently, html_message=html_message)

    @staticmethod
    def reset_password_success(mail, fail_silently=True):
        html_message = Mail.get_header()\
                       + Mail.get_line('You have reset your password!', 'title')\
                       + '<br>'\
                       + Mail.get_line('You might need to re-login to your account.')\
                       + Mail.get_footer()
        send_mail("Food For All - Reset successful", "", EMAIL_HOST_USER, [mail], fail_silently=fail_silently, html_message=html_message)
