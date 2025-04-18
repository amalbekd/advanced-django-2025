from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, AnalysisResultViewSet
from .views import ResumeAnalyzeView

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet)
router.register(r'analyses', AnalysisResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analyze/', ResumeAnalyzeView.as_view(), name='resume-analyze'),
]