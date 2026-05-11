from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Направления (разделы меню)
DIRECTION_CHOICES = [
	('avito', 'Авито'),
	('dev',   'Разработка'),
	('seo',   'СЕО'),
	('direct','Яндекс Директ'),
]

# Услуги — по разделам
SERVICE_CHOICES = [
	# Авито
	('avito_ads',      'Создание и ведение рекламной кампании'),
	('avito_day',      'Авитолог на день'),
	('avito_consult',  'Консультация Авитолога'),
	('avito_autoload', 'Создание автозагрузочных файлов'),
	# Разработка
	('shop',           'Разработка интернет-магазина'),
	('landing',        'Разработка лендинга'),
	('website',        'Разработка сайта'),
	('html_css',       'Верстка сайтов'),
	# СЕО
	('seo_setup',      'Внутренняя настройка СЕО'),
	('seo_full',       'Ведение проекта под ключ'),
	('seo_top',        'Вывод сайта в топ Яндекса'),
	# Яндекс Директ
	('direct_ads',     'Ведение рекламных кампаний'),
]

# Типы блоков страницы кейса
BLOCK_TYPE_CHOICES = [
	('intro',         'Вводный текст'),
	('task_resume',   'Задача + резюме проекта'),
	('tasks_grid',    'Сетка задач (что мы решали)'),
	('content_full',  'Контент-блок: на всю ширину'),
	('content_two',   'Контент-блок: две колонки'),
	('metrics',       'Результаты / цифры'),
	('team',          'Команда'),
	('cta',           'Призыв к действию (CTA)'),
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
	title = models.CharField(
		'Заголовок кейса',
		max_length=200,
		help_text='Короткое название проекта. Отображается в карточке на странице /cases/ и в заголовке страницы кейса. Пример: «SEO под ключ для интернет-магазина стройматериалов»'
	)
	slug = models.SlugField(
		'URL (slug)',
		max_length=200,
		unique=True,
		blank=True,
		help_text='Часть адреса страницы. Заполняется автоматически из заголовка. Можно изменить вручную — только латиница, цифры и дефисы. Пример: seo-stroymaterialy'
	)
	service = models.CharField(
		'Услуга',
		max_length=50,
		choices=SERVICE_CHOICES,
		help_text='Выберите услугу, которая была оказана клиенту. Используется для фильтрации кейсов.'
	)
	direction = models.CharField(
		'Направление',
		max_length=20,
		choices=DIRECTION_CHOICES,
		help_text='Категория кейса для сайдбара и фильтров. Авито / SEO / Яндекс.Директ / Разработка.'
	)
	industry = models.CharField(
		'Отрасль',
		max_length=100,
		blank=True,
		help_text='Сфера бизнеса клиента. Пример: Строительство, Медицина, Интернет-магазин, HoReCa. Необязательное поле.'
	)
	tags = models.ManyToManyField(
		Tag,
		blank=True,
		verbose_name='Теги',
		help_text='Дополнительные метки для фильтрации. Можно выбрать несколько. Теги создаются отдельно в разделе «Теги».'
	)

	# Карточка в списке
	description = models.TextField(
		'Короткое описание',
		help_text='1–2 предложения о проекте. Отображается в карточке на странице /cases/ и в превью при наведении. Пример: «Вывели сайт в топ-3 по 47 запросам за 4 месяца»'
	)
	cover = models.URLField(
		'Обложка (URL)',
		blank=True,
		help_text='Ссылка на изображение для карточки кейса. Пример: https://example.com/image.jpg'
	)

	# Герой страницы кейса
	hero_bg = models.URLField(
		'Фоновое изображение героя (URL)',
		blank=True,
		help_text='Ссылка на фоновое изображение героя. Пример: https://example.com/hero.jpg'
	)
	client_url = models.URLField(
		'Сайт клиента',
		blank=True,
		help_text='Ссылка на сайт клиента. Показывается в герое страницы кейса кнопкой «Перейти на сайт». Пример: https://example.ru. Необязательное поле.'
	)
	year = models.CharField(
		'Год проекта',
		max_length=10,
		blank=True,
		help_text='Год выполнения проекта. Показывается в герое рядом с тегами. Пример: 2024'
	)

	# Мета
	meta_title = models.CharField(
		'Meta Title',
		max_length=200,
		blank=True,
		help_text='Заголовок для поисковых систем. Если не заполнен — используется «Заголовок кейса». Рекомендуемая длина: 50–70 символов.'
	)
	meta_description = models.TextField(
		'Meta Description',
		blank=True,
		help_text='Описание страницы для поисковых систем. Если не заполнено — используется «Короткое описание». Рекомендуемая длина: 120–160 символов.'
	)

	# Служебное
	is_published = models.BooleanField(
		'Опубликован',
		default=False,
		help_text='Включите, чтобы кейс появился на сайте. Пока галочка не стоит — кейс виден только в админке.'
	)
	published_at = models.DateField(
		'Дата публикации',
		default=timezone.now,
		help_text='Определяет порядок в списке — новые кейсы идут выше. Подставляется автоматически, можно изменить вручную.'
	)
	created_at = models.DateTimeField('Дата создания', auto_now_add=True)

	class Meta:
		verbose_name = 'Кейс'
		verbose_name_plural = 'Кейсы'
		ordering = ['-published_at', '-created_at']

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title, allow_unicode=True)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title


