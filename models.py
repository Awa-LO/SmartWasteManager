from django.db import models
from django.utils import timezone

class FillLevel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    fill_level = models.FloatField()

    def __str__(self):
        return f"Fill Level: {self.fill_level}% at {self.timestamp}"

class AirQuality(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    ppm = models.FloatField()
    qualite = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Air Quality: {self.ppm} ppm ({self.qualite}) at {self.timestamp}"

class GasDetection(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    gas_detected = models.IntegerField()
    ppm = models.FloatField(null=True, blank=True)
    nh3 = models.FloatField(null=True, blank=True)
    ch4 = models.FloatField(null=True, blank=True)
    h2s = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Gas Detected: {self.gas_detected} at {self.timestamp} with {self.ppm} ppm of CO2"

class BinState(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    state = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Poubelle {self.state} à {self.timestamp}"