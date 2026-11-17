"""Write the main menu (with dropdowns) into the homepage and the About page.

Usage: python3 tools/build_nav.py .   then run the page build scripts so every page picks it up.
Edit MENU below to add or move pages.
"""
import os
import re
import sys

REPO = sys.argv[1] if len(sys.argv) > 1 else '.'
MENU = [
  ('Assessments', '/diagnosis-main-page/', [
     ('Children &amp; young people', [('ADHD assessment', '/diagnosis-main-page/child-adolescent-adhd/'), ('Autism (ASD) assessment', '/diagnosis-main-page/child-adolescent-autism-asd/'), ('Combined ADHD + autism', '/diagnosis-main-page/combined-adhd-asd/'), ('Psychiatric assessment', '/diagnosis-main-page/child-adolescent-psychiatric/')]),
     ('Adults', [('Adult ADHD assessment', '/adult-adhd-assessment/'), ('Adult autism assessment', '/adult-autism-assessment/'), ('Women’s ADHD &amp; perimenopause', '/care-main-page/adhd-assessments-for-women-approaching-perimenopause/')]),
  ]),
  ('Neuroscience', '/neuroscience-main-page/', [
     ('Brain mapping &amp; neuromodulation', [('qEEG brain mapping', '/neuroscience-main-page/qeeg-brain-mapping/'), ('Exomind TMS', '/neuroscience-main-page/exomind/'), ('Neurofeedback', '/neuroscience-main-page/neurofeedback/'), ('Photobiomodulation (tPBM)', '/neuroscience-main-page/photobiomodulation/'), ('At-home brain therapy', '/at-home-brain-therapy-2/')]),
  ]),
  ('Brain care', '/care-main-page/', [
     ('Ongoing care', [('NeuroHormone Clinic', '/neurohormone-clinic/'), ('ADHD medication pathway', '/care-main-page/adhd-medication-treatment-pathway/'), ('HRT treatment pathway', '/care-main-page/hrt-treatment-pathway/')]),
  ]),
  ('Prices', '/prices/', None),
  ('Learn', '/learning-page/', [
     ('Learn with us', [('Brain Learning Hub', '/learning-page/'), ('Neuro blog', '/neuro-blog/')]),
  ]),
  ('About us', '/about-us/', [
     ('Refocus', [('About us', '/about-us/'), ('Our team', '/about-us/#team'), ('Contact us', '/contact/')]),
  ]),
]

# Sections kept in MENU but not shown in the menu for now. Remove a label to show it again.
HIDDEN = {'Brain care'}


def nav(indent='      '):
    lis = []
    for label, href, groups in MENU:
        if label in HIDDEN:
            continue
        if not groups:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
            continue
        cols = ''.join(f'<div class="sub-col"><p class="sub-h">{g}</p><ul>' + ''.join(f'<li><a href="{h}">{t}</a></li>' for t, h in items) + '</ul></div>' for g, items in groups)
        OV = {'Assessments': 'All assessments', 'Neuroscience': 'Neuroscience overview', 'Brain care': 'Brain care overview'}
        ov = f'<a class="sub-overview" href="{href}">{OV[label]} <span aria-hidden="true">→</span></a>' if label in OV else ''
        lis.append(f'<li class="has-sub"><a href="{href}">{label}</a><button class="sub-toggle" type="button" aria-expanded="false" aria-label="Show {label} pages"></button>'
                   f'<div class="sub"><div class="sub-inner{" is-wide" if len(groups) > 1 else ""}">{cols}{ov}</div></div></li>')
    return (f'{indent}<nav class="main-nav" id="main-nav" aria-label="Main">\n{indent}  <ul>\n' + ''.join(f'{indent}    {l}\n' for l in lis) + f'{indent}  </ul>\n{indent}</nav>')

for rel, cur in [('index.html', None), ('about-us/index.html', '/about-us/')]:
    path = os.path.join(REPO, rel)
    s = open(path, encoding='utf8').read()
    new = nav()
    if cur:
        new = new.replace(f'<a href="{cur}">', f'<a href="{cur}" aria-current="page">')
    s, n = re.subn(r'      <nav class="main-nav" id="main-nav" aria-label="Main">.*?</nav>', lambda m: new, s, count=1, flags=re.S)
    assert n == 1, path
    open(path, 'w', encoding='utf8').write(s)
    print('nav updated', path)
