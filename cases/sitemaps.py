from django.contrib.sitemaps import Sitemap
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

	# (url, priority)
	pages = [
		('/',                    0.9),
		('/cases/',              0.8),
		# Разработка
		('/ecommerce/',          0.7),
		('/landing/',            0.7),
		('/site-development/',   0.7),
		('/verstka/',            0.7),
		# SEO
		('/seo-optimization/',   0.7),
		('/seo-promotion/',      0.7),
		('/yandex-top/',         0.7),
		('/yandex-direct/',      0.7),
		# Авито
		('/avitolog-vedenie/',   0.7),
		('/avito-setup/',        0.7),
		('/avito-consulting/',   0.7),
		('/avito-feed/',         0.7),
		# Прочее
		('/contacts/',           0.6),
	]

	def items(self):
		return self.pages

	def location(self, item):
		return item[0]

	def priority(self, item):
		return item[1]