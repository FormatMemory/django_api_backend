from django.conf import settings
from django.db import models
from v1.general.created_modified import CreatedModified
from v1.utils import constants
from v1.categories.models.category import Category
from taggit.managers import TaggableManager
from django_mysql.models import JSONField


class Post(CreatedModified):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    body = models.TextField() # Description
    image = models.ImageField(blank=True, upload_to="")
    deal_link = models.URLField(blank=True)
    date_expire = models.DateTimeField(null=True, blank=True) # DurationField
    # date_posted = models.DateTimeField(null=True, auto_now_add=True)
    # last_modified = models.DateTimeField(null=True, auto_now=True)
    status = models.CharField(choices=constants.POST_STATUS_CHOICES, default=constants.STATUS_ACTIVE, max_length=30)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)

    # new add
    source = models.CharField(max_length=55, blank = True, null=True)
    sku = models.CharField(max_length=25, blank = True, null=True)
    customer_review = models.DecimalField(blank = True, null=True,  max_digits=4, decimal_places=2)
    details = JSONField(null=True, blank=True)
    dollar_savings = models.DecimalField(blank = True, null=True, max_digits=12, decimal_places=2)
    features = JSONField(null=True, blank=True)
    manufacturer = models.CharField(max_length=30, blank = True, null=True)
    model_number = models.CharField(max_length=30, blank = True, null=True)
    percent_savings = models.DecimalField(blank = True, null=True,  max_digits=5, decimal_places=2)
    regular_price = models.DecimalField(blank = True, null=True, max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(blank = True, null=True, max_digits=12, decimal_places=2)
    date_start =  models.DateTimeField(null=True, blank=True) # DurationField


    tags = TaggableManager(blank=True)

    class Meta:
        default_related_name = 'posts'
        ordering = ['-created_time']

    def __str__(self):
        return self.title