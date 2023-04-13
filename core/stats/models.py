from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.

class Statistic(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse('stats:dashboard', kwargs={"slug": self.slug})

    @property
    def data(self):
        return self.dataitem_set.all() # return all dataitem with relaited static


    def __str__(self):
        return str(self.name)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name) # return ASCII. Например = Naprimer
        super().save(*args,**kwargs)


class DataItem(models.Model):
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()
    owner = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.owner}: {self.value}"