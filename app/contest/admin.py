from django.contrib import admin
from .models import Contest, TeamModel

# Register your models here.
@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_filter = ['contestStatus']
    list_display = ['contestName', 'contestStatus', 'createTime', 'signupEndTime']
    list_per_page = 10
    search_fields = ['contestName']

@admin.register(TeamModel)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['works_name', 'team_name', 'guide_teacher', 'submission_date', 'member_number']
    search_fields = ['team_name', 'work_name', 'guide_teacher']
    list_per_page = 20