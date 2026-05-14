from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
	path('', views.cases_list, name='list'),
	# Редирект /cases/web-dev/ → /cases/?direction=dev
	path('web-dev/', views.web_dev_redirect, name='web_dev_redirect'),
	path('<slug:slug>/', views.case_detail, name='detail'),
]