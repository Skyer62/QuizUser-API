from django.contrib import admin

from .models import Answer, Choice, Question, Quiz


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'description')
    search_fields = ('name',)
    list_filter = ('start_date',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'type_question', 'quiz',)
    search_fields = ('text',)
    list_filter = ('text',)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'question',)
    search_fields = ('name',)
    list_filter = ('name',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'uuid', 'question', 'many_choices',
                    'one_choice', 'self_text')
    search_fields = ('author__username',)
    list_filter = ('question',)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
