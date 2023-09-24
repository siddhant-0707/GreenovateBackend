# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import TipsSerializer
from .models import Factor, Emissionrecord, Tips, Organization
from django.db.models import Sum
from rest_framework import status

@api_view(['GET'])
def get_emission_delta_tips(request, org_id, year1, year2):
    try:
        organisation = Organization.objects.get(id=org_id)
    except Organization.DoesNotExist:
        return Response({"error": "Organisation not found"}, status=404)

    factors = Factor.objects.all()
    max_delta = 0
    max_delta_factors = []

    for factor in factors:

        emission_year1 = Emissionrecord.objects.filter(
            organization=organisation,
            subsubfactor__sub_factor__factor=factor,
            record_year=year1
        ).aggregate(total_emission=Sum('net_emission'))['total_emission'] or 0

        emission_year2 = Emissionrecord.objects.filter(
            organization=organisation,
            subsubfactor__sub_factor__factor=factor,
            record_year=year2
        ).aggregate(total_emission=Sum('net_emission'))['total_emission'] or 0


        delta = abs(emission_year2 - emission_year1)

        if delta > max_delta:
            max_delta = delta
            max_delta_factors.append(factor)


        if len(max_delta_factors) > 2:
            max_delta_factors.remove(min(max_delta_factors, key=lambda f: abs(
                Emissionrecord.objects.filter(
                    organisation=organisation,
                    subsubfactor__sub_factor__factor=f,
                    record_year=year2
                ).aggregate(total_emission=Sum('net_emission'))['total_emission'] or 0 -
                Emissionrecord.objects.filter(
                    organisation=organisation,
                    subsubfactor__sub_factor__factor=f,
                    record_year=year1
                ).aggregate(total_emission=Sum('net_emission'))['total_emission'] or 0
            )))


    tips_for_factors = Tips.objects.filter(factor__in=max_delta_factors)
    tips_data = [
        {
            "factor": tip.factor.name, 
            "tip": tip.tip,
            "a": tip.desc_1,
            "b": tip.desc_2,
            "c": tip.desc_3,
            "d": tip.desc_4,
            "reduction_message": f"If you plan to implement the following suggested emission reduction stratergy, you will be able to notice your emissions level drop to {emission_year2 - (emission_year2 * (tip.potential_reduction_percentage / 100))}"
        }
        for tip in tips_for_factors
    ]

    return Response({"tips": tips_data}, status=200)



@api_view(['POST'])
def create_tip(request):
    if request.method == 'POST':
        serializer = TipsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
