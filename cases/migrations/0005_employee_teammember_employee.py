from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

	dependencies = [
		('cases', '0004_case_hero_arrow_value'),
	]

	operations = [
		# Новая модель сотрудника
		migrations.CreateModel(
			name='Employee',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('name', models.CharField(max_length=100, verbose_name='Имя', help_text='Пример: «Иван Петров»')),
				('role', models.CharField(max_length=150, verbose_name='Роль', help_text='Пример: «SEO-специалист»')),
				('photo', models.URLField(blank=True, verbose_name='Фото (URL)', help_text='Ссылка на фото сотрудника. Рекомендуется квадратное, минимум 200×200 px.')),
			],
			options={
				'verbose_name': 'Сотрудник',
				'verbose_name_plural': 'Сотрудники',
				'ordering': ['name'],
			},
		),
		# FK на Employee в TeamMember
		migrations.AddField(
			model_name='teammember',
			name='employee',
			field=models.ForeignKey(
				blank=True,
				null=True,
				on_delete=django.db.models.deletion.SET_NULL,
				to='cases.employee',
				verbose_name='Сотрудник из базы',
				help_text='Выберите сотрудника — имя, роль и фото подтянутся автоматически. Или заполните вручную ниже.'
			),
		),
		# name и role теперь необязательные
		migrations.AlterField(
			model_name='teammember',
			name='name',
			field=models.CharField(blank=True, max_length=100, verbose_name='Имя (вручную)', help_text='Заполняется автоматически из базы сотрудников. Можно переопределить вручную.'),
		),
		migrations.AlterField(
			model_name='teammember',
			name='role',
			field=models.CharField(blank=True, max_length=150, verbose_name='Роль (вручную)', help_text='Заполняется автоматически из базы сотрудников. Можно переопределить вручную.'),
		),
	]