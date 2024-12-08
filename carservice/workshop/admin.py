from django.contrib import admin
from .models import Service, Client, Mechanic, Box, CarRepairBooking


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'discount')


@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty')


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('number', 'available_spots')


@admin.register(CarRepairBooking)
class CarRepairBookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'mechanic', 'box', 'booking_time', 'total_price')
