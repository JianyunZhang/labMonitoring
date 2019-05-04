from django import forms
from captcha.fields import CaptchaField


# 对表单进行判断
class CaptchaForm(forms.Form):
    captcha = CaptchaField(label='验证码')
    # captcha = CaptchaField(error_messages={"invalid": "验证码错误"})  # 加入验证码
