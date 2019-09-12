from django.contrib import admin
from .models import *

# Register your models here.


#
class PersonDetailAdmin(admin.ModelAdmin):
    list_display = ('username', 'number', 'weight', 'age', 'gender', 'breed', 'feed','publish_date', 'special_case')
    readonly_fields = ('id', 'create_date')
    list_filter = ["number", "publish_date"]


admin.site.register(InfoFields, PersonDetailAdmin)


# @admin.register(InfoFields)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('username', 'number', 'weight', 'age', 'gender', 'breed', 'feed', 'special_case', 'publish_date', 'create_date')
#

