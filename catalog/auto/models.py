from django.db import models


class Mark(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'


class Model(models.Model):
    name = models.CharField(max_length=64)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.mark}'


class FileXML(models.Model):
    file = models.FileField(upload_to='xml/')