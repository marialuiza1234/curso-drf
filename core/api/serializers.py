from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from core.models import PontosTuristicos, Atracao
from atracoes.api.serializers import AtracaoSerializer
from endereco.api.serializers import EnderecoSerializer
from endereco.models import Endereco


class PontoTuristicoSerializer(ModelSerializer):
    atracoes = AtracaoSerializer(many=True)
    endereco = EnderecoSerializer(read_only=True)
    descricao_completa = SerializerMethodField()

    class Meta:
        model = PontosTuristicos
        fields = ('id', 'nome', 'descricao', 'aprovado', 'foto', 'atracoes', 'comentarios',
                  'endereco', 'avaliacoes', 'descricao_completa', 'descricao_completa2',)
        read_only_fields = ('comentarios', 'avaliacoes')

    def cria_atracoes(self, atracoes, ponto):
        for atracao in atracoes:
            at = Atracao.objects.create(**atracao)
            ponto.atracoes.add(at)

    def create(self, validated_data):
        atracoes = self.request.data['atracoes']
        del validated_data['atracoes']
	
        endereco = validated_data['endereco']
        del validated_data['endereco']

        doc = validated_data['doc_identificacao']
        ponto = PontosTuristicos.objects.create(**validated_data)
        self.cria_atracoes(atracoes, ponto)
        end = Endereco.objects.create(**endereco)
        ponto.endereco = end
        ponto.doc_identificacao = doc
        ponto.save()
        return ponto

    def get_descricao_completa(self, obj):
        return '%s - %s' % (obj.nome, obj.descricao)