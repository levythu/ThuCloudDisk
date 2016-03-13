# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            nickname=nickname
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    nickname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
        
    
# share object table
class shareObject(models.Model):
    ownerMail = models.CharField(max_length = 50)
    sharerMail = models.CharField(max_length = 50)
    parentObject = models.CharField(max_length=200)
    object = models.CharField(max_length = 200)
 
# public object table
class publicObject(models.Model):
    ownerMail = models.CharField(max_length = 50)
    object = models.CharField(max_length = 200)

# user bucket table
class userBucket(models.Model):
    ownerMail = models.CharField(max_length = 50)
    bucket = models.CharField(max_length = 50)

# 公开分享文件
class openSharedObject(models.Model):
    # 生成的随机验证码
    randomCode = models.CharField(max_length = 64,primary_key=True)
    # 文件拥有者的邮件
    ownerEmail = models.CharField(max_length = 255)
    # 文件路径：可能是文件夹
    objectName = models.CharField(max_length=255)

    # 用户设置的密码
    secret = models.CharField(max_length = 255)

