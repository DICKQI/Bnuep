from django.http import JsonResponse
from rest_framework.views import APIView
from app.contest.models import Contest
from django.forms import model_to_dict
from Common.UserCommon import check_login, getUser
from django.db.models import Q


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
        )
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
    def post(self, request):
        '''

        :param request:
        :return:
        '''