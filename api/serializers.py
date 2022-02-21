from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Note
from django.contrib.auth.models import User


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
    


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['username'] = user.username
        # ...

        return token

class UserSeriliazer(ModelSerializer):
    class Meta:
        model = User 
        fields = "__all__"
    
    def create(self, validated_data):   
        user = User(first_name=validated_data.get("first_name"),
                    last_name=validated_data.get("last_name"),
                    username=validated_data.get("username"),
                    email=validated_data.get("email"))
        user.set_password(validated_data.get("password"))
        user.save()

        return user