# ── Метрики карточки кейса ───────────────────────────────────────────────────

class CaseMetric(models.Model):
	"""Одна метрика в карточке кейса (до 6 штук)."""
	case = models.ForeignKey(
		Case,
		on_delete=models.CASCADE,
		related_name='metrics',
		verbose_name='Кейс'
	)
	value = models.CharField(
		'Значение',
		max_length=50,
		help_text='Число или короткий текст. Примеры: «+142%», «топ-3», «4 мес»'
	)
	label = models.CharField(
		'Подпись',
		max_length=100,
		help_text='Что означает это число. Пример: «рост трафика», «позиции в Яндексе»'
	)
	order = models.PositiveSmallIntegerField('Порядок', default=0)

	class Meta:
		verbose_name = 'Метрика'
		verbose_name_plural = 'Метрики'
		ordering = ['order']

	def __str__(self):
		return f'{self.value} — {self.label}'


# ── Блок контента кейса ──────────────────────────────────────────────────────

class CaseBlock(models.Model):
	"""Один контентный блок страницы кейса."""

	case = models.ForeignKey(
		Case,
		on_delete=models.CASCADE,
		related_name='content_blocks',
		verbose_name='Кейс'
	)
	block_type = models.CharField(
		'Тип блока',
		max_length=30,
		choices=BLOCK_TYPE_CHOICES,
		help_text='Выберите тип — ниже появятся только нужные поля.'
	)
	order = models.PositiveIntegerField(
		'Порядок',
		default=0,
		help_text='Подставляется автоматически. Блоки отображаются по возрастанию этого числа.'
	)
	is_visible = models.BooleanField(
		'Показывать на сайте',
		default=True,
		help_text='Снимите галочку, чтобы временно скрыть блок не удаляя его.'
	)

	# ── intro ────────────────────────────────────────────────────────────────
	intro_text = models.TextField(
		'Вводный текст',
		blank=True,
		help_text='Крупный абзац в начале страницы. Описывает контекст: кто клиент, какая была ситуация, почему обратились. Длина: 3–6 предложений.'
	)

	# ── task_resume ──────────────────────────────────────────────────────────
	task_text = models.TextField(
		'Задача заказчика',
		blank=True,
		help_text='Одна–две фразы: что именно попросил сделать клиент. Показывается в акцентном блоке слева. Пример: «Вывести сайт в топ-10 по 50 целевым запросам за 6 месяцев»'
	)

	# ── tasks_grid ───────────────────────────────────────────────────────────
	tasks_title = models.CharField(
		'Заголовок (сетка задач)',
		max_length=300,
		blank=True,
		help_text='Заголовок над сеткой карточек. Пример: «Какие задачи мы решали в проекте с Ивановым»'
	)

	# ── content_full ─────────────────────────────────────────────────────────
	cf_label = models.CharField(
		'Лейбл категории',
		max_length=100,
		blank=True,
		help_text='Маленький текст над заголовком. Пример: «SEO», «Сайты»'
	)
	cf_title = models.CharField(
		'Заголовок блока',
		max_length=300,
		blank=True,
		help_text='Крупный заголовок. Пример: «Собрали семантическое ядро из 850 запросов»'
	)
	cf_text_main = models.TextField(
		'Основной текст',
		blank=True,
		help_text='Главный абзац — 2–4 предложения, суть работы.'
	)
	cf_text_secondary = models.TextField(
		'Дополнительный текст',
		blank=True,
		help_text='Второй абзац — детали, подробности. Необязательное поле.'
	)
	cf_image = models.URLField(
		'Изображение (URL)',
		blank=True,
		help_text='Ссылка на изображение. Показывается справа от текста.'
	)
	cf_link_text = models.CharField(
		'Текст ссылки',
		max_length=200,
		blank=True,
		help_text='Подпись перед ссылкой. Пример: «Вот посмотрите:»'
	)
	cf_link_url = models.URLField(
		'URL ссылки',
		blank=True,
		help_text='Адрес сайта или страницы. Пример: https://client-site.ru'
	)

	# ── content_two — левая колонка ──────────────────────────────────────────
	left_label = models.CharField(
		'Лейбл (левая колонка)',
		max_length=100,
		blank=True,
		help_text='Необязательное поле.'
	)
	left_title = models.CharField(
		'Заголовок (левая колонка)',
		max_length=300,
		blank=True,
	)
	left_text_main = models.TextField(
		'Основной текст (левая колонка)',
		blank=True,
	)
	left_text_secondary = models.TextField(
		'Дополнительный текст (левая колонка)',
		blank=True,
		help_text='Необязательное поле.'
	)
	left_link_text = models.CharField(
		'Текст ссылки (левая колонка)',
		max_length=200,
		blank=True,
		help_text='Необязательное поле.'
	)
	left_link_url = models.URLField(
		'URL ссылки (левая колонка)',
		blank=True,
		help_text='Необязательное поле.'
	)

	# ── content_two — правая колонка ─────────────────────────────────────────
	right_label = models.CharField(
		'Лейбл (правая колонка)',
		max_length=100,
		blank=True,
		help_text='Необязательное поле.'
	)
	right_title = models.CharField(
		'Заголовок (правая колонка)',
		max_length=300,
		blank=True,
	)
	right_text_main = models.TextField(
		'Основной текст (правая колонка)',
		blank=True,
	)
	right_text_secondary = models.TextField(
		'Дополнительный текст (правая колонка)',
		blank=True,
		help_text='Необязательное поле.'
	)
	right_link_text = models.CharField(
		'Текст ссылки (правая колонка)',
		max_length=200,
		blank=True,
		help_text='Необязательное поле.'
	)
	right_link_url = models.URLField(
		'URL ссылки (правая колонка)',
		blank=True,
		help_text='Необязательное поле.'
	)

	# ── metrics ──────────────────────────────────────────────────────────────
	metrics_title = models.CharField(
		'Заголовок блока результатов',
		max_length=200,
		blank=True,
		help_text='Пример: «Немного цифр», «Результат работ»'
	)
	metrics_subtitle = models.CharField(
		'Подзаголовок',
		max_length=300,
		blank=True,
		help_text='Одна–две строки под заголовком. Необязательное поле.'
	)

	# ── cta ──────────────────────────────────────────────────────────────────
	cta_title = models.CharField(
		'Заголовок CTA',
		max_length=200,
		blank=True,
		help_text='Крупный заголовок. Пример: «Заказать проект», «Есть похожая задача?»'
	)
	cta_text = models.TextField(
		'Текст CTA',
		blank=True,
		help_text='1–2 предложения под заголовком.'
	)
	cta_btn_text = models.CharField(
		'Текст кнопки',
		max_length=100,
		blank=True,
		default='Написать',
		help_text='Надпись на кнопке. По умолчанию: «Написать»'
	)
	cta_btn_url = models.CharField(
		'Ссылка кнопки',
		max_length=200,
		blank=True,
		default='#contact',
		help_text='Куда ведёт кнопка. Можно указать якорь (#contact) или полный URL.'
	)

	class Meta:
		verbose_name = 'Блок кейса'
		verbose_name_plural = 'Блоки кейса'
		ordering = ['order']

	def __str__(self):
		return f'{self.get_block_type_display()} (порядок {self.order})'


