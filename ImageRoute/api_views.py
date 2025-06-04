from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Route, RoutePoint
from .serializers import RouteSerializer, RoutePointSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RouteListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(operation_summary="Lista tras użytkownika")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Utwórz nową trasę")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RouteDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

    @swagger_auto_schema(operation_summary="Pobierz szczegóły trasy")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Usuń trasę")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class RoutePointListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Pobierz punkty trasy")
    def get(self, request, route_id):
        route = get_object_or_404(Route, id=route_id, user=request.user)
        points = route.points.all()
        serializer = RoutePointSerializer(points, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Dodaj punkt do trasy",
        request_body=RoutePointSerializer,
        responses={201: RoutePointSerializer}
    )
    def post(self, request, route_id):
        route = get_object_or_404(Route, id=route_id, user=request.user)
        # print(route.id)
        data = request.data.copy()
        data['route'] = route.id
        data['order'] = route.points.count() + 1
        # print(data)
        serializer = RoutePointSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RoutePointDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Usuń punkt z trasy")
    def delete(self, request, route_id, point_id):
        route = get_object_or_404(Route, id=route_id, user=request.user)
        point = get_object_or_404(RoutePoint, id=point_id, route=route)
        point.delete()
        return Response(status=204)
