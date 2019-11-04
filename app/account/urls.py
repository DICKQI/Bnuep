from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    # base
    path('', AccountBaseView.as_view(), name='login_logout'),
    path('register/', RegisterView.as_view(), name='register'),
    #userControl
    path('myself/', UserControlView.as_view(), name='myself'),
    #userContestControl
    path('myteam/<int:cid>/', UserContestView.as_view(), name='myTeam'), # 查看我的队伍
    path('myteam/<int:cid>/<int:tid>/', UserContestView.as_view(), name='myTeamWorks'), # 提交作品
]