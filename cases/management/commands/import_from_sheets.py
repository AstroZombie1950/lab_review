import urllib.request
import urllib.parse
import json
import logging
import hashlib
import os
import urllib.error

from pathlib import Path
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.db import transaction

from cases.models import (
	Case, Tag, CaseMetric, CaseBlock,
	ResumeItem, TaskItem, MetricItem, TeamMember,
	DevCaseImage, Employee,
)

logger = logging.getLogger(__name__)


def download_image(url, subfolder):
	"""
	Скачать изображение по URL и сохранить в media/{subfolder}/.
	Имя файла = MD5(url).ext — повторно не скачивается если файл уже есть.
	Возвращает относительный путь для сохранения в поле модели (строку).
	"""
	url = url.strip()
	if not url:
		return ''

	# Определяем расширение из URL (берём последнюю часть пути без параметров)
	path_part = urllib.parse.urlparse(url).path
	ext = os.path.splitext(path_part)[1].lower() or '.jpg'
	# Ограничиваем допустимые расширения
	if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'):
		ext = '.jpg'

	# Имя файла — MD5 от URL
	md5 = hashlib.md5(url.encode()).hexdigest()
	filename = f'{md5}{ext}'
	rel_path = f'{subfolder}/{filename}'
	abs_path = settings.MEDIA_ROOT / rel_path

	# Если файл уже есть — не скачиваем
	if abs_path.exists():
		return f'/media/{rel_path}'

	# Создаём папку если нет
	abs_path.parent.mkdir(parents=True, exist_ok=True)

	try:
		req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		with urllib.request.urlopen(req, timeout=15) as resp:
			data = resp.read()
			content_type = resp.headers.get('Content-Type', '').split(';')[0].strip()
			ct_map = {
				'image/jpeg':    '.jpg',
				'image/png':     '.png',
				'image/gif':     '.gif',
				'image/webp':    '.webp',
				'image/svg+xml': '.svg',
			}
			detected_ext = ct_map.get(content_type)
			if detected_ext:
				ext = detected_ext
				filename = f'{md5}{ext}'
				rel_path = f'{subfolder}/{filename}'
				abs_path = settings.MEDIA_ROOT / rel_path
				abs_path.parent.mkdir(parents=True, exist_ok=True)
		with open(abs_path, 'wb') as f:
			f.write(data)
		logger.info('Скачано: %s → %s', url, rel_path)
		return f'/media/{rel_path}'
	except Exception as e:
		logger.warning('Не удалось скачать %s: %s', url, e)
		return url  # fallback — оставляем оригинальный URL

logger = logging.getLogger(__name__)

# Фиксированный CTA для всех кейсов из таблицы
CTA_DEFAULTS = {
	'cta_title':    'Есть похожая задача?',
	'cta_text':     'Расскажите о проекте — обсудим и предложим решение.',
	'cta_btn_text': 'Написать',
	'cta_btn_url':  '#contact',
	'cta_image':    '',
}


def fetch_sheet(api_key, sheet_id):
	"""Получить все строки из первого листа таблицы."""
	range_ = urllib.parse.quote('A:CH')
	url = (
		f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}'
		f'/values/{range_}?key={api_key}'
	)
	with urllib.request.urlopen(url, timeout=15) as resp:
		data = json.loads(resp.read())
	rows = data.get('values', [])
	if not rows:
		return []
	headers = rows[0]
	# Собираем список словарей {заголовок: значение}
	return [
		{headers[i]: row[i] if i < len(row) else '' for i in range(len(headers))}
		for row in rows[1:]
	]


def parse_published_at(raw):
	"""Парсим дату ДД.ММ.ГГГГ, при ошибке возвращаем текущее время."""
	raw = raw.strip()
	if raw:
		try:
			return timezone.make_aware(datetime.strptime(raw, '%d.%m.%Y'))
		except ValueError:
			logger.warning('Не удалось распарсить дату: %s', raw)
	return timezone.now()


def _unique_tag_slug(name):
	"""Сгенерировать slug, не конфликтующий с уже существующими тегами."""
	base = slugify(name, allow_unicode=True) or 'tag'
	slug = base
	i = 2
	# Если slug занят другим тегом — добавляем суффикс
	while Tag.objects.filter(slug=slug).exists():
		slug = f'{base}-{i}'
		i += 1
	return slug


