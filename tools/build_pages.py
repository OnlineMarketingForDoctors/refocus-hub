"""Build the Refocus inner pages from the homepage's head, header and footer.

Usage: python3 build_pages.py /home/user/refocus-hub
Each page is written to <repo>/<slug>/index.html.
"""
import re
import sys
from html import escape

REPO = sys.argv[1] if len(sys.argv) > 1 else '.'
HOME = open(f'{REPO}/index.html', encoding='utf8').read()
FREE_CALL = '/free-consultation/'

EXTRA_ICONS = '''    <symbol id="i-down" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" d="M5 9l7 7 7-7"/></symbol>
    <symbol id="i-mail" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M4 7l8 6 8-6"/></g></symbol>
    <symbol id="i-pin" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></g></symbol>
    <symbol id="i-clock" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></g></symbol>
    <symbol id="i-whatsapp" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l1.3-3.8A8.5 8.5 0 1 1 8 19z"/><path d="M9 8.5c0 3.5 2.8 6.5 6.5 6.5l1-1.6-2-1-1 .9a4.5 4.5 0 0 1-2.4-2.4l.9-1-1-2z"/></g></symbol>
    <symbol id="i-sun" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/></g></symbol>
    <symbol id="i-drop" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M12 3.5s6 6.4 6 10.5a6 6 0 0 1-12 0C6 9.9 12 3.5 12 3.5z"/></symbol>
    <symbol id="i-spark" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="2"/><circle cx="18" cy="7" r="2"/><circle cx="12" cy="17" r="2"/><path d="M7.7 7.2l3.2 8M16.6 8.5l-3.6 6.8M8 6.2l8 .6"/></g></symbol>
    <symbol id="i-calendar" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/></g></symbol>
    <symbol id="i-cart" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h2.5l2.2 11h10.6L20.5 7H7"/><circle cx="9.5" cy="19" r="1.4"/><circle cx="17" cy="19" r="1.4"/></g></symbol>
    <symbol id="i-gift" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="8.5" width="17" height="4" rx="1"/><path d="M5 12.5V20h14v-7.5M12 8.5V20M12 8.5c-1.5-3-5.5-3.5-5.5-1S10 8.5 12 8.5zm0 0c1.5-3 5.5-3.5 5.5-1S14 8.5 12 8.5z"/></g></symbol>
'''


