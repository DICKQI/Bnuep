from django.http import JsonResponse
from app.account.models import UserAccount

def getUser(name):
    return UserAccount.objects.get(name=name)

def check_login(func):
    def wrapper(self, request, *args, **kwargs):
        if request.session.get('login') != None:
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({
                'status': False,
                'errMsg': '你还未登录'
            }, status=401)
    return wrapper