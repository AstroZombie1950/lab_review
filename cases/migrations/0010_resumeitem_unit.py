from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('cases', '0009_caseblock_cta_image'),
	]

	operations = [
		migrations.AddField(
			model_name='resumeitem',
			name='unit',
			field=models.CharField(
				blank=True,
				max_length=100,
				verbose_name='Единица / уточнение',
				help_text='Отображается рядом с значением меньшим шрифтом. Пример: «месяца», «2022»'
			),
		),
	]