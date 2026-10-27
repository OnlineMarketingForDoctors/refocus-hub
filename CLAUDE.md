# refocus-hub

## Search indexing: this site must stay no-indexed

Until the owner explicitly says the site is ready to launch, it must not be indexed by search engines.

- Every HTML page must include `<meta name="robots" content="noindex, nofollow">` in its `<head>`. If a framework generates pages, set it in the shared layout or metadata config so no page is missed.
- `vercel.json` sends an `X-Robots-Tag: noindex, nofollow` header on every response. Keep it, and merge any new `vercel.json` settings into the existing file rather than replacing it.
- Do not add `Disallow: /` to `robots.txt`. A blocked crawler never fetches the page, so it never sees the noindex and can still list the bare URL.
- Do not generate a sitemap or submit the site to Google Search Console.
- When the owner says to launch, remove the meta tag and the `X-Robots-Tag` header together.

## Publishing

Push every change straight to `main`.

## Homepage

`index.html`, `styles.css` and `main.js` at the repo root are the homepage. It shares its design system (colours, type, header, footer, reviews, team, FAQ) with the adult ADHD landing page in `OnlineMarketingForDoctors/refocus`. Links to other pages point to the live site at https://refocushub.co.uk/. Services that have no page on the live site stay unlinked.
