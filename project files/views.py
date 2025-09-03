from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Campaign, Donation, Volunteer
from .serializers import CampaignSerializer, DonationSerializer, VolunteerSerializer

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .forms import CampaignForm
import qrcode
import io
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Home Page
def home(request):
    return HttpResponse("Welcome to the Charity Funding Platform")

# Create a campaign
def campaign_create(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = CampaignForm()
    return render(request, "campaign_form.html", {"form": form})

# Campaign detail page
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    return render(request, "campaign_detail.html", {"campaign": campaign})


def campaign_qr_refresh(request, pk):
    # Get campaign by primary key
    campaign = get_object_or_404(Campaign, pk=pk)

    # Example: campaign donation URL (you can replace with real payment link later)
    donation_url = f"http://127.0.0.1:8000/campaign/{campaign.id}/donate/"

    # Generate QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(donation_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to HTTP response (PNG)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type="image/png")


def verify_donation(request, pk):
    """
    A simple donation verification view.
    You can later extend it (e.g., check payment gateway, confirmation, etc.).
    """
    donation = get_object_or_404(Donation, pk=pk)

    # Example logic: mark as verified if amount > 0
    verified = donation.amount > 0

    return JsonResponse({
        "donation_id": donation.id,
        "donor_name": donation.donor_name,
        "amount": str(donation.amount),
        "verified": verified
    })


@api_view(['POST'])
def volunteer_set_availability(request, pk):
    """
    API endpoint to update a volunteer's availability.
    Example: PATCH /volunteer/1/avail/  with JSON { "available": true }
    """
    if request.method == "PATCH" or request.method == "POST":
        volunteer = get_object_or_404(Volunteer, pk=pk)

        import json
        try:
            body = json.loads(request.body)
            available = body.get("available", None)
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if available is not None:
            volunteer.available = available
            volunteer.save()
            return JsonResponse({
                "volunteer_id": volunteer.id,
                "name": volunteer.name,
                "available": volunteer.available
            })
        else:
            return JsonResponse({"error": "Missing 'available' field"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)
# Create campaign
@api_view(['POST'])  
def create_campaign(request):
        return Response({"message": "Campaign created"})


# List campaigns
@api_view(['GET'])
def list_campaigns(request):
    campaigns = Campaign.objects.all()
    serializer = CampaignSerializer(campaigns, many=True)
    return Response(serializer.data)

# Donate to a campaign
@api_view(['POST'])
def donate(request):
    serializer = DonationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Volunteer registration
@api_view(['POST'])
def volunteer(request):
    serializer = VolunteerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
