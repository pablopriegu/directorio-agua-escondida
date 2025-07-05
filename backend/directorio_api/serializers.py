from rest_framework import serializers
from .models import Category, Provider, Comment, User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'user', 'body', 'created_at')

# ESTA ES LA CLASE IMPORTANTE
class ProviderSerializer(serializers.ModelSerializer):
    # Estas líneas leen los valores calculados de tu modelo
    global_rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    # Esto muestra el nombre de la categoría, no solo su ID
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Provider
        # Esta lista define todos los campos que se enviarán
        fields = ('id', 'name', 'phone', 'location', 'category', 'global_rating', 'rating_count')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'phone_number')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', "")
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

class RatingSerializer(serializers.Serializer):
    CHOICES = [('Muy bueno', 'Muy bueno'), ('Bueno', 'Bueno'), ('Regular', 'Regular'), ('Malo', 'Malo')]
    quality = serializers.ChoiceField(choices=CHOICES)
    price = serializers.ChoiceField(choices=CHOICES)
    communication = serializers.ChoiceField(choices=CHOICES)
    deadline = serializers.ChoiceField(choices=CHOICES)

class ProviderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('name', 'phone', 'location', 'category')
