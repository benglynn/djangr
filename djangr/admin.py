from django.contrib import admin
from djangr.models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'active')
    search_fields = ('title',)

admin.site.register(Photo, PhotoAdmin)