from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Booktitle(models.Model):
    title = models.CharField(max_length=250)
    author = models.TextField(blank=True, null=True)
    edition = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=250, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=250, blank=True, null=True)
    series = models.TextField(blank=True, null=True)
    subjects = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - ({})".format(self.title, self.year)

class Bookitem(models.Model):
    LOCATION = (
        ('1/F Collection', '1/F Collection'),
        ('2/F Collection', '2/F Collection'),
        ('3/F Collection', '3/F Collection'),
        ('1/F Reference Section', '1/F Reference Section')
    )
    STATUS = (
        ('available', 'available'),
        ('checked-out', 'checked-out'),
        ('on holdshelf', 'on holdshelf'),
        ('lib use only', 'lib use only'),
        ('in purchase', 'in purchase'),
        ('in process', 'in process'),
        ('library display', 'library display'),
        ('lost', 'lost'),
        ('withdrawn', 'withdrawn')
    )

    title = models.ForeignKey(Booktitle, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=10, unique=True)
    location = models.CharField(max_length=25, choices=LOCATION)
    callno = models.CharField(max_length=100)
    status = models.CharField(max_length=25, choices=STATUS)
    duedate = models.DateField(blank=True, null=True)
    current_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_in_use")
    previous_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_previous_use")
    total_checkedout = models.IntegerField(default=0)
    renewal = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100, blank=True, null=True)
    holdlist = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.title, self.callno)

    def show_status(self):
        if self.status == "checked-out":
            return self.duedate
        else:
            return self.status


class CircAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=True)
    fine = models.IntegerField(blank=True, null=True, default=0)
    hold = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.user)