from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api import views

from .swagger import schema_view

router = DefaultRouter()

router.register('active_quizzes', views.ActiveQuizListViewSet)
router.register(
    'my_quizzes',
    views.UserIdQuizListViewSet,
    basename='list_userid_quizs'
)
router.register(
    'quizzes/(?P<id>\d+)/questions',
    views.QuestionViewSet,
    basename='questions'
)
router.register(
    'quizzes/(?P<id>\d+)/questions/(?P<question_pk>\d+)/choices',
    views.ChoiceViewSet,
    basename='choices'
)
router.register(
    'quizzes/(?P<id>\d+)/questions/(?P<question_pk>\d+)/answers',
    views.AnswerCreateViewSet,
    basename='answers'
)
router.register('quizzes', views.QuizViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    url(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]
