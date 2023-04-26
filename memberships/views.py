import stripe
from django.contrib import messages
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from accounts.forms import SignupForm
from answer_ai import settings
from memberships.models import Membership, UserMembership, Subscription
from my_ai.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.publishable_key = settings.STRIPE_PUBLISHABLE_KEY


def membershipsView(request):
    memberships = Membership.objects.all()
    context = {'memberships': memberships}

    return render(request, 'memberships/memberships_view.html', context)


def get_user_membership(request):
    user_membership = UserMembership.objects.filter(user=request.user)
    return user_membership.first() if user_membership.exists() else None


def get_user_subscription(request, user_membership):
    user_subscription = Subscription.objects.filter(user_membership=user_membership)
    return user_subscription.first() if user_subscription.exists() else None


def is_valid_subscription(request):
    """Verify if current subscription is valid or not"""
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request, user_membership)
    remain_words = 10000 - get_user(request).number_of_words
    return user_subscription.active if user_subscription is not None else remain_words > 0


def checkoutView(request):
    membership_id = request.POST["membership_id"]
    selected_membership = get_object_or_404(Membership, stripe_plan_id=membership_id)

    """ Verify if selected membership not already exist"""
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request, user_membership)

    if (
            user_membership is not None
            and user_membership.membership == selected_membership
            and user_subscription is not None
            and user_subscription.active
    ):
        messages.info(request, f""" You have already this membership.
             Your subscription expires {user_subscription.get_next_billing_date} """)
        return HttpResponse(messages.get_messages(request), status=200)

    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
            mode='subscription',
            customer_email=request.user.email if request.user.is_authenticated else None,
            success_url=request.build_absolute_uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('pricing')),

            line_items=[
                {
                    'price': selected_membership.stripe_plan_id,
                    'quantity': 1,

                },
            ],
        )
        response = HttpResponse()
        response['HX-Redirect'] = checkout_session.url
        return response

    except Exception as e:
        print(e)
    return "Server error", 500


def get_membership(stripe_price_id):
    return get_object_or_404(Membership, stripe_plan_id=stripe_price_id)


def create_user_membership(client_reference_id, membership, stripe_customer_id):
    user_model = get_user_model()
    user = get_object_or_404(user_model, id=client_reference_id)

    user_membership, created = UserMembership.objects.get_or_create(user=user)
    user_membership.membership = membership
    user_membership.stripe_customer_id = stripe_customer_id
    user_membership.save()

    return user_membership


def create_subscription(user_membership, stripe_subscription_id):
    subscription, created = Subscription.objects.get_or_create(user_membership=user_membership)
    subscription.stripe_subscription_id = stripe_subscription_id
    subscription.active = True
    subscription.cancelled = False
    subscription.save()

    return subscription


def create_new_customer(request, stripe_session):
    client_reference_id = stripe_session.get('client_reference_id')
    stripe_customer_id = stripe_session.get('customer')
    stripe_subscription_id = stripe_session.get('subscription')
    line_items = stripe.checkout.Session.list_line_items(stripe_session.get("id"))
    stripe_price_id = line_items["data"][0]["price"]["id"]
    membership = get_membership(stripe_price_id)

    # Create UserMembership
    user_membership = create_user_membership(client_reference_id,
                                             membership, stripe_customer_id)

    return create_subscription(user_membership, stripe_subscription_id)


# This is your Stripe CLI webhook secret for testing your endpoint locally.

"""stripe listen --forward-to localhost:8000/memberships/stripe_webhook/"""


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.WEBHOOK_ENDPOINT_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == "checkout.session.completed":
        stripe_session = event['data']['object']
        create_new_customer(request, stripe_session)

    if event["type"] == 'customer.subscription.deleted':
        subscription_id = event.data.object.id
        subscription = get_object_or_404(Subscription,
                                         stripe_subscription_id=subscription_id)
        subscription.active = False
        subscription.save()

    return HttpResponse(status=200)


@login_required
def get_profile_context(request):
    user = get_user(request)
    context = {"user_number_of_words": user.number_of_words}
    if user_membership := get_user_membership(request):
        context["user_subscription"] = get_user_subscription(request, user_membership)
    else:
        credit = 10000
        context["number_of_words_remaining"] = max(credit - user.number_of_words, 0)
    return context


def cancelCheckoutSession(request):
    return redirect('pricing')


def checkoutSuccess(request):
    context = {}
    return render(request, 'memberships/success.html', context)


def cancelSubscription(request):
    modifySubscription(request, cancel_at_period_end=True,
                       message="Your subscription has been successfully cancelled!\n"
                               "You can resume it at before the end of the billing period")
    return HttpResponse(messages.get_messages(request))


def resumeSubscription(request):
    modifySubscription(request, cancel_at_period_end=False, message="Your subscription has been resumed")
    return HttpResponse(messages.get_messages(request))


def modifySubscription(request, cancel_at_period_end: bool, message: str):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request, user_membership=user_membership)
    try:
        stripe.Subscription.modify(user_subscription.stripe_subscription_id,
                                   cancel_at_period_end=cancel_at_period_end)
        messages.success(request, message)
    except stripe.error.InvalidRequestError as e:
        messages.error(request, e)
    user_subscription.cancelled = cancel_at_period_end
    user_subscription.save()


def customer_portal(request):
    """Redirect to Stripe Billing Portal"""
    session = stripe.billing_portal.Session.create(
        customer=get_user_membership(request).stripe_customer_id,
        return_url=request.build_absolute_uri(reverse('home'))
    )
    response = HttpResponse()
    response['HX-Redirect'] = session.url
    return response


class UpdateProfileView(UpdateView):
    model = User
    form_class = SignupForm
    template_name = 'memberships/profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        """Add user's memberships.Profile to accounts.UpdateProfileView.context"""
        context = super().get_context_data(**kwargs)
        context.update(get_profile_context(self.request))
        return context
