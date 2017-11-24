# Chocolate sales email notifications

![Dark 85% Green & Blacks Chocolate](http://i6.goodness-direct.co.uk/d/591836b.jpg)

---

## Overview

Simple python script that runs on a heroku scheduled worker - sending an email to a mailgun mailing list if green & blacks chocolate is on sale.

Uses DynamoDB to store result of previous scheduled worker that way we do not keep sending emails about the same chocolate sale. The sale has to end before the emails are sent again. Little bit over engineered but hey, it's free!


## Technology Stack
- Python 3
- Heroku Work Scheduler
- AWS DynamoDB
- Mailgun

## Notes
- For sandbox mailgun domains you can't send an email to whole mailing list AFAIK. Current workaround is to send an email to each individual using a loop.
- Have to use some kind of persistant storage to, i.e. DynamoDB, to determine whether or not we have recently sent an email about the same sale.
- Coles API endpoint and object retrieval is hardcoded, don't know how often / if this changes
