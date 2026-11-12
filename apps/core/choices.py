from django.db import models


class PublicationStatus(models.TextChoices):
    """Publication workflow shared by fanfics and chapters."""

    DRAFT = "brouillon", "Brouillon"
    PUBLISHED = "publié", "Publié"
