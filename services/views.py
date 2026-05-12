import os
import json
import urllib.request
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from cases.models import Case

logger = logging.getLogger(__name__)

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT = os.getenv('TG_CHAT')


# Главная страница
def home(request):
    cases = Case.objects.filter(is_published=True)[:7]
    return render(request, 'home.html', {'cases': cases})

def contacts(request):
    return render(request, 'contacts.html')

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

# Авито-страницы
def avito_ads(request):
    return render(request, 'services/avito-ads.html')

def avito_day(request):
    return render(request, 'services/avito-day.html')

def avito_consult(request):
    return render(request, 'services/avito-consult.html')

def avito_autoload(request):
    return render(request, 'services/avito-autoload.html')


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
        url = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage'
        payload = json.dumps({'chat_id': TG_CHAT, 'text': text}).encode()
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
        return JsonResponse({'ok': True})
    except Exception as e:
        logger.error('send_form error: %s', e)
        return JsonResponse({'ok': False}, status=500)