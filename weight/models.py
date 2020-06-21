from django.db import models

# Create your models here.
class Menu(models.Model):
    menu_name = models.CharField(max_length=30)

    def __str__(self):
        return "PK:{0}, name:{1}".format(self.pk, self.menu_name)

class Record(models.Model):
    weight_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    weight_record = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "PK:{0}, FK:{1}, weight:{2}, created:{3}".format(self.pk, self.weight_menu, self.weight_record, self.created_at)