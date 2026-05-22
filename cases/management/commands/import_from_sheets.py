import urllib.request
import urllib.parse
import json
import logging

from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from cases.models import (
	Case, Tag, CaseMetric, CaseBlock,
	ResumeItem, TaskItem, MetricItem, TeamMember,
	DevCaseImage,
)

logger = logging.getLogger(__name__)

# Фиксированный CTA для всех кейсов из таблицы
CTA_DEFAULTS = {
	'cta_title':    'Есть похожая задача?',
	'cta_text':     'Расскажите о проекте — обсудим и предложим решение.',
	'cta_btn_text': 'Написать',
	'cta_btn_url':  '#contact',
}


def fetch_sheet(api_key, sheet_id):
	"""Получить все строки из первого листа таблицы."""
	range_ = urllib.parse.quote('A:BV')
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


def get_or_create_tags(raw):
	"""Создать теги из строки через запятую, вернуть список."""
	tags = []
	for name in raw.split(','):
		name = name.strip()
		if name:
			tag, _ = Tag.objects.get_or_create(name=name)
			tags.append(tag)
	return tags


def import_row(row):
	"""Импортировать один кейс из строки таблицы."""
	slug = row.get('slug', '').strip()
	if not slug:
		logger.warning('Пропущена строка без slug')
		return None, 'skip'

	# Основные поля кейса
	defaults = {
		'title':            row.get('title', ''),
		'service':          row.get('service', ''),
		'direction':        row.get('direction', ''),
		'industry':         row.get('industry', ''),
		'description':      row.get('description', ''),
		'cover':            row.get('cover', ''),
		'hero_bg':          row.get('hero_bg', ''),
		'hero_image':       row.get('hero_image', ''),
		'hero_arrow_svg':   row.get('hero_arrow_svg', ''),
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
		label = row.get(f'resume_{i}_label', '').strip()
		value = row.get(f'resume_{i}_value', '').strip()
		if label or value:
			ResumeItem.objects.create(block=block, label=label, value=value, order=i)

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
		name = row.get(f'member_{i}_name', '').strip()
		role = row.get(f'member_{i}_role', '').strip()
		if name:
			TeamMember.objects.create(block=block, name=name, role=role, order=i)

	# Блок: CTA — фиксированный
	_make_block(case, order, 'cta', CTA_DEFAULTS)

	# Изображения ленты (только для dev-кейсов)
	case.dev_images.all().delete()
	images_raw = row.get('dev_images', '').strip()
	if images_raw:
		for idx, url in enumerate(images_raw.split(','), start=1):
			url = url.strip()
			if url:
				DevCaseImage.objects.create(case=case, url=url, order=idx)

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
				_, status = import_row(row)
				if status == 'created':
					created += 1
				elif status == 'updated':
					updated += 1
				else:
					skipped += 1
			except Exception as e:
				slug = row.get('slug', '?')
				logger.error('Ошибка импорта кейса slug=%s: %s', slug, e)
				self.stderr.write(f'Ошибка в строке slug={slug}: {e}')
				skipped += 1

		self.stdout.write(
			self.style.SUCCESS(
				f'Готово. Создано: {created}, обновлено: {updated}, пропущено: {skipped}'
			)
		)