from django.contrib import admin


from .models import Issue, Message

admin.site.register(Message)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("title", 'user', 'date_time', 'priority', 'status')
