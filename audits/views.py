import pandas as pd

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Audit, RawRow, Activity
from .serializers import ActivitySerializer, AuditSerializer

@api_view(['POST'])
def upload_csv(request):
    file = request.FILES.get('file')
    audit_name = request.data.get('name')
    source_type = request.data.get('source_type')

    if Audit.objects.filter(name=audit_name).exists():
        return Response(
            {'error': 'Audit name already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    audit = Audit.objects.create(
        name=audit_name,
        source_type=source_type
    )

    df = pd.read_csv(file)

    for _, row in df.iterrows():
        raw_dict = row.to_dict()

        RawRow.objects.create(
            audit=audit,
            raw_data=raw_dict
        )

        amount = 0

        for value in raw_dict.values():
            if isinstance(value, (int, float)):
                amount = value
                break

        flagged = amount <= 0

        Activity.objects.create(
            audit=audit,
            category=source_type,
            amount=amount,
            unit='kWh' if source_type == 'utility' else 'L',
            scope='Scope 1' if source_type == 'sap' else 'Scope 2',
            is_flagged=flagged
        )

    return Response({'message': 'Upload successful'})

@api_view(['GET'])
def get_activities(request):
    activities = Activity.objects.all().order_by('-id')
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_audits(request):
    audits = Audit.objects.all().order_by('-id')
    serializer = AuditSerializer(audits, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def approve_activity(request, id):
    activity = Activity.objects.get(id=id)
    activity.status = 'approved'
    activity.locked = True
    activity.save()

    return Response({'message': 'approved'})

@api_view(['PATCH'])
def reject_activity(request, id):
    activity = Activity.objects.get(id=id)
    activity.status = 'rejected'
    activity.save()

    return Response({'message': 'rejected'})