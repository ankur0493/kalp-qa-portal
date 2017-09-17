from rest_framework import serializers

from qas.models import Question, Answer


class BaseSerializer(serializers.Serializer):
    user_id = serializers.CharField( source="user.id" )
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.first_name + obj.user.last_name

    class Meta:
        abstract = True


class AnswerSerializer(BaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('body', 'user_id', 'user_name')

class QuestionSerializer(BaseSerializer, serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'user_id','user_name', 'answers' )
