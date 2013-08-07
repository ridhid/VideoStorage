#coding: utf-8
__author__ = 'ridhid'

from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=255)

    def to_dict(self):
        cams = [cam.url for cam in self.cams.all()]
        return dict(name=self.name, cams=cams)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'


class Camera(models.Model):
    url = models.CharField(max_length=255)
    room = models.ForeignKey(Room, related_name="cams")

    def __unicode__(self):
        return " ".join((self.url, self.room.name))

    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"