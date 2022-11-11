from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
# create your models here

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    balance = models.CharField(max_length=100, null=True, default=0)
    phone_no = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    user_type = models.IntegerField(null=True, default=0)
    # verification_code = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)

    def __str__(self):
         return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



# def for hotel
class category(models.Model):
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='category/', null=True)

    def __str__(self):
        return self.name
    

    class Meta():
        db_table = 'category'


# for category
class hotel(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, default=1)
    hotel_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='hotel/', null=True)
    status = models.IntegerField(null=True, default=1)

    def __str__(self):
        return self.name
    
    class Meta():
        db_table = 'hotel'


# for hotel images
class hotel_gallery(models.Model):
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE, default=1)   
    image = models.ImageField(upload_to='hotel/', null=True)

    def __str__(self):
        return self.hotel.name 

    class Meta():
        db_table = 'hotel_gallery'


# for booking
class booking(models.Model):
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE, default=1)   
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    booking_id = models.CharField(max_length=100, unique=True, null=True)
    check_in = models.DateField(max_length=100, null=True)
    check_out = models.DateField(max_length=100, null=True)
    amount = models.CharField(max_length=100, null=True)
    guest = models.CharField(max_length=10, null=True)
    room = models.CharField(max_length=10, null=True)
    status = models.IntegerField(null=True, default=0)
    date = models.DateTimeField(max_length=100, null=True)

    def __str__(self):
        return  "#" + self.booking_id + " - " + self.hotel.name +" - ordered by  "+ self.user.username
    


    class Meta():
        db_table = 'booking'


# row for cancellation of order
class canceled_booking(models.Model):
    booking = models.ForeignKey(booking, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    reason = models.TextField(max_length=200, null=True)
    date = models.DateTimeField(max_length=100, null=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return "#"+self.booking.booking_id + " - " +self.booking.hotel.name + " - request by "+self.booking.user.username


    class Meta():
        db_table = 'canceled_booking'


# for tickets
class ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    ticket_id = models.CharField(max_length=100, editable=False, unique=True)
    issue = models.CharField(max_length=100, null=True)
    priority = models.CharField(max_length=100, null=True)
    message = models.TextField(max_length=1000, null=True)
    date = models.DateTimeField(max_length=100, null=True)
    status = models.IntegerField(null=True, default=1)

    def __str__(self):
        return self.user.username+" - #"+self.ticket_id+" - "+self.issue

    class Meta():
        db_table = 'ticket'


# for tickets replys
class ticket_reply(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    ticket = models.ForeignKey(ticket, on_delete=models.CASCADE, null=True)  
    message = models.TextField(max_length=1000, null=True)
    date = models.DateTimeField(max_length=100, null=True)

    def __str__(self):
        return self.ticket.issue

    class Meta():
        db_table = 'ticket_reply'



# for the contact form 
class contact(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone_no = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone_no = models.CharField(max_length=15, null=True)
    message = models.TextField(max_length=500, null=True)
    date = models.DateTimeField(max_length=100, null=True)

    def __str__(self):
        return self.name
    

    class Meta():
        db_table = 'contact'