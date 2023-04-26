from django.contrib import admin
from django.contrib.admin import ModelAdmin

from memberships.models import Membership, MembershipChoices, UserMembership, Subscription


class MembershipAdmin(ModelAdmin):
    list_display = ("number_of_words", "membership_price_per_period", "membership_type")


class SubscriptionAdmin(ModelAdmin):
    list_display = ("user_membership", "active", "get_created_date", "get_next_billing_date")


admin.site.register(MembershipChoices)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(UserMembership)
admin.site.register(Subscription, SubscriptionAdmin)
