# myapp/models.py

from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()  # 例如可以添加邮箱信息

    def __str__(self):
        return self.name