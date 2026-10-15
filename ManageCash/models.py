from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AddCash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.source} (+{self.amount})"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.description} (-{self.amount})"