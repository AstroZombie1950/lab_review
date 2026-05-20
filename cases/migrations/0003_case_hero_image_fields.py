from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('cases', '0002_devcaseimage_devcase_casenondev'),
	]

	operations = [
		migrations.AddField(
			model_name='case',
			name='hero_image',
			field=models.URLField(
				verbose_name='Изображение в герое (URL)',
				blank=True,
				help_text='Скриншот или картинка для правой части героя. Если не заполнено — показывается стандартный дашборд.'
			),
		),
		migrations.AddField(
			model_name='case',
			name='hero_arrow_x',
			field=models.PositiveSmallIntegerField(
				verbose_name='Стрелка: позиция X (%)',
				blank=True,
				null=True,
				help_text='Горизонтальная позиция стрелки в процентах от ширины блока. Пример: 65'
			),
		),
		migrations.AddField(
			model_name='case',
			name='hero_arrow_y',
			field=models.PositiveSmallIntegerField(
				verbose_name='Стрелка: позиция Y (%)',
				blank=True,
				null=True,
				help_text='Вертикальная позиция стрелки в процентах от высоты блока. Пример: 40'
			),
		),
		migrations.AddField(
			model_name='case',
			name='hero_arrow_label',
			field=models.CharField(
				verbose_name='Подпись у стрелки',
				max_length=100,
				blank=True,
				help_text='Текст рядом со стрелкой. Пример: «10.44%»'
			),
		),
	]