# Supermarket sales email notifications

## Overview

Simple python script that runs on a aws lambda function once a day - sending emails to registered users that are interested in particular items being on sale.

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
- AWS DynamoDB
- AWS Lambda
- Mailgun

## Notes
- For sandbox mailgun domains you can't send an email to whole mailing list AFAIK. Current workaround is to send an email to each individual using a loop.
- Coles API endpoint and object retrieval is hardcoded, don't know how often / if this changes


## Woolworths Steps
1. Search for product
2. Click on product
3. Copy product stockcode from url (can also see it in networks tab - devtools)

## Coles Steps
1. Open devtools
2. Search for product
3. Click on product to go to details page
4. Find JSON api request for product (uses prefix as listed in `items.json`)