# ── Инлайн-модели для блоков ─────────────────────────────────────────────────

class ResumeItem(models.Model):
	"""Одна строка резюме проекта (блок task_resume)."""
	block = models.ForeignKey(
		CaseBlock,
		on_delete=models.CASCADE,
		related_name='resume_items',
		verbose_name='Блок'
	)
	label = models.CharField(
		'Метка',
		max_length=100,
		help_text='Пример: «Старт работ», «Сдача проекта», «Длительность»'
	)
	value = models.CharField(
		'Значение',
		max_length=100,
		help_text='Пример: «январь 2024», «6 месяцев»'
	)
	order = models.PositiveSmallIntegerField('Порядок', default=0)

	class Meta:
		verbose_name = 'Строка резюме'
		verbose_name_plural = 'Резюме проекта'
		ordering = ['order']

	def __str__(self):
		return f'{self.label}: {self.value}'


class TaskItem(models.Model):
	"""Одна карточка в сетке задач (блок tasks_grid)."""
	block = models.ForeignKey(
		CaseBlock,
		on_delete=models.CASCADE,
		related_name='task_items',
		verbose_name='Блок'
	)
	title = models.CharField(
		'Заголовок карточки',
		max_length=200,
		help_text='Пример: «Собрали семантику», «Устранили технические ошибки»'
	)
	text = models.TextField(
		'Текст карточки',
		blank=True,
		help_text='Краткое описание. Пример: «Подобрали 300 ключевых запросов с учётом региона»'
	)
	order = models.PositiveSmallIntegerField('Порядок', default=0)

	class Meta:
		verbose_name = 'Карточка задачи'
		verbose_name_plural = 'Карточки задач'
		ordering = ['order']

	def __str__(self):
		return self.title


