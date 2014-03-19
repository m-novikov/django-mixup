# -*- coding: utf-8 -*-
from django.db import models
from .decorators import seq_value

class OrderedManager(models.Manager):
    def get_query_set(self):
        super(OrderedManager, self).get_query_set().order_by('index')

class OrderedMixin(models.Model):
    """
    Класс реализующий определенный порядок моделей в базе
    """
    index = models.IntegerField(default=1)

    objects = models.Manager()
    ordered = OrderedManager()

    def get_object_at_offset(self, offset):
        """
        Получаем модель по смещению порядка 
        Наример offset = 1 следующая offset = -1 предыдущая
        """
        try:
            return self.objects.get(index=self.index + offset)
        except self.DoesNotExist:
            return None

    get_next = lambda self: self.get_object_at_offset(1)
    get_previous = lambda self: self.get_object_at_offset(-1)

    def swap_index_with(self, instance):
        """ Меняем два элемента местами """
        if not instance:
            return
        self.index, instance.index = instance.index, self.index
        for obj in (self, instance):
            obj.save()

    def move_up(self):
        """ Перемещает элемент на порядок вверх """
        next_one = self.get_next()
        self.swap_index_with(next_one)

    def move_down(self):
        """ Перемещает элемент на порядок вниз """
        prev_one = self.get_previous()
        self.swap_index_with(prev_one)

    @seq_value('index')
    def save(self, *args, **kwargs):
        super(OrderedMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
