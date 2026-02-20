#!/usr/bin/env python3
"""Assembles HTML pages from source files and shared _includes/ partials.

Replaces <!-- @@NAV@@ --> and <!-- @@FOOTER@@ --> markers in each page
with the contents of _includes/nav.html and _includes/footer.html.

Nav behavior:
  - On index.html: brand link → "#", CTA → "#request" (fragment-only)
  - On other pages: links stay as "index.html" / "index.html#request"
  - The current page's nav link gets active styling (solid white text)
"""
import os
import shutil

PAGES = ["index.html", "pricing.html", "services.html"]
STATIC = ["favicon.png", "CNAME", "sitemap.xml", "robots.txt"]
BUILD_DIR = "_site"


def main():
    os.makedirs(BUILD_DIR, exist_ok=True)

    nav_template = open("_includes/nav.html").read()
    footer = open("_includes/footer.html").read()

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

        content = content.replace("<!-- @@NAV@@ -->", nav)
        content = content.replace("<!-- @@FOOTER@@ -->", footer)

        with open(os.path.join(BUILD_DIR, page), "w") as f:
            f.write(content)

    for asset in STATIC:
        if os.path.exists(asset):
            shutil.copy2(asset, os.path.join(BUILD_DIR, asset))


if __name__ == "__main__":
    main()
