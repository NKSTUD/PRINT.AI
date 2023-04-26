from datetime import datetime

import stripe
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

MEMBERSHIP_PERIOD_CHOICES = (
    ("Month", "Month"),
    ("Year", "Year"),
    ("Custom", "Custom"),
)


class MembershipChoices(models.Model):
    name = models.CharField(max_length=255, blank=True, unique=True)

    @classmethod
    def free_membership(cls):
        free_membership, _ = cls.objects.get_or_create(name="Free")
        return free_membership

    def __str__(self):
        return self.name


class Membership(models.Model):
    membership_type = models.ForeignKey(MembershipChoices, to_field="name", on_delete=models.SET_DEFAULT,
                                        default=MembershipChoices.free_membership,
                                        verbose_name=_('Membership type'))
    membership_period = models.CharField(choices=MEMBERSHIP_PERIOD_CHOICES, max_length=200, blank=True, null=True)
    number_of_words = models.PositiveBigIntegerField(default=0, verbose_name=_('number of words'))
    price = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    stripe_plan_id = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.number_of_words} words'

    def membership_price_per_period(self):
        return f"{self.price}$ / {self.membership_period}"


class UserMembership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.email


class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=False)

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.created)

    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.current_period_end)

    @property
    def get_status(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return subscription.status

    def __str__(self):
        return f"{self.user_membership.user.email} - {self.user_membership.membership.membership_period} " \
               f" - {self.user_membership.membership.membership_type.name} "
