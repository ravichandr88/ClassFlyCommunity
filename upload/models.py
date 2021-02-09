from django.db import models

# Create your models here.
class Contact_number(models.Model):
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "created_on {}".format(self.created_on)