from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('cases', '0008_alter_case_cover_alter_case_hero_bg_and_more'),
	]

	operations = [
		migrations.AddField(
			model_name='caseblock',
			name='cta_image',
			field=models.URLField(
				blank=True,
				verbose_name='Изображение CTA (URL)',
				help_text='Картинка в левой части CTA-блока. Необязательное поле.'
			),
		),
	]