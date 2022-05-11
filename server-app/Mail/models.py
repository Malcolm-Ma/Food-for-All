from django.core.mail import send_mail
from FoodForAll.settings import EMAIL_HOST_USER, VERIFY_CODE_EXPIRES


class Mail(object):
    # This class consists of functions for sending emails to users under different circumstances.

    @staticmethod
    def get_line(text, style=''):
        # Rich text template for a single line.
        if style == 'code':
            return '<div style="text-align: center;"><b style="color: rgb(51, 51, 51);' \
                   + ' font-size: x-large;"><u>' + text + '</u></b></div>'
        else:
            return '<div style="text-align: center;"><span style="color: rgb(51, 51, 51);' \
                   + (' font-size: x-large;' if style == 'title' else '') + '">' + text + '</span></div>'

    @staticmethod
    def get_header():
        # Rich text template for email header.
        return '<br>' + \
               Mail.get_line('- Food For All by Apex08 -', 'title') + \
               '<br>' + \
               '<hr>' + \
               '<br>'

    @staticmethod
    def get_footer():
        # Rich text template for email footer.
        return '<br>' + \
               '<hr>' + \
               Mail.get_line('© Food For All') + \
               '<br>'

    @staticmethod
    # Send an email with verification code for a user to register.
    def regis_verify(mail, code, fail_silently=True):
        html_message = Mail.get_header() + \
                       Mail.get_line('Thank you for signing up to Food For All!', 'title') + \
                       Mail.get_line('Your verification code is:', 'title') + \
                       Mail.get_line(code, 'code') + \
                       '<br>' + \
                       Mail.get_line('Please do not show the verification code to others.') + \
                       Mail.get_line('The validity period is {minutes} minutes.'
                                     .format(minutes=str(int(VERIFY_CODE_EXPIRES / 60)))) + \
                       Mail.get_line('Please complete verification before the code expires.') + \
                       Mail.get_footer()
        send_mail('Food For All - Your verification code',
                  '', EMAIL_HOST_USER, [mail], fail_silently=fail_silently, html_message=html_message)

    @staticmethod
    # Send a welcome email when a user completes registration.
    def welcome(mail, fail_silently=True):
        html_message = Mail.get_header() + \
                       Mail.get_line('Welcome to Food For All!', 'title') + \
                       '<br>' + \
                       Mail.get_line('Your registration is complete.') + \
                       Mail.get_line('Now you have full access to our best features!') + \
                       Mail.get_footer()
        send_mail('Welcome to Food For All!',
                  '', EMAIL_HOST_USER, [mail], fail_silently=fail_silently, html_message=html_message)

    @staticmethod
    def reset_password_verify(mail, code, fail_silently=True):
        # Send an email with verification code for a user to reset password.
        html_message = Mail.get_header() + \
                       Mail.get_line('You\'re trying to reset your password.', 'title') + \
                       Mail.get_line('Your verification code is:', 'title') + \
                       Mail.get_line(code, 'code') + \
                       '<br>' + \
                       Mail.get_line('Please do not show the verification code to others.') + \
                       Mail.get_line('The validity period is {minutes} minutes.'
                                     .format(minutes=str(int(VERIFY_CODE_EXPIRES / 60)))) + \
                       Mail.get_line('Please complete verification before the code expires.') + \
                       Mail.get_line('If you don\'t expect for this email,') + \
                       Mail.get_line('please reset your password ASAP.') + \
                       Mail.get_footer()
        send_mail('Food for All - Your verification code for password reset',
                  '', EMAIL_HOST_USER, [mail], fail_silently=fail_silently, html_message=html_message)

    @staticmethod
    def reset_password_success(mail, fail_silently=True):
        # Send an email to inform a user when password is successfully reset.
        html_message = Mail.get_header() + \
                       Mail.get_line('You have reset your password!', 'title') + \
                       '<br>' + \
                       Mail.get_line('You might need to re-login to your account.') + \
                       Mail.get_footer()
        send_mail('Food For All - You have reset your password',
                  '', EMAIL_HOST_USER, [mail], fail_silently=fail_silently, html_message=html_message)

    @staticmethod
    # Send an email to invite user's friends to the page of the donated project.
    def share(share_info, fail_silently=True):
        share_info['user_name'] = '' if not share_info['user_name'] else ' ' + share_info['user_name']
        share_info['donate_num'] = '' if not share_info['donate_num'] else ' ' + str(share_info['donate_num']) + ' meal(s)'
        html_message = Mail.get_header() + \
                       Mail.get_line('Your friend{user_name} has just donated'
                                     .format(user_name=share_info['user_name']), 'title') + \
                       Mail.get_line('{donate_num} to project "{project_name}".'
                                     .format(donate_num=share_info['donate_num'],
                                             project_name=share_info['project_name']),
                                     'title') + \
                       '<br>' + \
                       Mail.get_line('We sincerely look forward to your participation!') + \
                       Mail.get_line('Check it out now at: {project_url}'
                                     .format(project_url=share_info['project_url'])) + \
                       Mail.get_footer()
        send_mail('Food For All - Invitation to make the world a little better',
                  '', EMAIL_HOST_USER, share_info['mail'], fail_silently=fail_silently, html_message=html_message)
