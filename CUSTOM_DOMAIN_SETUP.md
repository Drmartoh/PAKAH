# Custom domain setup: pakahomedeliveries.co.ke → PythonAnywhere

Use your domain **pakahomedeliveries.co.ke** so visitors land on your PAKA HOME app. This works on **paid** PythonAnywhere accounts.

**Recommended:** Serve the site at **www.pakahomedeliveries.co.ke** and redirect **pakahomedeliveries.co.ke** (no www) to it. That way DNS stays simple (CNAME) and both URLs work.

---

## Part 1: PythonAnywhere – point the domain to your app

### Option A: You already have the app (e.g. pakaapp.pythonanywhere.com)

1. Log in to [PythonAnywhere](https://www.pythonanywhere.com) and open the **Web** tab.
2. Find your PAKA HOME web app and click the **pencil icon** next to its name.
3. Change the domain from `pakaapp.pythonanywhere.com` to:
   ```text
   www.pakahomedeliveries.co.ke
   ```
   Use **www.pakahomedeliveries.co.ke** (with `www`), not `pakahomedeliveries.co.ke`.
4. Save. The same app (same code, WSGI, virtualenv) now serves this domain.
5. On the same Web tab you’ll see a **“Domain”** / **“DNS”** section with a **CNAME** value, e.g.:
   ```text
   webapp-12345.pythonanywhere.com
   ```
   Copy this; you’ll use it at your domain provider in Part 2.

### Option B: You’re adding the domain as a new web app

1. On the **Web** tab, click **“Add a new web app”**.
2. When asked for the domain, enter:
   ```text
   www.pakahomedeliveries.co.ke
   ```
3. Complete the wizard (Manual configuration, same Python version as your existing app).
4. In the new web app’s configuration:
   - Set **Source code** and **Working directory** to the same paths as your current app (where `manage.py` and `venv` are).
   - Set **Virtualenv** to your existing venv path.
   - Edit the **WSGI file** and use the same content as your existing app (path to project, `pakahome.settings`, `get_wsgi_application()`).
5. Copy the **CNAME** value shown for this domain (e.g. `webapp-XXXX.pythonanywhere.com`) for Part 2.

---

## Part 2: Domain provider (where you bought pakahomedeliveries.co.ke)

You need to add **one CNAME record** so that `www.pakahomedeliveries.co.ke` points to PythonAnywhere.

1. Log in to the control panel where you manage **pakahomedeliveries.co.ke** (e.g. registrar or DNS host).
2. Open **DNS** / **DNS management** / **Manage DNS records** for this domain.
3. Add a **CNAME** record:

   | Field (names vary by provider) | Value |
   |--------------------------------|--------|
   | **Name / Host / Alias**       | `www`  |
   | **Target / Points to / Value**| The CNAME from PythonAnywhere (e.g. `webapp-12345.pythonanywhere.com`) |

   - **Name** = `www` only (not `www.pakahomedeliveries.co.ke`).
   - **Target** = exactly what PythonAnywhere shows (e.g. `webapp-12345.pythonanywhere.com`), no `https://`, no trailing slash.
4. Save. DNS can take from a few minutes up to 24–48 hours to propagate.

**Optional but recommended:** Remove any existing **A** or **CNAME** record for `www` if it points somewhere else, so only this CNAME remains for `www`.

---

## Part 3: Naked domain redirect (pakahomedeliveries.co.ke → www)

So that typing **pakahomedeliveries.co.ke** (no www) also lands on your app:

1. In the **same** DNS/domain control panel, look for:
   - **“Forwarding”**, **“Redirect”**, **“URL redirect”**, or **“Domain forward”**.
2. Add a redirect:
   - **From:** `pakahomedeliveries.co.ke` (or “@” / “apex”)
   - **To:** `https://www.pakahomedeliveries.co.ke`
   - Prefer **301 (permanent)** if the option exists.
3. Save.

If your provider only supports HTTP redirect (to `http://www...`), that’s still fine for most visitors; you can add HTTPS and “Force HTTPS” on PythonAnywhere next.

---

## Part 4: HTTPS and force HTTPS (PythonAnywhere)

Do this **after** the CNAME is working and the site loads at `http://www.pakahomedeliveries.co.ke`.

1. **Web** tab → your app **www.pakahomedeliveries.co.ke**.
2. Open **“SSL certificate”** (or **“HTTPS”**).
3. Click **“Enable HTTPS”** and follow the steps to get a certificate for `www.pakahomedeliveries.co.ke`.
4. When HTTPS works, enable **“Force HTTPS”** so HTTP requests are redirected to HTTPS.

References:
- [Setting up HTTPS](https://help.pythonanywhere.com/pages/HTTPSSetup)
- [Forcing HTTPS](https://help.pythonanywhere.com/pages/ForcingHTTPS)

---

## Part 5: App settings (already done in this project)

Your Django app is already allowed to serve this domain. In `pakahome/settings.py`:

- `ALLOWED_HOSTS` includes `pakahomedeliveries.co.ke` and `www.pakahomedeliveries.co.ke`.

No code change is required for the domain to be accepted. If you use a `.env` or environment variables, you can optionally set:

```bash
ALLOWED_HOSTS=pakahomedeliveries.co.ke,www.pakahomedeliveries.co.ke
```

---

## Checklist

| Step | Where | Action |
|------|--------|--------|
| 1 | PythonAnywhere | Set domain to **www.pakahomedeliveries.co.ke** (pencil icon or new web app). |
| 2 | PythonAnywhere | Copy the **CNAME** value (e.g. `webapp-XXXX.pythonanywhere.com`). |
| 3 | Domain provider | Add **CNAME**: name `www` → target = that CNAME value. |
| 4 | Domain provider | Set **redirect**: pakahomedeliveries.co.ke → https://www.pakahomedeliveries.co.ke. |
| 5 | PythonAnywhere | After DNS works: **Enable HTTPS** then **Force HTTPS**. |
| 6 | Browser | Test: **www.pakahomedeliveries.co.ke** and **pakahomedeliveries.co.ke** both open the app. |

---

## Quick reference

- **Official help:** [Custom domains](https://help.pythonanywhere.com/pages/CustomDomains/), [Using a new domain for existing webapp](https://help.pythonanywhere.com/pages/UsingANewDomainForExistingWebApp/), [Naked domains](https://help.pythonanywhere.com/pages/NakedDomains).
- **CNAME:** Only for **www** (e.g. `www.pakahomedeliveries.co.ke`). Do **not** use CNAME for the naked domain `pakahomedeliveries.co.ke`; use redirect/forwarding instead.
- **Testing DNS:** After saving the CNAME, you can check propagation at [whatsmydns.net](https://www.whatsmydns.net/) (query **CNAME** for `www.pakahomedeliveries.co.ke`). PythonAnywhere’s Web tab will also show if the CNAME is correct.

Once the CNAME and redirect are in place and HTTPS is enabled, typing **pakahomedeliveries.co.ke** or **www.pakahomedeliveries.co.ke** will land users on your PAKA HOME web app.
