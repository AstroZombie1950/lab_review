from django.db import migrations
import django.db.models.fields.files


class Migration(migrations.Migration):

	dependencies = [
		('cases', '0011_resumeitem_value_blank'),
	]

	operations = [
		migrations.AlterField(
			model_name='employee',
			name='photo',
			field=django.db.models.fields.files.ImageField(
				blank=True,
				help_text='Загрузите фото сотрудника. Рекомендуется квадратное, минимум 200×200 px.',
				upload_to='employees/',
				verbose_name='Фото',
			),
		),
	]