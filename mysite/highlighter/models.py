from django.db import models

# Create your models here.


#see many to one.
class LabelType(models.Model):
    label = models.CharField(max_length=30)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return self.label

class SummaryEntry(models.Model):
    title = models.CharField(max_length=100)
    original = models.TextField() #can i not do textfield, need charfield?
    labels = models.ManyToManyField(LabelType)
    processed = models.TextField(blank=True)


    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

