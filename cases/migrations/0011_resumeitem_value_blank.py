from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('cases', '0010_resumeitem_unit'),
	]

	operations = [
		migrations.AlterField(
			model_name='resumeitem',
			name='value',
			field=models.CharField(
				blank=True,
				max_length=100,
				verbose_name='Значение',
				help_text='Число или текст. Пример: «2,5», «январь»'
			),
		),
	]