from django.urls import path
from .views import *
app_name = 'contest'

urlpatterns = [
    # signup
    path('createteam/<int:cid>/', SignupView.as_view(), name='create team'), # 创建比赛队伍
    path('team/<int:tid>/<int:cid>/', SignupView.as_view(), name='teamInfo'), # 加入或退出退伍
    path('team/<int:tid>/<int:cid>/<int:mid>/', SignupView.as_view(), name='deleteMember'), # 队长踢出成员
    # contest
    path('list/', ContestListView.as_view(), name='contestList'), # 比赛列表
    path('<int:cid>/', ContestView.as_view(), name='contestInfo'), # 比赛操作
    # admin
    path('contestadmin/dk3562810/<int:cid>/', AdminView.as_view(), name='adminAPI'), # 内部接口
]