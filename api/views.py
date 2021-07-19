from rest_framework import viewsets, mixins, permissions
from rest_framework.generics import get_object_or_404
from api.models import Quiz, Question, Answer, Choice
from api.serializers import (
    QuizSerializer, QuestionSerializer, AnswerSerializer,
    UserQuizSerializer, AnswerOneTextSerializer,
    AnswerOneChoiceSerializer, AnswerMultipleChoiceSerializer,
    ChoiceSerializer,
)
from datetime import datetime
import uuid

UUID4 = uuid.uuid4()


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (permissions.IsAdminUser,)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        quiz = get_object_or_404(Quiz, id=self.kwargs['id'])
        return quiz.questions.all()

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['id'])
        serializer.save(quiz=quiz)


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question,
            pk=self.kwargs['question_pk'],
            quiz__id=self.kwargs['id'],
        )
        serializer.save(question=question)

    def get_queryset(self):
        question = get_object_or_404(Question, id=self.kwargs['question_pk'])
        return question.choices.all()


class ActiveQuizListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Quiz.objects.filter(end_date__gte=datetime.today())
    serializer_class = QuizSerializer
    permission_classes = (permissions.AllowAny,)


class AnswerCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        question = get_object_or_404(
            Question,
            pk=self.kwargs['question_pk'],
            quiz__id=self.kwargs['id'],
        )
        if question.type_question == 'text_field':
            return AnswerOneTextSerializer
        elif question.type_question == 'radio':
            return AnswerOneChoiceSerializer
        else:
            return AnswerMultipleChoiceSerializer

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question,
            pk=self.kwargs['question_pk'],
            quiz__id=self.kwargs['id'],
        )
        if self.request.user.is_anonymous:
            serializer.save(uuid=UUID4, question=question)
        else:
            serializer.save(author=self.request.user, question=question)


class UserIdQuizListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserQuizSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_anonymous:
            queryset = Quiz.objects.exclude(questions__answers__uuid=UUID4)
        else:
            queryset = Quiz.objects.exclude(
                questions__answers__author__id=user_id)
        return queryset
