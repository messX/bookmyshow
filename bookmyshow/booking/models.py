from datetime import datetime

from django.db import models

# Create your models here.
# Create your models here.
class Theatre(models.Model):
    city_choice=(
        ('DELHI','Delhi'),
        ('KOLKATA','Kolkata'),
        ('MUMBAI','Mumbai'),
        ('CHENNAI','Chennai'),
        ('BANGALORE','Bangalore'),
        ('HYDERABAD','Hyderabad'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=False)
    city = models.CharField(max_length=9,choices=city_choice,null=False)
    address = models.CharField(max_length=30, null=True)
    no_of_screen = models.IntegerField()


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)

class Screen(models.Model):
    name = models.CharField(max_length=100, null=False)
    theater = models.ForeignKey(Theatre, on_delete=models.CASCADE)

class Show(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

class Seat(models.Model):
    seat_choice = (
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    )
    id = models.AutoField(primary_key=True)
    no = models.CharField(max_length=3,null=True,blank=False)
    seat_type = models.CharField(max_length=8, choices=seat_choice, blank=False)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def as_json(self):
        return {
            'id': self.id,
            'number': self.no,
            'seat_type': self.seat_type,
            'show': self.show.id
        }

class Booking(models.Model):
    payment_choice = (
        ('Credit Card', 'Credit Card'),
    )
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)
    payment_type = models.CharField(max_length=11, choices=payment_choice, default='Credit Card')
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    def as_json(self):
        return {
            'id':self.id,
            'time': datetime.strftime(self.timestamp, "%Y-%m-%d %H %M"),
            'payment_type':self.payment_type,
            'paid_amount': float(self.paid_amount)
        }

class ShowSheatMapping(models.Model):
    id = models.AutoField(primary_key=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    status_choice = (
        ('Booked', 'Booked'),
        ('Blocked', 'Blocked'),
        ('Empty', 'Empty'),
    )
    status = models.CharField(max_length=11, choices=status_choice, default='Empty')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)

    def as_json(self):
        return {
            'id': self.id,
            'seat': self.seat.as_json(),
            'status': self.status,
            'booking': self.booking.id,
            'show':self.show.id
        }

