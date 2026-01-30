# API Credentials Configuration

## M-Pesa Daraja API

The following credentials have been configured in `settings.py`:

- **Consumer Key (CLIENT ID)**: R48HC6Rknl7vmW6YfJ2gjf-ayc5medeCpZfLNuW-iuU
- **Consumer Secret (CLIENT SECRET)**: --jgwMLZQcb4Q-a5MA0xMi-lhhteG0mhoCngO7LUgwY
- **Shortcode / Till (production)**: K217328
- **Passkey (API KEY)**: f09c5e6a1658b952652dca36684dc02951d60c8a (production)
- **Till Number (display)**: K217328 (live); override with MPESA_TILL_NUMBER env if needed
- **Environment**: production (default in code); set KOPOKOPO_ENVIRONMENT for sandbox

## Google Maps API

- **API Key**: AIzaSyCWRd5iIRByvjiazilDc4RZywsEf_XR614

## Note

These credentials are now hardcoded in `settings.py` as defaults. You can still override them using environment variables in your `.env` file if needed.

For production, make sure to:
1. Use production M-Pesa credentials
2. Set `MPESA_ENVIRONMENT = 'production'`
3. Configure proper callback URLs
4. Restrict Google Maps API key to your domain

