import os
import django
from datetime import datetime

# Django sozlamalarini yuklash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agencybackend.settings")
django.setup()

from packages.models import (
    Tour, Agency, Category, TourImage, Highlight,
    IncludedItem, NotIncludedItem, ItineraryDay, ItineraryActivity,
    Facility
)

# JSON ma'lumot
data = [
  {
    "id": 1,
    "title": "Dubai Premium Safari",
    "agency": "Grand Tours",
    "location": "Dubai, BAA",
    "price": 2500000,
    "originalPrice": 3000000,
    "travelingDate": "2026-01-17",
    "rating": 4.8,
    "reviews": 142,
    "discount": 17,
    "category": "Luxe",
    "images": [
      "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200&q=80",
      "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=1200&q=80"
    ],
    "description": "Dubai sharida unutilmas sayohat. Burj Khalifa, sahro safari, zamonaviy diqqatga sazovor joylar va hashamatli shahar hayotini his eting.",
    "highlights": [
      "Burj Khalifa 124-125 qavatlar",
      "Sahro safari",
      "Dubai Mall va Fountain shousi",
      "Palm Jumeirah",
      "Marina bo‘ylab sayohat"
    ],
    "included": [
      "5 yulduzli mehmonxona",
      "Nonushta",
      "Transfer",
      "Gid",
      "Sug‘urta"
    ],
    "notIncluded": ["Tushlik/kechki ovqat", "Shaxsiy xarajatlar"],
    "itinerary": [
      {
        "day": 1,
        "title": "Kelish",
        "activities": ["Transfer", "Joylashish", "Dubai Mall"]
      },
      {
        "day": 2,
        "title": "Burj Khalifa",
        "activities": ["Ko‘tarilish", "Marina", "JBR Beach"]
      },
      {
        "day": 3,
        "title": "Sahro safari",
        "activities": ["Dune bashing", "Tuya minish", "BBQ kechki ovqat"]
      },
      {
        "day": 4,
        "title": "Palm Jumeirah",
        "activities": ["Monorels", "Atlantis"]
      },
      { "day": 5, "title": "Xayrlashuv", "activities": ["Transfer"] }
    ],
    "facilities": [
      { "name": "Mehmonxona", "icon": "🏨" },
      { "name": "Transfer", "icon": "🚗" },
      { "name": "Ovqat", "icon": "🍽" },
      { "name": "Gid", "icon": "👤" }
    ],
    "featured": True
  },

  {
    "id": 2,
    "title": "Istanbul Tarixiy Sayohati",
    "agency": "Silk Road Travel",
    "location": "Istanbul, Turkiya",
    "price": 1800000,
    "originalPrice": 2200000,
    "travelingDate": "2026-03-05",
    "rating": 4.9,
    "reviews": 218,
    "discount": 18,
    "category": "Tarix",
    "images": [
      "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=1200&q=80",
      "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200&q=80"
    ],
    "description": "Istanbul tarix bilan boy shahar. Ayasofya, Topkapi saroyi, Bosfor bo‘g‘ozi va ko‘plab tarixiy maskanlar bilan sayohat.",
    "highlights": [
      "Ayasofya",
      "Ko‘k masjid",
      "Topkapi saroyi",
      "Bosfor kruizi",
      "Grand Bazaar"
    ],
    "included": ["4 yulduzli mehmonxona", "Nonushta", "Gid", "Transfer"],
    "notIncluded": ["Ovqatlar", "Shaxsiy xarajatlar"],
    "itinerary": [
      {
        "day": 1,
        "title": "Kelish",
        "activities": ["Joylashish", "Galata ko‘prigi"]
      },
      {
        "day": 2,
        "title": "Tarixiy markaz",
        "activities": ["Ayasofya", "Ko‘k masjid", "Topkapi"]
      },
      {
        "day": 3,
        "title": "Bosfor kruizi",
        "activities": ["Kruiz", "Grand Bazaar"]
      },
      { "day": 4, "title": "Xayrlashuv", "activities": ["Transfer"] }
    ],
    "facilities": [
      { "name": "Mehmonxona", "icon": "🏨" },
      { "name": "Transfer", "icon": "🚗" },
      { "name": "Gid", "icon": "👤" }
    ]
  },

  {
    "id": 3,
    "title": "Parij Romantik Tour",
    "agency": "Europe Express",
    "location": "Parij, Fransiya",
    "price": 3200000,
    "originalPrice": 3800000,
    "travelingDate": "2026-06-21",
    "rating": 4.7,
    "reviews": 95,
    "discount": 16,
    "category": "Ekskursiya",
    "images": [
      "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200&q=80"
    ],
    "description": "Parij — sevgi va san'at shahri. Eyfel minorasi, Luvr muzeyi, Sena kruizi va Montmartre bo‘ylab romantik sayr.",
    "highlights": [
      "Eyfel minorasi",
      "Luvr",
      "Sena kruizi",
      "Montmartre",
      "Triumf arkasi"
    ],
    "included": [
      "4 yulduzli mehmonxona",
      "Nonushta",
      "Transfer",
      "Gid",
      "Viza"
    ],
    "notIncluded": [
      "Aviachiptalar",
      "Tushlik/kechki ovqat",
      "Shaxsiy xarajatlar"
    ],
    "itinerary": [
      {
        "day": 1,
        "title": "Kelish",
        "activities": ["Mehmonxona", "Sena bo‘yi sayri"]
      },
      {
        "day": 2,
        "title": "Luvr",
        "activities": ["Luvr muzeyi", "Eyfel minorasi"]
      },
      {
        "day": 3,
        "title": "Montmartre",
        "activities": ["San'at ko‘chalari", "Kofe tashrifi"]
      },
      { "day": 4, "title": "Versal", "activities": ["Versal saroyi"] },
      { "day": 5, "title": "Shaxsiy vaqt", "activities": ["Shopping"] },
      { "day": 6, "title": "Xayrlashuv", "activities": ["Transfer"] }
    ],
    "facilities": [
      { "name": "Mehmonxona", "icon": "🏨" },
      { "name": "Transfer", "icon": "🚗" },
      { "name": "Ovqat", "icon": "🍽" },
      { "name": "Gid", "icon": "👤" },
      { "name": "Viza", "icon": "📄" }
    ]
  },

  {
    "id": 4,
    "title": "Bali Tropik Ta'tili",
    "agency": "Asia Dreams",
    "location": "Bali, Indoneziya",
    "price": 2100000,
    "originalPrice": 2500000,
    "travelingDate": "2026-08-09",
    "rating": 4.9,
    "reviews": 167,
    "discount": 16,
    "category": "Plyaj",
    "images": [
      "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1200&q=80"
    ],
    "description": "Bali — tropik orol. Plyajlar, yoga markazlari, ma'badlar va tabiat bag‘rida dam olish uchun eng yaxshi joy.",
    "highlights": [
      "Kuta va Nusa Dua plyajlari",
      "Ubud maymunlar o‘rmoni",
      "Tegallalang terassalari",
      "Tanah Lot ma’badi",
      "Spa va wellness kunlari"
    ],
    "included": ["4 yulduzli mehmonxona", "Nonushta", "Transfer", "Sug‘urta"],
    "notIncluded": ["Kechki ovqat", "Spa xizmatlari"],
    "itinerary": [
      { "day": 1, "title": "Kuta", "activities": ["Joylashish", "Plyaj"] },
      {
        "day": 2,
        "title": "Ubud",
        "activities": ["Maymunlar o‘rmoni", "Tegallalang"]
      },
      {
        "day": 3,
        "title": "Nusa Dua",
        "activities": ["Plyaj", "Suv sportlari"]
      },
      { "day": 4, "title": "Tanah Lot", "activities": ["Ma’bad safari"] },
      { "day": 5, "title": "Spa kuni", "activities": ["Massaj", "Wellness"] },
      { "day": 6, "title": "Erkin kun", "activities": ["Shopping"] },
      { "day": 7, "title": "Xayrlashuv", "activities": ["Transfer"] }
    ],
    "facilities": [
      { "name": "Mehmonxona", "icon": "🏨" },
      { "name": "Transfer", "icon": "🚗" },
      { "name": "Ovqat", "icon": "🍽" },
      { "name": "Sug'urta", "icon": "🛡" }
    ]
  },

  {
    "id": 5,
    "title": "Maldiv Orollari Lux",
    "agency": "Ocean Travels",
    "location": "Maldivlar",
    "price": 4500000,
    "originalPrice": 5500000,
    "travelingDate": "2026-09-14",
    "rating": 5.0,
    "reviews": 89,
    "discount": 18,
    "category": "Luxe",
    "images": [
      "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=1200&q=80"
    ],
    "description": "Maldivlarda hashamatli dam olish: suv ustidagi bungalolar, kristall toza suv, oq qumli plyajlar va sokin tropik atmosferasi.",
    "highlights": [
      "Suv ustidagi bungalolar",
      "Shnorkeling va diving",
      "Okean ustida kechki ovqat",
      "Spa va massaj",
      "Sunset cruise"
    ],
    "included": [
      "5 yulduzli resort",
      "All inclusive ovqatlanish",
      "Transfer (suv taxi)",
      "Sug‘urta"
    ],
    "notIncluded": ["Premium xizmatlar", "Spa paketlari"],
    "itinerary": [
      {
        "day": 1,
        "title": "Kelish",
        "activities": ["Suv taxi", "Bungalo joylashish"]
      },
      { "day": 2, "title": "Plyaj kuni", "activities": ["Snorkeling", "Spa"] },
      { "day": 3, "title": "Ocean tour", "activities": ["Delfin cruise"] },
      { "day": 4, "title": "Sunset", "activities": ["Sunset dinner"] },
      { "day": 5, "title": "Xayrlashuv", "activities": ["Transfer"] }
    ],
    "facilities": [
      { "name": "Mehmonxona", "icon": "🏨" },
      { "name": "Transfer", "icon": "🚤" },
      { "name": "Ovqat", "icon": "🍽" },
      { "name": "Sug'urta", "icon": "🛡" }
    ],
    "featured": True
  },

  {
    "id": 6,
    "title": "Rim Antik Sayohati",
    "agency": "Europe Express",
    "location": "Rim, Italiya",
    "price": 2800000,
    "originalPrice": 3200000,
    "travelingDate": "2026-12-02",
    "rating": 4.8,
    "reviews": 134,
    "discount": 13,
    "category": "Tarix",
    "images": [
      "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1200&q=80"
    ],
    "description": "Qadimgi Rim tarixi bilan boy sayohat: Kolizey, Vatikan, Pantheon, Rim forumi va mashhur tarixiy maskanlar.",
    "highlights": [
      "Kolizey",
      "Vatikan",
      "Rim forumi",
      "Fontana di Trevi",
      "Pantheon"
    ],
    "included": ["Mehmonxona", "Nonushta", "Gid", "Viza", "Transfer"],
    "notIncluded": ["Ovqatlar", "Shaxsiy xarajatlar"],
    "itinerary": [
      {
        "day": 1,
        "title": "Kelish",
        "activities": ["Transfer", "Piazza Navona"]
      },
      {
        "day": 2,
        "title": "Kolizey",
        "activities": ["Kolizey", "Forum Romanum"]
      },
      {
        "day": 3,
        "title": "Vatikan",
        "activities": ["Sankt-Peter Bazilikasi", "Vatikan muzeylari"]
      },
      {
        "day": 4,
        "title": "Shaharna tadqiq",
        "activities": ["Trevi", "Pantheon"]
      },
      { "day": 5, "title": "Xayrlashuv", "activities": ["Transfer"] }
    ],
    "facilities": [
      { "name": "Mehmonxona", "icon": "🏨" },
      { "name": "Transfer", "icon": "🚗" },
      { "name": "Gid", "icon": "👤" },
      { "name": "Viza", "icon": "📄" }
    ]
  }
]


