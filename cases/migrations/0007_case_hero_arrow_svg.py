from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		# На сервере есть merge 0006, локально последняя — 0005
		('cases', '0005_employee_teammember_employee'),
	]

	operations = [
		# Убираем старые поля стрелки
		migrations.RemoveField(model_name='case', name='hero_arrow_x'),
		migrations.RemoveField(model_name='case', name='hero_arrow_y'),
		migrations.RemoveField(model_name='case', name='hero_arrow_label'),
		migrations.RemoveField(model_name='case', name='hero_arrow_value'),
		# Добавляем новое поле SVG-слоя
		migrations.AddField(
			model_name='case',
			name='hero_arrow_svg',
			field=models.URLField(
				blank=True,
				verbose_name='Стрелка поверх (SVG, URL)',
				help_text='SVG с прозрачным фоном того же размера, что и основное изображение. Накладывается поверх. Если не заполнено — стрелка не показывается.'
			),
		),
	]