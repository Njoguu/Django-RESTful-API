from rest_framework import serializers
from .models import developers

class developersSerializer(serializers.ModelSerializer):

    class Meta: 
        model = developers
        fields = ('fname', 'lname', 'github_username', 'stacks')