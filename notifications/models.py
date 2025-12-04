from django.db import models


class SMSLog(models.Model):
    """Log of SMS notifications sent"""
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"SMS to {self.phone_number} - {self.status}"

