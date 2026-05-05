import os
import json
import urllib.request

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from dotenv import load_dotenv

from cases.models import Case

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT = os.getenv('TG_CHAT')


# Главная страница
def home(request):
	cases = Case.objects.filter(is_published=True).order_by('-created_at')[:3]
	return render(request, 'home.html', {'cases': cases})


def internet_shop(request):
	return render(request, 'services/internet-shop.html')

def landing(request):
	return render(request, 'services/landing.html')

def website(request):
	return render(request, 'services/website.html')

def html_css(request):
	return render(request, 'services/html-css.html')

# SEO-страницы
def seo_setup(request):
	return render(request, 'services/seo-setup.html')

def seo_full(request):
	return render(request, 'services/seo-full.html')

def seo_top(request):
	return render(request, 'services/seo-top.html')

def yandex_direct(request):
	return render(request, 'services/yandex-direct.html')


# Отправка формы в Telegram
@require_POST
def send_form(request):
	try:
		data = json.loads(request.body)
		text = data.get('text', '')
		url = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage'
		payload = json.dumps({'chat_id': TG_CHAT, 'text': text}).encode()
		req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
		urllib.request.urlopen(req)
		return JsonResponse({'ok': True})
	except Exception:
		return JsonResponse({'ok': False}, status=500)