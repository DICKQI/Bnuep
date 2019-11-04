from django.http import JsonResponse
from rest_framework.views import APIView
from app.contest.models import Contest, TeamModel
from app.account.models import UserAccount
from app.contest.views.signupInfo import SignupView
from django.forms import model_to_dict
from Common.UserCommon import check_login, getUser
from django.db.models import Q
import json

class UserContestView(APIView):

    COMMON_FIELDS = [
        'works_name', 'team_name', 'member_number', 'id'
    ]

    signupFunc = SignupView()

    @check_login
    def put(self, request, cid, tid):
        '''
        队长提交作品链接
        :param request:
        :param cid:
        :return:
        '''
        try:
            user = getUser(request.session.get('login'))
            contest = self.signupFunc.getContest(cid)
            if contest == False:
                return JsonResponse({
                    'status': False,
                    'errMsg': '比赛已截止报名或者未开始'
                }, status=401)
            team = TeamModel.objects.filter(
                Q(contest=contest) &
                Q(id=tid)
            )
            if not team.exists:
                return JsonResponse({
                    'status': False,
                    'errMsg': '队伍不存在'
                }, status=404)
            team = team[0]
            '''队长权限检查'''
            leader = team.teamMember.get(memberRoles='leader').account
            if leader != user:
                return JsonResponse({
                    'status': False,
                    'errMsg': '你没有修改的权限'
                }, status=401)
            jsonParams = json.loads((request.body).decode('utf-8'))
            team.works_link = jsonParams.get('link')
            team.save()
            return JsonResponse({
                'status': True,
                'tid': tid,
                'cid': cid
            })
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': str(ex)
            }, status=403)

    @check_login
    def get(self, request, cid):
        '''
        获取本账户在本比赛的队伍
        :param request:
        :param cid:
        :return:
        '''
        user = getUser(request.session.get('login'))
        contest = self.signupFunc.getContest(cid)
        if contest == False:
            return JsonResponse({
                'status': False,
                'errMsg': '比赛不存在或者已截止'
            }, status=404)
        myTeam = contest.team.filter(teamMember__account=user)
        team = [model_to_dict(t, fields=self.COMMON_FIELDS) for t in myTeam]
        for i in range(len(team)):
            teamMember = myTeam[i].teamMember.all()
            team[i]['member'] = [model_to_dict(tm, exclude=['is_cancel', 'id']) for tm in teamMember]
            for j in team[i]['member']:
                j['name'] = UserAccount.objects.get(id=j['account']).name
            if teamMember.get(memberRoles='leader').account == user:
                team[i]['leader'] = True
            else:
                team[i]['leader'] = False
        return JsonResponse({
            'status': True,
            'team': team
        })