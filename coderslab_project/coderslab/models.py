from datetime import date, datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
import math


SIZE = (
    (25.4, "DN25"),
    (50.8, "DN50"),
    (76.2, "DN75"),
    (101.6, "DN100"),
)

WALL_THK = (
    (0.9, "0.9 mm"),
    (1.6, "1.6 mm"),
    (2.0, "2 mm"),
    (3.2, "3.2 mm"),
)

MATERIAL = (
    ("SS-304", "SS-316"),
    ("SS-304", "SS-304"),
    )

class PipeOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    size = models.FloatField(choices=SIZE, max_length=6)
    wall_thk = models.FloatField(choices=WALL_THK, max_length=6)
    material = models.CharField(choices=MATERIAL, max_length=6)
    length = models.IntegerField(validators=[MaxValueValidator(6000), MinValueValidator(50)])
    quantity = models.IntegerField(validators=[MaxValueValidator(9999), MinValueValidator(1)])

    @property
    def wall_thk_mm(self):
        return  dict(WALL_THK)[self.wall_thk]

    @property
    def size_sch(self):
        return  dict(SIZE)[self.size]

class TestModel(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)




class Branch(models.Model):
    pipe_order = models.ForeignKey(PipeOrder, on_delete=models.CASCADE)
    position = models.IntegerField()
    size = models.FloatField()
    angle = models.FloatField(validators=[MaxValueValidator(360), MinValueValidator(0)])



