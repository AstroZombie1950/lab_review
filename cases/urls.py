from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
	path('', views.cases_list, name='list'),
	path('<slug:slug>/', views.case_detail, name='detail'),
]