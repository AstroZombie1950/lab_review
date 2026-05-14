from django.shortcuts import render, get_object_or_404, redirect
from .models import Case, Tag, DIRECTION_CHOICES


def cases_list(request):
	cases = Case.objects.filter(is_published=True).prefetch_related('tags')

	# Фильтр по направлению
	direction = request.GET.get('direction')
	if direction:
		cases = cases.filter(direction=direction)

	# Фильтр по отрасли
	industry = request.GET.get('industry')
	if industry:
		cases = cases.filter(industry=industry)

	# Фильтр по тегу
	tag = request.GET.get('tag')
	if tag:
		cases = cases.filter(tags__slug=tag)

	# Поиск по названию
	search = request.GET.get('search')
	if search:
		cases = cases.filter(title__icontains=search)

	all_tags = Tag.objects.all()
	all_industries = (
		Case.objects
		.filter(is_published=True)
		.values_list('industry', flat=True)
		.distinct()
	)

	# Имя выбранного тега для кнопки
	selected_tag_name = ''
	if tag:
		try:
			selected_tag_name = Tag.objects.get(slug=tag).name
		except Tag.DoesNotExist:
			pass

	context = {
		'cases': cases,
		'all_tags': all_tags,
		'all_industries': [i for i in all_industries if i],
		'direction_choices': DIRECTION_CHOICES,
		'selected_direction': direction,
		'selected_industry': industry,
		'selected_tag': tag,
		'selected_tag_name': selected_tag_name,
		'search': search or '',
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
		# Сайдбар: все другие опубликованные dev-кейсы
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