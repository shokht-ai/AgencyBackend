from django.db import models

# --------------------
# Kategoriya
# --------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# --------------------
# Agentlik (Travel agency)
# --------------------
class Agency(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

# --------------------
# Asosiy Tour
# --------------------
class Tour(models.Model):
    title = models.CharField(max_length=255)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="tours")
    location = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    original_price = models.PositiveIntegerField()
    traveling_date = models.DateField()
    rating = models.FloatField()
    reviews = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="tours")
    description = models.TextField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# --------------------
# Tour Images
# --------------------
class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="images")
    url = models.URLField()

    def __str__(self):
        return self.url

# --------------------
# Highlights
# --------------------
class Highlight(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="highlights")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

# --------------------
# Included / Not Included
# --------------------
class IncludedItem(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="included")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class NotIncludedItem(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="not_included")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

# --------------------
# Itinerary
# --------------------
class ItineraryDay(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="itinerary")
    day = models.PositiveIntegerField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.day} - {self.title}"

class ItineraryActivity(models.Model):
    itinerary_day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name="activities")
    activity = models.CharField(max_length=255)

    def __str__(self):
        return self.activity

# --------------------
# Facilities
# --------------------
class Facility(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="facilities")
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)  # Emoji yoki ikon URL

    def __str__(self):
        return self.name
