from django.shortcuts import render
from .forms import RegisterForm
# Create your views here.




def register(request):
    if request.mathod == 'POST':
    # 사용자의 요청이 POST 요청이면 폼데이터를 처리하는 if 문

        user_form = RegisterForm(request.POST)\
        # 폼 인스턴스를 생성하고 요청에 의한 데이터로 해당 필드의 속성 값을 채운다 (binding)

        if user_form.is_valid():
        # 폼이 유효한지 체크 한다.
        # is_valid() 같은 경우 해당 폼의 clean()을 호출해서 유효성 검사를 하는 것 이다.
        # is_valid()는 그안에서 어떠한 동작이 일어나던지 True 아니면 False가 나오는 메소드 이다.
        # 즉 True 이면 유효성 검사 통과 해서 밑에 코드가 실행 되고 아니면 에러를 발생 한다.

            user = user_form.save(commit=False)
            # 유효성 검사를 체크한 후 해당 Form 과 해당 데이터가 True이면 user 변수해 저장한다.
            # commit=False 로 옵션값을 주었기 때문에 DB에 저장되는 것이 아니라 메모리상에 객체가 만들어 지는 것 이다. True로 하면 DB에
            # 저장 되나 봄 (이건 아직 확인 필요)

            user.set_password(user_form.cleaned_data['password'])
            # .set_password(): 지정 암호를 암호화 해서 password 필드에 저장 (save 함수 호출 안함)

            user.save()
            # 유효한 데이터 체크 한 후 password 까지 암호화 해서 해당 데이터를 저장한다.

            return render(request, 'registration/login.html', {'user': user})
    else:
        user_form = RegisterForm()
    # 만약 요청 메소드가 POST가 아니면 그냥 RegisterForm() 이 보여지도록 설정 한 값

    return render(request, 'registration/register.html', {'user_form': user_form})
