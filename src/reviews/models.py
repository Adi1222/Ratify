from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import numpy as np

deleted_choices = [('N', 'No'), ('Y', 'Yes')]


class Category(models.Model):
    catname = models.CharField(unique=True, blank=False, max_length=100)
    # catimg = models.ImageField(upload_to='cat_img', blank=True, null=True)

    def calculate_products(self):
        return self.product_set.count()

    def __str__(self):
        return self.catname + " " + str(self.id)

    class Meta:
        managed = True
        db_table = "Category"


class Product(models.Model):
    pname = models.CharField(max_length=30, blank=False)
    company = models.CharField(max_length=30)  # one category has many products
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=25)
    is_deleted = models.CharField(
        max_length=1, choices=deleted_choices, default='N')
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    pimg = models.ImageField(upload_to='prod_img', blank=True, null=True)

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(list(all_ratings))

    def total_rating(self):
        return self.review_set.count()

    def __str__(self):
        return self.pname + "" + str(id)

    class Meta:
        managed = True
        db_table = "Product"


class Appuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    is_deleted = models.CharField(
        max_length=1, choices=deleted_choices, default='N')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+91'. Up to 15 digits allowed.")
    is_deleted = models.CharField(
        max_length=1, choices=deleted_choices, default='N')
    mobile = models.CharField(
        validators=[phone_regex], max_length=12, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        managed = True
        db_table = "Appuser"


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(Appuser, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300)
    rating = models.IntegerField(choices=RATING_CHOICES)
    pub_date = models.DateTimeField('date published')
    upvote = models.IntegerField(
        name='upvote', blank=True, null=True, default=0)
    downvote = models.IntegerField(
        name='downvote', blank=True, null=True, default=0)

    def increment_upvote(self):
        self.upvote += 1

    def decrement_downvote(self):
        self.downvote += 1

    def __str__(self):
        return self.product.pname + " by " + self.rated_by.user.username

    class Meta:
        managed = True
        db_table = "Review"
