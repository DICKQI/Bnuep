from django.urls import path
from .views import *
app_name = 'contest'

urlpatterns = [
    # signup
    path('createteam/<int:cid>/', SignupView.as_view(), name='create team'), # 创建比赛队伍
    path('team/<int:tid>/<int:cid>/', SignupView.as_view(), name='teamInfo'), # 加入或退出退伍
    # contest
]