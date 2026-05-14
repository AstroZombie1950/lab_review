from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

	dependencies = [
		('cases', '0001_initial'),
	]

	operations = [

		# Прокси-модель для кейсов разработки
		migrations.CreateModel(
			name='DevCase',
			fields=[],
			options={
				'verbose_name': 'Кейс по веб-разработке',
				'verbose_name_plural': 'Кейсы по веб-разработке',
				'proxy': True,
				'indexes': [],
				'constraints': [],
			},
			bases=('cases.case',),
		),

		# Прокси-модель для остальных кейсов
		migrations.CreateModel(
			name='CaseNonDev',
			fields=[],
			options={
				'verbose_name': 'Кейс (Авито / СЕО / Директ)',
				'verbose_name_plural': 'Кейсы (Авито, СЕО, Директ)',
				'proxy': True,
				'indexes': [],
				'constraints': [],
			},
			bases=('cases.case',),
		),

		# Модель изображений ленты
		migrations.CreateModel(
			name='DevCaseImage',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('url', models.URLField(
					verbose_name='URL изображения',
					help_text='Прямая ссылка на изображение. Пример: https://example.com/screen1.jpg',
				)),
				('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
				('case', models.ForeignKey(
					on_delete=django.db.models.deletion.CASCADE,
					related_name='dev_images',
					to='cases.case',
					verbose_name='Кейс',
				)),
			],
			options={
				'verbose_name': 'Изображение',
				'verbose_name_plural': 'Изображения (лента)',
				'ordering': ['order'],
			},
		),
	]