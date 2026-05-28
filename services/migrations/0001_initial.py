from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

	initial = True

	dependencies = [
		('cases', '0014_resumeitem_refactor'),
	]

	operations = [
		migrations.CreateModel(
			name='ServicePage',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('slug', models.CharField(
					choices=[
						('avito-ads',      'Авито — Ведение рекламы'),
						('avito-day',      'Авито — Авитолог на день'),
						('avito-consult',  'Авито — Консультация'),
						('avito-autoload', 'Авито — Автозагрузка'),
						('website',        'Разработка сайта'),
						('internet-shop',  'Разработка интернет-магазина'),
						('landing',        'Разработка лендинга'),
						('html-css',       'Вёрстка по макету'),
						('seo-setup',      'SEO — Внутренняя настройка'),
						('seo-full',       'SEO — Под ключ'),
						('seo-top',        'SEO — Вывод в топ'),
						('yandex-direct',  'Яндекс Директ'),
					],
					max_length=50,
					unique=True,
					verbose_name='Страница услуги',
				)),
			],
			options={
				'verbose_name': 'Страница услуги',
				'verbose_name_plural': 'Страницы услуг',
				'ordering': ['slug'],
			},
		),
		migrations.CreateModel(
			name='ServicePageEmployee',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
				('employee', models.ForeignKey(
					on_delete=django.db.models.deletion.CASCADE,
					to='cases.employee',
					verbose_name='Сотрудник',
				)),
				('service_page', models.ForeignKey(
					on_delete=django.db.models.deletion.CASCADE,
					to='services.servicepage',
					verbose_name='Страница',
				)),
			],
			options={
				'verbose_name': 'Сотрудник на странице',
				'verbose_name_plural': 'Сотрудники на странице',
				'ordering': ['order', 'employee__name'],
			},
		),
		migrations.AddField(
			model_name='servicepage',
			name='employees',
			field=models.ManyToManyField(
				blank=True,
				through='services.ServicePageEmployee',
				to='cases.employee',
				verbose_name='Сотрудники',
			),
		),
		migrations.AlterUniqueTogether(
			name='servicepageemployee',
			unique_together={('service_page', 'employee')},
		),
	]