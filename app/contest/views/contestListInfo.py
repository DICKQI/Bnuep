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
        objPage = Paginator(contestsOBJ, 10)
        page = request.GET.get('page')
        try:
            objList = objPage.page(page)
        except PageNotAnInteger:
            objList = objPage.page(1)
        except EmptyPage:
            objList = objPage.page(1)
        contests = [model_to_dict(con, exclude=self.EXCLUDE_FIELDS) for con in objList if con.contestStatus]
        for c in contests:
            c['beginTime'] = str(c['beginTime'])[:10]
            c['signupEndTime'] = str(c['signupEndTime'])[:10]
        return JsonResponse({
            'status': True,
            'contest': contests,
            'has next': objList.has_next(),
            'has previous': objList.has_previous()
        })