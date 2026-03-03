from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    dimension_code = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    reality_rules = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.name} ({self.dimension_code})"


class Booking(models.Model):
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    check_in = models.DateField()
    nights = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} - {self.room.name} ({self.check_in})"
