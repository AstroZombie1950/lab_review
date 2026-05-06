from django.shortcuts import render, get_object_or_404
from .models import Case, Tag, SERVICE_CHOICES


def cases_list(request):
	cases = Case.objects.filter(is_published=True).prefetch_related('tags')

	# Фильтр по услуге
	service = request.GET.get('service')
	if service:
		cases = cases.filter(service=service)

	industry = request.GET.get('industry')
	if industry:
		cases = cases.filter(industry=industry)

	tag = request.GET.get('tag')
	if tag:
		cases = cases.filter(tags__slug=tag)

	search = request.GET.get('search')
	if search:
		cases = cases.filter(title__icontains=search)

	all_tags = Tag.objects.all()
	all_industries = Case.objects.filter(is_published=True).values_list('industry', flat=True).distinct()

	# Имя выбранного тега для отображения в кнопке
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
		'service_choices': SERVICE_CHOICES,
		'selected_service': service,
		'selected_industry': industry,
		'selected_tag': tag,
		'selected_tag_name': selected_tag_name,
		'search': search or '',
	}
	return render(request, 'cases/list.html', context)


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
	return render(request, 'cases/detail.html', {'case': case})