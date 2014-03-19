# -*- coding: utf-8 -*-
from functools import wraps

def unique_boolean(field):
    def factory(func):
        @wraps(func)
        def decorator(self):
            if getattr(self, field):
                try:
                    tmp = self.__class__.objects.get(**{ field: True })
                    if self != tmp:
                        setattr(tmp, field, False)
                        tmp.save()
                except self.__class__.DoesNotExist:
                    pass
            return func(self)
        return decorator
    return factory

def seq_value(field):
    """
    Декоратор для последовательного инкремента заданного поля
    """
    # TODO: Возможны проблемы при конкурентных сохранениях 
    # Возможно решаемо заданием уникального индекса по полю 
    # и бесконечным повтором вставки при ошибке (ref. upserts Postgres)
    def factory(func):
        @wraps(func)
        def decorator(self):
            if not self.id:
                try:
                    last = self.__class__.objects.all().order_by('-'+field)[0]
                    last_val = getattr(last, field)
                    if last_val == None:
                        setattr(self, field, 1)
                    else:
                        setattr(self, field, last_val + 1)
                except IndexError:
                    setattr(self, field, 1)
            return func(self)
        return decorator
    return factory
