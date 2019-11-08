from app.contest.models import TeamMember, TeamModel, Contest
from rest_framework.views import APIView
from django.http import JsonResponse
from Common.UserCommon import check_login, getUser
from django.db.models import Q
import json


class SignupView(APIView):

    def getContest(self, cid):
        contest = Contest.objects.filter(id=cid)
        if not contest.exists:
            return False
        contest = contest[0]
        if contest.status == 'NotStarted' or contest.status == 'RegisterDeadline':
            return False
        return contest

    @check_login
    def post(self, request, cid):
        '''
        报名比赛（队长创建团队）
        :param request:
        :return:
        '''
        try:
            user = getUser(request.session.get('login'))
            contest = self.getContest(cid)
            if contest == False:
                return JsonResponse({
                    'status': False,
                    'errMsg': '比赛已截止报名或者未开始'
                }, status=401)
            '''判断该用户在这次比赛中参加的队伍数量是否超过3个'''
            if contest.team.all().filter(teamMember__account=user).count() >= 3:
                return JsonResponse({
                    'status': False,
                    'errMsg': '你在本次比赛中参加的队伍过多'
                }, status=401)
            jsonParams = json.loads((request.body).decode('utf-8'))
            if jsonParams.get('works_name') == '':
                return JsonResponse({
                    'status': False,
                    'errMsg': '作品名不能为空'
                }, status=403)
            if jsonParams.get('team_name') == '':
                return JsonResponse({
                    'status': False,
                    'errMsg': '团队名不能为空'
                }, status=403)
            if jsonParams.get('guide_teacher') == '':
                return JsonResponse({
                    'status': False,
                    'errMsg': '指导老师不能为空'
                }, status=403)
            '''创建队伍与临时比赛账户'''
            leader = TeamMember.objects.create(account=user)
            team = TeamModel.objects.create(
                works_name=jsonParams.get('works_name'),
                team_name=jsonParams.get('team_name'),
                guide_teacher=jsonParams.get('guide_teacher'),
                member_number=1
            )
            team.teamMember.add(leader)
            team.save()
            '''将队伍加入比赛'''
            contest.team.add(team)
            '''json响应'''
            return JsonResponse({
                'status': True,
                'tid': team.id,
                'mid': leader.id
            })
        except:
            return JsonResponse({
                'status': False,
                'errMsg': '出现未知错误'
            }, status=403)

    @check_login
    def get(self, request, tid, cid):
        '''
        报名比赛（队员加入队伍）
        :param request:
        :param tid:
        :param cid:
        :return:
        '''
        try:
            contest = self.getContest(cid)
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
            '''判断本队伍是否是本次比赛的'''
            if not team.contest_set.filter(team__contest=contest).exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '队伍不存在'
                }, status=404)
            '''判断队伍人数是否超过上限'''
            if team.member_number == contest.UpperLimit:
                return JsonResponse({
                    'status': False,
                    'errMsg': '队伍人数已超上限'
                }, status=401)
            user = getUser(request.session.get('login'))
            '''判断是否已经在队伍中'''
            if team.teamMember.filter(account=user).exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '你已经在队伍中'
                }, status=401)
            '''判断该用户在这次比赛中参加的队伍数量是否超过3个'''
            if contest.team.all().filter(teamMember__account=user).count() >= 3:
                return JsonResponse({
                    'status': False,
                    'errMsg': '你在本次比赛中参加的队伍过多'
                }, status=401)
            member = TeamMember.objects.create(
                account=user,
                memberRoles='member'
            )
            team.member_number += 1
            team.save()
            team.teamMember.add(member)
            return JsonResponse({
                'status': True,
                'tid': tid,
                'cid': cid,
                'mid': member.id
            })
        except:
            return JsonResponse({
                'status': False,
                'errMsg': '出现未知错误'
            }, status=403)

    @check_login
    def delete(self, request, tid, cid, mid=0):
        '''
        退出队伍/移除队员
        :param request:
        :param tid: team id
        :param cid: contest id
        :param mid: member id
        :return:
        '''
        contest = self.getContest(cid)
        if contest == False:
            return JsonResponse({
                'status': False,
                'errMsg': '比赛已截止报名或者未开始'
            }, status=401)
        team = TeamModel.objects.filter(id=tid)
        if not team.exists:
            return JsonResponse({
                'status': False,
                'errMsg': '队伍不存在'
            }, status=404)
        team = team[0]
        user = getUser(request.session.get('login'))
        if mid == 0:
            '''自己退出队伍'''
            member = team.teamMember.filter(account=user)
            if not member.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '你并不在该队伍中'
                }, status=401)
            member = member[0]
        else:
            '''队长移除队员'''
            leader = team.teamMember.get(memberRoles='leader').account
            if leader != user:
                return JsonResponse({
                    'status': False,
                    'errMsg': '你不是队长，无权限操作'
                }, status=401)
            member = team.teamMember.filter(id=mid)
            if not member.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '队员并不在队伍中'
                }, status=404)
            member = member[0]
        team.teamMember.remove(member)
        team.member_number -= 1
        team.save()
        if member.memberRoles == 'leader':
            '''如果是队长离队，则解散队伍'''
            team.delete()
            return JsonResponse({
                'status': True,
                'cid': cid,
                'tid': tid,
                'mid': mid,
            })
        if team.member_number == 0:
            """队伍没人了就删除这个队伍"""
            team.delete()
        return JsonResponse({
            'status': True,
            'cid': cid,
            'tid': tid,
            'mid': mid,
        })

    @check_login
    def put(self, request, cid, tid):
        '''
        修改队伍信息（队长）
        :param request:
        :param cid:
        :param tid:
        :return:
        '''
        contest = self.getContest(cid)
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
        user = getUser(request.session.get('login'))
        if team.teamMember.get(memberRoles='leader').account != user:
            return JsonResponse({
                'status': False,
                'errMsg': '你没有权限操作'
            }, status=401)
        jsonParams = json.loads((request.body).decode('utf-8'))
        if jsonParams.get('works name'):
            team.works_name = jsonParams.get('works name')
        if jsonParams.get('team name'):
            team.team_name = jsonParams.get('team name')
        if jsonParams.get('guide teacher'):
            team.guide_teacher = jsonParams.get('guide teacher')
        team.save()
        return JsonResponse({
            'status': True,
            'cid': cid,
            'tid': tid,
            'works name': team.works_name,
            'team name': team.team_name
        })
