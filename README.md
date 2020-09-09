# AstroPrint.com
##### Final Milestone Project by Seán Carley
This e-commerce website is intended to allow photographers sell their work 
without the photographer having to host and manage their own site. The site 
will allow users to sign-up and upload a gallery of images that other users 
can view, and purchse. Users are able to leave a comment about any images that 
they purchase.

## UX
AstroPrint.com is intended to provide Astro-Photographers a platform to display 
their work, and allow other users be able to buy the work. The site will also 
allow the users to be able to leave a rating and comments about the sellers 
work etc...

### User Stories
#### Unregistered User:
- As an unregistered user, I would like to:
  - [x] Get information as to the purpose of the website
  - [x] View a selection of the available works that can be purchased
  - [x] Have the option to sign up to the website

#### Registered User (seller):
- As a registered seller user, I would like to:
  - [x] Be able to log in to my account
  - [x] Be able to update my account details
  - [x] See the list of works that I have made available on the site
  - [x] See the number of sales of each of my items
  - [x] Be able to upload new items
  - [x] Be able to remove items that are no longer for sale
  - [x] Be able to set/modify the selling price
  - [x] Have the same functionality as a customer to search, view, and purchase from other sellers on the site.
#### Registered User (buyer):
- As a registered seller user, I would like to:
  - [x] Be able to log in to my account
  - [x] Be able to update my account details
  - [x] Be able to see my purchase history
  - [x] Be able to see my current shopping basket
  - [x] Be able to search for images
#### Admin User:
- As an admin user, I want to be able to:
  - [x] Log in to the site as a Admin user
  - [x] Be able to view all the images available
  - [x] Be able to remove any images
  - [x] Be able to review comments left by customers
  - [x] Be able to remove comments left by customers

