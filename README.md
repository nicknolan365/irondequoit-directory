# Irondequoit Directory

A fast, free-to-host local business directory for Irondequoit, NY. Built with [Hugo](https://gohugo.io/) and designed for deployment on Cloudflare Pages.

---

## Quick Start

```bash
cd irondequoit-directory
hugo server -D
```

Open `http://localhost:1313` in your browser.

---

## Adding a Single Business

```bash
hugo new businesses/business-name-here.md
```

Open the file at `content/businesses/business-name-here.md` and fill in the front matter:

```yaml
---
title: "Business Name"
tagline: "One-line description"
description: "Full description paragraph."
phone: "(585) 555-1234"
address: "123 Ridge Road, Rochester, NY 14622"
website: "https://example.com"
email: ""
image: "business-photo.jpg"           # Place file in static/images/businesses/
premium: false                         # true = featured + do-follow link
categories:
  - "Restaurants"                      # One of the 9 main categories
subcategories:
  - "Pizza"                            # One subcategory
hours:
  sunday: "Closed"
  monday: "8AM–5PM"
  tuesday: "8AM–5PM"
  wednesday: "8AM–5PM"
  thursday: "8AM–5PM"
  friday: "8AM–5PM"
  saturday: "9AM–1PM"
---
```

## Batch Importing from CSV

1. Fill out a CSV with columns matching `sample-businesses.csv`
2. Run:

```bash
python3 import-businesses.py your-file.csv
```

3. To overwrite existing files:

```bash
python3 import-businesses.py your-file.csv --overwrite
```

---

## Adding Photos

1. Place the image file in `static/images/businesses/`
2. Set the `image` field in the business front matter to the filename:

```yaml
image: "jc-automotive.jpg"
```

Supported formats: JPG, PNG, WebP. Recommended size: 800x500px minimum.
If no image is set, a branded placeholder with the category icon will display.

---

## Premium Listings

Set `premium: true` in a business's front matter. Premium businesses get:

- ⭐ **Featured badge** on their card and detail page
- Listed in the **Featured Businesses** section on the homepage
- Listed in the **Featured** section on their category page
- **Do-follow link** to their website (regular listings get nofollow)
- **Priority ranking** in search results

---

## Categories

| Category              | Subcategories |
|-----------------------|---------------|
| Restaurants           | Sit-Down Dining, Pizza, Coffee & Bakeries, Fast Food & Takeout, Bars & Pubs |
| Home Services         | Plumbing, Electrical, HVAC, Landscaping & Lawn Care, Cleaning, Roofing & Exteriors, General Contractors |
| Shopping              | Grocery & Convenience, Clothing & Accessories, Gift & Specialty, Hardware & Home, Pet Supplies |
| Health & Wellness     | Medical & Doctors, Dental, Chiropractic & Physical Therapy, Mental Health, Pharmacy, Vision Care, Fitness & Gyms |
| Salons & Barbers      | Hair Salons, Barber Shops, Nails & Spa |
| Professional Services | Tax & Accounting, Legal, Insurance, Real Estate, Financial Planning |
| Auto & Repairs        | Auto Repair, Body Shops, Tire & Quick Service, Car Wash, Dealerships |
| Parks & Outdoor       | Parks, Trails & Nature, Sports Fields, Waterfront |
| Activities            | Arts & Culture, Entertainment & Events, Youth & Family, Community Organizations |

To add or modify categories, edit `data/categories.yaml` and update `hugo.toml` menu entries.

---

## Deploying to Cloudflare Pages

Same process as Steel AF:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/irondequoit-directory.git
git branch -M main
git push -u origin main
```

In Cloudflare dashboard: **Workers & Pages → Create → Pages → Connect to Git**

Build settings:
- **Framework preset:** Hugo
- **Build command:** `hugo --minify`
- **Output directory:** `public`
- **Environment variable:** `HUGO_VERSION` = `0.145.0`

Add `irondequoitdirectory.com` as a custom domain.

---

## Publishing Workflow

Edit or add content, then:

```bash
git add .
git commit -m "Add new businesses"
git push
```

Cloudflare rebuilds automatically. Live in ~30 seconds.

---

## Project Structure

```
irondequoit-directory/
├── archetypes/businesses/    # Template for new business pages
├── content/businesses/       # All business markdown files
├── data/categories.yaml      # Category/subcategory definitions
├── layouts/
│   ├── _default/baseof.html  # Base HTML wrapper
│   ├── businesses/           # Business list + single page templates
│   ├── categories/           # Category listing templates
│   ├── subcategories/        # Subcategory listing templates
│   ├── partials/             # Header, footer, business card
│   └── index.html            # Homepage
├── static/
│   ├── css/style.css         # Stylesheet (brand colors, fonts)
│   ├── js/search.js          # Client-side search
│   └── images/businesses/    # Business photos
├── hugo.toml                 # Site config
├── import-businesses.py      # CSV batch import script
├── sample-businesses.csv     # CSV format template
└── wrangler.toml             # Cloudflare build config
```

## Cost

**$0/month.** Hugo is free, Cloudflare Pages free tier is more than enough. Only cost is domain renewal.
