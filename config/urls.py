from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView
from cases.sitemaps import CaseSitemap, StaticSitemap

# Реестр sitemap
sitemaps = {
	'cases': CaseSitemap,
	'static': StaticSitemap,
}

urlpatterns = [
	path('admin/', admin.site.urls),
	path('cases/', include('cases.urls')),
	path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

	# Статические страницы (новые URL)
	path('privacy/', TemplateView.as_view(template_name='privacy-policy.html'), name='privacy_policy'),
	path('offer/', TemplateView.as_view(template_name='oferta.html'), name='oferta'),
	path('cookies/', TemplateView.as_view(template_name='cookie-consent.html'), name='cookie_consent'),
	path('requisites/', TemplateView.as_view(template_name='requisites.html'), name='requisites'),

	# Редиректы 301 — старые URL статических страниц
	path('privacy-policy/', RedirectView.as_view(url='/privacy/', permanent=True)),
	path('oferta/', RedirectView.as_view(url='/offer/', permanent=True)),
	path('cookie-consent/', RedirectView.as_view(url='/cookies/', permanent=True)),

	# Редиректы 301 — старые URL услуг
	path('seo-top/', RedirectView.as_view(url='/yandex-top/', permanent=True)),
	path('seo-full/', RedirectView.as_view(url='/seo-promotion/', permanent=True)),
	path('seo-setup/', RedirectView.as_view(url='/seo-optimization/', permanent=True)),
	path('html-css/', RedirectView.as_view(url='/verstka/', permanent=True)),
	path('website/', RedirectView.as_view(url='/site-development/', permanent=True)),
	path('internet-shop/', RedirectView.as_view(url='/ecommerce/', permanent=True)),
	path('avito-ads/', RedirectView.as_view(url='/avitolog-vedenie/', permanent=True)),
	path('avito-day/', RedirectView.as_view(url='/avito-setup/', permanent=True)),
	path('avito-consult/', RedirectView.as_view(url='/avito-consulting/', permanent=True)),
	path('avito-autoload/', RedirectView.as_view(url='/avito-feed/', permanent=True)),

	path('', include('services.urls')),
	path('nested_admin/', include('nested_admin.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
handler403 = 'django.views.defaults.permission_denied'