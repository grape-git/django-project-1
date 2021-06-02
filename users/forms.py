from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    # 회원가입 폼
    # 장고에서는 HTML 입력 요소를 widget(위젯)이라고 말한다.
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender', 'email']

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        # 각 필드에 clean 메소드가 호출된 후에 호출되는 메소드 이다.
        # 유효성 검사를 할 때 사용하는 메소드 이다.
        # 그래서 만약 다른 유효성 검사를 한다고 할때 메소드 이름을 "clean_유효성 검사 필드 이름" 형식으로 작성하면 된다.
        # 현재는 clean_confirm_password
        # clean  필드 형태의 메소드 에서는 해당 필드의 값을 사용할 때는 꼭 필드 값을 찾아서 사용해야 한다.
        # 즉, 명시적으로 입력해서 사용해야 하는 것

        return cd['confirm_password']