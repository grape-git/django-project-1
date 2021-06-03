from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    # class Meta 에 abstract = True 옵션 설정이 없으면 DB 에서 해당 모델을 테이블로
    # 생성하게 된다. 하지만 현재는 베이스 모델로 사용하는 것 이기 때문에 추상 클래스라고
    # 선언한 후 DB에 해당 모델이 테이블로 생성이 되지 않게 옵션을 설정 한 것 !


# BaseModel 을 생성하는 이유는 말 그대로 다른 app 들의 모델에 Base 가 되는 모델을 생상허는 것
# 이렇게 만드는 이유는 공통적으로 들어가는 필드 와 정보들을 취합 해서 한번에 설정하기 위해서 이다.
