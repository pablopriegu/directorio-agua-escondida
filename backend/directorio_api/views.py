from .models import Comment
from .serializers import CommentSerializer
from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Provider, User, Rating
from .serializers import (
    CategorySerializer, ProviderSerializer, RegisterSerializer, RatingSerializer, ProviderCreateSerializer
)
import math

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # This permission allows anyone to view, but only admins to edit.
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return super().get_permissions()


class ProviderViewSet(viewsets.ModelViewSet):
    # This permission allows anyone to view, but only logged-in users to create/edit.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Provider.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return ProviderCreateSerializer
        return ProviderSerializer

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class RateProviderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ... (the rest of your RateProviderView code remains the same)
        provider = Provider.objects.get(pk=pk)
        if Rating.objects.filter(provider=provider, user=request.user).exists():
            return Response({"error": "Ya has calificado a este proveedor."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            multipliers = {'Muy bueno': 1.0, 'Bueno': 0.8, 'Regular': 0.4, 'Malo': 0.0}

            quality_score = 10 * multipliers[data['quality']]
            price_raw = 4 * multipliers[data['price']]
            comm_raw = 3 * multipliers[data['communication']]
            deadline_raw = 3 * multipliers[data['deadline']]

            price_score = math.floor(price_raw) if data['price'] == 'Bueno' else round(price_raw)
            comm_score = math.floor(comm_raw) if data['communication'] == 'Bueno' else round(comm_raw)
            deadline_score = math.floor(deadline_raw) if data['deadline'] == 'Bueno' else round(deadline_raw)

            total_score = quality_score + price_score + comm_score + deadline_score

            Rating.objects.create(
                provider=provider,
                user=request.user,
                quality_score=quality_score,
                price_score=price_score,
                communication_score=comm_score,
                deadline_score=deadline_score,
                total_score=total_score
            )
            return Response({"success": "Calificación enviada con éxito."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Filtra los comentarios por el ID del proveedor que viene en la URL
        provider_pk = self.kwargs.get('provider_pk')
        return Comment.objects.filter(provider_id=provider_pk, is_visible=True)

    def perform_create(self, serializer):
        provider = Provider.objects.get(pk=self.kwargs.get('provider_pk'))
        serializer.save(user=self.request.user, provider=provider)