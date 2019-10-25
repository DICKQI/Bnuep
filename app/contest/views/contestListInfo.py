from ..models import Contest
from django.http import JsonResponse
from Common.UserCommon import check_login, getUser
from django.forms import model_to_dict
from rest_framework.views import APIView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class ContestListView(APIView):

    EXCLUDE_FIELDS = [
        'createTime', 'team', 'UpperLimit', 'picture'
    ]

    def get(self, request):
        '''
        获取比赛信息列表
        :param request:
        :return:
        '''
        contestsOBJ = Contest.objects.all()
        contests = [model_to_dict(con, exclude=self.EXCLUDE_FIELDS) for con in contestsOBJ if con.contestStatus]
        for c in contests:
            c['beginTime'] = str(c['beginTime'])[:10]
            c['signupEndTime'] = str(c['signupEndTime'])[:10]
        return JsonResponse({
            'status': True,
            'contest': contests,
        })