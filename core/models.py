from django.db import models


# Create your models here.
class RsaKey(models.Model):
    class KeyType(models.TextChoices):
        PRIVATE = 'PR', 'Private'
        PUBLIC = 'PB', 'Public'

    key_type = models.CharField(
        choices=KeyType.choices,
        default=KeyType.PUBLIC,
        max_length=2,
        null=False,
        blank=False,
        unique=True
    )

    content = models.TextField()

    def __str__(self) -> str:
        return str(self.get_key_type_display())
