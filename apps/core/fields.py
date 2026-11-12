from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    """Positive integer filled with ``last + 1`` when left empty.

    ``for_fields`` scopes the numbering, e.g. ``OrderField(for_fields=["fanfic"])``
    numbers chapters per fanfic.
    """

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is not None:
            return super().pre_save(model_instance, add)
        queryset = self.model._default_manager.all()
        if self.for_fields:
            queryset = queryset.filter(
                **{field: getattr(model_instance, field) for field in self.for_fields}
            )
        try:
            value = getattr(queryset.latest(self.attname), self.attname) + 1
        except ObjectDoesNotExist:
            value = 0
        setattr(model_instance, self.attname, value)
        return value
