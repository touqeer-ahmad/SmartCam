from myapp.models import Mode, Action
from rest_framework import serializers

class ModeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mode
        fields = ('url', 'name')

class ActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Action
        fields = ('url', 'name')
