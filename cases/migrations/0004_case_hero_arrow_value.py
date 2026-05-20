from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('cases', '0003_case_hero_image_fields'),
	]

	operations = [
		migrations.AddField(
			model_name='case',
			name='hero_arrow_value',
			field=models.CharField(
				verbose_name='Значение у стрелки (снизу)',
				max_length=100,
				blank=True,
				help_text='Текст под стрелкой. Пример: «10.44%»'
			),
		),
	]