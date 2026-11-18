"""Write the main menu (with dropdowns) into the homepage and the About page.

Usage: python3 tools/build_nav.py .   then run the page build scripts so every page picks it up.
Edit MENU below to add or move pages.
"""
import os
import re
import sys

REPO = sys.argv[1] if len(sys.argv) > 1 else '.'
DX = '/diagnosis-main-page/'
MENU = [  # (label, link, [(group heading or '', [(item, link), ...]), ...] or None)
  ('About Us', '/about-us/', None),
  ('ADHD', DX, [('', [('ADHD in Children &amp; Young People', DX + 'child-adolescent-adhd/'), ('Combined ADHD + Autism (ASD)', DX + 'combined-adhd-asd/'),
                      ('Adult ADHD Assessment', '/adult-adhd-assessment/'), ('ADHD Assessments for Women', '/care-main-page/adhd-assessments-for-women-approaching-perimenopause/')])]),
  ('ASD', DX, [('', [('Autism (ASD) in Children &amp; Young People', DX + 'child-adolescent-autism-asd/'), ('Adult Autism Assessment', '/adult-autism-assessment/')])]),
  ('Mental Health', DX + 'child-adolescent-psychiatric/', [('', [('Children &amp; Young People Psychiatric', DX + 'child-adolescent-psychiatric/')])]),
  ('Neuroscience', '/neuroscience-main-page/', [('', [('qEEG Brain Mapping', '/neuroscience-main-page/qeeg-brain-mapping/'), ('Exomind TMS', '/neuroscience-main-page/exomind/'),
                                                     ('Neurofeedback', '/neuroscience-main-page/neurofeedback/'), ('Photobiomodulation (tPBM)', '/neuroscience-main-page/photobiomodulation/')])]),
  ('Treatments', '/at-home-brain-therapy-2/', [('', [('At Home Brain Therapy', '/at-home-brain-therapy-2/'), ('ADHD Medication Treatment Pathway', '/care-main-page/adhd-medication-treatment-pathway/')])]),
  ('Pricing', '/prices/', None),
  ('Brain Learning Hub', '/learning-page/', [('', [('Neuro Blog', '/neuro-blog/')])]),
  ('Contact', '/contact/', None),
]
# Overview link at the foot of a dropdown
OV = {'ADHD': ('All assessments', DX), 'ASD': ('All assessments', DX), 'Neuroscience': ('Neuroscience overview', '/neuroscience-main-page/'), 'Brain Learning Hub': ('Brain Learning Hub', '/learning-page/')}

# Pages that exist but are kept out of the menu and the site map for now (Brain care).
UNLISTED = {'/care-main-page/', '/neurohormone-clinic/', '/care-main-page/hrt-treatment-pathway/'}
HIDDEN = set()  # kept for older scripts; menu sections are simply left out of MENU now


def nav(indent='      '):
    lis = []
    for label, href, groups in MENU:
        if not groups:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
            continue
        cols = ''.join('<div class="sub-col">' + (f'<p class="sub-h">{g}</p>' if g else '') + '<ul>' + ''.join(f'<li><a href="{h}">{t}</a></li>' for t, h in items) + '</ul></div>' for g, items in groups)
        ov = f'<a class="sub-overview" href="{OV[label][1]}">{OV[label][0]} <span aria-hidden="true">→</span></a>' if label in OV else ''
        lis.append(f'<li class="has-sub"><a href="{href}">{label}</a><button class="sub-toggle" type="button" aria-expanded="false" aria-label="Show {label} pages"></button>'
                   f'<div class="sub"><div class="sub-inner{" is-wide" if len(groups) > 1 else ""}">{cols}{ov}</div></div></li>')
    return (f'{indent}<nav class="main-nav" id="main-nav" aria-label="Main">\n{indent}  <ul>\n' + ''.join(f'{indent}    {l}\n' for l in lis) + f'{indent}  </ul>\n{indent}</nav>')


if __name__ == '__main__':
    for rel, cur in [('index.html', None), ('about-us/index.html', '/about-us/')]:
        path = os.path.join(REPO, rel)
        s = open(path, encoding='utf8').read()
        new = nav()
        if cur:
            new = new.replace(f'<a href="{cur}">', f'<a href="{cur}" aria-current="page">', 1)
        s, n = re.subn(r'      <nav class="main-nav" id="main-nav" aria-label="Main">.*?</nav>', lambda m: new, s, count=1, flags=re.S)
        assert n == 1, path
        open(path, 'w', encoding='utf8').write(s)
        print('nav updated', path)
