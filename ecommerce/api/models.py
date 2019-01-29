from django.db import models


class APIClient(models.Model):
    name = models.CharField(max_length=128)
    accesskey = models.CharField(max_length=32)
    secretkey = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def is_staff(self):
        return True

    def is_authenticated(self):
        return True

    def save(self, *args, **kwargs):
        self.full_clean()
        super(APIClient, self).save(*args, **kwargs)
