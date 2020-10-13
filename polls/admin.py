"""Admin setup for poll application."""
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Settings for Choice display in admin page."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Question form setting for admin page."""

    fieldssets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Ending date information', {'fields': ['end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'end_date', 'is_poll_end')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
