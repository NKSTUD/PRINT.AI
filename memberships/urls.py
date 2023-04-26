from django.urls import path

from memberships.views import membershipsView, checkoutView, checkoutSuccess, webhook, cancelSubscription, \
    resumeSubscription, UpdateProfileView, customer_portal

urlpatterns = [
    path('pricing/', membershipsView, name='pricing'),
    path('checkout/', checkoutView, name='checkout'),
    path('success/', checkoutSuccess, name='success'),
    path('stripe_webhook/', webhook, name='webhook'),
    path('cancel-subscription/', cancelSubscription, name='cancel-subscription'),
    path('resume-subscription/', resumeSubscription, name='resume-subscription'),
    path('update_profile', UpdateProfileView.as_view(), name='update-profile'),
    path('customer_portal', customer_portal, name='customer_portal'),

]
