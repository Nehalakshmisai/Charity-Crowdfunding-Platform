from django.db import models

from django.utils.timezone import now

created_at = models.DateTimeField(auto_now_add=True, default=now)


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def progress_percent(self):
        if self.goal_amount > 0:
            return (self.raised_amount / self.goal_amount) * 100
        return 0

    def __str__(self):
        return self.title


class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    donor_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} donated {self.amount}"


class Volunteer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
