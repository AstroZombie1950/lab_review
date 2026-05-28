import os
import json
import urllib.request
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from cases.models import Case, Employee
from .models import ServicePage

logger = logging.getLogger(__name__)

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT  = os.getenv('TG_CHAT')


def _svc_ctx(slug):
	"""Контекст для страницы услуги — сотрудники из ServicePage или все."""
	try:
		page = ServicePage.objects.prefetch_related('servicepageemployee_set__employee').get(slug=slug)
		employees = [spe.employee for spe in page.servicepageemployee_set.all()]
	except ServicePage.DoesNotExist:
		# Страница ещё не настроена в админке — показываем всех сотрудников
		employees = list(Employee.objects.all())
	return {'employees': employees}


# Главная страница
def home(request):
	cases = Case.objects.filter(is_published=True)[:7]
	return render(request, 'home.html', {'cases': cases})

def contacts(request):
	return render(request, 'contacts.html')


def internet_shop(request):
	return render(request, 'services/internet-shop.html', _svc_ctx('internet-shop'))

def landing(request):
	return render(request, 'services/landing.html', _svc_ctx('landing'))

def website(request):
	return render(request, 'services/website.html', _svc_ctx('website'))

def html_css(request):
	return render(request, 'services/html-css.html', _svc_ctx('html-css'))

# SEO-страницы
def seo_setup(request):
	return render(request, 'services/seo-setup.html', _svc_ctx('seo-setup'))

def seo_full(request):
	return render(request, 'services/seo-full.html', _svc_ctx('seo-full'))

def seo_top(request):
	return render(request, 'services/seo-top.html', _svc_ctx('seo-top'))

def yandex_direct(request):
	return render(request, 'services/yandex-direct.html', _svc_ctx('yandex-direct'))

# Авито-страницы
def avito_ads(request):
	return render(request, 'services/avito-ads.html', _svc_ctx('avito-ads'))

def avito_day(request):
	return render(request, 'services/avito-day.html', _svc_ctx('avito-day'))

def avito_consult(request):
	return render(request, 'services/avito-consult.html', _svc_ctx('avito-consult'))

def avito_autoload(request):
	return render(request, 'services/avito-autoload.html', _svc_ctx('avito-autoload'))


# Отправка формы в Telegram
@require_POST
def send_form(request):
	try:
		data = json.loads(request.body)
		text = data.get('text', '').strip()
		if not text:
			return JsonResponse({'ok': False, 'error': 'empty'}, status=400)
		if len(text) > 4000:
			text = text[:4000]
		url     = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage'
		payload = json.dumps({'chat_id': TG_CHAT, 'text': text}).encode()
		req     = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
		urllib.request.urlopen(req, timeout=10)
		return JsonResponse({'ok': True})
	except Exception as e:
		logger.error('send_form error: %s', e)
		return JsonResponse({'ok': False}, status=500)