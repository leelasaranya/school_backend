from rest_framework import serializers
from .models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    judge_name = serializers.CharField(
        source='judge.username',
        read_only=True
    )

    class Meta:
        model = Evaluation
        fields = [
            'id',
            'performance',
            'judge',
            'judge_name',
            'creativity',
            'technique',
            'presentation',
            'total_score',
            'feedback',
            'created_at'
        ]
        read_only_fields = ['judge', 'total_score', 'created_at']

