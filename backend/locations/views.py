from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from locations.repositories.location_repository import LocationRepository


class CityListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            data = LocationRepository.get_all_cities()
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VenueListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        city_id_param = request.query_params.get('city_id')
        city_id = None

        if city_id_param is not None:
            try:
                city_id = int(city_id_param)
            except ValueError:
                return Response(
                    {"success": False, "error": "Invalid city_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            data = LocationRepository.get_all_venues(city_id=city_id)
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )