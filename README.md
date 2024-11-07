Simple Calendar API
==================
Simple Calendar API acts as a backend server and hosts the endpoints for a simple calendar app. <br/>
<br/>
It is a creative playground for Julie to hone her backend skills and experiment with some new ideas. <br/>
Why a calendar? Julie is passionate about staying organized, and her calendar app serves as the foundation for her daily routines and tasks.<br/>
<br/>

Primary Calendar Features:
------------
- Schedule activities / tasks on a specific day & time (WIP)
- User profile (WIP)

Future Feature Ideas:
------------
- To-do list feature with schedulable tasks


Django API Starter
==================

This starter template was created by [Input Logic](https://www.inputlogic.ca/).

Requirements
------------
- [Docker (Desktop)](https://www.docker.com/products/docker-desktop/)


Versions
--------
- Python 3.11.x
- Django 4.1.x
- Postgres 15.x


Local Development
-----------------

To run the project via Docker, do:

```
$ make run
```
This will handle building the initial image and starting the project. If you change any system
level files like `requirements.txt` make sure you re-build the image with:

```
$ make build
```

If you want to run commands on the container such as `./manage.py <command>`, do:

```
$ make shell
```

This will open a bash shell on the web container. 


Integrations
------------
This section is meant to outline integrations and their purpose.

- [Postmark](https://postmarkapp.com) for sending emails.
- [Firebase](https://firebase.google.com) for sending push notifications to mobile.
- [Sentry](https://sentry.io) for tracking Django errors.
- [Stripe](https://stripe.com) for handling payments.


Additional
----------
This section is meant for project-specific logic. Include a [Loom](https://www.loom.com) if more detail is required.

### Stripe
We use Stripe's subscription model to bill clients on a monthly or annual basis. Each plan includes a 14 day free trial.

- [Loom walkthrough](https://loom.com)
- All payment logic is stored on Stripe.
- Our database only stores client and subscription ids, nothing else.
- All payment logic is handled via [webhooks](https://stripe.com/docs/billing/subscriptions/webhooks).
