from django.contrib import admin
from .models import Part, Team, Personnel, Aircraft

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'aircraft_type', 'quantity')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('type', 'wing', 'body', 'tail', 'avionic')
