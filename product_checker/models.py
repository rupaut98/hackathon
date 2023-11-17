from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    is_unhealthy = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    country_banned_in = models.TextField(blank=True, null=True)
    severity = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()  # Convert name to lowercase before saving
        super(Ingredient, self).save(*args, **kwargs)