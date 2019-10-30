from rest_framework.views import APIView
from app.contest.models import Contest
from django.http import JsonResponse

class AdminInfo(APIView):
    '''
    这是一个内部接口
    '''
