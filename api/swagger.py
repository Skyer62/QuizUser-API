from drf_yasg import openapi
from drf_yasg.views import get_schema_view

info = openapi.Info(
    title="QuizUser API",
    default_version='v1',
    description="API schema for QuizUser project",
)

schema_view = get_schema_view(
    info=info,
    public=True,
)
