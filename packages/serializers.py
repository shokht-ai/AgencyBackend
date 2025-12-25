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
    # activities = ItineraryActivitySerializer(many=True, read_only=True)
    activities = serializers.SerializerMethodField()

    class Meta:
        model = ItineraryDay
        fields = ['day', 'title', 'activities']

    @staticmethod
    def get_activities(obj):
        activities = ItineraryActivity.objects.filter(itinerary_day=obj)
        return [i.activity for i in activities]


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['name', 'icon']


# --------------------
# Main Tour serializer
# --------------------
class TourSerializer(serializers.ModelSerializer):
    itinerary = ItineraryDaySerializer(many=True, read_only=True)
    facilities = FacilitySerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()
    highlights = serializers.SerializerMethodField()
    included = serializers.SerializerMethodField()
    notIncluded = serializers.SerializerMethodField()

    travelingDate = serializers.SerializerMethodField()
    originalPrice = serializers.SerializerMethodField()

    category = serializers.CharField(source='category.name')
    agency = serializers.CharField(source='agency.name')

    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'agency', 'location', 'price', 'originalPrice',
            'travelingDate', 'rating', 'reviews', 'discount', 'category',
            'images', 'description', 'highlights', 'included', 'notIncluded',
            'itinerary', 'facilities', 'featured'
        ]

    @staticmethod
    def get_travelingDate(obj):
        return obj.traveling_date

    @staticmethod
    def get_originalPrice(obj):
        return obj.original_price

    @staticmethod
    def get_images(obj):
        images = TourImage.objects.filter(tour=obj)
        return [i.url for i in images]

    @staticmethod
    def get_highlights(obj):
        highlights = Highlight.objects.filter(tour=obj)
        return [i.text for i in highlights]

    @staticmethod
    def get_included(obj):
        items = IncludedItem.objects.filter(tour=obj)
        return [i.text for i in items]

    @staticmethod
    def get_notIncluded(obj):
        items = NotIncludedItem.objects.filter(tour=obj)
        return [i.text for i in items]


class TourBookingSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    agency = serializers.CharField(source='agency.name')
    class Meta:
        model = Tour
        fields = ['id', 'title', 'agency', 'images', 'traveling_date']

    def get_images(self, obj):
        images_data = TourImage.objects.filter(tour=obj.pk).first()
        return images_data.url