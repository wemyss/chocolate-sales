# Chocolate sales email notifications

Simple python script that runs on a heroku scheduled worker - sending an email to a mailgun mailing list if green & blacks chocolate is on sale.

Uses DynamoDB to store result of previous scheduled worker that way we do not keep sending emails about the same chocolate sale. The sale has to end before the emails are sent again. Little bit over engineered but hey, it's free!
