from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('cases', '0013_employee_photo_imagefield'),
	]

	operations = [
		# value → text
		migrations.RenameField(
			model_name='resumeitem',
			old_name='value',
			new_name='text',
		),
		# Порядок для text (дефолт 2 — после крупного)
		migrations.AddField(
			model_name='resumeitem',
			name='text_order',
			field=models.PositiveSmallIntegerField(
				default=2,
				help_text='Позиция в строке: 1, 2 или 3',
				verbose_name='Порядок текста',
			),
		),
		# Порядок для unit (дефолт 1 — первым)
		migrations.AddField(
			model_name='resumeitem',
			name='unit_order',
			field=models.PositiveSmallIntegerField(
				default=1,
				help_text='Позиция в строке: 1, 2 или 3',
				verbose_name='Порядок значения',
			),
		),
		# Доп. мелкий текст
		migrations.AddField(
			model_name='resumeitem',
			name='text_add',
			field=models.CharField(
				blank=True,
				help_text='Необязательно. Мелкий шрифт. Пример: «2022», «года»',
				max_length=100,
				verbose_name='Доп. текст (мелкий)',
			),
		),
		# Порядок для text_add (дефолт 3 — последним)
		migrations.AddField(
			model_name='resumeitem',
			name='text_add_order',
			field=models.PositiveSmallIntegerField(
				default=3,
				help_text='Позиция в строке: 1, 2 или 3',
				verbose_name='Порядок доп. текста',
			),
		),
		# verbose_name у label
		migrations.AlterField(
			model_name='resumeitem',
			name='label',
			field=models.CharField(
				help_text='Пример: «Старт работ», «Сдача проекта», «Длительность»',
				max_length=100,
				verbose_name='Заголовок',
			),
		),
		# verbose_name у unit
		migrations.AlterField(
			model_name='resumeitem',
			name='unit',
			field=models.CharField(
				blank=True,
				help_text='Крупный шрифт. Пример: «2,5», «топ-3»',
				max_length=100,
				verbose_name='Значение (крупное)',
			),
		),
	]