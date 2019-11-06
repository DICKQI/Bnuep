from rest_framework.views import APIView
from app.contest.models import Contest
from django.http import StreamingHttpResponse, Http404, HttpResponse
import xlwt


class AdminView(APIView):
    '''
    这是一个内部接口
    '''

    def get(self, request, cid):
        '''
        获取比赛所有队伍的报名信息
        :param request:
        :param cid:
        :return:
        '''

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('报名汇总')
        init_sheet = ['队伍名', '作品名', '负责人', '成员1', '成员2', '作品链接']
        for i in range(6):
            sheet.write(0, i, init_sheet[i])
        contest = Contest.objects.filter(id=cid)
        if not contest.exists():
            return HttpResponse('比赛不存在')
        contest = contest[0]
        contest_team = contest.team.all()
        for i in range(1, contest_team.count() + 1):
            teamOBJ = contest_team[i - 1]
            teamMember = teamOBJ.teamMember.filter(memberRoles='member')
            write_array = [teamOBJ.team_name, teamOBJ.works_name,
                           teamOBJ.teamMember.filter(memberRoles='leader')[0].account.name]
            for name in teamMember:
                write_array.append(name.account.name)
            for j in range(len(write_array)):
                sheet.write(i, j, write_array[j])
            sheet.write(i, 5, teamOBJ.works_link)
        workbook.save('sheet/' + contest.contestName + '报名表.xls')

        try:
            response = StreamingHttpResponse(open('sheet/' + contest.contestName + '报名表.xls', 'rb'))
            response['Content-Type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + 'signupForm.xls'

            return response
        except:
            raise Http404