## Features
[AstroPrint.com](https://sc-finalmilestone-astroprint.herokuapp.com/) allows 
users to view image. Images can be searched for by a number of criteria. Users 
can also register on the site, wich provides a means to save their details, 
including, address, email, previous orders. Users can also select the option 
to allow them to upload images, with the intention to sell them. Users that 
purchase images can leave comments and a rating for the image. This rating is 
used to determine the overall rating of the image on the site. I would have 
liked to avail of the functionality to accept a payment in Stripe and then 
forward part of this payment to another entity. This would allow for the image 
seller to receive their portion of the payment, and forward the commission to 
site owner.

## Technology Used
1. HTML - Used to define the structure of webpages
1. CSS - Used to style web pages
1. Bootstrap - Framework to simplify webpage design
1. JavaScript - A lightweight, interpreted, or just-in-time compiled 
   programming language
   * Fancyapp - JavaScript lightbox library for presenting various types of media.
                 Responsive, touch-enabled and customizable.
1. JQuery - A fast, small, and feature-rich JavaScript library
1. Python - A programming language that lets you work more quickly 
   and integrate your systems more effectively
1. Django - High-level Python Web framework that encourages rapid development 
   and clean, pragmatic design
1. Heroku - a platform as a service (PaaS) that enables developers to build, 
   run, and operate applications entirely in the cloud.
   * PostgreSQL - Powerful, open source object-relational database system
1. Amazon Web Services (AWS) - Comprehensive, evolving cloud computing 
   platform provided by Amazon that includes a mixture of infrastructure as a 
   service (IaaS), platform as a service (PaaS) and packaged software as a 
   service (SaaS) offerings.

## Testing
Throughout the development of the project I used various techniques to test 
and troubleshoot functionlality. To trouble-shoot numerous issues, I used 
temporary print statements to show what information was actually being passed by 
the application versus what should heve been sent. 

This allowed me to single out the piece of code that was not performing as 
expected, or a conditions that was not being met. As an example, I was 
experiencing an issue where orders were being added to the order table but the 
order item was being duplicated. The issue was a typo, that caused the webhook 
to try add the order to the table, but the order number was already present. 
It would however add another instance of the image to the order. Using this 
print trouble shooting alloed me to see that the search for the order was not 
exactly matching the information passed back by the webhook.

I have also included a number of test files to double check the majority of 
the forms and view used in the application. These automated tests use the 
TestCase module.

## Deployment
This project has been made available on Heroku at the following link 
[https://sc-finalmilestone-astroprint.herokuapp.com/](https://sc-finalmilestone-astroprint.herokuapp.com/). 
A PostGres database was initiated on heroku to be used as the production 
database. To populate this database 2 fixture files were used to populate the 
Image and Image_Data tables. The Image_Data data needs to be loaded first 
followed by the Image data. I also had to manually enter the users associated 
with the images to the user table as I was unsure how to do this. 

The DATABASE_URL variable also had to be added to the heroku environment, as 
well as an IF statement in the settings.py to instruct Django to use this 
database if accessing via Heroku, or use the development SQLite database in 
the development environment, as the static files can be accessed using the 
static and media urls.

```python
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
```

A number of variables had also to be set up on Heroku for Amazon Web Services 
(AWS). These variables allow Heroku to access the Static and Media files 
stored on AWS. These variables are not needed in the development environment. 

Similarly, a number of variables had to be added for stripe. For this project 
the variables are the same for both the development and production 
environments. However, in a real-world situation, stripe provide the means for 
development and production API keys.

To store the media and static files a new bucket was created on AWS. The 
images were manually added to the media folder in this bucket, while a number 
of variables were created in the settings.py file:

```python
""" variables required to tess app to use AWS in production """
if 'USE_AWS' in os.environ:
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }
    AWS_STORAGE_BUCKET_NAME = '<aws_storage_bucket_name>'
    AWS_S3_REGION_NAME = 'eu-west-1'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATICFILES_LOCATION = '<staticfilelocation>'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIAFILES_LOCATION = '<mediafilelocation>'

    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

```

### Dev Environment Variables:
* DEVELOPMENT
* SECRET_KEY (django secret key)
* STRIPE_PRIV_KEY (private key for use with Stripe payments)
* STRIPE_PUB_KEY (public key for use with Stripe payments)
* STRIPE_WH_KEY (key for use with Stripe WebHooks)

### Prod Emvironment Variables:
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* DATABASE_URL (url for heroku PostgreSQL instance)
* EMAIL_HOST_PASS (password for email sending)
* EMAIL_HOST_USER (username for email sending)
* SECRET_KEY (django secret key)
* STRIPE_PRV_KEY (private key for use with Stripe payments)
* STRIPE_PUB_KEY (public key for use with Stripe payments)
* STRIPE_WH_KEY (key for use with Stripe WebHooks)
* USE_AWS

### Issues Experienced with Deployment to Heroku
When I was setting up the PostGres database on Heroku, I recveived an error 
ralating to an issue pushing the migrations. The issue was related to the 
changes I had made converting a column from an integer field (defined in the 
initial migration) to a boolean field. To enable the migrations to be pushed 
to the PostGRES database I had to modify the affected migration file to remove 
the column and re-add it as a boolean. From the information available, this 
issue seems to be related to Django not casting data-types, and PostgreSQL 
requiring the data-types to be cast.

```python
class Migration(migrations.Migration):

    dependencies = [
        ('images', '0019_auto_20200822_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='img_status',
        ),
        migrations.AddField(
            model_name='image',
            name='img_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='tmnl_img',
            field=models.ImageField(upload_to='user_images/', verbose_name=''),
        ),
    ]
```

## Credits
The images used in this project were obtained from the site 
[unsplash.com](https://unsplash.com/). The images on this site are unlicenced, 
and are available to use.

I used the [Django documentation](https://docs.djangoproject.com/en/3.1/) for 
inspiration, information, and troubleshooting. I also relied on 
[StackOverflow](https://stackoverflow.com/) to help understand concepts and 
troubleshooting.

Code for the displaying of the images was sourced from the 
[FancyApp](https://fancyapps.com/fancybox/3/) site.

Code relating to the Stripe functionality was sourced from the
[Stripe](https://stripe.com/en-ie) site.