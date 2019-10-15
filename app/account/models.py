from django.db import models

# Create your models here.

class AccountPassword(models.Model):
    password = models.CharField(verbose_name='密码密文', max_length=100, default='', blank=False)



class UserAccount(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=10, default='', blank=False)

    password = models.ForeignKey(AccountPassword, verbose_name='关联密码', default='', blank=False, on_delete=models.CASCADE)

    student_id = models.IntegerField(verbose_name='学号', default=0, blank=False, unique=True)

    grade = models.CharField(verbose_name='年级', max_length=15, default='', blank=False)

    major = models.CharField(verbose_name='专业', max_length=15, default='', blank=False)

    email = models.EmailField(verbose_name='邮箱', default='', blank=False)

    qq_number = models.IntegerField(verbose_name='qq号码', default=0, blank=False)

    wechat = models.CharField(verbose_name='微信', default='', blank=False, max_length=30)

    phone_number = models.CharField(verbose_name='手机长号', default=0, blank=False, max_length=20)

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = '账户'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'Account_User'