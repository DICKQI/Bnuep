from rest_framework.views import APIView
from app.account.models import UserAccount
from Common.UserCommon import check_login
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import json


class AccountBaseView(APIView):

    def post(self, request):
        '''
        登录账户
        :param request:
        :return:
        '''
        try:
            jsonParams = json.loads((request.body).decode('utf-8'))
            name = jsonParams.get('name')
            password = jsonParams.get('password')
            user = UserAccount.objects.filter(name=name)
            if not user.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '用户不存在，请先注册'
                }, status=404)
            user = user[0]
            db_password = user.password.password
            if not check_password(password, db_password):
                return JsonResponse({
                    'status': False,
                    'errMsg': '密码错误，请重新输入'
                }, status=401)
            request.session['login'] = user.name
            return JsonResponse({
                'status': True,
                'id': user.id,
                'name': user.name
            })
        except:
            return JsonResponse({
                'status': False,
                'errMsg': '出现未知错误'
            }, status=403)

    @check_login
    def delete(self, request):
        '''
        登出账户
        :param request:
        :return:
        '''
        request.session['login'] = None
        return JsonResponse({
            'status': True,
        })
