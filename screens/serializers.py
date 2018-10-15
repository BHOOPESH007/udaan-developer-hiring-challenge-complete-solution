from screens.models import Screens, Seats
from rest_framework import serializers


class ScreensSerializer(serializers.ModelSerializer):

    class Meta:
        model= Screens
        fields = ['name', 'seatInfo']

class SeatsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Seats
        fields = ['seat_table']