from django.http import JsonResponse
from rest_framework.views import APIView
from app.contest.models import Contest
from django.forms import model_to_dict
from Common.UserCommon import check_login, getUser
from django.db.models import Q
import json


class UserControlView(APIView):
    EXCLUDE_FIELDS = [
        'createTime', 'team', 'UpperLimit', 'picture'
    ]

    @check_login
    def get(self, request):
        '''
        获取当前账户参加的报名中的比赛和个人信息
        :param request:
        :return:
        '''
        user = getUser(request.session.get('login'))
        hadJoinedContest = Contest.objects.filter(
            Q(team__teamMember__account=user) &
            Q(contestStatus='Started')
        ).distinct()
        contest = [model_to_dict(con, exclude=self.EXCLUDE_FIELDS) for con in hadJoinedContest]
        userDetail = model_to_dict(user, exclude=['password'])
        for c in contest:
            c['beginTime'] = str(c['beginTime'])[:10]
            c['signupEndTime'] = str(c['signupEndTime'])[:10]
        return JsonResponse({
            'status': True,
            'MyContest': contest,
            'myDetail': userDetail
        })

    @check_login
    def put(self, request):
        '''
        修改个人信息
        :param request:
        :return:
        '''
        try:
            jsonParams = json.loads((request.body).decode('utf-8'))
            user = getUser(request.session.get('login'))
            if jsonParams.get('email') != '':
                user.email = jsonParams.get('email')
            if jsonParams.get('phone_number') != '':
                user.phone_number = jsonParams.get('phone_number')
            if jsonParams.get('wechat') != '':
                user.wechat = jsonParams.get('wechat')
            if jsonParams.get('qq_number') != '':
                user.qq_number = jsonParams.get('qq_number')
            if jsonParams.get('student_id') != '':
                user.student_id = jsonParams.get('student_id')
            if jsonParams.get('major') != '':
                user.major = jsonParams.get('major')
            if jsonParams.get('grade') != '':
                user.grade = jsonParams.get('grade')
            user.save()
            return JsonResponse({
                'status': True,
                'id': user.id
            })
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': str(ex)
            })