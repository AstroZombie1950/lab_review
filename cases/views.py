from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Case, Tag, DIRECTION_CHOICES


def cases_list(request):
	base_qs = Case.objects.filter(is_published=True).prefetch_related('tags')

	# Фильтр по направлению
	direction = request.GET.get('direction', '')
	industry  = request.GET.get('industry', '')
	tag       = request.GET.get('tag', '')
	search    = request.GET.get('search', '')

	# База для динамических списков — только по direction
	filtered_by_dir = base_qs.filter(direction=direction) if direction else base_qs

	# Отрасли и теги только из кейсов текущего направления
	all_industries = (
		filtered_by_dir
		.exclude(industry='')
		.values_list('industry', flat=True)
		.distinct()
		.order_by('industry')
	)
	all_tags = (
		Tag.objects
		.filter(case__in=filtered_by_dir, case__is_published=True)
		.distinct()
		.order_by('name')
	)

	# Применяем остальные фильтры к итоговой выборке
	cases = filtered_by_dir
	if industry:
		cases = cases.filter(industry=industry)
	if tag:
		cases = cases.filter(tags__slug=tag)
	if search:
		# SQLite не умеет icontains для кириллицы — ищем по обоим регистрам
		s = search.strip()
		cases = cases.filter(
			Q(title__icontains=s) |
			Q(title__icontains=s.lower()) |
			Q(title__icontains=s.upper()) |
			Q(title__icontains=s.capitalize())
		)

	# Имя выбранного тега для кнопки дропдауна
	selected_tag_name = ''
	if tag:
		try:
			selected_tag_name = Tag.objects.get(slug=tag).name
		except Tag.DoesNotExist:
			pass

	context = {
		'cases':              cases,
		'all_tags':           all_tags,
		'all_industries':     list(all_industries),
		'direction_choices':  DIRECTION_CHOICES,
		'selected_direction': direction,
		'selected_industry':  industry,
		'selected_tag':       tag,
		'selected_tag_name':  selected_tag_name,
		'search':             search,
	}
	return render(request, 'cases/list.html', context)


def web_dev_redirect(request):
	"""Редирект /cases/web-dev/ → /cases/?direction=dev"""
	return redirect('/cases/?direction=dev', permanent=True)


def case_detail(request, slug):
	case = get_object_or_404(
		Case.objects.prefetch_related(
			'content_blocks__resume_items',
			'content_blocks__task_items',
			'content_blocks__metric_items',
			'content_blocks__team_members',
			'tags',
		).select_related(),
		slug=slug,
		is_published=True,
	)
	# Dev-кейсы открываются в своём шаблоне
	if case.direction == 'dev':
		sidebar_cases = (
			Case.objects
			.filter(is_published=True, direction='dev')
			.exclude(pk=case.pk)
			.only('title', 'slug', 'service')
		)
		return render(request, 'cases/detail_dev.html', {
			'case': case,
			'sidebar_cases': sidebar_cases,
		})
	return render(request, 'cases/detail.html', {'case': case})