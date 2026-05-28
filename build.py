#!/usr/bin/env python3
"""Assembles HTML pages from source files and shared _includes/ partials.

Replaces <!-- @@NAV@@ --> and <!-- @@FOOTER@@ --> markers in each page
with the contents of _includes/nav.html and _includes/footer.html.
Replaces <!-- @@REVIEWS@@ --> in index.html with live Google reviews
(or a static fallback) fetched from the Google Places API at build time.

Nav behavior:
  - On index.html: brand link → "#", CTA → "#request" (fragment-only)
  - On other pages: links stay as "index.html" / "index.html#request"
  - The current page's nav link gets active styling (solid white text)
"""
import html
import json
import os
import shutil
import subprocess
import urllib.parse
import urllib.request

GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "")
FORM_ENDPOINT = os.environ.get("FORM_ENDPOINT", "")
GOOGLE_REVIEW_URL = "https://g.page/r/Cc6vDXUxByncEAI/review"

_STATIC_REVIEWS = [
    ("Gary S.", "SOBO appliance was recommended by a friend and they did a great job fixing my washing machine! Highly recommend Kyle as he is attentive to detail and is super handy!"),
    ("Ra H.", "Kyle came right on time and handled both my washer and garbage disposal like a pro. He explained exactly what was going on and addressed everything promptly without hesitation. I really appreciate his thoroughness and efficiency — I highly recommend!"),
    ("James W.", "We couldn't be happier with the results. His knowledge of preventative maintenance was clear, and he completed the job efficiently while keeping our home clean. Kyle is a top choice for any home maintenance tasks."),
]


def _fetch_place_reviews():
    """Return (rating, total, reviews_list) from Google Places API, or None on failure."""
    if not GOOGLE_PLACES_API_KEY:
        return None

    try:
        # Step 1: resolve Place ID from business name
        find_url = (
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            "?input=" + urllib.parse.quote("SOBO Appliance Repair Baltimore")
            + "&inputtype=textquery"
            "&fields=place_id"
            "&key=" + GOOGLE_PLACES_API_KEY
        )
        with urllib.request.urlopen(find_url, timeout=10) as resp:
            find_data = json.loads(resp.read())
        candidates = find_data.get("candidates", [])
        if not candidates:
            print("WARNING: Places findplacefromtext returned no candidates")
            return None
        place_id = candidates[0]["place_id"]

        # Step 2: fetch reviews + rating
        details_url = (
            "https://maps.googleapis.com/maps/api/place/details/json"
            "?place_id=" + place_id
            + "&fields=reviews,rating,user_ratings_total"
            "&key=" + GOOGLE_PLACES_API_KEY
        )
        with urllib.request.urlopen(details_url, timeout=10) as resp:
            details_data = json.loads(resp.read())
        result = details_data.get("result", {})
        return {
            "rating": result.get("rating"),
            "total": result.get("user_ratings_total"),
            "reviews": result.get("reviews", []),
        }
    except Exception as e:
        print(f"WARNING: Google Places API fetch failed: {e}")
        return None


def _build_reviews_html(api_data):
    """Return the full reviews section HTML."""
    if api_data and api_data["reviews"]:
        rating = api_data["rating"]
        total = api_data["total"]
        cards = []
        for r in api_data["reviews"][:3]:
            author = html.escape(r.get("author_name", ""))
            text = html.escape(r.get("text", ""))
            cards.append(
                f'          <div class="bg-white border rounded-xl p-6">\n'
                f'            <p class="text-amber-400 mb-3">&#9733;&#9733;&#9733;&#9733;&#9733;</p>\n'
                f'            <p class="text-gray-700 text-sm leading-relaxed mb-4 line-clamp-5">&ldquo;{text}&rdquo;</p>\n'
                f'            <p class="text-xs text-gray-400 font-medium">{author} &middot; Google review</p>\n'
                f'          </div>'
            )
        rating_display = f"{rating}"
        total_display = f"{total} {'review' if total == 1 else 'reviews'}"
    else:
        # Static fallback
        rating_display = "5.0"
        total_display = "6 reviews"
        cards = [
            f'          <div class="bg-white border rounded-xl p-6">\n'
            f'            <p class="text-amber-400 mb-3">&#9733;&#9733;&#9733;&#9733;&#9733;</p>\n'
            f'            <p class="text-gray-700 text-sm leading-relaxed mb-4">&ldquo;{html.escape(text)}&rdquo;</p>\n'
            f'            <p class="text-xs text-gray-400 font-medium">{html.escape(author)} &middot; Google review</p>\n'
            f'          </div>'
            for author, text in _STATIC_REVIEWS
        ]

    cards_html = "\n".join(cards)
    return (
        '    <!-- Reviews -->\n'
        '    <section class="bg-gray-50 border-t">\n'
        '      <div class="max-w-5xl mx-auto px-4 py-16">\n'
        '        <h2 class="text-2xl md:text-3xl font-bold text-center mb-2">What Neighbors Are Saying</h2>\n'
        '        <p class="text-center text-sm text-gray-500 mb-10">\n'
        '          <span class="text-amber-400 font-semibold">&#9733;&#9733;&#9733;&#9733;&#9733;</span>\n'
        f'          {rating_display} &middot; {total_display} &middot;\n'
        f'          <a href="{GOOGLE_REVIEW_URL}" target="_blank" rel="noopener" class="text-brand-700 underline hover:text-brand-800">See on Google</a>\n'
        '        </p>\n'
        '        <div class="grid md:grid-cols-3 gap-6">\n'
        f'{cards_html}\n'
        '        </div>\n'
        '      </div>\n'
        '    </section>'
    )


