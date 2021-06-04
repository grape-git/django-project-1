from django.db import models
# from taggit.managers import TaggableManager
# taggit 은 태그 라이브러리 패키지로 django-taggit 패키지를 따로 설치해서 사용해야 한다.
from helpers.models import BaseModel
from users.models import User


class Post(BaseModel):  # helpers app 에서 만든 BaseModel 을 상속 받는다.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.id}, {self.user}'
    # return 값에 포매팅으로 값을 넘기는 이유는 id와 user 가 Foreignkey 로 참조 키이다.
    # 이말은 즉, id 값과 string 값을 2개 가 적용될 수 있기 때문에 return 시 string 타입으로 변환 오류가 발생할 수 있다.
    # id 값은 숫자(int) 이기때문에 타입 에러 발생 !
    # 포매팅 적용 시 타입이 string 으로 변환 되어서 포매팅을 사용하는 것이 좋다.

