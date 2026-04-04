#!/usr/bin/env python3
"""
CSV to Hugo Business Importer
==============================
Converts a CSV file of businesses into Hugo markdown content files.

Usage:
    python3 import-businesses.py businesses.csv

CSV Columns (header row required):
    name, tagline, description, phone, address, website, email,
    category, subcategory, premium,
    hours_sun, hours_mon, hours_tue, hours_wed, hours_thu, hours_fri, hours_sat,
    image

Example CSV row:
    J C Automotive,Dependable auto repair.,Full description here.,(585) 266-4710,"1700 East Ridge Road, Rochester, NY 14622",,,,Auto & Repairs,Auto Repair,false,Closed,8AM-5PM,8AM-5PM,8AM-5PM,8AM-5PM,8AM-5PM,8AM-1PM,

Notes:
    - 'premium' should be 'true' or 'false'
    - Leave fields blank if unknown
    - The script will NOT overwrite existing files unless you pass --overwrite
    - Image filenames should match files in static/images/businesses/
"""

import csv
import os
import re
import sys
from datetime import datetime


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def create_markdown(row):
    """Generate Hugo front matter markdown from a CSV row."""
    name = row.get('name', '').strip()
    if not name:
        return None, None

    slug = slugify(name)
    premium = row.get('premium', 'false').strip().lower() == 'true'

    # Build front matter
    lines = [
        '---',
        f'title: "{name}"',
        f'date: {datetime.now().strftime("%Y-%m-%d")}',
        'draft: false',
        f'tagline: "{row.get("tagline", "").strip()}"',
        f'description: "{row.get("description", "").strip()}"',
        f'phone: "{row.get("phone", "").strip()}"',
        f'address: "{row.get("address", "").strip()}"',
        f'website: "{row.get("website", "").strip()}"',
        f'email: "{row.get("email", "").strip()}"',
        f'image: "{row.get("image", "").strip()}"',
        f'premium: {str(premium).lower()}',
        'categories:',
        f'  - "{row.get("category", "").strip()}"',
        'subcategories:',
        f'  - "{row.get("subcategory", "").strip()}"',
        'hours:',
        f'  sunday: "{row.get("hours_sun", "").strip()}"',
        f'  monday: "{row.get("hours_mon", "").strip()}"',
        f'  tuesday: "{row.get("hours_tue", "").strip()}"',
        f'  wednesday: "{row.get("hours_wed", "").strip()}"',
        f'  thursday: "{row.get("hours_thu", "").strip()}"',
        f'  friday: "{row.get("hours_fri", "").strip()}"',
        f'  saturday: "{row.get("hours_sat", "").strip()}"',
        '---',
        '',
    ]

    return slug, '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 import-businesses.py <csv-file> [--overwrite]")
        print("\nSee script header for CSV format details.")
        sys.exit(1)

    csv_path = sys.argv[1]
    overwrite = '--overwrite' in sys.argv

    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'content', 'businesses')
    os.makedirs(output_dir, exist_ok=True)

    created = 0
    skipped = 0
    errors = 0

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=2):  # start=2 for line numbers (header=1)
            try:
                slug, content = create_markdown(row)
                if not slug:
                    print(f"  Line {i}: Skipped (no name)")
                    skipped += 1
                    continue

                filepath = os.path.join(output_dir, f"{slug}.md")

                if os.path.exists(filepath) and not overwrite:
                    print(f"  Line {i}: Skipped '{slug}.md' (already exists)")
                    skipped += 1
                    continue

                with open(filepath, 'w', encoding='utf-8') as out:
                    out.write(content)

                status = "PREMIUM" if 'true' in row.get('premium', '').lower() else "standard"
                print(f"  Line {i}: Created '{slug}.md' [{status}]")
                created += 1

            except Exception as e:
                print(f"  Line {i}: ERROR - {e}")
                errors += 1

    print(f"\nDone! Created: {created} | Skipped: {skipped} | Errors: {errors}")
    print(f"Files written to: {output_dir}")


if __name__ == '__main__':
    main()
