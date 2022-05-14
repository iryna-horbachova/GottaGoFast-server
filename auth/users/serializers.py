from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import User, Client, Driver, Vehicle


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'gender', 'phone_number']


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ['user']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'model', 'type', 'insurance_policy_number',
                  'adults_seats_number', 'children_seats_number', 'animal_seats_number',
                  'trunk_capacity', 'air_conditioner_present', 'category']


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    vehicle = VehicleSerializer()

    class Meta:
        model = Driver
        fields = ['user', 'vehicle', 'passport_number', 'driver_license_number',
                  'taxi_license_number', 'status']


class DriverRegistrationSerializer(DriverSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta(DriverSerializer.Meta):
        fields = DriverSerializer.Meta.fields + ['password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        user = attrs.get('user', None)
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)

        if not user:
            raise serializers.ValidationError(_('Required account information is missing.'))

        existing_user = User.objects.filter(email=user['email']).first()
        if existing_user:
            raise serializers.ValidationError(_('Email must be unique.'))

        if password != confirm_password:
            raise serializers.ValidationError(_('"Password" and "Confirm password" do not match.'))
        return attrs

    def create(self, validated_data):
        # Create User account
        user = validated_data['user']
        email = user['email']
        password = validated_data['password']
        first_name = user['first_name']
        last_name = user['last_name']
        gender = user['gender']
        #birth_date = user['birth_date']
        phone_number = user['phone_number']

        created_user = User.objects.create_user(email=email, password=password,
                                                first_name=first_name, last_name=last_name,
                                                gender=gender, birth_date=None, phone_number=phone_number)

        # Create Vehicle entity
        vehicle = validated_data['vehicle']
        model = vehicle['model']
        type = vehicle['type']
        category = vehicle['category']
        insurance_policy_number = vehicle['insurance_policy_number']
        adults_seats_number = vehicle['adults_seats_number']
        children_seats_number = vehicle['children_seats_number']
        animal_seats_number = vehicle['animal_seats_number']
        trunk_capacity = vehicle['trunk_capacity']
        air_conditioner_present = vehicle['air_conditioner_present']

        created_vehicle = Vehicle.objects.create(model=model, type=type, insurance_policy_number=insurance_policy_number,
                                                 adults_seats_number=adults_seats_number, children_seats_number=children_seats_number,
                                                 animal_seats_number=animal_seats_number, trunk_capacity=trunk_capacity,
                                                 air_conditioner_present=air_conditioner_present, category=category)

        # Create Driver entity
        passport_number = validated_data['passport_number']
        driver_license_number = validated_data['driver_license_number']
        taxi_license_number = validated_data['taxi_license_number']

        driver = Driver.objects.create(user=created_user, vehicle=created_vehicle,
                                       passport_number=passport_number,
                                       driver_license_number=driver_license_number,
                                       taxi_license_number=taxi_license_number)
        return driver


class ClientRegistrationSerializer(ClientSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta(ClientSerializer.Meta):
        fields = ClientSerializer.Meta.fields + ['password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        user = attrs.get('user', None)
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)

        if not user:
            raise serializers.ValidationError(_('Required account information is missing.'))

        existing_user = User.objects.filter(email=user['email']).first()
        if existing_user:
            raise serializers.ValidationError(_('Email must be unique.'))

        if password != confirm_password:
            raise serializers.ValidationError(_('"Password" and "Confirm password" do not match.'))
        return attrs

    def create(self, validated_data):
        # Create User account
        user = validated_data['user']
        email = user['email']
        password = validated_data['password']
        first_name = user['first_name']
        last_name = user['last_name']
        gender = user['gender']
        #birth_date = user['birth_date']
        phone_number = user['phone_number']

        created_user = User.objects.create_user(email=email, password=password,
                                                first_name=first_name, last_name=last_name,
                                                gender=gender, birth_date=None, phone_number=phone_number)

        client = Client.objects.create(user=created_user)
        return client


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return data