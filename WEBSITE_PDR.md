# PAKA HOME Website – Page Design Reference (PDR)

## Overview

This document describes the design and content structure for the PAKA HOME public website, ensuring a professional, eye-catching presentation with clear information hierarchy.

---

## 1. Design Principles

- **Brand consistency**: Orange (#FCA311) and blue (#4A90E2) gradients, black accents, white backgrounds.
- **Clarity**: Section badges, clear headings, and short paragraphs for quick scanning.
- **Trust**: Partnership section, process steps, and contact/WhatsApp access build credibility.
- **Mobile-first**: Responsive layout; WhatsApp widget and CTAs remain accessible on small screens.

---

## 2. Page Structure (Landing)

| Order | Section | Purpose |
|-------|---------|---------|
| 1 | **Hero** | Main value proposition: fast parcel delivery, CTA (Get Started / Book Now). |
| 2 | **Our Services** | Three core offerings: Door to Door, Last Mile, Special Parcel Delivery. |
| 3 | **How It Works** | Generic 3-step flow: Place Order → Pay → Track & Receive. |
| 4 | **Last Mile Delivery Process** | 4-step process for last mile (mark parcel → driver assigned → notified + tracking → exact delivery). |
| 5 | **Partnership** | Message that PAKA partners with Saccos/companies for last mile door-to-door on their behalf. |
| 6 | **Pricing** | Nairobi KES 150 / Nationwide KES 300. |
| 7 | **Contact** | Phone, M-Pesa Till, office location. |

---

## 3. Components

### 3.1 WhatsApp Floating Widget

- **Position**: Fixed, bottom-right (24px from edges).
- **Appearance**: Green (#25D366) circle, WhatsApp icon, hover scale + tooltip “Chat with us on WhatsApp”.
- **Action**: Links to `https://wa.me/254792044622` (opens in new tab).
- **Scope**: Included in `base.html` so it appears on all pages.

### 3.2 Services Section

- **Badge**: “What We Offer”.
- **Headline**: “Our Services”.
- **Cards** (3):
  1. **Door to Door Parcel Delivery** – Pickup and delivery from/to doorstep; no depot visits.
  2. **Last Mile Parcel Delivery** – Final leg from partner depots to exact address; real-time tracking.
  3. **Special Parcel Delivery** – Fragile, high-value, time-sensitive; white-glove style service.

- **Style**: Card hover (lift + top border gradient), icon in gradient box.

### 3.3 Last Mile Process (4 Steps)

- **Badge**: “Process”.
- **Headline**: “How Last Mile Delivery Works”.
- **Subtitle**: From partner depot to exact destination.
- **Steps**:
  1. **Mark for PAKA HOME** – Client indicates parcel is under PAKA HOME care for last mile (until exact location).
  2. **Driver Assigned** – PAKA assigns driver to pick up as soon as parcel arrives at Sacco/depot.
  3. **You Get Notified** – Client notified and given tracking number for online tracking.
  4. **Exact Destination Delivery** – Parcel delivered to exact address (apartment, office, gate).

- **Style**: Dark blue gradient background; step cards with glass effect and orange step numbers.

### 3.4 Partnership Section

- **Badge**: “Partnership”.
- **Headline**: “Trusted Last Mile Partner”.
- **Message**: Partnered with parcel delivery Saccos/companies; PAKA handles **last mile door-to-door delivery** on their behalf.
- **Body**: When parcels arrive at partners’ depots, PAKA assigns driver, notifies client with tracking, and delivers to exact destination; partners offer true door-to-door while PAKA specializes in the final leg.

- **Style**: Light grey background; single card with orange left border and handshake icon.

---

## 4. Navigation & Footer

- **Navbar**: “Services” link → `/#services` (smooth scroll on home).
- **Footer Quick Links**: Home, Our Services (`/#services`), Last Mile Process (`/#last-mile`), Partners (`/#partners`), Track Order, Careers, Terms.
- **Smooth scroll**: `html { scroll-behavior: smooth; }` in base template for anchor links.

---

## 5. Content Tone

- **Professional**: Clear, concise copy; avoid jargon.
- **Action-oriented**: “We collect,” “We deliver,” “You get notified.”
- **Trust**: “Partnered with,” “Trusted Last Mile Partner,” “exact destination.”

---

## 6. Contact & Support

- **Phone**: 0792-044-622 (displayed in navbar and footer).
- **WhatsApp**: Same number via floating widget (254792044622).
- **Location**: Nairobi CBD, Mfangano Street, Ndaragwa Hse, Mezanine MF22.

---

## 7. File Changes Summary

| File | Changes |
|------|---------|
| `templates/base.html` | WhatsApp widget (HTML + CSS), `{% load static %}`, Services nav link, footer anchor links, smooth scroll. |
| `templates/landing.html` | Our Services section, Last Mile Process (4 steps), Partnership section; CSS for service cards, last mile steps, partnership card; hero subtitle updated. |

---

*Last updated: January 2025*
