# Readme

This Python script checks for updates in a HTTP file by doing an HTTP HEAD request, so it doesn't need to download the entire file to check the last-updated HTTP header.

The check will be performed every 60 seconds by default.

Once there is a change this programs sends an email notifying the update.

## Instalation
### Libraries
`pip install dotenv`

`pip install sendgrid`

`pip install pytz`

### SendGrid Configuration
Enviromental variables should be stored in a file called .env that should look as follows:

```
export SENDGRID_API_KEY='sendgrid_api_key'
export SENDGRID_FROM_EMAIL='noreply@domain.com'
export SENDGRID_TO_EMAIL='to@domain.com'
```
### Execution
`python check_updates.py "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/678x678.jpg"`