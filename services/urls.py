from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
	path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
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
	# avito-страницы
    path('avito-ads/', views.avito_ads, name='avito_ads'),
    path('avito-day/', views.avito_day, name='avito_day'),
    path('avito-consult/', views.avito_consult, name='avito_consult'),
    path('avito-autoload/', views.avito_autoload, name='avito_autoload'),
]