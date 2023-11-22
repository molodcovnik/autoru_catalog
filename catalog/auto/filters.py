import django_filters
from django_filters import ModelChoiceFilter, ChoiceFilter

from .models import Model, Mark


class ModelFilterSet(django_filters.FilterSet):
    mark = ChoiceFilter(choices=[(choice.id, choice) for choice in Mark.objects.all()])
    class Meta:
        model = Model
        fields = ['mark']