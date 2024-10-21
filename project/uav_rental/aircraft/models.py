from django.db import models

# Define the parts model
class Part(models.Model):
    PART_CHOICES = [
        ('Kanat', 'Kanat'),  # Wing
        ('Gövde', 'Gövde'),  # Body
        ('Kuyruk', 'Kuyruk'),  # Tail
        ('Aviyonik', 'Aviyonik'),  # Avionics
    ]
    
    AIRCRAFT_CHOICES = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'AKINCI'),
        ('KIZILELMA', 'KIZILELMA'),
    ]

    name = models.CharField(max_length=100, choices=PART_CHOICES)
    aircraft_type = models.CharField(max_length=50, choices=AIRCRAFT_CHOICES)
    quantity = models.PositiveIntegerField(default=0)  # Stock quantity

    def __str__(self):
        return f"{self.name} for {self.aircraft_type}"

# Define the teams responsible for parts production and assembly
class Team(models.Model):
    TEAM_CHOICES = [
        ('Kanat Takımı', 'Kanat Takımı'),
        ('Gövde Takımı', 'Gövde Takımı'),
        ('Kuyruk Takımı', 'Kuyruk Takımı'),
        ('Aviyonik Takımı', 'Aviyonik Takımı'),
        ('Montaj Takımı', 'Montaj Takımı'),
    ]
    
    name = models.CharField(max_length=100, choices=TEAM_CHOICES)

    def __str__(self):
        return self.name

# Define the personnel model
class Personnel(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Define the aircraft model for assembly
class Aircraft(models.Model):
    AIRCRAFT_CHOICES = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'AKINCI'),
        ('KIZILELMA', 'KIZILELMA'),
    ]

    type = models.CharField(max_length=50, choices=AIRCRAFT_CHOICES)
    wing = models.OneToOneField(Part, related_name='wing_part', on_delete=models.SET_NULL, null=True)
    body = models.OneToOneField(Part, related_name='body_part', on_delete=models.SET_NULL, null=True)
    tail = models.OneToOneField(Part, related_name='tail_part', on_delete=models.SET_NULL, null=True)
    avionic = models.OneToOneField(Part, related_name='avionic_part', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.type} Aircraft"
