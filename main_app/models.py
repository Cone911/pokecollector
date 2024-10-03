from django.db import models
from django.urls import reverse

MEALS = (
    ('A', 'Apple'),
    ('B', 'Berry'),
    ('G', 'Grapes'),
    ('H', 'Hot Dog'),
    ('P', 'Pizza'),
    ('S', 'Sushi'),
    ('T', 'Tonkatsu'),
)

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    poke_id = models.IntegerField()
    xp = models.IntegerField()
    type = models.CharField(max_length=100)
    abilities = models.TextField()
    image_url = models.URLField()
    nickname = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
       return f'{self.name} (ID: {self.poke_id})'

    def get_absolute_url(self):
        return reverse('poke-detail', kwargs={'poke_id': self.poke_id})
    
class Feeding(models.Model):
    date = models.DateField('Feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"



