from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import stripe


def webhook(request):
    """ listener for webhooks from stripe """
    # keys
    wh_prv = settings.STRIPE_WH_KEY
    stripe.api_key = settings.STRIPE_PRV_KEY

    # verify WH signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_prv
        )
    except ValueError as e:
        # payload error
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # signature error
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400)

    # WH handler
    handler = StripeWH_Handler(request)
    