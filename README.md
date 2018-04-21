# Supermarket sales email notifications

<img src="http://i6.goodness-direct.co.uk/d/591836b.jpg" alt="Dark 85% Green & Blacks Chocolate" height="300px"></img>
<img src="https://cdn0.woolworths.media/content/wowproductimages/large/516942.jpg" alt="Supercoat Active Dry Dog Food" height="300px"></img>

---

## Overview

Simple python script that runs on a heroku scheduled worker once a day - sending emails to registered users that are interested in particular items being on sale.

Uses DynamoDB to store the previous price so we don't continually send emails and we can detect price drops.

## DB layout
```js
// Users table example item
{
  email: 'my@email.com',
  item_keywords: {
    'Chocolate',
    'Dog food'
   }
}

// Items table example item
{
  name: 'Green & Blacks 85% Chocolate',
  price: 10.09
}
```


## Technology Stack
- Python 3
- Heroku Work Scheduler
- AWS DynamoDB
- Mailgun

## Notes
- For sandbox mailgun domains you can't send an email to whole mailing list AFAIK. Current workaround is to send an email to each individual using a loop.
- Have to use some kind of persistant storage to, i.e. DynamoDB, to determine whether or not we have recently sent an email about the same sale.
- Coles API endpoint and object retrieval is hardcoded, don't know how often / if this changes