def get_or_create_tags(raw):
	"""Создать недостающие теги из строки через запятую, вернуть список.
	Slug уникализируется явно, чтобы импорт не падал на коллизиях slug."""
	tags = []
	for name in raw.split(','):
		name = name.strip()
		if not name:
			continue
		# Ищем по точному имени; если нет — создаём с гарантированно уникальным slug
		tag = Tag.objects.filter(name=name).first()
		if tag is None:
			tag = Tag.objects.create(name=name, slug=_unique_tag_slug(name))
		tags.append(tag)
	return tags


def import_row(row):
	"""Импортировать один кейс из строки таблицы."""
	slug = row.get('slug', '').strip()
	if not slug:
		logger.warning('Пропущена строка без slug')
		return None, 'skip'

	# Основные поля кейса — картинки скачиваем локально
	defaults = {
		'title':            row.get('title', ''),
		'service':          row.get('service', ''),
		'direction':        row.get('direction', ''),
		'industry':         row.get('industry', ''),
		'description':      row.get('description', ''),
		'cover':            download_image(row.get('cover', ''),            'cases/cover'),
		'hero_bg':          download_image(row.get('hero_bg', ''),          'cases/hero_bg'),
		'hero_image':       download_image(row.get('hero_image', ''),       'cases/hero_image'),
		'hero_arrow_svg':   download_image(row.get('hero_arrow_svg', ''),   'cases/hero_arrow'),
		'client_url':       row.get('client_url', ''),
		'year':             row.get('year', ''),
		'meta_title':       row.get('meta_title', ''),
		'meta_description': row.get('meta_description', ''),
		'is_published':     row.get('is_published', '').lower() in ('true', '1', 'да', 'yes'),
		'published_at':     parse_published_at(row.get('published_at', '')),
	}

	case, created = Case.objects.update_or_create(slug=slug, defaults=defaults)

	# Теги
	tags = get_or_create_tags(row.get('tags', ''))
	case.tags.set(tags)

	# Метрики карточки (Hero) — только 3
	case.metrics.all().delete()
	for i in range(1, 4):
		value = row.get(f'metric_{i}_value', '').strip()
		label = row.get(f'metric_{i}_label', '').strip()
		if value or label:
			CaseMetric.objects.create(case=case, value=value, label=label, order=i)

	# Удаляем старые блоки перед пересозданием
	case.content_blocks.all().delete()

	order = 1

	# Блок: intro
	_make_block(case, order, 'intro', {'intro_text': row.get('intro_text', '')})
	order += 1

	# Блок: task_resume
	block = _make_block(case, order, 'task_resume', {'task_text': row.get('task_text', '')})
	order += 1
	for i in range(1, 4):
		label    = row.get(f'resume_{i}_label',         '').strip()
		unit     = row.get(f'resume_{i}_unit',          '').strip()
		text     = row.get(f'resume_{i}_text',          '').strip()
		text_add = row.get(f'resume_{i}_text_add',      '').strip()
		# Порядки — дефолты: unit=1, text=2, text_add=3
		unit_order     = int(row.get(f'resume_{i}_unit_order',     1) or 1)
		text_order     = int(row.get(f'resume_{i}_text_order',     2) or 2)
		text_add_order = int(row.get(f'resume_{i}_text_add_order', 3) or 3)
		if label or unit:
			ResumeItem.objects.create(
				block=block, label=label,
				unit=unit, unit_order=unit_order,
				text=text, text_order=text_order,
				text_add=text_add, text_add_order=text_add_order,
				order=i,
			)

	# Блок: tasks_grid
	block = _make_block(case, order, 'tasks_grid', {'tasks_title': row.get('tasks_title', '')})
	order += 1
	for i in range(1, 7):
		title = row.get(f'task_{i}_title', '').strip()
		text  = row.get(f'task_{i}_text', '').strip()
		if title:
			TaskItem.objects.create(block=block, title=title, text=text, order=i)

	# Блок: metrics (результаты/цифры)
	block = _make_block(case, order, 'metrics', {
		'metrics_title':    row.get('metrics_title', ''),
		'metrics_subtitle': row.get('metrics_subtitle', ''),
	})
	order += 1
	for i in range(1, 4):
		value = row.get(f'metric_item_{i}_value', '').strip()
		unit  = row.get(f'metric_item_{i}_unit', '').strip()
		label = row.get(f'metric_item_{i}_label', '').strip()
		if value:
			MetricItem.objects.create(block=block, value=value, unit=unit, label=label, order=i)

	# Блок: team — 4 участника
	block = _make_block(case, order, 'team', {})
	order += 1
	for i in range(1, 5):
		name  = row.get(f'member_{i}_name',  '').strip()
		role  = row.get(f'member_{i}_role',  '').strip()
		photo = row.get(f'member_{i}_photo', '').strip()
		if not name:
			continue
		# Ищем сотрудника по имени без учёта регистра
		employee = Employee.objects.filter(name__iexact=name).first()
		if not employee:
			employee = Employee.objects.create(name=name, role=role)
		elif role and employee.role != role:
			employee.role = role
			employee.save(update_fields=['role'])
		# Скачиваем фото если передан URL и это новый файл
		if photo:
			local_photo = download_image(photo, 'employees')
			# Сохраняем только если изменилось (сравниваем без /media/ префикса)
			stored = str(employee.photo)
			if stored != local_photo and f'/media/{stored}' != local_photo:
				employee.photo = local_photo
				employee.save(update_fields=['photo'])
		TeamMember.objects.create(block=block, employee=employee, order=i)

	# Блок: CTA — фиксированный текст, картинка из таблицы
	cta_fields = dict(CTA_DEFAULTS)
	cta_fields['cta_image'] = download_image(row.get('cta_image', '').strip(), 'cases/cta')
	_make_block(case, order, 'cta', cta_fields)

	# Изображения ленты (только для dev-кейсов)
	case.dev_images.all().delete()
	images_raw = row.get('dev_images', '').strip()
	if images_raw:
		for idx, url in enumerate(images_raw.split(','), start=1):
			url = url.strip()
			if url:
				local = download_image(url, 'cases/dev')
				DevCaseImage.objects.create(case=case, url=local, order=idx)

	return case, 'created' if created else 'updated'


