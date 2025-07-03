from django.db import models

# Create your models here.

class CatalogRAGQuery(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query {self.id} at {self.created_at}"
