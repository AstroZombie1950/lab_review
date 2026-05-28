from django.contrib import admin
from .models import ServicePage, ServicePageEmployee


class ServicePageEmployeeInline(admin.TabularInline):
	model = ServicePageEmployee
	extra = 1
	fields = ('employee', 'order')
	autocomplete_fields = ('employee',)
	ordering = ('order',)


@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'employee_count')
	inlines = (ServicePageEmployeeInline,)

	def employee_count(self, obj):
		return obj.employees.count()
	employee_count.short_description = 'Сотрудников'