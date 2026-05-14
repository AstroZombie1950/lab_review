from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Case


class CaseSitemap(Sitemap):
	"""Все опубликованные кейсы, кроме разработки."""
	changefreq = 'monthly'
	priority = 0.8

	def items(self):
		return Case.objects.filter(is_published=True).exclude(direction='dev')

	def lastmod(self, obj):
		return obj.published_at

	def location(self, obj):
		return f'/cases/{obj.slug}/'


class StaticSitemap(Sitemap):
	"""Статические страницы сайта."""
	changefreq = 'monthly'
	priority = 0.6

	# (url_name, priority)
	pages = [
		('/',            0.9),
		('/cases/',      0.8),
		('/internet-shop/', 0.7),
		('/landing/',    0.7),
		('/website/',    0.7),
		('/html-css/',   0.7),
		('/seo-setup/',  0.7),
		('/seo-full/',   0.7),
		('/seo-top/',    0.7),
		('/yandex-direct/', 0.7),
		('/contacts/',   0.6),
	]

	def items(self):
		return self.pages

	def location(self, item):
		return item[0]

	def priority(self, item):
		return item[1]