def _make_block(case, order, block_type, fields):
	"""Создать блок кейса с заданными полями."""
	return CaseBlock.objects.create(
		case=case,
		block_type=block_type,
		order=order,
		is_visible=True,
		**fields,
	)


class Command(BaseCommand):
	help = 'Импорт кейсов из Google Sheets'

	def add_arguments(self, parser):
		parser.add_argument(
			'--dev',
			action='store_true',
			help='Импортировать только кейсы разработки (direction=dev)',
		)

	def handle(self, *args, **kwargs):
		# Файловый лог импорта — изолированно, не трогает глобальный logging сайта
		log_dir = settings.BASE_DIR / 'logs'
		log_dir.mkdir(exist_ok=True)
		if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
			fh = logging.FileHandler(log_dir / 'import_from_sheets.log', encoding='utf-8')
			fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
			logger.addHandler(fh)
		logger.setLevel(logging.INFO)

		dev_only = kwargs['dev']
		api_key  = settings.GOOGLE_API_KEY

		# Выбираем таблицу в зависимости от режима
		if dev_only:
			sheet_id = settings.GOOGLE_SHEET_ID_DEV
			if not sheet_id:
				self.stderr.write('GOOGLE_SHEET_ID_DEV не задан в .env')
				return
		else:
			sheet_id = settings.GOOGLE_SHEET_ID
			if not sheet_id:
				self.stderr.write('GOOGLE_SHEET_ID не задан в .env')
				return

		if not api_key:
			self.stderr.write('GOOGLE_API_KEY не задан в .env')
			return

		self.stdout.write('Загружаем данные из таблицы...')
		try:
			rows = fetch_sheet(api_key, sheet_id)
		except Exception as e:
			self.stderr.write(f'Ошибка при запросе к Sheets API: {e}')
			return

		self.stdout.write(f'Строк найдено: {len(rows)}')

		created = updated = skipped = 0
		for row in rows:
			try:
				# Транзакция на строку: кейс импортируется либо целиком, либо откатывается
				with transaction.atomic():
					_, status = import_row(row)
				if status == 'created':
					created += 1
				elif status == 'updated':
					updated += 1
				else:
					skipped += 1
			except Exception as e:
				slug = row.get('slug', '?')
				# Полный трейсбек уходит в файл лога — для поиска причины сбоя
				logger.error('Ошибка импорта кейса slug=%s: %s', slug, e, exc_info=True)
				self.stderr.write(f'Ошибка в строке slug={slug}: {e}')
				skipped += 1

		self.stdout.write(
			self.style.SUCCESS(
				f'Готово. Создано: {created}, обновлено: {updated}, пропущено: {skipped}'
			)
		)