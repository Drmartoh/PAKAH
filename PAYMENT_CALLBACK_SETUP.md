# STK Push & Payment Callback Setup

## Production Callback URL

For production (KopoKopo), the webhook callback URL is:

**`https://pakahomeparceldelivery.website/api/payments/callback/`**

- Configure this URL in your **KopoKopo dashboard** (webhook / incoming payment callback).
- The callback endpoint is **CSRF-exempt** so KopoKopo can POST to it.
- It accepts **POST** only and expects JSON in KopoKopo’s incoming payment format.

## Configuration

- **`KOPOKOPO_CALLBACK_URL`** (in `pakahome/settings.py` or `.env`):  
  Default: `https://pakahomeparceldelivery.website/api/payments/callback/`

- **`KOPOKOPO_ENVIRONMENT`**: `production` uses the above callback; `sandbox` uses the request host (e.g. `http://localhost:8000/api/payments/callback/`).

## Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/payments/stkpush/` | POST | Customer (session) | Initiate M-Pesa STK push |
| `/api/payments/callback/` | POST | None (webhook) | KopoKopo payment result callback |
| `/api/payments/` | GET | Customer/Admin | List payments |

## Testing Endpoints

From project root:

```bash
python test_payment_endpoints.py
```

This checks:

- `KOPOKOPO_CALLBACK_URL` is set to pakahomeparceldelivery.website
- Callback accepts POST without CSRF (returns 400 for invalid body, not 403)
- Callback invalid JSON → 400
- Callback valid structure without order → 400
- STK push without auth → 403

## Manual Callback Test (curl)

```bash
# Should return 400 (invalid JSON)
curl -X POST https://pakahomeparceldelivery.website/api/payments/callback/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

If you get **403**, the callback is not CSRF-exempt or the host is not allowed. If you get **400**, the endpoint is reachable and processing the body.
