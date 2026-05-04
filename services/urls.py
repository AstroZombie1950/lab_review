from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
	path('', views.home, name='home'),
	path('internet-shop/', views.internet_shop, name='internet_shop'),
	path('send-form/', views.send_form, name='send_form'),
	path('landing/', views.landing, name='landing'),
	path('website/', views.website, name='website'),
	path('html-css/', views.html_css, name='html_css'),
	# SEO-страницы
	path('seo-setup/', views.seo_setup, name='seo_setup'),
	path('seo-full/', views.seo_full, name='seo_full'),
	path('seo-top/', views.seo_top, name='seo_top'),
	path('yandex-direct/', views.yandex_direct, name='yandex_direct'),
]