from django.db import migrations


SLUGS = [
	'avito-ads',
	'avito-day',
	'avito-consult',
	'avito-autoload',
	'website',
	'internet-shop',
	'landing',
	'html-css',
	'seo-setup',
	'seo-full',
	'seo-top',
	'yandex-direct',
]


def create_service_pages(apps, schema_editor):
	ServicePage = apps.get_model('services', 'ServicePage')
	for slug in SLUGS:
		ServicePage.objects.get_or_create(slug=slug)


def delete_service_pages(apps, schema_editor):
	ServicePage = apps.get_model('services', 'ServicePage')
	ServicePage.objects.filter(slug__in=SLUGS).delete()


class Migration(migrations.Migration):

	dependencies = [
		('services', '0001_initial'),
	]

	operations = [
		migrations.RunPython(create_service_pages, delete_service_pages),
	]