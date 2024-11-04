from django.contrib import admin
from .models import Stock
from .models import Order
from .models import Feedback
from .models import ContactMessage
from .models import Store


# Register your models here.
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(Feedback)
admin.site.register(ContactMessage)
admin.site.register(Store)