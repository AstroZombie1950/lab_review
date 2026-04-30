from django.db import models
from django.utils.text import slugify

# Направления для сайдбара
DIRECTION_CHOICES = [
	('avito', 'Авито'),
	('seo', 'СЕО'),
	('direct', 'Яндекс.Директ'),
	('dev', 'Разработка'),
]

# Услуги (7 штук по ТЗ)
SERVICE_CHOICES = [
	('avito_ads', 'Создание и ведение рекламной кампании Авито'),
	('seo_full', 'СЕО под ключ'),
	('seo_top', 'Вывод сайта в топ Яндекса'),
	('direct_ads', 'Ведение рекламных кампаний в Яндекс Директ'),
	('landing', 'Разработка лендинга'),
	('shop', 'Разработка интернет-магазина'),
	('website', 'Разработка сайта'),
]


class Tag(models.Model):
	name = models.CharField('Название', max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True, blank=True)

	class Meta:
		verbose_name = 'Тег'
		verbose_name_plural = 'Теги'

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name, allow_unicode=True)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name


class Case(models.Model):
	# Основное
	title = models.CharField('Заголовок', max_length=200)
	slug = models.SlugField('URL', max_length=200, unique=True, blank=True)
	service = models.CharField('Услуга', max_length=50, choices=SERVICE_CHOICES)
	direction = models.CharField('Направление', max_length=20, choices=DIRECTION_CHOICES)
	industry = models.CharField('Отрасль', max_length=100, blank=True)
	tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')

	# Для карточки в списке
	description = models.TextField('Короткое описание')
	cover = models.ImageField('Обложка', upload_to='cases/covers/', blank=True, null=True)
	metrics = models.JSONField('Метрики', default=list, blank=True, help_text='Список строк: ["+142% заявок", "-31% лид"]')

	# Внутренняя страница
	blocks = models.JSONField('Блоки страницы', default=list, blank=True)

	# Мета
	meta_title = models.CharField('Meta Title', max_length=200, blank=True)
	meta_description = models.TextField('Meta Description', blank=True)

	# Служебное
	is_published = models.BooleanField('Опубликован', default=False)
	created_at = models.DateTimeField('Дата создания', auto_now_add=True)

	class Meta:
		verbose_name = 'Кейс'
		verbose_name_plural = 'Кейсы'
		ordering = ['-created_at']

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title, allow_unicode=True)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title