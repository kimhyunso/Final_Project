from django.db import models

class POST(models.Model):
    title = models.CharField(max_length=50)
    Content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}] {self.title}'
