from rest_framework import serializers
from .models import Filterlog, Roles



class AllFilterLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filterlog
        fields = '__all__'



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class LogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filterlog
        fields = ['is_know', 'id']
