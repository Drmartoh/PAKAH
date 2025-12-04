# API Credentials Configuration

## M-Pesa Daraja API

The following credentials have been configured in `settings.py`:

- **Consumer Key (CLIENT ID)**: R48HC6Rknl7vmW6YfJ2gjf-ayc5medeCpZfLNuW-iuU
- **Consumer Secret (CLIENT SECRET)**: --jgwMLZQcb4Q-a5MA0xMi-lhhteG0mhoCngO7LUgwY
- **Shortcode**: 5630946
- **Passkey (API KEY)**: 5d3fd56fbfbc3dcb3daecbb1420bd2db1269e5c4
- **Till Number**: 5630946
- **Environment**: sandbox

## Google Maps API

- **API Key**: AIzaSyCWRd5iIRByvjiazilDc4RZywsEf_XR614

## Note

These credentials are now hardcoded in `settings.py` as defaults. You can still override them using environment variables in your `.env` file if needed.

For production, make sure to:
1. Use production M-Pesa credentials
2. Set `MPESA_ENVIRONMENT = 'production'`
3. Configure proper callback URLs
4. Restrict Google Maps API key to your domain

