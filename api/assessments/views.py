from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status

from api.applications.models import GoodOnApplication
from api.assessments.serializers import AssessmentSerializer


class MakeAssessmentsView(generics.UpdateAPIView):

    serializer_class = AssessmentSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self, ids):
        return GoodOnApplication.objects.filter(
            application_id=self.kwargs["case_pk"],
            id__in=ids,
        )

    def update(self, request, *args, **kwargs):
        ids = validate_ids(request.data)
        instances = self.get_queryset(ids)
        serializer = self.get_serializer(instances, data=request.data, partial=False, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return JsonResponse(data={}, status=status.HTTP_200_OK)


def validate_ids(data, unique=True):

    ids = [record["id"] for record in data]

    if unique and len(ids) != len(set(ids)):
        raise ValidationError("Multiple updates to a single GoodOnApplication id found")

    return ids
