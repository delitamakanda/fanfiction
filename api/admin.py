from django.contrib import admin

from api.models import FlatPages, Notification

class FlatPagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'created']
    search_fields = ['content', 'title']
    list_filter = ['updated', 'type']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created',)
    list_filter = ('created',)
    search_fields = ('verb',)


admin.site.register(FlatPages, FlatPagesAdmin)
admin.site.register(Notification, NotificationAdmin)
