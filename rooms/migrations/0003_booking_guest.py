# Generated manually — adds Booking.guest ForeignKey to AUTH_USER_MODEL

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0002_booking_adjusted_checkout_booking_adjusted_nights_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="guest",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bookings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
