from django.db import models
from cases.models import Employee


# Слаги всех 12 страниц услуг
SERVICE_SLUG_CHOICES = [
	('avito-ads',      'Авито — Ведение рекламы'),
	('avito-day',      'Авито — Авитолог на день'),
	('avito-consult',  'Авито — Консультация'),
	('avito-autoload', 'Авито — Автозагрузка'),
	('website',        'Разработка сайта'),
	('internet-shop',  'Разработка интернет-магазина'),
	('landing',        'Разработка лендинга'),
	('html-css',       'Вёрстка по макету'),
	('seo-setup',      'SEO — Внутренняя настройка'),
	('seo-full',       'SEO — Под ключ'),
	('seo-top',        'SEO — Вывод в топ'),
	('yandex-direct',  'Яндекс Директ'),
]


class ServicePage(models.Model):
	"""Страница услуги — хранит привязанных сотрудников."""
	slug = models.CharField(
		'Страница услуги',
		max_length=50,
		unique=True,
		choices=SERVICE_SLUG_CHOICES,
	)
	employees = models.ManyToManyField(
		Employee,
		through='ServicePageEmployee',
		verbose_name='Сотрудники',
		blank=True,
	)

	class Meta:
		verbose_name = 'Страница услуги'
		verbose_name_plural = 'Страницы услуг'
		ordering = ['slug']

	def __str__(self):
		return self.get_slug_display()


class ServicePageEmployee(models.Model):
	"""Промежуточная модель — сотрудник на странице услуги с порядком."""
	service_page = models.ForeignKey(
		ServicePage,
		on_delete=models.CASCADE,
		verbose_name='Страница',
	)
	employee = models.ForeignKey(
		Employee,
		on_delete=models.CASCADE,
		verbose_name='Сотрудник',
	)
	order = models.PositiveSmallIntegerField(
		'Порядок',
		default=0,
	)

	class Meta:
		verbose_name = 'Сотрудник на странице'
		verbose_name_plural = 'Сотрудники на странице'
		ordering = ['order', 'employee__name']
		unique_together = [('service_page', 'employee')]

	def __str__(self):
		return f'{self.service_page} — {self.employee}'