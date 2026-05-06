from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
	path('admin/', admin.site.urls),
	path('cases/', include('cases.urls')),
	path('privacy-policy/', TemplateView.as_view(template_name='privacy-policy.html'), name='privacy_policy'),
	path('oferta/', TemplateView.as_view(template_name='oferta.html'), name='oferta'),
	path('cookie-consent/', TemplateView.as_view(template_name='cookie-consent.html'), name='cookie_consent'),
	path('requisites/', TemplateView.as_view(template_name='requisites.html'), name='requisites'),
	path('', include('services.urls')),
    path('nested_admin/', include('nested_admin.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)