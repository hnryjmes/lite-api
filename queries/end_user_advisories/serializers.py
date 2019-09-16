from rest_framework import serializers

from conf.serializers import PrimaryKeyRelatedSerializerField
from end_user.serializers import EndUserSerializer
from organisations.models import Organisation
from organisations.serializers import TinyOrganisationViewSerializer
from queries.end_user_advisories.models import EndUserAdvisoryQuery


class EndUserAdvisorySerializer(serializers.ModelSerializer):
    organisation = PrimaryKeyRelatedSerializerField(queryset=Organisation.objects.all(),
                                                    serializer=TinyOrganisationViewSerializer)
    end_user = EndUserSerializer()
    reasoning = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=2000)
    note = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=2000)

    class Meta:
        model = EndUserAdvisoryQuery
        fields = ['id', 'end_user', 'reasoning', 'note', 'organisation']

    def create(self, validated_data):
        end_user_data = validated_data.pop('end_user')

        # We set the country and organisation back to their string IDs, otherwise
        # the end_user serializer struggles to save them
        end_user_data['country'] = end_user_data['country'].id
        end_user_data['organisation'] = end_user_data['organisation'].id

        end_user_serializer = EndUserSerializer(data=end_user_data)
        if end_user_serializer.is_valid():
            end_user = end_user_serializer.save()
        else:
            raise serializers.ValidationError({'errors': end_user_serializer.errors})

        end_user_advisory_query = EndUserAdvisoryQuery.objects.create(**validated_data, end_user=end_user)
        end_user_advisory_query.save()

        return end_user_advisory_query
