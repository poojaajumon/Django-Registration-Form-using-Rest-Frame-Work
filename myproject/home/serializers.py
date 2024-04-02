#serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PhoneNumber
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number']



class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            'password1': {'write_only': True},
            'password2': {'write_only': True},
        }

    def create(self, validated_data):
        phone_number_data = validated_data.pop('phone_number')
        password = validated_data.pop('password')  # Get the password from validated_data
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()  # Save the user
        PhoneNumber.objects.create(user=user, **phone_number_data)

        self.send_welcome_email(user.email, user.username)
        return user
    
   
    
    def send_welcome_email(self, email, username):
        subject = 'Welcome to Our Platform!'
        html_message = render_to_string('index.html', {'username': username})
        plain_message = strip_tags(html_message)
        from_email = ''  # Change this to your email address
        recipient_list = [email]

        # Create the email object with HTML content
        email_message = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
        email_message.attach_alternative(html_message, "text/html")  # Attach HTML content
        email_message.send()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the input data.
        """
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        # Attach the authenticated user to the serializer instance for later use
        self.user = user

        return data

    def to_representation(self, instance):
        """
        Return the authenticated user instance.
        """
        return {'user': self.user.username, 'id': self.user.id}







