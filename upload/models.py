from django.db import models

# Create your models here.
class Contact_number(models.Model):
    filename = models.CharField(max_length=50,default='')
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "filename {} created_on {}".format(self.filename,self.created_on)



