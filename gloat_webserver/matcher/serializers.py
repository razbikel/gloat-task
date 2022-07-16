from abc import ABC

from rest_framework import serializers
from .models import Skill, Candidate


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name"]


class CandidateSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = ["title", "id", "skills"]