class MetricItem(models.Model):
	"""Одна цифра в блоке результатов (блок metrics)."""
	block = models.ForeignKey(
		CaseBlock,
		on_delete=models.CASCADE,
		related_name='metric_items',
		verbose_name='Блок'
	)
	value = models.CharField(
		'Значение',
		max_length=50,
		help_text='Число или текст. Примеры: «+142», «топ-3»'
	)
	unit = models.CharField(
		'Единица измерения',
		max_length=20,
		blank=True,
		help_text='После числа. Примеры: «%», «мес», «тыс». Можно оставить пустым.'
	)
	label = models.CharField(
		'Подпись',
		max_length=150,
		help_text='Пример: «рост органического трафика»'
	)
	order = models.PositiveSmallIntegerField('Порядок', default=0)

	class Meta:
		verbose_name = 'Показатель'
		verbose_name_plural = 'Показатели'
		ordering = ['order']

	def __str__(self):
		return f'{self.value}{self.unit} — {self.label}'


class TeamMember(models.Model):
	"""Один участник команды (блок team)."""
	block = models.ForeignKey(
		CaseBlock,
		on_delete=models.CASCADE,
		related_name='team_members',
		verbose_name='Блок'
	)
	name = models.CharField(
		'Имя',
		max_length=100,
		help_text='Пример: «Иван Петров»'
	)
	role = models.CharField(
		'Роль',
		max_length=150,
		help_text='Пример: «SEO-специалист», «Копирайтер»'
	)
	order = models.PositiveSmallIntegerField('Порядок', default=0)

	class Meta:
		verbose_name = 'Участник команды'
		verbose_name_plural = 'Команда'
		ordering = ['order']

	def __str__(self):
		return f'{self.name} — {self.role}'