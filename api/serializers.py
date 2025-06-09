from rest_framework import serializers
from films.models import Film, Institution


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'code']

class FilmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmDetailSerializer(serializers.ModelSerializer):
    """Complete serializer for detail views"""
    institution = InstitutionSerializer(read_only=True)
    institution_id = serializers.IntegerField(write_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_id = serializers.IntegerField(source='created_by.id', read_only=True)
    
    class Meta:
        model = Film
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class FilmCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating films"""
    
    class Meta:
        model = Film
        exclude = ['created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)