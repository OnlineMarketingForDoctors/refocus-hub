"""Build the human-readable site map page (/sitemap/).

Usage: python3 tools/build_sitemap.py .   (run last, after the other page scripts)
Lists every local page, grouped by section, with each page's own <title>. This is a page for people, not an
XML sitemap: it is no-indexed like every other page, and nothing is submitted to search engines.
"""
import glob
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import build, hero, REPO  # noqa: E402

from build_nav import MENU, UNLISTED  # noqa: E402

GROUPS = [('Start here', ['/', '/free-consultation/'])]
for _label, _href, _groups in MENU:
    _urls = [_href] + [h for _, items in (_groups or []) for _, h in items]
    GROUPS.append((_label, list(dict.fromkeys(u.split('#')[0] for u in _urls))))

ICONS = {'Start here': 'i-compass', 'About Us': 'i-people', 'ADHD': 'i-brain', 'ASD': 'i-puzzle', 'Mental Health': 'i-heart', 'Neuroscience': 'i-wave',
         'Treatments': 'i-leaf', 'Pricing': 'i-gift', 'Brain Learning Hub': 'i-book', 'Contact': 'i-phone', 'Articles': 'i-book'}


def pages():
    found = {}
    for f in glob.glob(f'{REPO}/**/index.html', recursive=True):
        rel = os.path.relpath(os.path.dirname(f), REPO).replace(os.sep, '/')
        url = '/' if rel == '.' else f'/{rel}/'
        if url == '/sitemap/':
            continue
        t = re.search(r'<title>(.*?)</title>', open(f, encoding='utf8').read(), re.S).group(1)
        t = html.unescape(t).split(' | ')[0].strip()
        found[url] = html.escape(t)
    return found


def page():
    found = pages()
    seen, groups = set(), []
    for g, us in GROUPS:  # a page shared by two menu sections is listed once, under the first
        keep = [u for u in us if u in found and u not in seen and u not in UNLISTED]
        seen.update(keep)
        groups.append((g, keep))
    extra = sorted(u for u in found if u not in seen and u not in UNLISTED)
    if extra:
        groups.append(('Articles', extra))
    cards = ''
    for g, us in groups:
        if not us:
            continue
        lis = ''.join(f'<li><a href="{u}"><span>{found[u]}</span><small>{u}</small></a></li>' for u in us)
        cards += f'<section class="sm-group" aria-labelledby="sm-{g.lower().replace(" ", "-")}"><h2 id="sm-{g.lower().replace(" ", "-")}"><span class="ico"><svg><use href="#{ICONS[g]}"/></svg></span>{g}</h2><ul>{lis}</ul></section>'
    total = sum(len(us) for _, us in groups)
    main = '  <main id="main">\n' + hero('/img/clinic/lounge.webp', 'The Refocus clinic lounge', 'Site map', 'Every page, in one place',
                                        f'All {total} pages of the Refocus website, grouped by section.', [('Browse pages', '#start', 'btn-primary'), ('Book a free 15-minute call', '/free-consultation/', 'btn-ghost')], pos='60% center') + f'''
    <section class="section sm-sec" id="start" aria-label="All pages">
      <div class="wrap"><div class="sm-grid">{cards}</div></div>
    </section>
  </main>
'''
    build('sitemap', 'Site map | Refocus The Brain Hub', 'Every page of the Refocus website, grouped by section: assessments, neuroscience, brain care, learning and more.', '/img/clinic/lounge.webp', main)


if __name__ == '__main__':
    page()
