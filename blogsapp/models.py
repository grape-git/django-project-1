from django.db import models
from django.db import models
from taggit.managers import TaggableManager
# taggit 은 태그 라이브러리 패키지로 django-taggit 패키지를 따로 설치해서 사용해야 한다.
from helpers.models import BaseModel
from users.models import User


class Post(BaseModel):  # helpers app 에서 만든 BaseModel 을 상속 받는다.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.id, self.title
