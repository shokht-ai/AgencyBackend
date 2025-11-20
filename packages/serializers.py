from rest_framework import serializers
from .models import Tour, TourImage, Highlight, IncludedItem, NotIncludedItem, ItineraryDay, ItineraryActivity, Facility

# --------------------
# Nested serializers
# --------------------
class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = ['url']

class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = ['text']

class IncludedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncludedItem
        fields = ['text']

class NotIncludedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotIncludedItem
        fields = ['text']

class ItineraryActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryActivity
        fields = ['activity']

class ItineraryDaySerializer(serializers.ModelSerializer):
    activities = ItineraryActivitySerializer(many=True, read_only=True)

    class Meta:
        model = ItineraryDay
        fields = ['day', 'title', 'activities']

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['name', 'icon']

# --------------------
# Main Tour serializer
# --------------------
class TourSerializer(serializers.ModelSerializer):
    images = TourImageSerializer(many=True, read_only=True)
    highlights = HighlightSerializer(many=True, read_only=True)
    included = IncludedItemSerializer(many=True, read_only=True)
    not_included = NotIncludedItemSerializer(many=True, read_only=True)
    itinerary = ItineraryDaySerializer(many=True, read_only=True)
    facilities = FacilitySerializer(many=True, read_only=True)
    agency = serializers.CharField(source='agency.name')
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'agency', 'location', 'price', 'original_price',
            'traveling_date', 'rating', 'reviews', 'discount', 'category',
            'images', 'description', 'highlights', 'included', 'not_included',
            'itinerary', 'facilities', 'featured'
        ]
