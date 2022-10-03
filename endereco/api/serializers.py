from rest_framework.serializers import ModelSerializer
from endereco.models import Endereco


class EnderecoSerializer(ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('linha1', 'linha2', 'cidade', 'estado', 'latitude', 'longitude')