def build(slug, title, desc, hero_img, main, current=None):
    head = HOME[:HOME.index('<body>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(desc)}">', head)
    head = head.replace('href="favicon.png"', 'href="/favicon.png"')
    head = head.replace('<link rel="preload" as="image" href="video/hero-poster.webp">', f'<link rel="preload" as="image" href="{hero_img}">')
    head = head.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="/styles.css">\n  <link rel="stylesheet" href="/pages.css">')
    assert 'name="robots" content="noindex, nofollow"' in head

    top = HOME[HOME.index('<body>'):HOME.index('  <main id="main">')]
    top = top.replace('</svg>\n\n  <!-- ===== Header', EXTRA_ICONS + '  </svg>\n\n  <!-- ===== Header', 1)
    top = top.replace('<a class="brand" href="#top" aria-label="Refocus The Brain Hub, back to top">', '<a class="brand" href="/" aria-label="Refocus The Brain Hub home">')
    top = top.replace('src="img/', 'src="/img/')
    # Mark this page in the menu, and its section's top-level link
    top = top.replace(f'<a href="/{slug}/">', f'<a href="/{slug}/" aria-current="page">')
    if current and 'aria-current="page"' not in top:
        if f'<li class="has-sub"><a href="{current}">' in top:
            top = top.replace(f'<li class="has-sub"><a href="{current}">', f'<li class="has-sub"><a href="{current}" aria-current="page">', 1)
        else:
            top = top.replace(f'<li><a href="{current}">', f'<li><a href="{current}" aria-current="page">', 1)

    tail = HOME[HOME.index('  <!-- ===== Footer'):]
    tail = tail.replace('src="img/', 'src="/img/').replace('<script src="main.js" defer></script>', '<script src="/main.js" defer></script>\n  <script src="/pages.js" defer></script>')

    page = head + top + main + '\n' + tail
    assert 'id="i-down"' in page
    import os
    os.makedirs(f'{REPO}/{slug}', exist_ok=True)
    open(f'{REPO}/{slug}/index.html', 'w', encoding='utf8').write(page)
    print('built', slug)


def hero(img, alt, kicker, h1, sub, ctas, extra='', pos='70% center', w=2400, h=1018):
    btns = ''.join(f'<a class="btn {cls} btn-lg" href="{href}">{label}</a>' for label, href, cls in ctas)
    return f'''    <section class="pg-hero on-dark" aria-labelledby="pg-title">
      <img class="pg-hero-img" src="{img}" alt="{alt}" width="{w}" height="{h}" fetchpriority="high" style="object-position:{pos}">
      <div class="pg-hero-inner">
        <div class="pg-hero-copy">
          <p class="kicker">{kicker}</p>
          <h1 id="pg-title">{h1}</h1>
          <p class="pg-hero-sub">{sub}</p>
          <div class="btn-row">{btns}</div>
        </div>
        {extra}
      </div>
      <a class="pg-scroll" href="#start" aria-label="Scroll down"><svg><use href="#i-down"/></svg></a>
    </section>
'''


def cta_band(kicker, h2, text, img='/img/skyline.webp'):
    return f'''    <section class="closing on-dark" aria-labelledby="cta-title">
      <img src="{img}" alt="" width="2400" height="1018" loading="lazy" data-parallax>
      <div class="wrap closing-inner">
        <p class="kicker">{kicker}</p>
        <h2 id="cta-title">{h2}</h2>
        <p class="lede">{text}</p>
        <div class="btn-row">
          <a class="btn btn-primary btn-lg" href="{FREE_CALL}">Book a free 15-minute call</a>
          <a class="btn btn-ghost btn-lg" href="tel:+441614707093">Call 0161 470 7093</a>
        </div>
      </div>
    </section>
'''


def newsletter():
    return '''    <section class="section pg-news" aria-labelledby="news-title">
      <div class="wrap pg-news-card">
        <img class="pg-news-img" src="/img/learn-community.webp" alt="" width="1000" height="747" loading="lazy">
        <div class="pg-news-copy">
          <p class="kicker">Join our community</p>
          <h2 id="news-title">Get weekly insights, new resources, and exclusive content delivered straight to your inbox.</h2>
          <p>No spam, just support for your journey.</p>
          <form class="pg-news-form" data-mailto="hello@refocushub.co.uk" data-subject="Newsletter sign-up" novalidate>
            <label class="sr-only" for="news-email">Your email</label>
            <input id="news-email" name="email" type="email" autocomplete="email" placeholder="Your email*" required>
            <button class="btn btn-primary" type="submit">Subscribe</button>
            <p class="pg-form-status" role="status" hidden></p>
          </form>
          <p class="pg-small">By subscribing, you agree to our <a href="https://refocushub.co.uk/privacy-policy/">privacy policy</a>. Unsubscribe anytime.</p>
        </div>
      </div>
    </section>
'''


# ---------------------------------------------------------------- Prices
def price_opt(label, now, full=None, save=None, href=FREE_CALL, btn='Book now', note=None):
    if full:
        price = f'<div class="pc-price"><span class="pc-k">Offer price</span><strong>{now}</strong><span class="pc-full"><span class="pc-k">Full price</span> <s>{full}</s></span></div>'
    elif now:
        price = f'<div class="pc-price"><strong>{now}</strong></div>'
    else:
        price = ''
    savep = f'<span class="pc-save">{save}</span>' if save else ''
    notep = f'<p class="pc-note">{note}</p>' if note else ''
    cta = f'<a class="btn btn-primary pc-btn" href="{href}">{btn}</a>' if href else '<span class="pc-soon">Coming soon</span>'
    return f'<div class="pc-opt"><div class="pc-label">{label}{savep}</div>{price}{notep}{cta}</div>'


def price_card(title, img, opts, link=None, extra='', lvl='h3'):
    link_html = f' <a class="pc-more" href="{link}" aria-label="More about {escape(title)}"><svg><use href="#i-right"/></svg></a>' if link else ''
    return f'''          <article class="pc">
            <div class="pc-media"><img src="{img}" alt="" loading="lazy"><{lvl}>{title}</{lvl}>{link_html}</div>
            <div class="pc-opts">{''.join(opts)}</div>{extra}
          </article>
'''


def prices_page():
    kids = [
        price_card('Child &amp; Adolescent ADHD Assessments', '/img/svc-adhd.webp', [
            price_opt('Virtual ADHD assessment', '£750', '£890', 'Save £140', FREE_CALL),
            price_opt('Face-to-face ADHD assessment', '£850', '£1,150', 'Save £300', FREE_CALL)], '/diagnosis-main-page/child-adolescent-adhd/', lvl='h4'),
        price_card('Child &amp; Adolescent Autism (ASD) Assessments', '/img/svc-autism.webp', [
            price_opt('Virtual ASD assessment', '£1,300', '£1,500', 'Save £200', FREE_CALL),
            price_opt('Face-to-face ASD assessment', '£1,500', '£1,800', 'Save £300', FREE_CALL)], '/diagnosis-main-page/child-adolescent-autism-asd/', lvl='h4'),
        price_card('Combined ADHD + ASD Assessments', '/img/svc-complex.webp', [
            price_opt('Virtual ADHD + ASD assessment', '£1,700', '£1,900', 'Save £200', FREE_CALL),
            price_opt('Face-to-face ADHD + ASD assessment', '£2,000', '£2,200', 'Save £200', FREE_CALL)], '/diagnosis-main-page/combined-adhd-asd/', lvl='h4'),
        price_card('Child &amp; Adolescent Psychiatric Assessments', '/img/svc-camhs.webp', [
            price_opt('Psychiatry assessment, virtual or face-to-face', '£370', '£500', 'Save £130', FREE_CALL)], '/diagnosis-main-page/child-adolescent-psychiatric/', lvl='h4'),
    ]
    adults = [
        price_card('Adult ADHD Assessments', '/img/who-adult.webp', [
            price_opt('Virtual ADHD assessment', '£750', '£850', 'Save £100', FREE_CALL),
            price_opt('Face-to-face ADHD assessment', '£850', '£1,050', 'Save £200', FREE_CALL)], '/adult-adhd-assessment/', lvl='h4'),
        price_card('Adult Autism (ASD) Assessments', '/img/adult-autism.webp', [
            price_opt('Virtual ASD assessment', '£1,300', '£1,500', 'Save £200', FREE_CALL, 'Enquire'),
            price_opt('Face-to-face ASD assessment', '£1,500', '£1,800', 'Save £300', FREE_CALL, 'Enquire')], '/adult-autism-assessment/', lvl='h4'),
        price_card('Adult Combined ADHD + ASD Assessments', '/img/who-puzzle.webp', [
            price_opt('Virtual ADHD + ASD assessment', '£1,700', '£1,900', 'Save £200', FREE_CALL, 'Enquire'),
            price_opt('Face-to-face ADHD + ASD assessment', '£2,000', '£2,200', 'Save £200', FREE_CALL, 'Enquire')], lvl='h4'),
        price_card('Refocus Neuro-Hormone ADHD Pathway™', '/img/woman-light.webp', [
            price_opt('Virtual ADHD + mental health and perimenopause', '£750', '£900', 'Save £150', FREE_CALL),
            price_opt('Face-to-face ADHD + mental health and perimenopause', '£850', '£1,000', 'Save £150', FREE_CALL, 'Enquire')], '/care-main-page/adhd-assessments-for-women-approaching-perimenopause/', lvl='h4'),
    ]
    neuro = [
        price_card('Brain Mapping', '/img/qeeg-tablet.webp', [
            price_opt('qEEG brain mapping with clinical interpretation', '£350', None, None, FREE_CALL)],
            '/neuroscience-main-page/qeeg-brain-mapping/',
            '''<div class="pc-offer"><span class="pc-offer-tag"><svg><use href="#i-gift"/></svg>Special offer</span>
              <p class="pc-offer-line">qEEG brain mapping, booked alongside any Refocus service <span><s>£350</s> <strong>£200</strong></span></p>
              <p class="pc-note">Also £200 if you go on to a recommended assessment or treatment plan following your brain mapping.</p>
              <a class="text-link" href="/free-consultation/">Book qEEG <svg><use href="#i-right"/></svg></a></div>'''),
        price_card('Neuromodulation', '/img/svc-neuromod.webp', [
            price_opt('First session Exomind with medic appointment', '£350', None, None, FREE_CALL),
            price_opt('6 session Exomind (first session will be deducted)', '£1,000', '£1,800', 'Save £800', FREE_CALL)], '/neuroscience-main-page/exomind/'),
        price_card('Brain Training', '/img/blog/what-is-neurofeedback.webp', [
            price_opt('10 Neurofeedback sessions + qEEG brain mapping', '£950', None, None, FREE_CALL),
            price_opt('20 Neurofeedback sessions + qEEG brain mapping', '£1,350', None, None, FREE_CALL)], '/neuroscience-main-page/neurofeedback/'),
        price_card('Neuro-biological Support', '/img/home/helmet-fitting.webp', [
            price_opt('10 tPBM sessions with qEEG brain mapping', '£950', None, None, FREE_CALL),
            price_opt('20 tPBM sessions with qEEG brain mapping', '£1,350', None, None, FREE_CALL)], '/neuroscience-main-page/photobiomodulation/'),
    ]
    care = [
        price_card('Refocus Neuro-Hormone Clinic™', '/img/who-woman.webp', [
            price_opt('Virtual assessment', '£300', None, None, FREE_CALL)], '/neurohormone-clinic/'),
        price_card('At-Home Brain Therapy', '/img/home/helmet-home.webp', [
            price_opt('Refocus CORE 810 tPBM helmet, for personal home use', '£1,490', None, None, '/at-home-brain-therapy-2/', 'Learn more'),
            price_opt('Refocus DEEP 1070 tPBM helmet, for personal home use', '£1,690', None, None, '/at-home-brain-therapy-2/', 'Learn more')], '/at-home-brain-therapy-2/'),
        price_card('ADHD Medication Treatment Pathway', '/img/svc-medication.webp', [price_opt('Medication assessment, titration and monitoring', None, href=None)], '/care-main-page/adhd-medication-treatment-pathway/'),
        price_card('HRT Treatment Pathway', '/img/woman-window.webp', [price_opt('Hormone replacement therapy pathway', None, href=None)], '/care-main-page/hrt-treatment-pathway/'),
    ]
    faqs = [
        ('What is included in an assessment price?', 'Your price covers the pre-assessment questionnaires, your appointment with a consultant-led team, and a comprehensive written report you can share with your GP, school or employer.'),
        ('Do I need to pay a deposit?', 'Yes. A £250 deposit secures your assessment appointment and activates your secure patient portal. The balance is paid before your assessment.'),
        ('Do I need a GP referral?', 'No. You can book directly with us. No referral from your GP is required, and there is no waiting list.'),
        ('Are virtual and face-to-face assessments the same?', 'Yes. Both use the same senior clinicians, the same validated tools and the same written report. Many people find it easier to talk openly from home; others prefer our Manchester clinic.'),
        ('How long do the special offer prices last?', 'Special offer prices apply to bookings made by 30 November 2026. Full prices apply from 1 December 2026.'),
        ('Can I add qEEG brain mapping to an assessment?', 'Yes. qEEG brain mapping booked alongside any Refocus service costs £200 instead of £350, and your clinician will tell you honestly whether it is likely to help.'),
    ]
    faq_html = ''.join(f'<div class="acc-item"><h3><button class="acc-btn" type="button" aria-expanded="false">{q}<span class="pm" aria-hidden="true"></span></button></h3><div class="acc-panel"><div><p>{a}</p></div></div></div>' for q, a in faqs)

    main = '  <main id="main">\n' + hero(
        '/img/clinic/consult-room.webp', 'A Refocus consultation room with a desk, armchairs and the Refocus logo on a navy wall',
        'ADHD &amp; autism assessment prices, Manchester', 'Pricing',
        'Transparent prices for consultant-led ADHD and autism assessments for children and adults, plus qEEG brain mapping, neurofeedback and TMS. No hidden fees.',
        [('See assessment prices', '#diagnosis', 'btn-primary'), ('Book a free 15-minute call', FREE_CALL, 'btn-ghost')],
        pos='62% center', w=1600, h=1200) + f'''
    <!-- ===== Offer ===== -->
    <section class="pr-offer" id="start" aria-labelledby="offer-title">
      <div class="wrap pr-offer-card">
        <div>
          <span class="pill">Special offer</span>
          <h2 id="offer-title">Special offer prices until 30 November 2026</h2>
          <p>Save up to £300 on ADHD and autism assessments for children and adults, and £800 on a 6-session Exomind course. Offer prices apply to bookings made by 30 November 2026.</p>
        </div>
        <div class="pr-countdown" data-countdown="2026-11-30T23:59:59+00:00" aria-label="Time left on the offer">
          <span class="pr-cd-label">Offer ends in</span>
          <div><b data-d>00</b><span>days</span></div>
          <div><b data-h>00</b><span>hours</span></div>
          <div><b data-m>00</b><span>mins</span></div>
        </div>
      </div>
    </section>

    <nav class="pr-subnav" aria-label="Price categories">
      <div class="wrap">
        <a href="#diagnosis" class="is-active"><svg><use href="#i-doc"/></svg>Diagnosis</a>
        <a href="#neuroscience"><svg><use href="#i-brain"/></svg>Neuroscience</a>
        <a href="#care"><svg><use href="#i-heart"/></svg>Care</a>
      </div>
    </nav>

    <!-- ===== Diagnosis ===== -->
    <section class="section pr-group" id="diagnosis" aria-labelledby="diag-title">
      <img class="deco deco-waves" src="/img/waves-side.svg" alt="" width="300" height="900" style="width:170px;right:0;top:80px" loading="lazy">
      <div class="wrap">
        <div class="split-head">
          <div><p class="kicker">Refocus Diagnosis</p><h2 id="diag-title">Assessment prices</h2></div>
          <p class="lede">Consultant-led neurodevelopmental and psychiatric assessments for children, adolescents and adults, delivered virtually or face-to-face, with qEEG brain mapping available alongside.</p>
        </div>
        <div class="pr-tabs" role="tablist" aria-label="Who is the assessment for?">
          <button class="pr-tab" role="tab" id="tab-kids" aria-controls="panel-kids" aria-selected="true">Children &amp; Adolescents</button>
          <button class="pr-tab" role="tab" id="tab-adults" aria-controls="panel-adults" aria-selected="false" tabindex="-1">Adults</button>
        </div>
        <div class="pr-panel" role="tabpanel" id="panel-kids" aria-labelledby="tab-kids">
          <h3 class="sr-only">Children &amp; Adolescents</h3>
          <div class="pc-grid">
{''.join(kids)}          </div>
        </div>
        <div class="pr-panel" role="tabpanel" id="panel-adults" aria-labelledby="tab-adults" hidden>
          <h3 class="sr-only">Adults</h3>
          <div class="pc-grid">
{''.join(adults)}          </div>
        </div>
        <p class="pr-fine">Special offer prices apply to bookings made by 30 November 2026. Full prices apply from 1 December 2026.</p>

        <ul class="pr-included" aria-label="Included with every assessment">
          <li><svg><use href="#i-shield"/></svg><div><strong>Consultant-led</strong>Senior psychiatrists and psychologists</div></li>
          <li><svg><use href="#i-doc"/></svg><div><strong>Written report</strong>For your GP, school or employer</div></li>
          <li><svg><use href="#i-calendar"/></svg><div><strong>No waiting lists</strong>No GP referral required</div></li>
          <li><svg><use href="#i-gift"/></svg><div><strong>£250 deposit</strong>Secures your appointment</div></li>
        </ul>
      </div>
    </section>

    <!-- ===== Neuroscience ===== -->
    <section class="section pr-group pr-dark on-dark" id="neuroscience" aria-labelledby="neuro-title">
      <img class="pr-dark-bg" src="/img/neural.webp" alt="" width="2400" height="1018" loading="lazy">
      <div class="wrap">
        <div class="split-head">
          <div><p class="kicker">Refocus Neuroscience</p><h2 id="neuro-title">Brain mapping and neuromodulation prices</h2></div>
          <p class="lede">Advanced brain mapping and non-invasive neuromodulation therapies, TMS, neurofeedback and tPBM, guided by clinical qEEG interpretation.</p>
        </div>
        <div class="pc-grid">
{''.join(neuro)}        </div>
      </div>
    </section>

    <!-- ===== Care ===== -->
    <section class="section pr-group pr-care" id="care" aria-labelledby="care-title">
      <img class="deco deco-waves" src="/img/waves-corner.svg" alt="" width="900" height="420" style="width:520px;left:0;top:0" loading="lazy">
      <div class="wrap">
        <div class="split-head">
          <div><p class="kicker">Refocus Care</p><h2 id="care-title">Clinic and treatment pathway prices</h2></div>
          <p class="lede">Specialised clinics and ongoing treatment pathways for sustained mental health and hormonal wellbeing.</p>
        </div>
        <div class="pc-grid">
{''.join(care)}        </div>
      </div>
    </section>

    <!-- ===== FAQ ===== -->
    <section class="section faq" aria-labelledby="faq-title">
      <div class="wrap faq-grid">
        <div class="faq-aside">
          <p class="kicker">Questions about pricing</p>
          <h2 id="faq-title">Pricing FAQs</h2>
          <p class="lede">Not sure which assessment is right? Our team will help you choose on a free call.</p>
          <div class="help"><div><strong>Talk to us</strong><br><a href="tel:+441614707093">0161 470 7093</a><br><a href="mailto:hello@refocushub.co.uk">hello@refocushub.co.uk</a></div></div>
        </div>
        <div class="accordion" data-accordion>{faq_html}</div>
      </div>
    </section>

{cta_band('Not sure where to start?', 'Start with a free 15-minute call', 'Tell us what is going on and we will help you choose the right assessment, clinician and price option.')}  </main>
'''
    build('prices', 'ADHD &amp; Autism Assessment Prices Manchester | Refocus',
          'Transparent private ADHD and autism assessment prices for children and adults, plus qEEG brain mapping, neurofeedback and TMS. No hidden fees.',
          '/img/clinic/consult-room.webp', main, current='/prices/')


# ---------------------------------------------------------------- Contact
def contact_page():
    gallery = [
        ('consult-room', 'Consultation room with a desk and armchairs'), ('lounge-brain', 'Relaxation lounge with brain artwork'),
        ('lounge', 'Family lounge with raspberry sofas'), ('exomind-room', 'Exomind TMS treatment room'),
        ('children-room', 'Children’s assessment and play room'), ('quiet-room', 'Quiet room with soft seating'),
        ('desk-room', 'Clinician’s office'), ('education-wall', 'Brain education wall'), ('tms-room', 'Neuromodulation suite'),
    ]
    g_html = ''.join(f'<li><button class="ct-shot" type="button" data-full="/img/clinic/{f}.webp"><img src="/img/clinic/{f}.webp" alt="{alt}" loading="lazy"><span>{alt}</span></button></li>' for f, alt in gallery)
    main = '  <main id="main">\n' + hero(
        '/img/clinic/lounge.webp', 'The welcoming family lounge at the Refocus clinic in Manchester',
        'We’re here to help!', 'Have questions or need support?',
        'Reaching out can feel like a big step. If you’d like to ask a question or learn more about how we work, our team is here and happy to help.',
        [('Contact us', '#contact-form', 'btn-primary'), ('Book now', FREE_CALL, 'btn-ghost')], pos='50% center', w=1600, h=1200) + f'''
    <!-- ===== Contact options ===== -->
    <section class="ct-options" id="start" aria-labelledby="contact-title">
      <div class="wrap">
        <h2 id="contact-title" class="sr-only">Contact us</h2>
        <ul class="ct-cards">
          <li><a class="ct-card" href="tel:+441614707093"><span class="ico"><svg><use href="#i-phone"/></svg></span><span class="ct-k">Call the clinic</span><strong>0161 470 7093</strong><span>Speak to our team</span></a></li>
          <li><a class="ct-card" href="https://wa.me/447777112177"><span class="ico"><svg><use href="#i-whatsapp"/></svg></span><span class="ct-k">Mobile and WhatsApp</span><strong>07777 112177</strong><span>Contact us and we’ll reply ASAP</span></a></li>
          <li><a class="ct-card" href="mailto:hello@refocushub.co.uk"><span class="ico"><svg><use href="#i-mail"/></svg></span><span class="ct-k">Email us</span><strong>hello@refocushub.co.uk</strong><span>Write us your inquiry</span></a></li>
          <li><a class="ct-card" href="#find-us"><span class="ico"><svg><use href="#i-pin"/></svg></span><span class="ct-k">Visit us</span><strong>6 Oxford Place</strong><span>Manchester, M14 5RZ United Kingdom</span></a></li>
        </ul>
      </div>
    </section>

    <!-- ===== Form ===== -->
    <section class="section ct-form-sec" id="contact-form" aria-labelledby="form-title">
      <img class="deco deco-waves" src="/img/waves-side.svg" alt="" width="300" height="900" style="width:170px;left:0;top:60px;transform:scaleX(-1)" loading="lazy">
      <div class="wrap ct-form-grid">
        <div class="ct-form-copy">
          <p class="kicker">Contact us</p>
          <h2 id="form-title">Send us a message</h2>
          <p class="lede">Tell us a little about what you’re looking for and a member of our team will be in touch. Confidential, supportive and no pressure.</p>
          <div class="ct-hours">
            <span class="ico"><svg><use href="#i-clock"/></svg></span>
            <div><strong>Clinic hours</strong><p>Monday to Friday, 9am to 6pm<br>Saturday, 10am to 2pm</p></div>
          </div>
          <img class="ct-form-img reveal-img" src="/img/clinic/consult-room.webp" alt="A Refocus consultation room ready for an appointment" width="1600" height="1200" loading="lazy">
        </div>
        <div class="form-card">
          <h3>How can we help?</h3>
          <p class="sub">We reply as soon as we can, usually within one working day.</p>
          <form class="pg-form" data-mailto="hello@refocushub.co.uk" data-subject="Website enquiry" novalidate>
            <div class="form-grid">
              <div class="field"><label for="c-name">Your name</label><input id="c-name" name="name" autocomplete="name" required><span class="err" aria-live="polite"></span></div>
              <div class="field"><label for="c-phone">Phone <span class="opt">(optional)</span></label><input id="c-phone" name="phone" type="tel" autocomplete="tel"><span class="err" aria-live="polite"></span></div>
              <div class="field full"><label for="c-email">Your email</label><input id="c-email" name="email" type="email" autocomplete="email" required><span class="err" aria-live="polite"></span></div>
              <div class="field full"><label for="c-topic">I’m asking about</label>
                <select id="c-topic" name="topic">
                  <option>An ADHD assessment</option><option>An autism assessment</option><option>A child or teenager</option><option>qEEG brain mapping</option><option>Neuromodulation or at-home brain therapy</option><option>The Neuro-Hormone Clinic</option><option>Something else</option>
                </select></div>
              <div class="field full"><label for="c-msg">Your message</label><textarea id="c-msg" name="message" required></textarea><span class="err" aria-live="polite"></span></div>
            </div>
            <button class="btn btn-primary btn-lg" type="submit">Send message</button>
            <p class="pg-form-status" role="status" hidden></p>
          </form>
        </div>
      </div>
    </section>

    <!-- ===== Map ===== -->
    <section class="ct-map" id="find-us" aria-labelledby="map-title">
      <iframe title="Refocus The Brain Hub on Google Maps, 6 Oxford Place, Manchester" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2375.628190263757!2d-2.2211791!3d53.4572324!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x487bb15447b5b9a1%3A0x23a17b1081094834!2sRefocus%20-%20The%20Brain%20Hub%20%7C%20ADHD%20Assessment%20Manchester!5e0!3m2!1sen!2smx!4v1795641061017!5m2!1sen!2smx" allowfullscreen loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>
      <div class="wrap">
        <div class="ct-map-card">
          <img src="/img/logo.webp" alt="Refocus The Brain Hub" width="400" height="137" loading="lazy">
          <h2 id="map-title">We’re based just a short walk from Manchester Royal Hospital.</h2>
          <p class="ct-addr"><svg><use href="#i-pin"/></svg>6 Oxford Place, Manchester, M14 5RZ United Kingdom</p>
          <div class="btn-row"><a class="btn btn-primary" href="https://maps.app.goo.gl/cz7nrZcHDH2zS1cA6" target="_blank" rel="noopener">View on Google</a><a class="text-link" href="https://www.google.com/maps/dir/?api=1&amp;destination=53.4572324,-2.2211791" target="_blank" rel="noopener">Get directions <svg><use href="#i-right"/></svg></a></div>
        </div>
      </div>
    </section>

    <!-- ===== Gallery ===== -->
    <section class="section ct-gallery" aria-labelledby="gallery-title">
      <div class="wrap">
        <div class="split-head">
          <div><p class="kicker">Inside our clinic</p><h2 id="gallery-title">A calm space, designed for every brain</h2></div>
          <p class="lede">From quiet consultation rooms to a children’s assessment space and our neuromodulation suite, every room was designed to feel welcoming rather than clinical. Select a photo to see it larger.</p>
        </div>
        <ul class="ct-shots">{g_html}</ul>
      </div>
    </section>
    <dialog class="ct-lightbox" aria-label="Clinic photo"><button class="icon-btn ct-lb-close" type="button" aria-label="Close photo"><svg><use href="#i-close"/></svg></button><img alt=""><p></p></dialog>

{cta_band('Ready when you are', 'Prefer to talk it through?', 'Book a free 15-minute call and we’ll answer your questions and help you find the right next step.')}  </main>
'''
    build('contact', 'Contact Refocus | ADHD &amp; Brain Health Clinic Manchester',
          'Contact Refocus The Brain Hub, 6 Oxford Place, Manchester M14 5RZ. Call 0161 470 7093 or WhatsApp to ask about ADHD, autism assessments and brain mapping.',
          '/img/clinic/lounge.webp', main)


# ---------------------------------------------------------------- Blog data
POSTS = [
    ('Can Hormone Therapy Improve Neurodivergent Symptoms?', '/can-hormone-therapy-improve-neurodivergent-symptoms/', 'hormone-therapy', 'Mindfulness', 'June 25, 2026', '2026-06-25',
     'Even though the link between hormones and mood has been studied for over a century, it was only in the early 2000s that their direct influence over neurodivergent symptoms was'),
    ('Autism in Adults: What It Looks Like and How to Get a Diagnosis?', 'https://refocushub.co.uk/autism-in-adults-what-it-looks-like-and-diagnosis/', 'autism-adults', 'ADHD', 'June 11, 2026', '2026-06-11',
     'According to the World Health Organization (WHO), roughly one in 100 people are on the autism spectrum. However, these figures only scratch the surface, since a vast majority remain undiagnosed'),
    ('What is Neurofeedback?', 'https://refocushub.co.uk/what-is-neurofeedback/', 'what-is-neurofeedback', 'Neuroscience', 'June 8, 2026', '2026-06-08',
     'Maintaining optimal brain health may sometimes feel like tilting at windmills. While medication manages symptoms by altering brain chemistry, traditional talk therapy requires conscious reflection and self-disclosure. However, both fail'),
    ('Neurofeedback for Anxiety and Autism', 'https://refocushub.co.uk/neurofeedback-for-anxiety-and-autism/', 'neurofeedback-anxiety-autism', 'Neuroscience', 'June 5, 2026', '2026-06-05',
     'More than 1 in 100 people in the UK are autistic, according to the National Autistic Society. This translates to roughly 700,000 individuals who, along with their families and friends,'),
    ('ADHD Burnout and Masking in Women', 'https://refocushub.co.uk/adhd-burnout-and-masking-in-women/', 'adhd-burnout-masking', 'ADHD', 'May 28, 2026', '2026-05-28',
     'Most medical problems are non-apparent to the outside observer, but are experienced internally with obvious symptoms that make them easy to diagnose through biological tests. When it comes to ADHD'),
    ('Perimenopause, Menopause &amp; ADHD', 'https://refocushub.co.uk/perimenopause-menopause-adhd/', 'perimenopause-adhd', 'ADHD', 'May 27, 2026', '2026-05-27',
     'Many women live with ADHD and go to great lengths to mask its symptoms, just to comply with social norms and avoid judgment. Until perimenopause happens, and everything changes. Hormonal'),
    ('How to Explain ADHD to Others', 'https://refocushub.co.uk/how-to-explain-adhd-to-others/', 'explain-adhd', 'ADHD', 'May 12, 2026', '2026-05-12',
     'Living with ADHD in a world that was not built for your brain is a constant challenge. Society is designed for neurotypical individuals and expects everyone to function the same'),
    ('Neurodivergence in Children', 'https://refocushub.co.uk/neurodivergence-in-children/', 'neurodivergence-children', 'Neuroscience', 'February 7, 2026', '2026-02-07',
     'Neurodivergence in Children and Young People Understanding difference, supporting strengths, and how neurofeedback can help Neurodivergence is not a diagnosis; it is a way of describing natural differences in how'),
    ('ADHD &amp; Midlife: Why It Often Becomes Visible Later in Life', 'https://refocushub.co.uk/building-a-morningroutine-that-supports/', 'adhd-midlife', 'ADHD', 'February 4, 2026', '2026-02-04',
     'One of the most common questions we hear in clinic is: “Why does it feel like my ADHD suddenly appeared in my 40s or 50s?” The short answer is that'),
    ('QEEG Brain Mapping with iSyncWave® and Photobiomodulation (tPBM)', 'https://refocushub.co.uk/understanding-themind-heart-connection/', 'qeeg-isyncwave', 'QEEG', 'February 4, 2026', '2026-02-04',
     'Over the past two decades, brain mapping has moved from research labs into real-world clinical and performance settings. One of the most powerful tools in this space is QEEG'),
    ('Exomind TMS Overview', 'https://refocushub.co.uk/5-simple-grounding-techniques-for-anxiety-relief/', 'exomind-tms', 'Mindfulness', 'February 2, 2026', '2026-02-02',
     'Exomind® &amp; Transcranial Magnetic Stimulation (TMS) From established psychiatric treatment to modern brain wellbeing Transcranial Magnetic Stimulation (TMS) often sounds like a new or experimental technology, but in reality it'),
]
# Images that are too small or too wide to fill a card get a stronger substitute; the original still shows on the article itself.
CARD_IMG = {'adhd-midlife': '/img/who-woman.webp', 'exomind-tms': '/img/svc-neuromod.webp', 'autism-adults': '/img/adult-autism.webp'}


def post_card(p, cls='bl-card'):
    title, url, img, cat, date, iso, excerpt = p
    src = CARD_IMG.get(img, f'/img/blog/{img}.webp')
    return f'''<article class="{cls}" data-cat="{cat}">
            <a class="bl-img" href="{url}" tabindex="-1" aria-hidden="true"><img src="{src}" alt="" loading="lazy"></a>
            <div class="bl-body">
              <div class="bl-meta"><span class="bl-cat">{cat}</span><time datetime="{iso}">{date}</time></div>
              <h3><a href="{url}">{title}</a></h3>
              <p>{excerpt}…</p>
              <a class="text-link" href="{url}">Read more<span class="sr-only">: {title}</span> <svg><use href="#i-right"/></svg></a>
            </div>
          </article>'''


# ---------------------------------------------------------------- Learning hub
def learning_page():
    latest = ''.join(post_card(p) for p in POSTS[:3])
    topics = [('ADHD', 'Attention, masking, burnout and ADHD across life stages.', '/img/svc-adhd.webp'),
              ('Neuroscience', 'Neurofeedback, brain mapping and how the brain changes.', '/img/neural.webp'),
              ('QEEG', 'What a qEEG brain map shows, and how it guides care.', '/img/qeeg-tablet.webp'),
              ('Mindfulness', 'Hormones, wellbeing and modern brain care.', '/img/woman-light.webp')]
    t_html = ''.join(f'<li><a class="ln-topic" href="/neuro-blog/?topic={t}"><img src="{img}" alt="" loading="lazy"><span><strong>{t}</strong>{d}</span><span class="svc-go" aria-hidden="true"><svg><use href="#i-right"/></svg></span></a></li>' for t, d, img in topics)
    main = '  <main id="main">\n' + hero(
        '/img/hero-learning.webp', 'A woman reading in a navy armchair by a tall window, surrounded by books',
        'The Brain Learning Hub', 'Learn &amp; grow together',
        'Discover trusted, clinician-led insights on ADHD, autism, neurodiversity, and brain health at Refocus - The Brain Hub.',
        [('Explore resources', '#resources', 'btn-primary'), ('Read the latest articles', '#latest', 'btn-ghost')], pos='80% center') + f'''
    <!-- ===== Intro ===== -->
    <section class="section ln-intro" id="start" aria-labelledby="intro-title">
      <img class="deco deco-waves" src="/img/waves-side.svg" alt="" width="300" height="900" style="width:170px;right:0;top:40px" loading="lazy">
      <div class="wrap ln-intro-grid">
        <div class="ln-intro-media">
          <img class="main reveal-img" src="/img/brainmap-consult.webp" alt="A clinician explains colourful qEEG brain maps to a patient" width="1600" height="1073" loading="lazy">
          <img class="satellite" src="/img/learn-journal.webp" alt="Hands filling in a reflection worksheet with coloured pens" width="1000" height="747" loading="lazy">
        </div>
        <div>
          <p class="kicker">Library</p>
          <h2 id="intro-title">Complex neuroscience, made clear and practical</h2>
          <p class="lede">Our neuroscience-informed resources help children, adolescents, and adults understand attention, behaviour, emotions, cognition, and mental wellbeing.</p>
          <p>From ADHD and autism assessments to brain mapping, neurofeedback, and neuromodulation, we translate complex neuroscience into clear, practical knowledge you can use in everyday life.</p>
          <p>Whether you are exploring a possible diagnosis, supporting a neurodivergent child, or optimising your brain performance, our expert content is designed to guide you with clarity, compassion, and evidence.</p>
          <ul class="promise">
            <li><svg><use href="#i-shield"/></svg>Clinician-written</li>
            <li><svg><use href="#i-flask"/></svg>Evidence-based</li>
            <li><svg><use href="#i-heart"/></svg>Written with compassion</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ===== Resources ===== -->
    <section class="section ln-res" id="resources" aria-labelledby="res-title">
      <div class="wrap">
        <div class="section-head center">
          <p class="kicker">Learn more</p>
          <h2 id="res-title">Everything you need to thrive</h2>
        </div>
        <ul class="ln-res-grid">
          <li class="ln-res-card is-feature">
            <img src="/img/hero-blog.webp" alt="" loading="lazy" style="object-position:75% center">
            <div><span class="ico"><svg><use href="#i-book"/></svg></span><h3>The Brain Hub Insights</h3><p>Expert-written articles on mental health topics, self-care &amp; wellness.</p><a class="text-link" href="/neuro-blog/">Read the articles <svg><use href="#i-right"/></svg></a></div>
          </li>
          <li class="ln-res-card">
            <img src="/img/learn-journal.webp" alt="" loading="lazy">
            <div><span class="ico"><svg><use href="#i-doc"/></svg></span><h3>Printable resources</h3><p>Printable resources featuring exercises for journalling, goal-setting and self reflection.</p><a class="text-link" href="/contact/">Ask our team <svg><use href="#i-right"/></svg></a></div>
          </li>
          <li class="ln-res-card">
            <img src="/img/learn-community.webp" alt="" loading="lazy">
            <div><span class="ico"><svg><use href="#i-people"/></svg></span><h3>Real stories, real change</h3><p>Real stories from our community members sharing their special journeys.</p><a class="text-link" href="#news-title">Join our community <svg><use href="#i-right"/></svg></a></div>
          </li>
        </ul>
      </div>
    </section>

    <!-- ===== Topics ===== -->
    <section class="section ln-topics" aria-labelledby="topics-title">
      <div class="wrap">
        <div class="split-head">
          <div><p class="kicker">Explore by topic</p><h2 id="topics-title">Start with what matters to you</h2></div>
          <p class="lede">Browse our articles by subject, from ADHD and autism to brain mapping and hormonal health.</p>
        </div>
        <ul class="ln-topic-grid">{t_html}</ul>
      </div>
    </section>

    <!-- ===== Latest ===== -->
    <section class="section ln-latest" id="latest" aria-labelledby="latest-title">
      <div class="wrap">
        <div class="split-head">
          <div><p class="kicker">Latest articles</p><h2 id="latest-title">Fresh insights for your journey</h2></div>
          <a class="btn btn-ghost" href="/neuro-blog/">See all articles</a>
        </div>
        <div class="bl-grid">{latest}</div>
      </div>
    </section>

{newsletter()}
{cta_band('Questions about your brain?', 'Ask a clinician, not a search engine', 'If something you’ve read sounds familiar, a free 15-minute call is the easiest way to talk it through with our team.')}  </main>
'''
    build('learning-page', 'Brain Learning Hub: ADHD, Autism &amp; Brain Health | Refocus',
          'Clinician-written guides and research on ADHD, autism, qEEG brain mapping, neurofeedback and brain health from the Refocus team in Manchester.',
          '/img/hero-learning.webp', main)


# ---------------------------------------------------------------- Neuro blog
def blog_page():
    feat = POSTS[0]
    rest = ''.join(post_card(p) for p in POSTS[1:])
    cats = ['All'] + sorted({p[3] for p in POSTS})
    chips = ''.join(f'<button type="button" aria-pressed="{"true" if c == "All" else "false"}" data-filter="{c}">{c}</button>' for c in cats)
    t, url, img, cat, date, iso, ex = feat
    main = '  <main id="main">\n' + hero(
        '/img/hero-blog.webp', 'A writing desk by a window at dawn with a laptop, notebook and coffee',
        'Neuro blog', 'Brain Learning Hub',
        'Rewire. Reflect. Refocus - Learning made for the way your brain actually works.',
        [('Read the latest', '#start', 'btn-primary'), ('Book a free 15-minute call', FREE_CALL, 'btn-ghost')], pos='78% center') + f'''
    <!-- ===== Featured ===== -->
    <section class="section bl-featured-sec" id="start" aria-labelledby="feat-title">
      <div class="wrap">
        <article class="bl-feature" data-cat="{cat}">
          <a class="bl-img" href="{url}" tabindex="-1" aria-hidden="true"><img src="/img/blog/{img}.webp" alt="" loading="lazy"></a>
          <div class="bl-body">
            <span class="pill">Latest article</span>
            <div class="bl-meta"><span class="bl-cat">{cat}</span><time datetime="{iso}">{date}</time></div>
            <h2 id="feat-title"><a href="{url}">{t}</a></h2>
            <p>{ex}…</p>
            <a class="btn btn-primary" href="{url}">Read the article</a>
          </div>
        </article>
      </div>
    </section>

    <!-- ===== All posts ===== -->
    <section class="section bl-list" aria-labelledby="all-title">
      <img class="deco deco-waves" src="/img/waves-side.svg" alt="" width="300" height="900" style="width:170px;left:0;top:120px;transform:scaleX(-1)" loading="lazy">
      <div class="wrap">
        <div class="split-head">
          <div><p class="kicker">From our clinicians</p><h2 id="all-title">All articles</h2></div>
          <div class="ab-filter bl-filter" role="group" aria-label="Filter articles by topic">{chips}</div>
        </div>
        <div class="bl-grid" data-blog-grid>{rest}</div>
        <p class="bl-empty" hidden>No other articles in this topic yet. <button type="button" class="text-link" data-filter="All">Show all articles</button></p>
      </div>
    </section>

    <!-- ===== Refocus band ===== -->
    <section class="bl-band on-dark" aria-labelledby="band-title">
      <img src="/img/crowd.webp" alt="" width="2400" height="1018" loading="lazy" data-parallax>
      <div class="wrap">
        <p class="kicker">It’s time to refocus</p>
        <h2 id="band-title">Your brain is not broken, it just works differently.</h2>
        <p class="bl-band-q">Let’s find out how?</p>
        <a class="btn btn-primary btn-lg" href="{FREE_CALL}">Start with a free call</a>
      </div>
    </section>

{newsletter()}  </main>
'''
    build('neuro-blog', 'Neuro Blog: ADHD, Autism &amp; Neuroscience Articles | Refocus',
          'Articles from consultant psychiatrists and neuroscientists on ADHD in women, autism in adults, neurofeedback, brain mapping and brain health.',
          '/img/hero-blog.webp', main)


# ---------------------------------------------------------------- At-home brain therapy
def athome_page():
    def product(key, name, nm, tag, price, cart, paras, best, cls):
        ps = ''.join(f'<p>{p}</p>' for p in paras)
        return f'''<article class="ah-prod {cls}">
            <div class="ah-prod-media">
              <div class="ah-views" data-views>
                <img class="is-active" src="/img/home/{key}-front.webp" alt="{name} helmet, front view" width="1300" height="975" loading="lazy">
                <img src="/img/home/{key}-back.webp" alt="{name} helmet, inside view showing the near-infrared light array" width="1300" height="975" loading="lazy">
              </div>
              <div class="ah-view-btns" role="group" aria-label="{name} view">
                <button type="button" aria-pressed="true" data-view="0">Front view</button>
                <button type="button" aria-pressed="false" data-view="1">Inside view</button>
              </div>
              <span class="ah-nm">{nm} nm</span>
            </div>
            <div class="ah-prod-body">
              <span class="ah-tag">{tag}</span>
              <h3>{name}</h3>
              {ps}
              <div class="ah-best"><strong>Best for:</strong> {best}</div>
              <div class="ah-buy">
                <div class="ah-price"><strong>{price}</strong><span>One-time purchase</span></div>
                <a class="btn btn-primary" href="tel:+441614707093" aria-label="Call 0161 470 7093 to order the {name}"><svg><use href="#i-phone"/></svg>Call to order</a>
                <a class="text-link" href="/free-consultation/">Speak with our team <svg><use href="#i-right"/></svg></a>
              </div>
            </div>
          </article>'''
    core = product('core', 'Refocus CORE 810', '810', 'Essential brain energy support', '£1,490', 'https://refocushub.co.uk/cart/?add-to-cart=6431', [
        'Refocus CORE is our foundational at-home PBM system designed to support everyday brain optimisation, mental clarity, focus, and cognitive resilience.',
        'Using one of the most researched wavelengths in photobiomodulation, CORE is designed to support mitochondrial function, blood flow, and healthy brain energy production.',
        'Particularly suited for individuals experiencing stress, burnout, low mental energy, poor focus, sleep difficulties, or cognitive fatigue, and for those wanting to proactively support long-term brain wellness.'],
        'Early cognitive decline, stress, sleep support, mood regulation', 'is-core')
    deep = product('deep', 'Refocus DEEP 1070', '1070', 'Advanced deep brain neuromodulation', '£1,690', 'https://refocushub.co.uk/cart/?add-to-cart=6432', [
        'Refocus DEEP is our most advanced at-home PBM system, designed to provide deeper near-infrared penetration and more targeted neurological support.',
        'Using 1070nm technology, DEEP is designed to reach deeper brain structures involved in memory, cognition, processing speed, and neuroplasticity.',
        'May be particularly relevant for individuals concerned about cognitive decline, neurological recovery, healthy brain ageing, or more persistent cognitive difficulties, including emerging research on MCI, Alzheimer’s, and neurodegenerative pathways.'],
        'Alzheimer’s, moderate to severe cognitive decline, stroke, Parkinson’s, dementia', 'is-deep')
    rows = [('Best suited for', 'Brain fog, stress, focus, burnout, sleep, everyday optimisation', 'Cognitive decline concerns, MCI, memory support, advanced optimisation'),
            ('Primary focus', 'Brain energy and daily cognitive function', 'Deeper cognitive and neurological support'),
            ('Depth of support', 'Surface to mid brain networks', 'Deeper brain structures'),
            ('Ideal for', 'Everyday brain wellness and performance', 'More targeted neurological and cognitive pathways')]
    trs = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    main = '  <main id="main">\n' + hero(
        '/img/hero-athome.webp', 'A woman relaxing on her sofa at home wearing a Refocus near-infrared photobiomodulation helmet',
        'At-home brain therapy', '<span>Clinical-grade brain care.</span> <span>At home.</span>',
        'Non-invasive Photobiomodulation (PBM) technology designed to support brain energy, blood flow, and cellular function, helping you or your loved ones think clearer, feel better, and live more fully.',
        [('Compare CORE and DEEP', '#collection', 'btn-primary'), ('Book your free consultation', FREE_CALL, 'btn-ghost')], pos='82% center') + f'''
    <!-- ===== Benefits ===== -->
    <section class="section ah-benefits" id="start" aria-labelledby="ben-title">
      <img class="deco deco-waves" src="/img/waves-side.svg" alt="" width="300" height="900" style="width:170px;right:0;top:40px" loading="lazy">
      <div class="wrap ah-ben-grid">
        <div>
          <p class="kicker">How PBM supports your brain</p>
          <h2 id="ben-title">Gentle near-infrared light, working at cell level</h2>
          <ul class="ah-ben-list">
            <li><span class="ico"><svg><use href="#i-brain"/></svg></span>Supports brain energy</li>
            <li><span class="ico"><svg><use href="#i-drop"/></svg></span>Improves blood flow &amp; oxygenation</li>
            <li><span class="ico"><svg><use href="#i-spark"/></svg></span>Enhances neuroplasticity</li>
            <li><span class="ico"><svg><use href="#i-leaf"/></svg></span>Reduces inflammation</li>
          </ul>
          <div class="ah-safe">
            <h3>Safe. Gentle. Effective.</h3>
            <ul class="check-list ab-cols">
              <li>Drug-free &amp; non-invasive</li><li>Well tolerated</li><li>Used in clinical &amp; home settings</li><li>Backed by emerging neuroscience</li>
            </ul>
          </div>
        </div>
        <div class="ah-ben-media">
          <img class="main reveal-img" src="/img/home/helmet-home.webp" alt="An older woman relaxing at home while wearing a Refocus PBM helmet" width="1300" height="1002" loading="lazy">
          <img class="satellite" src="/img/home/helmet-controller.webp" alt="The Refocus helmet controller with its touchscreen" width="1024" height="992" loading="lazy">
        </div>
      </div>
    </section>

    <!-- ===== Philosophy ===== -->
    <section class="ah-belief on-dark" aria-labelledby="belief-title">
      <img src="/img/home/helmet-clinic.webp" alt="" width="1300" height="1137" loading="lazy" data-parallax>
      <div class="wrap ah-belief-inner">
        <h2 id="belief-title">Brain health should move beyond symptom-management, and become more proactive, personalised, and neuroscience-informed.</h2>
        <div class="ah-belief-cols">
          <p>Our at-home photobiomodulation pathways bring clinically informed brain support into everyday life through non-invasive near-infrared light therapy, designed to support brain energy, cognitive performance, and long-term brain wellness.</p>
          <p>Whether you are struggling with burnout, brain fog, poor focus, cognitive fatigue, or simply looking to better support your brain as you age, PBM offers a modern, drug-free approach to brain optimisation and neurological wellbeing.</p>
        </div>
      </div>
    </section>

    <!-- ===== Science ===== -->
    <section class="section ah-science" aria-labelledby="sci-title">
      <div class="wrap ah-sci-grid">
        <div class="ah-sci-media"><img class="reveal-img" src="/img/home/tpbm-infographic.webp" alt="Transcranial photobiomodulation infographic: improving mitochondrial activation and cerebral blood flow, stimulating neuronal growth, protecting cells and enhancing cognition" width="1300" height="1210" loading="lazy"></div>
        <div>
          <p class="kicker">The science</p>
          <h2 id="sci-title">Backed by emerging neuroscience.</h2>
          <p class="lede">Photobiomodulation is an evolving area of neuroscience research, with thousands of published studies exploring how near-infrared light may support cellular energy production, neuroplasticity, blood flow, and cognitive function.</p>
          <p>PBM works primarily through the mitochondria, the energy-producing structures inside cells, helping improve the production of ATP, the fuel the brain relies on to function efficiently.</p>
          <p>Research is also exploring the potential role of PBM in supporting cerebral oxygenation, reducing oxidative stress and inflammation, improving neuronal resilience, and supporting the brain’s natural recovery and waste-clearance systems.</p>
          <p class="ab-pull">Better brain energy may support better brain function.</p>
          <h3 class="ah-studies">Studies have explored potential benefits in:</h3>
          <ul class="ah-chips">
            <li>Mental clarity and focus</li><li>Brain fog and fatigue</li><li>Cognitive resilience and healthy ageing</li><li>Memory and processing</li><li>Mood and emotional wellbeing</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ===== Collection ===== -->
    <section class="section ah-collection" id="collection" aria-labelledby="col-title">
      <img class="deco deco-waves" src="/img/waves-corner.svg" alt="" width="900" height="420" style="width:520px;left:0;top:0" loading="lazy">
      <div class="wrap">
        <div class="section-head center">
          <p class="kicker">The collection</p>
          <h2 id="col-title">Introducing the Refocus PBM Collection.</h2>
          <p class="lede">Two clinically informed at-home pathways. Choose the one that fits where you are, and where you want your brain to be.</p>
        </div>
        <div class="ah-prods">{core}{deep}</div>
        <ul class="ah-specs">
          <li><svg><use href="#i-flask"/></svg><div><strong>Evidence-informed technology</strong>Built on emerging neuroscience and clinical research.</div></li>
          <li><svg><use href="#i-shield"/></svg><div><strong>Safe &amp; non-invasive</strong>No drugs. No side effects. Well tolerated.</div></li>
          <li><svg><use href="#i-home"/></svg><div><strong>Use at home</strong>Comfortable, easy-to-use and convenient.</div></li>
          <li><svg><use href="#i-clock"/></svg><div><strong>20-30 min sessions</strong>3-5 times per week recommended.</div></li>
          <li><svg><use href="#i-people"/></svg><div><strong>Clinical support</strong>Guidance from our expert clinical team.</div></li>
        </ul>
      </div>
    </section>

    <!-- ===== Compare ===== -->
    <section class="section ah-compare" aria-labelledby="cmp-title">
      <div class="wrap">
        <div class="section-head center">
          <p class="kicker">Compare</p>
          <h2 id="cmp-title">Which option is right for you?</h2>
        </div>
        <div class="ah-table-wrap">
          <table class="ah-table">
            <thead><tr><th scope="col">Pathway</th><th scope="col"><span>810 nm</span>Refocus CORE 810</th><th scope="col"><span>1070 nm</span>Refocus DEEP 1070</th></tr></thead>
            <tbody>{trs}</tbody>
          </table>
        </div>
        <div class="ah-advice">
          <p>If you are looking for foundational brain support, improved clarity, mental energy, and cognitive optimisation, <strong>Refocus CORE</strong> is usually the best starting point.</p>
          <p>If you are seeking more advanced support for memory, cognitive ageing, neurological resilience, or deeper-level optimisation, <strong>Refocus DEEP</strong> may be the more appropriate pathway.</p>
        </div>
      </div>
    </section>

    <!-- ===== qEEG pathway ===== -->
    <section class="section ah-path" aria-labelledby="path-title">
      <div class="wrap ah-path-grid">
        <div class="ah-path-media">
          <img class="main reveal-img" src="/img/home/helmet-fitting.webp" alt="A Refocus clinician fits a PBM helmet on an older man in the clinic" width="1300" height="867" loading="lazy">
          <img class="satellite" src="/img/home/helmet-stand.webp" alt="The Refocus CORE 810 helmet on its stand" width="1300" height="975" loading="lazy">
        </div>
        <div>
          <p class="kicker">Personalised pathways</p>
          <h2 id="path-title">Psychiatry, neuroscience, and modern neuromodulation, combined into more personalised brain health pathways.</h2>
          <p>For individuals wanting a deeper understanding of how their brain is functioning, we also offer optional <a href="/neuroscience-main-page/qeeg-brain-mapping/">qEEG brain mapping</a> to help identify patterns of overactivity, underactivity, cognitive overload, or inefficiencies across brain networks.</p>
          <p>This allows brain support pathways to become more informed, targeted, and individualised, because better brain health should never be one-size-fits-all.</p>
          <p class="ah-motto"><span>Small changes at brain level.</span><span>Meaningful changes in everyday life.</span></p>
        </div>
      </div>
    </section>

    <!-- ===== Final CTA ===== -->
    <section class="ah-final on-dark" aria-labelledby="final-title">
      <div class="wrap ah-final-grid">
        <div>
          <p class="kicker">Talk to our team</p>
          <h2 id="final-title">Ready to explore at-home brain therapy?</h2>
          <p class="lede">Speak with our team about your goals, your symptoms, and the pathway that fits you best.</p>
          <ul class="ah-final-list">
            <li>CORE vs DEEP pathways</li><li>Purchase and rental options</li><li>qEEG brain mapping</li><li>Personalised brain optimisation pathways</li>
          </ul>
          <div class="btn-row">
            <a class="btn btn-primary btn-lg" href="{FREE_CALL}">Book your free consultation</a>
            <a class="btn btn-ghost btn-lg" href="tel:01614707093">Call 0161 470 7093</a>
          </div>
        </div>
        <img class="ah-final-img" src="/img/home/helmet-stand.webp" alt="" width="1300" height="975" loading="lazy">
      </div>
    </section>
  </main>
'''
    build('at-home-brain-therapy-2', 'At-Home Photobiomodulation Devices | Refocus CORE &amp; DEEP',
          'Clinical-grade near-infrared photobiomodulation at home with the Refocus CORE 810 and DEEP 1070 headsets, guided by our Manchester clinic. Optional qEEG.',
          '/img/hero-athome.webp', main)



if __name__ == '__main__':
    prices_page()
    contact_page()
    learning_page()
    blog_page()
    athome_page()
