from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Question, Category, Choice


# @admin.register(Question)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('question', 'id', 'slug')
#     prepopulated_fields = {'slug': ('question',), }


# admin.site.register(User)
admin.site.register(Category)
admin.site.register(Choice)
admin.site.register(Question)



