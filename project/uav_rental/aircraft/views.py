from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Part, Team, Personnel, Aircraft
from .serializers import PartSerializer, TeamSerializer, PersonnelSerializer, AircraftSerializer

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

    def create(self, request, *args, **kwargs):
        team_name = request.data.get('team')  # Team creating the part
        part_name = request.data.get('name')  # Part being created
        aircraft_type = request.data.get('aircraft_type')

        # Ensure teams can only produce their assigned parts
        if not self.team_can_produce_part(team_name, part_name):
            return Response({"error": f"{team_name} cannot produce {part_name}"}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed to create the part
        return super().create(request, *args, **kwargs)

    def team_can_produce_part(self, team_name, part_name):
        team_part_map = {
            'Kanat Takımı': 'Kanat',
            'Gövde Takımı': 'Gövde',
            'Kuyruk Takımı': 'Kuyruk',
            'Aviyonik Takımı': 'Aviyonik',
        }
        return team_part_map.get(team_name) == part_name

    def destroy(self, request, *args, **kwargs):
        # Treat 'delete' as sending parts to recycling
        part = self.get_object()
        part.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

    def create(self, request, *args, **kwargs):
        # Retrieve the parts that will be used for the assembly
        wing_id = request.data.get('wing')
        body_id = request.data.get('body')
        tail_id = request.data.get('tail')
        avionic_id = request.data.get('avionic')

        wing = Part.objects.get(id=wing_id)
        body = Part.objects.get(id=body_id)
        tail = Part.objects.get(id=tail_id)
        avionic = Part.objects.get(id=avionic_id)

        # Ensure all parts belong to the same aircraft type
        aircraft_type = request.data.get('type')
        if not all(part.aircraft_type == aircraft_type for part in [wing, body, tail, avionic]):
            return Response({"error": "All parts must belong to the same aircraft type"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the parts are available in stock (quantity > 0)
        for part in [wing, body, tail, avionic]:
            if part.quantity <= 0:
                return Response({"error": f"Part {part.name} is out of stock"}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct part quantity from inventory after usage
        wing.quantity -= 1
        body.quantity -= 1
        tail.quantity -= 1
        avionic.quantity -= 1

        # Save updated quantities
        wing.save()
        body.save()
        tail.save()
        avionic.save()

        # Proceed to assemble the aircraft
        return super().create(request, *args, **kwargs)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PersonnelViewSet(viewsets.ModelViewSet):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer    