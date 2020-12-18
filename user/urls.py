from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import RegiterView, ActiveView, LoginView, send_email, UserCenterView

app_name = 'user'
urlpatterns =[
    path('register/', RegiterView.as_view(), name="register"),
    path('active/<str:token>', ActiveView.as_view(), name='active'),
    path('login/', LoginView.as_view(), name='login'),
    path('auth/', send_email),
    path('center/', UserCenterView.as_view(), name='center'),
]