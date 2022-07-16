from django.urls import path
from .views import (
    FindCandidateApiView, AddCandidateApiView, AddSkillApiView, AddJobApiView
)

urlpatterns = [
    path('find-candidate', FindCandidateApiView.as_view()),
    path('add-candidate', AddCandidateApiView.as_view()),
    path('add-skill', AddSkillApiView.as_view()),
    path('add-job', AddJobApiView.as_view()),
]
