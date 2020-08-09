/* Core logic/payment flow for this comes from here:
        https://stripe.com/docs/payments/accept-a-payment
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#012345',
        fontFamily: '"Roboto',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#6789ab'
        }
    },
    invalid: {
        color: '#cdef01',
        iconcolor: '#234567'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  card.update({'disabled': true});
  $().attr('disabled', true);
  $().fadeToggle(100);
  $().fadeToggle(100);
  var saveInfo = Boolean($().attr('checked'));
  // csrf token from form
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var postData = {
      'csrfmiddlewaretoken': csrfToken,
      'client_secret': clientSecret,
      'save_info': saveInfo
  };
  var url = '/checkout/cache_data/';

  $.post(url, postData).done(function() {
      stripe.confirmCardPayment(clientSecret, {
          payment_method: {
              card: card,
              billing_details: {
                  name: $.trim(form.full_name.value),
                  email: $.trim(form.email.value),
                  phone: $.trim(form.phone_no.value),
                  address: {
                      line1: $.trim(form.street1.value),
                      line2: $.trim(form.street2.value),
                      city: $.trim(form.town_city.value),
                      state: $.trim(form.county.value),
                      country: $.trim(form.country.value),
                  }
              }
          },
          shipping: {
              name: $.trim(form.full_name.value),
              phone: $.trim(form.phone_no.value),
              address: {
                  line1: $.trim(form.street1.value),
                  line2: $.trim(form.street2.value),
                  city: $.trim(form.town_city.value),
                  state: $.trim(form.county.value),
                  postal_code: $.trim(form.post_code.value),
                  country: $.trim(form.country.value),
              }
          },
      }).then(function(result) {
          if (result.error) {
              var errorDiv = document.getElementById('card-errors');
              var html = `
                <span class="" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>$.{result.error.message}</span>
              `;
              $(errorDiv).html(html);
              $().fadeToggle(100);
              $().fadeToggle(100);
              card.update({'disabled': false});
          } else {
              if (result.paymentIntent.status === 'succeeded') {
                  form.submit();
              }
          }
      });
  }).fail(function() {
      location.reload();
  })
});