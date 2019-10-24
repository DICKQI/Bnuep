from ..models import Contest
from app.account.models import UserAccount
from django.http import JsonResponse
from Common.UserCommon import check_login, getUser
from django.forms import model_to_dict
from rest_framework.views import APIView

class ContestView(APIView):

    COMMON_FIELDS = [
        'works_name', 'team_name', 'member_number', 'id'
    ]

    @check_login
    def get(self, request, cid):
        '''
        查看当前比赛的信息和比赛的所有参赛队伍
        :param request:
        :param cid:
        :return:
        '''
        contest = Contest.objects.filter(id=cid)
        if not contest.exists:
            return JsonResponse({
                'status': False,
                'errMsg': '比赛不存在'
            }, status=401)
        contest = contest[0]
        if contest.status == 'NotStarted' or contest.status == 'RegisterDeadline':
            return JsonResponse({
                'status': False,
                'errMsg': '比赛未开始或已截止报名'
            }, status=401)
        teamALL = contest.team.all()
        team = [model_to_dict(t, fields=self.COMMON_FIELDS) for t in teamALL]
        user = getUser(request.session.get('login'))
        for i in range(len(team)):
            teamMember = teamALL[i].teamMember.all()
            if teamMember.filter(account=user).exists():
                team[i]['joined'] = True
            else:
                team[i]['joined'] = False
            team[i]['member'] = [model_to_dict(tm, exclude=['is_cancel', 'id']) for tm in teamMember]
            for j in team[i]['member']:
                j['name'] = UserAccount.objects.get(id=j['account']).name
        return JsonResponse({
            'status': True,
            'team': team,
            'contest_name': contest.contestName,
        })