def _build_aggregate_rating_json(api_data):
    """Return the aggregateRating JSON fragment (comma-prefixed) or empty string."""
    if not api_data or not api_data.get("rating"):
        return ""
    return (
        ',\n'
        '        "aggregateRating": {\n'
        '          "@type": "AggregateRating",\n'
        f'          "ratingValue": "{api_data["rating"]}",\n'
        f'          "reviewCount": "{api_data["total"]}",\n'
        '          "bestRating": "5",\n'
        '          "worstRating": "1"\n'
        '        }'
    )

_VACATION_BANNER = """\
    <div id="vacation-banner" style="display:none" class="bg-amber-400 text-brand-900 text-sm font-medium text-center px-4 py-2.5">
      <strong>Out of Town (Jun 1&ndash;4):</strong>
      No in-home service calls during this period &mdash; calls &amp; messages are still monitored and will be answered.
      Scheduling resumes June&nbsp;5.
    </div>
    <script>
      (function(){
        var d=new Date(),y=d.getFullYear(),m=d.getMonth()+1,day=d.getDate();
        var after =(y>2026)||(y===2026&&m>6)||(y===2026&&m===6&&day>=1);
        var before=(y<2026)||(y===2026&&m<6)||(y===2026&&m===6&&day<=4);
        if(after&&before)document.getElementById('vacation-banner').style.display='';
      })();
    </script>"""

def _vacation_banner_html():
    return _VACATION_BANNER

PAGES = ["index.html", "pricing.html", "services.html"]
STATIC = ["favicon.png", "CNAME", "sitemap.xml", "robots.txt"]
BUILD_DIR = "_site"


def main():
    os.makedirs(BUILD_DIR, exist_ok=True)

    # Build Tailwind CSS (skipped gracefully if CLI is not installed locally)
    css_out = os.path.join(BUILD_DIR, "style.css")
    try:
        subprocess.run(
            ["tailwindcss", "-i", "src/input.css", "-o", css_out, "--minify"],
            check=True,
        )
    except (FileNotFoundError, PermissionError):
        print("WARNING: tailwindcss CLI not found or not executable — CSS not rebuilt (use pre-built or install CLI)")
    except subprocess.CalledProcessError as e:
        print(f"WARNING: Tailwind CSS build failed: {e}")

    nav_template = open("_includes/nav.html").read()
    footer = open("_includes/footer.html").read()
    mobile_bar_template = open("_includes/mobile-bar.html").read()

    vacation_banner = _vacation_banner_html()

    # Fetch reviews once (used only for index.html)
    api_data = _fetch_place_reviews()
    reviews_html = _build_reviews_html(api_data)
    aggregate_rating_json = _build_aggregate_rating_json(api_data)

    for page in PAGES:
        name = page.replace(".html", "")
        content = open(page).read()

        # Build nav with active-page styling
        nav = nav_template
        if name != "index":
            # Highlight the active page's nav link
            nav = nav.replace(
                f'data-nav="{name}" class="text-blue-200 hover:text-white',
                f'data-nav="{name}" class="text-white',
            )
        else:
            # On the home page, use fragment links for same-page navigation
            nav = nav.replace('href="index.html#request"', 'href="#request"')
            nav = nav.replace(
                'href="index.html" class="text-lg',
                'href="#" class="text-lg',
            )

        mobile_bar = mobile_bar_template
        if name == "index":
            mobile_bar = mobile_bar.replace('href="index.html#request"', 'href="#request"')

        nav = nav.replace("<!-- @@VACATION_BANNER@@ -->", vacation_banner)
        content = content.replace("@@FORM_ENDPOINT@@", FORM_ENDPOINT)
        content = content.replace("<!-- @@NAV@@ -->", nav)
        content = content.replace("<!-- @@FOOTER@@ -->", footer)
        content = content.replace("<!-- @@REVIEWS@@ -->", reviews_html)
        content = content.replace("<!-- @@MOBILE_BAR@@ -->", mobile_bar)
        content = content.replace("@@AGGREGATE_RATING_PLACEHOLDER@@", aggregate_rating_json)

        with open(os.path.join(BUILD_DIR, page), "w") as f:
            f.write(content)

    for asset in STATIC:
        if os.path.exists(asset):
            shutil.copy2(asset, os.path.join(BUILD_DIR, asset))


if __name__ == "__main__":
    main()
