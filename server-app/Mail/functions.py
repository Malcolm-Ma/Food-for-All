from django.core.mail import send_mail
from FoodForAll.settings import EMAIL_HOST_USER

# Create your views here.
class Mail(object):

    framework = '\
<body style="text-align:{align_method}">\
    <div style="margin:0 auto; width:{width}px;">\
    <table style="float:left; width:100%; text-align:left; font-size:12px;">\
         <tr><td style="padding-top:10px; padding-bottom:5px; border-bottom:1px solid #D9D9D9; color:#30ACE3; font-weight:bold; font-size:18px;">NowAPI</td></tr>\
        <tr><td style="padding:20px 0px 20px 0px; font-size:14px; line-height:23px;">尊敬的用户 <b>RHOWL</b><br>输入以下验证码完成邮箱验证，60分钟内有效，请不要将此验证码泄露给他人<br><br>验证码: <b>84613</b><br><br><br></td></tr>\
            \
        <tr><td style="padding-top:5px; padding-bottom:40px; border-top:1px solid #D9D9D9; color:#999999;">\
        此为系统邮件，请勿回复<br />请保管好您的邮箱，避免账户被他人盗用<br /><br />如有任何疑问，可浏览网站寻求协助 <a target="_blank" href="https://www.nowapi.com">https://www.nowapi.com</a>\
        </td></tr>\
    </table>\
    </div>\
</body>'

    @staticmethod
    def regis_verify(mail, code, fail_silently=True):
        #send_mail("a", "", EMAIL_HOST_USER, [mail], fail_silently=fail_silently, html_message=text)
        send_mail("Thank you for signing up to FoodForAll", "Your verification code is " + code, EMAIL_HOST_USER, [mail], fail_silently=fail_silently)

    @staticmethod
    def welcome(mail, fail_silently=True):
        send_mail("Welcome to FoodForAll", "Welcome to FoodForAll", EMAIL_HOST_USER, [mail], fail_silently=fail_silently)

    @staticmethod
    def reset_password_verify(mail, code, fail_silently=True):
        send_mail("Password Reset", "Your verification code is " + code, EMAIL_HOST_USER, [mail], fail_silently=fail_silently)

    @staticmethod
    def reset_password_success(mail, fail_silently=True):
        send_mail("Password Reset Successful", "You have successfully reset your password", EMAIL_HOST_USER, [mail], fail_silently=fail_silently)