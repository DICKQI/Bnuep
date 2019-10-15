from django.db import models
from django.utils.timezone import now
from app.account.models import UserAccount


# Create your models here.

class TeamMember(models.Model):
    roles = {
        ('leader', '组长'),
        ('member', '组员')
    }

    account = models.ForeignKey(UserAccount, verbose_name='关联账户', on_delete=models.CASCADE, default='', blank=False)

    memberRoles = models.CharField(verbose_name='成员身份', choices=roles, max_length=10, default='leader', blank=False)

    is_cancel = models.BooleanField(verbose_name='是否注销', default=False, blank=False)

    def __str__(self):
        return self.account.name + ' ' + self.memberRoles

class TeamModel(models.Model):
    works_name = models.CharField(verbose_name='作品名称', max_length=50, default='', blank=False)

    team_name = models.CharField(verbose_name='团队名称', max_length=20, default='', blank=False)

    guide_teacher = models.CharField(verbose_name='指导老师', max_length=15, default='', blank=False)

    submission_date = models.DateTimeField(verbose_name='报名日期', default=now)

    teamMember = models.ManyToManyField(TeamMember, verbose_name='团队成员', blank=True)

    member_number = models.IntegerField(verbose_name='成员人数', default=0, blank=False)

    def __str__(self):
        return self.works_name

    class Meta:
        verbose_name = '比赛队伍'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'Contest_Team'
        ordering = ['-submission_date']

class Contest(models.Model):

    status = {
        ('NotStarted', '未开始'),
        ('Started', '报名中'),
        ('RegisterDeadline', '报名截止')
    }

    contestName = models.CharField(verbose_name='比赛名称', max_length=50, default='', blank=False)

    contestStatus = models.CharField(verbose_name='比赛状态', default='NotStarted', choices=status, max_length=20, blank=False)

    createTime = models.DateTimeField(verbose_name='创建时间', max_length=50, default=now, blank=False)

    beginTime = models.DateTimeField(verbose_name='开始时间', default='', blank=False)

    signupEndTime = models.DateTimeField(verbose_name='报名截止时间', default='', blank=False)

    sponsor = models.CharField(verbose_name='主办方', max_length=100, default='', blank=False)

    organizer =  models.CharField(verbose_name='承办方', max_length=100, default='', blank=False)

    team = models.ManyToManyField(TeamModel, verbose_name='参赛队伍', blank=True)

    UpperLimit = models.IntegerField(verbose_name='队伍人数上限', default=3)

    def __str__(self):
        return self.contestName

    class Meta:
        verbose_name = '比赛'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'Contest_Contest'
        ordering = ['-createTime']
