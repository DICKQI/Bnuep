from django.http import JsonResponse
from rest_framework.views import APIView
from app.contest.models import Contest
from app.account.models import UserAccount
from django.forms import model_to_dict
from Common.UserCommon import check_login, getUser
from django.db.models import Q
import json

class UserContestView(APIView):

    COMMON_FIELDS = [
        'works_name', 'team_name', 'member_number', 'id'
    ]

    @check_login
    def get(self, request, cid):
        '''
        获取用户参加的比赛的团队
        :param request:
        :param cid:
        :return:
        '''
        try:
            user = getUser(request.session.get('login'))
            contest = Contest.objects.get(id=cid)
            if not contest.team.filter(teamMember__account=user):
                return JsonResponse({
                    'status': False,
                    'errMsg': '你没有参加这场比赛噢'
                }, status=401)
            teamFilter = contest.team.filter(teamMember__account=user)
            team = [model_to_dict(t, fields=self.COMMON_FIELDS) for t in teamFilter]
            for i in range(len(team)):
                teamMember = teamFilter[i].teamMember.all()
                team[i]['member'] = [model_to_dict(tm, exclude=['is_cancel', 'id']) for tm in teamMember]
                for j in team[i]['member']:
                    j['name'] = UserAccount.objects.get(id=j['account']).name

        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': str(ex)
            }, status=403)
