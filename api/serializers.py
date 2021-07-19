from rest_framework import serializers
from api.models import Quiz, Question, Answer, Choice


"""Опросы"""


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Quiz


"""Варианты ответов"""


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Choice


"""Вопросы"""


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Question


"""Ответа пользователей"""


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Answer


"""Вопросы с ответами пользователей"""


class QuestionListSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        fields = ['text', 'answers']
        model = Question

    def get_answers(self, question):
        author_id = self.context.get('request').user.id
        answers = Answer.objects.filter(
            question=question, author__id=author_id)
        serializer = AnswerSerializer(instance=answers, many=True)
        return serializer.data


"""Опросы с вопросами и ответами пользователей"""


class UserQuizSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Quiz


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        question_id = self.context.get('request').parser_context['kwargs'][
            'question_pk']
        request = self.context.get('request', None)
        queryset = super(UserFilteredPrimaryKeyRelatedField,
                         self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(question_id=question_id)


"""Ответ текстом"""


class AnswerOneTextSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['self_text']
        model = Answer


"""Выбор одного варианта ответа"""


class AnswerOneChoiceSerializer(serializers.ModelSerializer):
    one_choice = UserFilteredPrimaryKeyRelatedField(
        many=False,
        queryset=Choice.objects.all()
    )

    class Meta:
        fields = ['one_choice']
        model = Answer


"""Выбор нескольких вариантов ответа"""


class AnswerMultipleChoiceSerializer(serializers.ModelSerializer):
    many_choice = UserFilteredPrimaryKeyRelatedField(
        many=True,
        queryset=Choice.objects.all()
    )

    class Meta:
        fields = ['many_choice']
        model = Answer
