# refocus-hub

## Search indexing: this site must stay no-indexed

Until the owner explicitly says the site is ready to launch, it must not be indexed by search engines.

- Every HTML page must include `<meta name="robots" content="noindex, nofollow">` in its `<head>`. If a framework generates pages, set it in the shared layout or metadata config so no page is missed.
- `vercel.json` sends an `X-Robots-Tag: noindex, nofollow` header on every response. Keep it, and merge any new `vercel.json` settings into the existing file rather than replacing it.
- Do not add `Disallow: /` to `robots.txt`. A blocked crawler never fetches the page, so it never sees the noindex and can still list the bare URL.
- Do not generate a sitemap or submit the site to Google Search Console.
- When the owner says to launch, remove the meta tag and the `X-Robots-Tag` header together.