for tour_data in data:
    # Agency va Category
    agency_obj, _ = Agency.objects.get_or_create(name=tour_data["agency"])
    category_obj, _ = Category.objects.get_or_create(name=tour_data["category"])

    # Tour
    tour_obj = Tour.objects.create(
        title=tour_data["title"],
        agency=agency_obj,
        location=tour_data["location"],
        price=tour_data["price"],
        original_price=tour_data["originalPrice"],
        traveling_date=datetime.strptime(tour_data["travelingDate"], "%Y-%m-%d").date(),
        rating=tour_data["rating"],
        reviews=tour_data["reviews"],
        discount=tour_data["discount"],
        category=category_obj,
        description=tour_data["description"],
        featured=tour_data.get("featured", False)
    )

    # Images
    for img_url in tour_data.get("images", []):
        TourImage.objects.create(tour=tour_obj, url=img_url)

    # Highlights
    for highlight in tour_data.get("highlights", []):
        Highlight.objects.create(tour=tour_obj, text=highlight)

    # Included
    for inc in tour_data.get("included", []):
        IncludedItem.objects.create(tour=tour_obj, text=inc)

    # Not included
    for not_inc in tour_data.get("notIncluded", []):
        NotIncludedItem.objects.create(tour=tour_obj, text=not_inc)

    # Itinerary
    for day_data in tour_data.get("itinerary", []):
        day_obj = ItineraryDay.objects.create(
            tour=tour_obj,
            day=day_data["day"],
            title=day_data["title"]
        )
        for activity in day_data.get("activities", []):
            ItineraryActivity.objects.create(itinerary_day=day_obj, activity=activity)

    # Facilities
    for fac in tour_data.get("facilities", []):
        Facility.objects.create(tour=tour_obj, name=fac["name"], icon=fac.get("icon", ""))

print("Tours imported successfully!")
