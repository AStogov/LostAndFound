from django.db import models

# Create your models here.
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="创建时间", default=timezone.now, blank=True)
    modified_at = models.DateTimeField(verbose_name="修改时间", auto_now=True, blank=True)

    class Meta:
        abstract = True

    def format(self, if_time_format=True, time_format=''):
        import json
        dic = {}
        for f in self._meta.fields:
            dic[f.name] = getattr(self, f.name)
        for key in dic:
            if 'time' in key:
                dic[key] = dic[key].strftime("%Y-%m-%d %H:%M:%S")
        return dic

    # def querysetToJson(self, qset, if_time_format=True, time_format=''):
    #     return list(qset)
