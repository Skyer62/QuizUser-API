from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

QUESTION_TYPES = (
    ('text_field', 'Ответ текстом'),
    ('radio', 'Один вариант'),
    ('check_boxes', 'Выбор нескольких вариантов'),
)


class Quiz(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    start_date = models.DateField(
        auto_now_add=True, verbose_name='Дата старта')
    end_date = models.DateField(verbose_name='Дата окончания')
    description = models.CharField(max_length=200, verbose_name='Описаниние')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    text = models.TextField(verbose_name='Текст вопроса')
    type_question = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        verbose_name='Тип вопроса',
    )
    quiz = models.ForeignKey(
        Quiz, blank=True, on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Опрос'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    name = models.TextField(verbose_name='Вариант ответа')
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name='Вопрос'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


class Answer(models.Model):
    uuid = models.UUIDField(
        editable=False, null=True, verbose_name='Уникальный идентификатор')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    many_choice = models.ManyToManyField(Choice, verbose_name='Ответ выбором')
    one_choice = models.ForeignKey(
        Choice,
        null=True,
        on_delete=models.CASCADE,
        related_name='answers_one_choice',
        verbose_name='Выбранный ответ'
    )
    self_text = models.TextField(null=True, verbose_name='Ответ текстом')

    def many_choices(self):
        return ','.join([str(p) for p in self.many_choice.all()])

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
