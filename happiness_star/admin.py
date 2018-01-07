from django.contrib import admin
from . import models

class TagInline(admin.TabularInline):
    model = models.Tag.star.through
    extra = 1

class StarAdmin(admin.ModelAdmin):

    list_display = ['date', 'user', 'overall']
    fieldsets = [
        ('Ownership', {'fields': ['date', 'user']}),
        ('Ratings', {'fields': ['spirit', 'exercise', 'work', 'play', 'friends',
                     'adventure']}),
    ]

    inlines = [TagInline]


admin.site.register(models.Star, StarAdmin)
admin.site.register(models.Tag)
