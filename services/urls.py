from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
	path('', views.home, name='home'),
	path('contacts/', views.contacts, name='contacts'),
	path('send-form/', views.send_form, name='send_form'),
	# Разработка
	path('ecommerce/', views.internet_shop, name='internet_shop'),
	path('landing/', views.landing, name='landing'),
	path('site-development/', views.website, name='website'),
	path('verstka/', views.html_css, name='html_css'),
	# SEO
	path('seo-optimization/', views.seo_setup, name='seo_setup'),
	path('seo-promotion/', views.seo_full, name='seo_full'),
	path('yandex-top/', views.seo_top, name='seo_top'),
	path('yandex-direct/', views.yandex_direct, name='yandex_direct'),
	# Авито
	path('avitolog-vedenie/', views.avito_ads, name='avito_ads'),
	path('avito-setup/', views.avito_day, name='avito_day'),
	path('avito-consulting/', views.avito_consult, name='avito_consult'),
	path('avito-feed/', views.avito_autoload, name='avito_autoload'),
]