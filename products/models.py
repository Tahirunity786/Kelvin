from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)  # Explicitly define primary key
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    body = models.TextField()
    url = models.TextField()
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def summary(self):
        return self.body[:250]

    def votes_total(self):
        return self.vote_set.count()

class Vote(models.Model):
    id = models.BigAutoField(primary_key=True)  # Explicitly define primary key
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voter', 'product')


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)  # Explicitly define primary key
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.product.title}'
