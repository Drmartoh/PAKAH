from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .services import send_sms_notification
from .models import SMSLog
from rest_framework import generics
from django.db.models import Q


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_sms(request):
    """Send SMS notification (admin only)"""
    if request.user.role != 'admin':
        return Response(
            {'error': 'Only admins can send SMS'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    phone_number = request.data.get('phone_number')
    message = request.data.get('message')
    
    if not phone_number or not message:
        return Response(
            {'error': 'phone_number and message are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    success = send_sms_notification(phone_number, message)
    
    if success:
        return Response({'message': 'SMS sent successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Failed to send SMS'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class SMSLogListView(generics.ListAPIView):
    """List SMS logs (admin only)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'admin':
            return SMSLog.objects.none()
        return SMSLog.objects.all().order_by('-created_at')

