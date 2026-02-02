from rest_framework import serializers

class LeaderboardSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    student = serializers.CharField()
    school = serializers.CharField()
    performance_title = serializers.CharField()
    jury_avg = serializers.FloatField()
    votes = serializers.IntegerField()
    final_score = serializers.FloatField()

