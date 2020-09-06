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

## Technology Used
1. HTML - Used to define the structure of webpages
1. CSS - Used to style web pages
1. Bootstrap - Framework to simplify webpage design
1. Fancybox - A JavaScript lightbox library for presenting various types of 
media. Responsive, touch-enabled and customizable.
1. JavaScript - A lightweight, interpreted, or just-in-time compiled 
programming language
1. JQuery - A fast, small, and feature-rich JavaScript library
1. Python - A programming language that lets you work more quickly 
and integrate your systems more effectively
1. Django - High-level Python Web framework that encourages rapid development 
and clean, pragmatic design

## Testing
Throughout the development of the project I used various techniques to test 
and troubleshoot functionlality. To trouble shoot numerous issues, I used 
temporary print statements to show what information was actually being sent by 
the application versus what should heve been sent. 

This allowed me to single out the piece of code that was not performing as 
expected. For a time I was experiencing an issue where orders were being added 
to the order table but the order item was being duplicated. The issue was a 
typo, that caused the webhook to try add the order to the table, but the order 
number was already present. It would however add another instance of the image 
to the order. Using this print trouble shooting alloed me to see that the 
search for the order was not exactly matching the webhook.

I have also included a number of test files to double check the majority of 
the forms used in the application.

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

A number of variables had also to be set up on Heroku for Amazon Web Services 
(AWS). These variables allow Heroku to access the Static and Media files 
stored on AWS. These variables are not needed in the development environment. 

Similarly, a number of variables had to be added for stripe. For this project 
the variables are the same for both the development and production 
environments. However, in a real-world situation, stripe provide the means for 
development and production API keys.

### Issues Experienced with Deployment to Heroku
When I was setting up the PostGres database on Heroku, I recveived an error 
ralating to an issue pushing the migrations. The issue was related to the 
changes I had made converting a column from an integer field to a boolean field. 
To enable the migrations to be pushed to the PostGRES database I had to modify 
the affected migration file to remove the column and re-add it as a boolean. I 
also

## Credits
