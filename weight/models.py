from django.db import models

# Create your models here.
class Menu(models.Model):
    weight_menu = models.CharField(max_length=30)

    def __str__(self):
        return "{0}:{1}".format(self.pk, self.weight_menu)
    