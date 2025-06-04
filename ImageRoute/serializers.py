from rest_framework import serializers
from .models import Route, RoutePoint

class RoutePointSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())

    class Meta:
        model = RoutePoint
        fields = ['id', 'x', 'y', 'order', 'route']

class RouteSerializer(serializers.ModelSerializer):
    points = RoutePointSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'name', 'background', 'points']