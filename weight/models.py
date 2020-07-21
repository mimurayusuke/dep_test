from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Menu(models.Model):
    menu_name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        #下記のように記載すると、外部キーで参照されたときに
        #定義した内容で表示されてしまうので、コメントアウト。
        #return "PK:{0}, name:{1}".format(self.pk, self.menu_name)
        return self.menu_name

class Record(models.Model):
    weight_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    weight_record = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    rep = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "PK:{0}, FK:{1}, weight:{2}, rep:{3}, created:{4}".format(self.pk, self.weight_menu, self.weight_record, self.rep, self.created_at)