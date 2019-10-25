from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    # base
    path('', AccountBaseView.as_view(), name='login_logout'),
    path('register/', RegisterView.as_view(), name='register'),
    #userControl
    path('myself/', UserControlView.as_view(), name='myself'),
]