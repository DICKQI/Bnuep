from rest_framework.views import APIView
from app.account.models import UserAccount, AccountPassword
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json


class RegisterView(APIView):

    def post(self, request):
        '''
        注册账户
        :param request:
        :return:
        '''
        try:
            jsonParams = json.loads((request.body).decode('utf-8'))
            student_id = jsonParams.get('studentId')
            if UserAccount.objects.filter(student_id=student_id).exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '学号已存在'
                }, status=401)
            name = jsonParams.get('name')
            password = make_password(jsonParams.get('password'))
            grade = jsonParams.get('grade')
            major = jsonParams.get('major')
            email = jsonParams.get('email')
            qq_number = jsonParams.get('qq')
            wechat = jsonParams.get('wechat')
            phone_number = jsonParams.get('phone number')

            newPassword = AccountPassword.objects.create(password=password)
            newUser = UserAccount.objects.create(
                name=name,
                password=newPassword,
                student_id=student_id,
                grade=grade,
                email=email,
                major=major,
                qq_number=qq_number,
                wechat=wechat,
                phone_number=phone_number
            )
            return JsonResponse({
                'status': True,
                'id': newUser.id,
                'name': newUser.name
            })
        except Exception as ex:
            return JsonResponse({
                'status': False,
                'errMsg': str(ex)
            }, status=403)