from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe


@require_POST
@csrf_exempt
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
        return HttpResponse(content=e, status=400)

    # WH handler
    handler = StripeWH_Handler(request)

    # map events to handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_success,
        'payment_intent.payment_failed': handler.handle_payment_fail
    }

    # get webhook type
    event_type = event["type"]

    # use generic handler if no specific one in the event_map
    event_handler = event_map.get(event_type, handler.handle_event)

    # call the handler
    response = event_handler(event)
    return response
