from django.conf.urls import url
from django.urls import path
from mainapp import views
urlpatterns = [
    path('',views.general,name='general'),
    path('login',views.login,name="login"),
    path('send',views.send,name="send"),
    path('sendmessage',views.send_message,name="send"),
    path('greeting',views.send_greetings,name="send"),
    path('withdraw', views.withdraw,name="withdraw")
    
]