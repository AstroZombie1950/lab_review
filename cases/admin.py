from django.contrib import admin
from .models import Case, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
	# Список кейсов
	list_display = ['title', 'service', 'direction', 'industry', 'is_published', 'created_at']
	list_filter = ['direction', 'service', 'is_published']
	search_fields = ['title', 'description']
	prepopulated_fields = {'slug': ('title',)}
	filter_horizontal = ['tags']

	# Группировка полей в форме редактирования
	fieldsets = [
		('Основное', {
			'fields': ['title', 'slug', 'service', 'direction', 'industry', 'tags', 'is_published']
		}),
		('Карточка в списке', {
			'fields': ['description', 'cover', 'metrics']
		}),
		('Внутренняя страница', {
			'fields': ['blocks']
		}),
		('SEO', {
			'fields': ['meta_title', 'meta_description'],
			'classes': ['collapse']
		}),
	]