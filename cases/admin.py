import nested_admin
from django.contrib import admin
from .models import Case, Tag, CaseBlock, CaseMetric, ResumeItem, TaskItem, MetricItem, TeamMember


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}


# ── Метрики карточки кейса ────────────────────────────────────────────────────

class CaseMetricInline(nested_admin.NestedTabularInline):
	model = CaseMetric
	extra = 0
	fields = ['value', 'label', 'order']


# ── Вложенные инлайны для блоков ─────────────────────────────────────────────

class ResumeItemInline(nested_admin.NestedTabularInline):
	model = ResumeItem
	extra = 1
	fields = ['label', 'value', 'order']
	verbose_name_plural = 'Резюме проекта (строки)'


class TaskItemInline(nested_admin.NestedTabularInline):
	model = TaskItem
	extra = 1
	fields = ['title', 'text', 'order']
	verbose_name_plural = 'Карточки задач'


class MetricItemInline(nested_admin.NestedTabularInline):
	model = MetricItem
	extra = 1
	fields = ['value', 'unit', 'label', 'order']
	verbose_name_plural = 'Показатели'


class TeamMemberInline(nested_admin.NestedTabularInline):
	model = TeamMember
	extra = 1
	fields = ['name', 'role', 'order']
	verbose_name_plural = 'Участники команды'


# ── Блоки кейса с вложенными инлайнами ───────────────────────────────────────

class CaseBlockInline(nested_admin.NestedStackedInline):
	model = CaseBlock
	extra = 0
	ordering = ['order']

	# Каждый тип блока получает свои вложенные инлайны
	inlines = [ResumeItemInline, TaskItemInline, MetricItemInline, TeamMemberInline]

	class Media:
		js = ('cases/js/case_block_admin.js',)

	fieldsets = [

		('Настройки блока', {
			'fields': ['is_visible', 'block_type', 'order'],
		}),

		('Вводный текст', {
			'fields': ['intro_text'],
			'classes': ['block-section-intro'],
			'description': 'Крупный вступительный абзац сразу после героя страницы.',
		}),

		('Задача и резюме', {
			'fields': ['task_text'],
			'classes': ['block-section-task_resume'],
			'description': 'Левый блок — задача заказчика. Правый блок — строки резюме ниже.',
		}),

		('Сетка задач', {
			'fields': ['tasks_title'],
			'classes': ['block-section-tasks_grid'],
			'description': 'Заголовок над сеткой карточек. Сами карточки — ниже через «Карточки задач».',
		}),

		('Контент на всю ширину', {
			'fields': [
				'cf_label', 'cf_title',
				'cf_text_main', 'cf_text_secondary',
				'cf_image', 'cf_link_text', 'cf_link_url',
			],
			'classes': ['block-section-content_full'],
			'description': 'Текст слева, картинка справа. Картинка необязательна.',
		}),

		('Две колонки — левая', {
			'fields': [
				'left_label', 'left_title',
				'left_text_main', 'left_text_secondary',
				'left_link_text', 'left_link_url',
			],
			'classes': ['block-section-content_two'],
			'description': 'Левая колонка двухколоночного блока.',
		}),

		('Две колонки — правая', {
			'fields': [
				'right_label', 'right_title',
				'right_text_main', 'right_text_secondary',
				'right_link_text', 'right_link_url',
			],
			'classes': ['block-section-content_two'],
		}),

		('Результаты / цифры', {
			'fields': ['metrics_title', 'metrics_subtitle'],
			'classes': ['block-section-metrics'],
			'description': 'Заголовок и подзаголовок. Сами цифры — ниже через «Показатели».',
		}),

		('Команда', {
			'fields': [],
			'classes': ['block-section-team'],
			'description': 'Участников добавьте ниже через «Участники команды».',
		}),

		('Призыв к действию (CTA)', {
			'fields': ['cta_title', 'cta_text', 'cta_btn_text', 'cta_btn_url'],
			'classes': ['block-section-cta'],
			'description': 'Финальный блок страницы с кнопкой.',
		}),
	]


# ── Страница кейса ────────────────────────────────────────────────────────────

@admin.register(Case)
class CaseAdmin(nested_admin.NestedModelAdmin):
	list_display = ['title', 'service', 'direction', 'industry', 'published_at', 'is_published']
	list_filter = ['direction', 'service', 'is_published']
	search_fields = ['title', 'description']
	prepopulated_fields = {'slug': ('title',)}
	filter_horizontal = ['tags']
	inlines = [CaseMetricInline, CaseBlockInline]

	fieldsets = [
		('Основное', {
			'fields': ['title', 'slug', 'service', 'direction', 'industry', 'tags', 'is_published', 'published_at'],
			'description': (
				'<div style="background:#7a4f00;border:1px solid #b87300;border-radius:6px;padding:14px 16px;margin-bottom:8px;font-size:13px;line-height:1.7;color:#ffe8b0">'
				'<strong style="color:#fff">Заголовок</strong> — короткое название проекта для карточки и страницы.<br>'
				'<strong style="color:#fff">URL (slug)</strong> — заполняется автоматически, можно изменить вручную.<br>'
				'<strong style="color:#fff">Услуга</strong> — что именно было сделано для клиента.<br>'
				'<strong style="color:#fff">Направление</strong> — категория кейса (SEO, Директ и т.д.).<br>'
				'<strong style="color:#fff">Дата публикации</strong> — определяет порядок в списке. Подставляется автоматически.<br>'
				'<strong style="color:#fff">Опубликован</strong> — пока галочка не стоит, кейс не виден на сайте.'
				'</div>'
			)
		}),
		('Карточка в списке кейсов', {
			'fields': ['description', 'cover'],
			'description': (
				'<div style="background:#7a4f00;border:1px solid #b87300;border-radius:6px;padding:14px 16px;margin-bottom:8px;font-size:13px;line-height:1.7;color:#ffe8b0">'
				'Метрики карточки добавляются ниже через блок «Метрики».<br>'
				'<strong style="color:#fff">Описание</strong> — 1–2 предложения о проекте.<br>'
				'<strong style="color:#fff">Обложка</strong> — фото для карточки, рекомендуется 1200×800 px.'
				'</div>'
			)
		}),
		('Герой страницы кейса', {
			'fields': ['hero_bg', 'client_url', 'year'],
		}),
		('SEO', {
			'fields': ['meta_title', 'meta_description'],
			'description': 'Если оставить пустым — используются заголовок и описание из раздела «Основное».',
		}),
	]

	class Media:
		js = ('cases/js/case_block_admin.js',)
		css = {'all': ('cases/css/case_block_admin.css',)}