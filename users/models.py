from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Not to disclose')
)


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, gender=2, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, gender=gender, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username='', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # setdefault 는 key 값과 value 값 하나를 인자로 받는 dict의 메소드 이다.
        # setdefault 는 키값이 있다면 키값을 반환하고 없다면 두 번째 인자를 반환한다.
        # 여기서 사용된 방식은 is_staff를 key 값을 받고 해당 value 값에 False 값을 지정해서 관리자 권한이 아닌 일반 유저로서의
        # 설정을 지정하는 것 이다.
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, '', password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    username = models.CharField(max_length=30)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # # 필수로 받고 싶은 필드를 넣기

    def __str__(self):  # 매직 메소드
        return "<%d %s>" % (self.pk, self.email)
