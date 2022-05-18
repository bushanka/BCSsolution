from django.db import models


class TransactionsInfo(models.Model):
    Txid = models.CharField(max_length=64, primary_key=True)
    Description = models.TextField(default='No description', blank=True)

    def __str__(self):
        return self.Txid
