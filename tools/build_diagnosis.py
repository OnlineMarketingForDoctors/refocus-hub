"""Build the Refocus assessment pages (diagnosis hub, child, adult and women's pathways).

Usage: python3 tools/build_diagnosis.py .
Shares the page shell and helpers in tools/build_pages.py.
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import build, hero, cta_band, HOME, FREE_CALL  # noqa: E402

PRICES = '/prices/'

# Reuse the homepage's reviews carousel and regulated strip so every page shows the same verified content.
REVIEWS = re.search(r'    <!-- ===== Reviews ===== -->\n.*?</section>\n', HOME, re.S).group(0).replace('src="img/', 'src="/img/')
REGULATED = re.search(r'    <!-- ===== Regulated ===== -->\n.*?</section>\n', HOME, re.S).group(0).replace('src="img/', 'src="/img/')

TEAM = {
    'vrajitoriu': ('Dr Miriana Vrajitoriu', 'Consultant Child &amp; Adolescent Psychiatrist | Founder &amp; Medical Director', 'GMC Specialist Register | MRCPsych | ADOS-2 | ADI-R'),
    'qadir': ('Dr Arif Qadir', 'Consultant Child &amp; Adolescent Psychiatrist | Safeguarding Lead', 'ADI-R | DISCO-3 | Maudsley Adult ADHD Training'),
    'corciova': ('Dr Suzana Alexandra Corciova', 'Consultant Child &amp; Adolescent Psychiatrist', 'GMC Registered | MRCPsych | CCT | ADI-R | UKAAN'),
    'walsh': ('Dr Helen Walsh', 'Consultant Clinical Psychologist | Clinical Lead', 'ADOS Trained'),
    'hafeez': ('Dr Muhammad Adnan Hafeez', 'Consultant Psychiatrist | Adult ADHD &amp; Neuropsychiatry', 'GMC Registered'),
    'ashar': ('Dr Syeda Sabeen Ashar', 'Consultant Psychiatrist | Liaison Psychiatry &amp; Adult ADHD', 'GMC Specialist Register | MRCPsych | CCT | Section 12 Approved'),
    'williams': ('Sarah Williams', 'Advanced Clinical Practitioner | Women’s Neurodevelopmental Health Lead', 'RMN | V300 Non-Medical Prescriber | MSc Advanced Clinical Practice'),
    'mcguinness': ('Claire McGuinness', 'Advanced Nurse Practitioner | ADHD Medication Pathway Lead', 'NMC Registered | Independent Prescriber | MSc | First Class Honours'),
}


# ---------------------------------------------------------------- building blocks
def sec(cls, title_id, kicker, h2, lede='', body='', sid=None, center=False, deco='', dark=False):
    head_cls = 'section-head center' if center else 'section-head'
    k = f'<p class="kicker">{kicker}</p>' if kicker else ''
    l = f'<p class="lede">{lede}</p>' if lede else ''
    idattr = f' id="{sid}"' if sid else ''
    on = ' on-dark' if dark else ''
    return f'''    <section class="section dx {cls}{on}"{idattr} aria-labelledby="{title_id}">
      {deco}<div class="wrap">
        <div class="{head_cls}">{k}<h2 id="{title_id}">{h2}</h2>{l}</div>
        {body}
      </div>
    </section>
'''


def wave(side='right', top='60px'):
    flip = ';transform:scaleX(-1)' if side == 'left' else ''
    return f'<img class="deco deco-waves" src="/img/waves-side.svg" alt="" width="300" height="900" style="width:170px;{side}:0;top:{top}{flip}" loading="lazy">'


def ul(items, cls='check-list'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def chips(items, cls='dx-chips'):
    return ul(items, cls)


def features(items, cols=3):
    """items: (icon, title, text)"""
    lis = ''.join(f'<li><span class="ico"><svg><use href="#{i}"/></svg></span><div><h3>{t}</h3><p>{x}</p></div></li>' for i, t, x in items)
    return f'<ul class="dx-feat dx-feat-{cols}">{lis}</ul>'


def split(media, copy, reverse=False, cls=''):
    if not media:
        return f'<div class="dx-solo {cls}">{copy}</div>'
    r = ' is-reverse' if reverse else ''
    return f'<div class="dx-split{r} {cls}"><div class="dx-split-media">{media}</div><div class="dx-split-copy">{copy}</div></div>'


def collage(main, sat, alt_main, alt_sat=''):
    s = f'<img class="satellite" src="{sat}" alt="{alt_sat}" loading="lazy">' if sat else ''
    return f'<div class="dx-collage"><img class="main reveal-img" src="{main}" alt="{alt_main}" loading="lazy">{s}</div>'


def contrast(a_title, a_items, b_title, b_items, note=''):
    n = f'<p class="dx-contrast-note">{note}</p>' if note else ''
    return f'''<div class="dx-contrast">
          <div class="dx-without"><h3>{a_title}</h3>{ul(a_items, 'dx-x-list')}</div>
          <div class="dx-with"><h3>{b_title}</h3>{ul(b_items, 'dx-tick-list')}</div>
        </div>{n}'''


def tools(items):
    """items: (name, subtitle, html)"""
    cards = ''.join(f'<article class="dx-tool"><div class="dx-tool-head"><span class="dx-tool-name">{n}</span><span class="dx-tool-sub">{s}</span></div>{h}</article>' for n, s, h in items)
    return f'<div class="dx-tools">{cards}</div>'


def steps(items, img=None):
    """items: (label, title, html). Rendered as an interactive step list."""
    lis = ''.join(f'''<li class="dx-step{' is-open' if k == 0 else ''}">
            <button class="dx-step-btn" type="button" aria-expanded="{'true' if k == 0 else 'false'}"><span class="dx-step-n">{k + 1}</span><span><small>{lab}</small>{t}</span><span class="pm" aria-hidden="true"></span></button>
            <div class="dx-step-panel"><div>{h}</div></div>
          </li>''' for k, (lab, t, h) in enumerate(items))
    side = f'<div class="dx-steps-media"><img class="reveal-img" src="{img}" alt="" loading="lazy"></div>' if img else ''
    return f'<div class="dx-steps-wrap{" has-media" if img else ""}">{side}<ol class="dx-steps" data-steps>{lis}</ol></div>'


def booking(items, note=''):
    return ''  # booking-process steps are hidden on every page; prices stay
    lis = ''.join(f'<li><span class="n">{k + 1}</span><div><h3>{t}</h3><p>{x}</p></div></li>' for k, (t, x) in enumerate(items))
    n = f'<p class="dx-book-note">{note}</p>' if note else ''
    return f'<ol class="dx-book">{lis}</ol>{n}'


def team(keys, intro=''):
    cards = ''.join(f'''<li class="dx-person"><img src="/img/team-{k}.webp" alt="{TEAM[k][0]}" loading="lazy"><div><h3>{TEAM[k][0]}</h3><p class="role">{TEAM[k][1]}</p><p class="creds">{TEAM[k][2]}</p><a class="text-link" href="/about-us/#team">Read full profile<span class="sr-only"> of {TEAM[k][0]}</span> <svg><use href="#i-right"/></svg></a></div></li>''' for k in keys)
    return f'<ul class="dx-team dx-team-{min(len(keys), 3)}">{cards}</ul>'


def price_box(title, rows, note='Special offer prices apply to bookings made by 30 November 2026.'):
    """rows: (label, offer, full)"""
    r = ''.join(f'<li><span>{l}</span><span class="dx-p"><strong>{o}</strong>' + (f' <s>{f}</s>' if f else '') + '</span></li>' for l, o, f in rows)
    return f'''<aside class="dx-price" aria-label="{title}">
          <p class="dx-price-k"><svg><use href="#i-gift"/></svg>{title}</p>
          <ul>{r}</ul>
          <p class="pg-small">{note}</p>
          <div class="btn-row"><a class="btn btn-primary" href="{FREE_CALL}">Book a free 15-minute call</a><a class="text-link" href="{PRICES}">See all prices <svg><use href="#i-right"/></svg></a></div>
        </aside>'''


def statement(text):
    return f'<p class="dx-statement">{text}</p>'


def talk_band(title='Talk with a qualified professional', text='If you are unsure where to start, our team is here to help. We will listen carefully to your concerns, answer your questions honestly, and guide you towards the most appropriate next step.'):
    return f'''    <section class="dx-talk on-dark" aria-labelledby="talk-title">
      <img src="/img/clinic/consult-room.webp" alt="" width="1600" height="1200" loading="lazy" data-parallax>
      <div class="wrap dx-talk-inner">
        <div>
          <p class="kicker">Not sure where to start?</p>
          <h2 id="talk-title">{title}</h2>
          <p class="lede">{text}</p>
          <p class="pg-small dx-talk-small">Confidential, supportive, and no pressure.</p>
        </div>
        <div class="dx-talk-actions">
          <a class="btn btn-primary btn-lg" href="{FREE_CALL}">Book a free 15-minute call</a>
          <a class="dx-talk-link" href="tel:+441614707093"><svg><use href="#i-phone"/></svg><span><small>Ring Refocus</small>0161 470 7093</span></a>
          <a class="dx-talk-link" href="mailto:hello@refocushub.co.uk"><svg><use href="#i-mail"/></svg><span><small>Email us</small>hello@refocushub.co.uk</span></a>
        </div>
      </div>
    </section>
'''


def faq(items, title='Frequently asked questions', kicker='Questions, answered'):
    acc = ''.join(f'<div class="acc-item"><h3><button class="acc-btn" type="button" aria-expanded="false">{q}<span class="pm" aria-hidden="true"></span></button></h3><div class="acc-panel"><div>{a}</div></div></div>' for q, a in items)
    return f'''    <section class="section faq" aria-labelledby="faq-title">
      <div class="wrap faq-grid">
        <div class="faq-aside">
          <p class="kicker">{kicker}</p>
          <h2 id="faq-title">{title}</h2>
          <p class="lede">Can’t see your question? Our team is happy to help.</p>
          <div class="help"><div><strong>Talk to us</strong><br><a href="tel:+441614707093">0161 470 7093</a><br><a href="mailto:hello@refocushub.co.uk">hello@refocushub.co.uk</a></div></div>
        </div>
        <div class="accordion" data-accordion>{acc}</div>
      </div>
    </section>
'''


STD_BOOKING = [
    ('Complete a short screening', 'So we can match you to the most appropriate service and clinician.'),
    ('Pay a £250 deposit', 'This unlocks secure access to our clinical patient portal for questionnaires and communication.'),
    ('Complete online forms', 'Including patient and observer screening tools.'),
    ('Clinical review &amp; allocation', 'Our team carefully reviews your information and books you with the most appropriate clinician.'),
    ('Assessment appointment', 'The remaining balance is paid before the appointment.'),
]
QEEG_NOTE = 'qEEG brain mapping is available alongside your assessment at the reduced rate of £200.'


def page(slug, title, desc, hero_img, hero_html, sections):
    main = '  <main id="main">\n' + hero_html + ''.join(sections) + '  </main>\n'
    build(slug, title, desc, hero_img, main, current='/diagnosis-main-page/')


def H(img, alt, kicker, h1, sub, ctas=None):
    ctas = ctas or [('Book a free 15-minute call', FREE_CALL, 'btn-primary'), ('Learn more', '#start', 'btn-ghost')]
    return hero(img, alt, kicker, h1, sub, ctas, pos='78% center')


def intro(paras, img, alt, kicker='', h2='', sat=None, sid='start'):
    ps = ''.join(f'<p class="{"lede" if i == 0 else ""}">{p}</p>' for i, p in enumerate(paras))
    k = f'<p class="kicker">{kicker}</p>' if kicker else ''
    h = f'<h2 id="intro-title">{h2}</h2>' if h2 else ''
    lab = ' aria-labelledby="intro-title"' if h2 else ' aria-label="Introduction"'
    return f'''    <section class="section dx dx-intro" id="{sid}"{lab}>
      {wave('right', '40px')}<div class="wrap">
        {split(collage(img, sat, alt) if sat else f'<img class="dx-single reveal-img" src="{img}" alt="{alt}" loading="lazy">', k + h + ps)}
      </div>
    </section>
'''


# ================================================================ Diagnosis hub
def hub():
    svc = lambda img, title, text, feats, price, learn, extra='': f'''<article class="dx-svc">
            <div class="dx-svc-media"><img src="{img}" alt="" loading="lazy"></div>
            <div class="dx-svc-body">
              <h3><a href="{learn}">{title}</a></h3>
              <p>{text}</p>
              {f'<p class="dx-svc-k">Key features include:</p>{chips(feats)}' if feats else ''}
              {f'<p class="dx-svc-price"><em>{price}</em></p>' if price else ''}{extra}
              <div class="btn-row"><a class="btn btn-primary" href="{learn}">Learn more</a><a class="text-link" href="{FREE_CALL}">Book assessment <svg><use href="#i-right"/></svg></a></div>
            </div>
          </article>'''
    kids = ''.join([
        svc('/img/svc-adhd.webp', 'ADHD Assessments', 'Comprehensive diagnostic assessments using gold-standard tools, with clear outcomes and practical recommendations.', ['Expert assessment', 'Life-course history', 'Structured diagnostics', 'Objective testing', 'Clear guidance'], 'Assessments from £890 — no GP referral required — payment options available', '/diagnosis-main-page/child-adolescent-adhd/'),
        svc('/img/svc-autism.webp', 'Autism (ASD) Assessments', 'Detailed neurodevelopmental assessments exploring communication, social understanding, sensory processing, and strengths.', ['Gold-standard tools', 'Early development', 'MDT approach', 'Clear outcome', 'Neuroaffirmative'], 'Assessments from £1,500 — no GP referral required — payment options available', '/diagnosis-main-page/child-adolescent-autism-asd/'),
        svc('/img/svc-complex.webp', 'Combined ADHD + ASD Assessments', 'For children and young people where symptoms overlap or previous assessments have not brought clarity.', ['Overlapping symptoms', 'Holistic approach', 'Gold-standard tools', 'Multi-source input', 'Integrated recommendations'], 'Assessments from £1,900 — no GP referral required — payment options available', '/diagnosis-main-page/combined-adhd-asd/'),
        svc('/img/svc-camhs.webp', 'General Psychiatric Assessments', 'Specialist assessments for a wide range of mental health conditions affecting children and young people.', ['Anxiety disorders', 'Low mood and depression', 'Panic disorders', 'PTSD and trauma-related difficulties', 'OCD'], 'Assessments from £500 — no GP referral required — payment options available', '/diagnosis-main-page/child-adolescent-psychiatric/'),
    ])
    adults = ''.join([
        svc('/img/who-adult.webp', 'ADHD Assessments', 'Consultant psychiatrist-led adult ADHD assessment using the structured DIVA-5 interview, with observer input and optional qEEG brain mapping.', [], '', '/adult-adhd-assessment/'),
        svc('/img/adult-autism.webp', 'ASD Assessments', 'Adult autism assessment using ADOS-2 and ADI-R, the tools NICE recommends, with a report you can use at work, study and with your GP.', [], '', '/adult-autism-assessment/'),
        svc('/img/woman-light.webp', 'Women’s ADHD &amp; Perimenopause', 'A holistic pathway for women at midlife, recognising that ADHD, hormones and mental health intersect.', [], '', '/care-main-page/adhd-assessments-for-women-approaching-perimenopause/'),
        svc('/img/who-diagnosed.webp', 'General Psychiatric', 'Consultant psychiatric assessment for adults with anxiety, low mood and complex mental health presentations.', [], '', '/contact/'),
    ])
    faqs = [
        ('1. What does a Refocus assessment involve?', '''<p>At Refocus Diagnostics, every assessment is comprehensive, consultant-led and grounded in NICE-aligned clinical practice.</p><p>We offer specialist pathways for:</p>''' + ul(['Children &amp; Young People – ADHD and Autism Assessments', 'General Child &amp; Adolescent Psychiatry Assessments', 'Women’s ADHD &amp; Neurohormone Assessments']) + '<p>Each assessment includes:</p>' + ul(['A detailed developmental and clinical history', 'Structured diagnostic interviews', 'Standardised, evidence-based assessment tools', 'Multi-informant questionnaires (parents, school, self-report where appropriate)', 'Careful review of functional impact across education, work, relationships and wellbeing', 'Screening for co-existing conditions such as anxiety, mood difficulties, trauma, sleep disruption and hormonal factors']) + '<p>For women, we also explore hormonal transitions (including perimenopause and menopause) and how these may interact with attention, mood and cognitive function.</p><p>Following your assessment, you will receive:</p>' + ul(['A comprehensive diagnostic report', 'A clear clinical formulation', 'Individualised recommendations', 'A structured feedback session to explain findings and next steps']) + '<p>We focus not only on diagnosis, but on understanding the whole person.</p>'),
        ('2. Will my assessment be recognised by schools, universities, employers and the NHS?', '<p>Yes.</p><p>Assessments at Refocus are conducted by GMC-registered Consultant Psychiatrists and experienced clinicians working within national clinical guidelines and UK best-practice standards.</p><p>Our reports are suitable to support:</p>' + ul(['School and SENCO discussions', 'Exam access arrangements', 'University disability services', 'Access to Work applications', 'Communication with your GP']) + '<p>Most NHS services accept appropriately completed private consultant assessments. However, shared care arrangements for medication vary between GP practices and local NHS trusts.</p><p>We provide:</p>' + ul(['Clear, structured documentation', 'Guidance on shared care discussions', 'Professional communication where required']) + '<p>Our aim is to support continuity of care and integration with existing services wherever possible.</p>'),
        ('3. What happens after the assessment?', '<p>Following your assessment, we provide a clear roadmap tailored to you or your child.</p><p>Depending on clinical need, this may include:</p><p><strong>ADHD Care Pathway</strong></p>' + ul(['Medication discussion and initiation (if appropriate)', 'Structured titration and monitoring', 'School or workplace support guidance', 'Psychological or coaching referrals']) + '<p><strong>Women’s ADHD &amp; Neurohormone Pathway</strong></p>' + ul(['Integrated review of hormonal and attentional symptoms', 'Medication options where indicated', 'Cognitive, sleep and lifestyle strategies', 'Ongoing specialist review']) + '<p><strong>Child &amp; Adolescent Psychiatry</strong></p>' + ul(['Diagnostic clarification and formulation', 'Emotional and behavioural support planning', 'Medication where clinically appropriate', 'Therapeutic recommendations']) + '<p>Refocus is designed as a connected hub: <strong>Diagnostics → Care → Neuroscience</strong></p><p>Some families or adults choose to continue with ongoing psychiatric care. Others may explore optional neuroscience services such as QEEG brain mapping, neurofeedback, Exomind TMS or transcranial photobiomodulation.</p><p>There is no obligation to continue beyond your assessment. You may take your report and pursue support elsewhere if you wish.</p><p>Our role is to provide clarity, expertise and informed choice — so you can move forward with confidence.</p>'),
    ]
    sections = [
        f'''    <section class="dx-belief" id="start" aria-label="Our promise">
      <div class="wrap"><p>We don’t just diagnose. <span>We understand complexity.</span></p></div>
    </section>
''',
        sec('dx-why', 'why-title', 'Why choose Refocus?', 'Assessments that truly make a difference', 'We bring together deep clinical expertise, compassionate care, and cutting-edge neuroscience to provide assessments that truly make a difference.',
            split(collage('/img/consultation.webp', '/img/framework-map.webp', 'A consultant psychiatrist listens to a patient in the Refocus consultation room', 'A clinician fits a qEEG headset'),
                  features([('i-shield', 'Consultant-led assessments', 'All assessments are led by highly experienced Consultant Psychiatrists with over 20 years’ experience each in psychiatry and neurodevelopment.'),
                            ('i-puzzle', 'Complex minds need more than tick-boxes', 'We recognise overlapping presentations— ADHD, autism, anxiety, trauma, mood, tics— and take time to understand the whole person.'),
                            ('i-brain', 'Neuroscience-informed when needed', 'Where presentations are complex or unclear, we can add qEEG brain mapping and neuromodulation insight to support deeper clinical understanding.'),
                            ('i-compass', 'Second-opinion level expertise', 'Our service is designed to offer clarity where families feel stuck, uncertain, or unheard.')], cols=1)), deco=wave('right')),
        sec('dx-kids', 'kids-title', 'Children &amp; young people', 'Assessments for children and young people', 'Available online and face-to-face for ages 7-18.', f'<div class="dx-svc-grid">{kids}</div>', sid='children'),
        sec('dx-adults', 'adults-title', 'Adult services', 'Assessments for adults', 'Consultant-led ADHD and autism assessments for adults, online or face-to-face in Manchester. Structured diagnostic evaluations that combine gold-standard clinical methods with neuroscience-informed insight.', f'<div class="dx-svc-grid dx-svc-compact">{adults}</div>', sid='adults', dark=True),
        REVIEWS,
        faq(faqs, 'FAQ'),
        REGULATED,
        cta_band('Not sure which assessment is right?', 'Start with a free 15-minute call', 'We’ll listen, answer your questions and guide you to the right assessment, with the right clinician, at the right time.'),
    ]
    page('diagnosis-main-page', 'ADHD, Autism &amp; Psychiatric Assessments | Refocus Manchester',
         'Consultant-led ADHD, autism and psychiatric assessments for children and adults in Manchester or online. NICE-aligned, recognised reports. Free call.',
         '/img/hero-dx.webp',
         H('/img/hero-dx.webp', 'A consultant psychiatrist talks with a mother and her daughter in a calm Refocus consultation room', 'Refocus Diagnostics',
           '<span>Clear answers.</span> <span>Specialist insight.</span> <span>Neuroscience when it matters.</span>',
           'Refocus Diagnostics is the assessment arm of Refocus – The Brain Hub. This page is your starting point—guiding families and adults to the right assessment, with the right clinician, at the right time.',
           [('Explore our approach', '#start', 'btn-primary'), ('Book now', FREE_CALL, 'btn-ghost')]), sections)


# ================================================================ Child ADHD
def child_adhd():
    sections = [
        REGULATED,
        intro(['Diagnosing ADHD in children and young people can be complex. Attention, behaviour, learning, emotional regulation, sleep, anxiety, and sensory differences often overlap with other neurodevelopmental or mental-health conditions. At Refocus, our goal is not simply to label difficulties, but to deeply understand your child’s brain, development, and lived experience, so we can guide meaningful, personalised support.',
               'All Refocus assessments are NHS-recognised and fully compliant with NICE guidelines and the ADHD Assessment Quality Assurance Standard for Children and Teenagers (CAAQAS), ensuring gold-standard, evidence-based diagnostic practice.'],
              '/img/svc-adhd.webp', 'A boy looking up thoughtfully in a classroom', 'Child &amp; adolescent ADHD', 'Understanding your child’s brain, not just labelling it', sat='/img/who-child.webp'),
        sec('dx-signs', 'signs-title', 'Is it ADHD?', 'Is an ADHD assessment right for my child?', 'ADHD can look very different from one child to another:',
            features([('i-wave', 'Visibly active', 'Some children are visibly hyperactive and impulsive'),
                      ('i-compass', 'Quietly struggling', 'Others appear calm but struggle with focus, organisation, emotional regulation, or mental fatigue'),
                      ('i-home', 'Masking at school', 'Many children (especially girls) mask their difficulties at school and only “fall apart” at home')]) +
            '<h3 class="dx-sub">Symptoms commonly overlap with:</h3>' + chips(['Autism spectrum differences', 'Anxiety, low mood, trauma or attachment difficulties', 'Sleep disorders, sensory processing differences, or medical conditions', 'Dyslexia and learning differences']) +
            statement('If you’ve been told “something isn’t quite right” but answers feel unclear or inconsistent, a specialist, multidisciplinary assessment can bring clarity and reassurance.')),
        sec('dx-matters', 'matters-title', 'Why it matters', 'Why early and accurate diagnosis matters', 'Children with undiagnosed ADHD are often misunderstood.',
            contrast('They may be labelled as:', ['“Naughty”, “lazy”, “not trying hard enough”', '“Bright but not reaching potential”', '“Too emotional” or “too sensitive”'],
                     'Over time, repeated criticism can deeply impact:', ['Self-esteem and confidence', 'Emotional wellbeing', 'School engagement and peer relationships'],
                     'An early, thoughtful diagnosis helps adults respond differently, reduce blame, and support your child in ways that genuinely work for their brain.'), deco=wave('left')),
        sec('dx-team-sec', 'team-title', 'Meet the specialists', 'Our team specialists in children &amp; young people', '', team(['vrajitoriu', 'qadir', 'corciova'])),
        sec('dx-approach', 'approach-title', 'Our approach', 'Our approach at Refocus: beyond questionnaires', 'ADHD is a neurodevelopmental condition, so our assessments combine gold-standard clinical methods with advanced neuroscience tools when clinically appropriate.',
            features([('i-shield', 'Consultant Psychiatrist', 'Assessment by an experienced Consultant Child and Adolescent Psychiatrist with robust experience in neurodevelopmental assessments'),
                      ('i-book', 'Developmental History', 'Full developmental and psychosocial history with parents/carers'),
                      ('i-people', 'Young DIVA-5 Interview', 'Young DIVA-5 interview conducted during the appointment'),
                      ('i-doc', 'Evidence-based Questionnaires', 'Completed by parents/carers, school (teachers or SENCO), and the child or young person (where age-appropriate)'),
                      ('i-layers', 'Comprehensive Screening', 'Screening for co-occurring conditions (anxiety, autism, learning differences, mood difficulties)')]), center=True, dark=True),
        sec('dx-tool-sec', 'tool-title', 'The gold standard', 'What is the Young DIVA-5?', '',
            split('<img class="dx-single reveal-img" src="/img/svc-learning.webp" alt="A child completing a structured activity with a clinician" loading="lazy">',
                  '<p class="lede">The Young DIVA-5 is a gold-standard, NICE-aligned diagnostic interview for ADHD in children and adolescents.</p><p>It:</p>' +
                  ul(['Maps symptoms directly to DSM-5 ADHD criteria', 'Explores how symptoms present across settings (home, school, social life)', 'Considers developmental history, age-related changes, and functional impact', 'Helps differentiate ADHD from other conditions that can look similar']) +
                  '<p class="ab-pull">Using the Young DIVA-5 ensures the assessment is structured, consistent, and clinically robust, while still allowing space for your child’s individual story.</p>')),
        sec('dx-adv', 'adv-title', 'Beyond the interview', 'Advanced tools we may include', 'Depending on your child’s presentation, age, and complexity, we may also use:',
            tools([('MOXO AI ADHD Test', 'Objective attention testing', '<p>A computer-based, FDA-cleared objective test measuring:</p>' + chips(['Attention', 'Impulsivity', 'Hyperactivity', 'Timing under real-life distractors']) + '<p>This provides objective performance data to complement clinical assessment and parental/school reports.</p>'),
                   ('qEEG Brain Mapping', 'When indicated', f'<p><strong>{QEEG_NOTE}</strong></p><p>qEEG is not required for diagnosis, but in complex cases it can:</p>' + ul(['Add neurobiological insight when questionnaires give mixed signals', 'Support understanding of attention, regulation, and processing patterns', 'Help guide personalised recommendations and future interventions']) + '<p>We are transparent about when qEEG is helpful and when it is not, and it is never used in isolation.</p>')]), deco=wave('right')),
        sec('dx-process', 'process-title', 'Step by step', 'The assessment process', '',
            steps([('Step 1', 'Before the appointment', '<p>Once a deposit is paid, families receive secure access to our digital patient portal via electronic help record (ETR).</p><p>Through ETR, we send:</p>' + ul(['Parent and school questionnaires', 'Developmental and mental-health screening tools', 'Age-appropriate child/young person forms']) + '<p>Our clinicians carefully review all information before the appointment so your time together is focused, efficient, and meaningful.</p>'),
                   ('Step 2', 'During the assessment', '<p>You and your child meet with a senior clinician experienced in ADHD and neurodevelopmental conditions.</p><p>The session includes the Young DIVA-5 interview, alongside:</p>' + ul(['Early development and milestones', 'School and learning experiences', 'Emotional wellbeing and relationships', 'Strengths, interests, and coping strategies']) + '<p>We also explore co-occurring conditions, as ADHD rarely exists in isolation. Where possible, we will share our clinical impression during the appointment and discuss next steps together.</p>'),
                   ('Step 3', 'After the assessment', '<p>You will receive a comprehensive, clear, and practical report, including:</p>' + ul(['Diagnostic outcome (where criteria are met)', 'Differential diagnoses considered', 'Individualised recommendations']) + '<p>We understand families often wish to return to the NHS. We will support you in understanding shared-care options, while being honest about local GP variability.</p>')],
                  img='/img/svc-camhs.webp')),
        sec('dx-how', 'how-title', 'Booking', 'How do our ADHD assessments work?', 'At Refocus, we offer comprehensive ADHD assessments for children and young people, delivered by experienced consultant psychiatrists within a clinically governed framework. Our assessments follow NICE and NHS guidance and are aligned with the CAAQAS quality standards.',
            split(booking(STD_BOOKING), price_box('Child &amp; adolescent ADHD assessment', [('Virtual assessment', '£750', '£890'), ('Face-to-face assessment', '£850', '£1,150')]), cls='dx-how-split')),
        talk_band(),
    ]
    page('diagnosis-main-page/child-adolescent-adhd', 'Child &amp; Teen ADHD Assessment Manchester | Refocus',
         'Private ADHD assessment for children and teenagers led by consultant child psychiatrists. Young DIVA-5, school input and optional qEEG brain mapping.',
         '/img/hero-child-adhd.webp',
         H('/img/hero-child-adhd.webp', 'A mother patiently helps her young son with homework at the kitchen table', 'Child &amp; adolescent ADHD',
           'ADHD in children &amp; young people', 'A neuroscience-informed, child-centred assessment at Refocus The Brain Hub.'), sections)


# ================================================================ Child autism
def child_asd():
    sections = [
        REGULATED,
        intro(['Autism Spectrum Disorder (ASD) is a neurodevelopmental difference, not a single presentation. Children and young people experience the world, relationships, communication, and sensory input in unique ways. At Refocus, our aim is to understand your child as a whole person—their strengths, challenges, environment, and development—so families can access the right support with confidence.',
               'All our ASD assessments are NHS-recognised and aligned with NICE guidance, delivered by an experienced multidisciplinary team (MDT).'],
              '/img/svc-autism.webp', 'A girl drawing calmly at her desk', 'Child &amp; adolescent autism', 'Understanding your child as a whole person', sat='/img/clinic/children-room.webp'),
        sec('dx-signs', 'signs-title', 'Is it autism?', 'Is an autism assessment right for my child?', 'Autism can present very differently from one child to another and may change with age. Some children show clear early signs, while others mask their difficulties—particularly girls and cognitively able young people.',
            '<div class="dx-cols3">' +
            f'<div class="dx-col"><span class="ico"><svg><use href="#i-people"/></svg></span><h3>Social Communication &amp; Interaction</h3>{ul(["Differences in eye contact, facial expression, or gestures", "Difficulty starting or maintaining conversations", "Literal interpretation of language or difficulty understanding social nuance", "Preference for solitary play or specific friendships"])}</div>' +
            f'<div class="dx-col"><span class="ico"><svg><use href="#i-path"/></svg></span><h3>Behaviour, Routines &amp; Interests</h3>{ul(["Strong need for predictability or routine", "Distress with unexpected change", "Highly focused or intense interests", "Repetitive behaviours or movements"])}</div>' +
            f'<div class="dx-col"><span class="ico"><svg><use href="#i-sun"/></svg></span><h3>Sensory Processing</h3>{ul(["Sensitivity to noise, light, textures, or smells", "Seeking sensory input (movement, pressure, spinning)", "Overwhelm in busy or unpredictable environments"])}</div>' +
            '</div>' + statement('Autistic traits can overlap with ADHD, anxiety, learning differences, or trauma, making specialist assessment essential.')),
        sec('dx-matters', 'matters-title', 'Why it matters', 'Why timely and accurate diagnosis matters', '',
            contrast('Without understanding why a child struggles, they may be:', ['Mislabelled as ‘difficult’, ‘anxious’, or ‘oppositional’', 'Pushed to cope in environments that overwhelm them', 'Left without appropriate school adjustments or support'],
                     'A clear diagnosis can:', ['Reduce self-blame and shame', 'Improve understanding at home and school', 'Open access to tailored educational and therapeutic support', 'Help young people develop a positive sense of identity']), deco=wave('left')),
        sec('dx-team-sec', 'team-title', 'Meet the specialist', 'Our team specialist', '', team(['vrajitoriu', 'walsh'])),
        sec('dx-approach', 'approach-title', 'Our approach', 'Our autism assessment approach at Refocus', 'ASD assessment requires depth, structure, and clinical expertise. We follow NICE-compliant pathways and use gold-standard diagnostic tools, alongside comprehensive information from families and schools. Every Refocus ASD assessment includes:',
            features([('i-shield', 'Expert-Led Assessment', 'Assessment led by highly experienced clinicians, including consultant child &amp; adolescent psychiatrists'),
                      ('i-book', 'ADI-R Interview', 'A detailed developmental history appointment with parents/carers using ADI-R'),
                      ('i-puzzle', 'ADOS-2 Assessment', 'A structured ADOS-2 assessment with the child or young person'),
                      ('i-doc', 'Comprehensive Questionnaires', 'Evidence-based questionnaires completed by parents/carers, school (teachers or SENCO), and the young person (where age-appropriate)')], cols=4), center=True, dark=True),
        sec('dx-adv', 'tools-title', 'The gold standard', 'Gold-standard assessment tools we use', '',
            tools([('ADI-R', 'Autism Diagnostic Interview – Revised', '<p>The ADI-R is a gold-standard developmental history interview conducted with parents or carers by a consultant psychiatrist.</p><p><strong>It explores:</strong></p>' + ul(['Early childhood development', 'Social communication and interaction', 'Play, imagination, routines, and behaviours', 'How traits have changed over time']) + '<p>This provides crucial longitudinal insight that cannot be captured by observation alone.</p>'),
                   ('ADOS-2', 'Autism Diagnostic Observation Schedule', '<p>The ADOS-2 is a structured, standardised observation carried out directly with the child or young person by a highly trained clinician.</p><p><strong>It looks at:</strong></p>' + ul(['Communication and social interaction', 'Use of language and non-verbal communication', 'Play, imagination, and flexibility']))]) +
            statement('Together, ADI-R + ADOS-2 form the internationally recognised gold standard for ASD diagnosis.'), deco=wave('right')),
        sec('dx-how', 'how-title', 'Booking', 'How do our autism assessments work?', 'At Refocus, we provide comprehensive autism assessments for children and young people, delivered within a clinically governed, multidisciplinary framework. Our assessments follow NICE and NHS guidance and are aligned with the CAAQAS standards for high-quality neurodevelopmental assessment.',
            '<p class="dx-how-extra">Our assessments focus not only on diagnosis, but on understanding the child or young person’s strengths, needs, communication profile, and sensory world.</p>' +
            split(booking(STD_BOOKING), price_box('Child &amp; adolescent autism assessment', [('Virtual assessment', '£1,300', '£1,500'), ('Face-to-face assessment', '£1,500', '£1,800')]), cls='dx-how-split')),
        talk_band(),
    ]
    page('diagnosis-main-page/child-adolescent-autism-asd', 'Child &amp; Teen Autism (ASD) Assessment Manchester | Refocus',
         'Private autism assessment for children and teenagers using ADOS-2 and ADI-R, led by consultant child psychiatrists. In clinic from 5, online from 8.',
         '/img/hero-child-asd.webp',
         H('/img/hero-child-asd.webp', 'A girl wearing ear defenders lines up colourful blocks while her father watches', 'Child &amp; adolescent autism',
           'Autism (ASD) assessment in children &amp; young people', 'A thoughtful, gold-standard assessment at Refocus The Brain Hub.'), sections)


# ================================================================ Combined
def combined():
    sections = [
        REGULATED,
        intro(['Neurodevelopmental differences such as ADHD and Autism frequently overlap. Many children and young people show features of both, and separating them without a joined-up approach can lead to missed or partial answers.',
               'At Refocus, we offer a combined ADHD + ASD assessment that is NHS-recognised, NICE-aligned, and delivered by a highly experienced multidisciplinary team (MDT)—so families receive clarity, not fragmented opinions.'],
              '/img/svc-complex.webp', 'A clinician reviewing previous assessment reports', 'Children &amp; young people neurodevelopmental assessments', 'Clarity, not fragmented opinions', sat='/img/svc-camhs.webp'),
        sec('dx-signs', 'signs-title', 'Is it right for my child?', 'Is a combined neurodevelopmental assessment right for my child?', 'A combined assessment may be helpful if your child:',
            ul(['Shows attention, impulsivity, or emotional-regulation difficulties and social-communication or sensory differences', 'Has mixed or conflicting questionnaire results', 'Has previously been assessed for one condition but concerns remain', 'Masks difficulties at school but struggles significantly at home', 'Has anxiety, learning differences, or emotional challenges alongside neurodevelopmental traits'], 'dx-cards-list') +
            statement('ADHD and autism can look different across ages and genders, particularly in girls and cognitively able young people. A single, integrated pathway helps us understand how traits interact and what support will genuinely help.')),
        sec('dx-team-sec', 'team-title', 'Meet the specialists', 'Our team specialists in children &amp; young people', '', team(['vrajitoriu', 'qadir', 'corciova'])),
        sec('dx-matters', 'matters-title', 'Why it matters', 'Why timely and accurate diagnosis matters', '',
            contrast('Without a combined approach, children may:', ['Receive an incomplete diagnosis', 'Be offered support that only partially fits their needs', 'Continue to struggle despite “doing all the right things”'],
                     'A combined assessment allows us to:', ['Consider overlap, interaction, and differences between ADHD and ASD', 'Reduce repeated assessments and delays', 'Provide clear, practical recommendations for home, school, and wellbeing']), deco=wave('left')),
        sec('dx-approach', 'approach-title', 'Our approach', 'Our Refocus approach: clinical depth + neuroscience insight', 'All our neurodevelopmental assessments:',
            features([('i-shield', 'NICE &amp; NHS standards', 'Follow NICE guidance and recognised NHS standards'), ('i-flask', 'Gold-standard tools', 'Use gold-standard diagnostic tools'), ('i-people', 'Full MDT review', 'Are discussed in full MDT meetings before conclusions are reached')]) +
            '<div class="dx-includes"><h3>Your combined ADHD + ASD assessment includes:</h3>' + ul(['Oversight by consultant child &amp; adolescent psychiatrists', 'A detailed developmental history with parents/carers', 'Structured ADHD and ASD diagnostic interviews and observations', 'Evidence-based questionnaires from parents/carers, school (teachers or SENCO), and the young person (where age-appropriate)', 'Full MDT discussion of all findings together, not in isolation']) + '</div>', center=True, dark=True),
        sec('dx-adv', 'tools-title', 'The gold standard', 'Gold-standard tools used in the combined pathway', 'We use internationally recognised diagnostic instruments to ensure accuracy and consistency.',
            tools([('Young DIVA-5', 'ADHD', '<p>The Young DIVA-5 is a gold-standard, NICE-aligned structured interview mapping symptoms directly to DSM-5 ADHD criteria.</p>' + ul(['Inattention, hyperactivity, and impulsivity', 'Functional impact across settings (home, school, social life)', 'Developmental change over time']) + '<p>In the combined pathway, the young person attends the final hour of the parent appointment to complete the Young DIVA-5 with the clinician.</p>'),
                   ('MOXO AI ADHD Test', 'Objective attention testing', '<p>A computer-based, FDA-cleared objective test measuring:</p>' + chips(['Attention', 'Impulsivity', 'Hyperactivity', 'Timing under real-life distractors']) + '<p>This provides objective performance data to complement clinical interviews and reports.</p>'),
                   ('ADI-R', 'Developmental history', '<p>A gold-standard developmental history interview conducted with parents/carers by a consultant psychiatrist.</p>' + ul(['Early childhood development', 'Social communication and interaction', 'Play, routines, interests, and behaviours', 'How traits have evolved over time'])),
                   ('ADOS-2', 'Structured observation', '<p>A structured, standardised observation completed directly with the young person by a highly experienced clinician.</p>' + ul(['Duration: approximately 1 hour', 'Available face-to-face or online, where clinically appropriate', 'Targets communication, social skills, play, imagination, and flexibility.']))]) +
            statement('Together, ADI-R + ADOS-2 form the international gold standard for ASD diagnosis.'), deco=wave('right')),
        sec('dx-structure', 'struct-title', 'Appointment structure', 'Appointment structure (combined assessment)', '',
            '<ol class="dx-timeline">'
            '<li><span class="n">01</span><div><h3>Parents/Carers Appointment</h3><p class="dx-dur"><svg><use href="#i-clock"/></svg>Duration: 2–3 hours</p>' + ul(['Full developmental history (ADI-R)', 'ADHD exploration', 'Contextual, educational, and emotional review']) + '</div></li>'
            '<li><span class="n">02</span><div><h3>Young Person Joins For The Final Hour</h3><p>Young DIVA-5 ADHD interview</p></div></li>'
            '<li><span class="n">03</span><div><h3>ADOS-2 Session</h3><p class="dx-dur"><svg><use href="#i-clock"/></svg>Duration: 1 hour</p>' + ul(['Conducted separately with the young person', 'Online or face-to-face']) + '</div></li>'
            '<li><span class="n">04</span><div><h3>MDT Review</h3><p>All information is then reviewed together in an MDT meeting.</p></div></li></ol>'),
        sec('dx-how', 'how-title', 'Booking', 'How do our combined assessments work?', 'At Refocus, we offer integrated ADHD and autism (ASD) assessments for children and young people, designed for situations where features of both conditions may be present and a combined approach provides clearer understanding. Our assessments follow NICE and NHS guidance and are aligned with the CAAQAS quality standards.',
            '<p class="dx-how-extra">This combined approach helps distinguish between overlapping traits, understand strengths as well as challenges, and guide the most appropriate support.</p>' +
            split(booking(STD_BOOKING), price_box('Combined ADHD + ASD assessment', [('Virtual assessment', '£1,700', '£1,900'), ('Face-to-face assessment', '£2,000', '£2,200')]), cls='dx-how-split')),
        talk_band(),
    ]
    page('diagnosis-main-page/combined-adhd-asd', 'Combined ADHD &amp; Autism Assessment for Children | Refocus',
         'Private combined ADHD and autism assessment for children and young people. Gold-standard tools, consultant-led, with clear personalised recommendations.',
         '/img/hero-combined.webp',
         H('/img/hero-combined.webp', 'A clinician and a boy work together on a structured play activity', 'Children &amp; young people neurodevelopmental assessments',
           'Combined ADHD + Autism (ASD) Assessment', 'A gold-standard, integrated pathway at Refocus The Brain Hub.'), sections)


# ================================================================ Child psychiatric
def psychiatric():
    sections = [
        intro(['Children and young people can struggle with anxiety, low mood, obsessive thoughts, trauma, tics or school refusal, and the reasons are not always obvious. At Refocus, our consultant child and adolescent psychiatrists take time to understand what is driving the difficulties and how best to support recovery.',
               'Our assessments follow NICE guidance and recognised NHS standards, with clear verbal feedback and written recommendations so families know exactly what happens next.'],
              '/img/svc-camhs.webp', 'A mother and her teenage son talk openly with a clinician', 'Children &amp; young people psychiatric assessments', 'Understanding what is driving the difficulties', sat='/img/who-teen.webp'),
        sec('dx-signs', 'signs-title', 'Is it right for my child?', 'Is a psychiatric assessment right for my child?', 'A psychiatric assessment may be helpful if your child or young person is experiencing:',
            ul(['Ongoing anxiety or panic symptoms', 'Obsessive thoughts or compulsive behaviours (OCD)', 'Low mood or emotional dysregulation', 'Trauma-related symptoms or PTSD', 'Tics or Tourette’s syndrome', 'Selective mutism or school refusal', 'Emotional and behavioural difficulties at home or school'], 'dx-cards-list') +
            statement('Some children present with clear mental-health symptoms, while others show distress through behaviour, avoidance, or physical complaints. A specialist psychiatric assessment helps us understand what is driving the difficulties and how best to support recovery.')),
        sec('dx-matters', 'matters-title', 'Why it matters', 'Why a comprehensive psychiatric assessment matters', '',
            contrast('Without a full understanding of a child’s developmental and emotional history:', ['Symptoms may be treated in isolation rather than in context', 'Underlying neurodevelopmental differences may be missed', 'Interventions may be less effective or poorly tolerated'],
                     'Our assessments focus on:', ['Mapping symptoms across development', 'Identifying triggers, protective factors, and patterns over time', 'Recommendations that are individualised, realistic, and clinically meaningful']), deco=wave('left')),
        sec('dx-team-sec', 'team-title', 'Meet the specialists', 'Our consultant child &amp; adolescent psychiatrists', '', team(['vrajitoriu', 'qadir', 'corciova'])),
        sec('dx-approach', 'approach-title', 'Our approach', 'Our Refocus psychiatric assessment approach', 'All our generic psychiatric assessments:',
            features([('i-shield', 'NICE &amp; NHS standards', 'Follow NICE guidance and recognised NHS standards'), ('i-person', 'Consultant-led', 'Are conducted by consultant child &amp; adolescent psychiatrists'),
                      ('i-doc', 'Evidence-based screening', 'Use structured, evidence-based screening tools'), ('i-people', 'Team review', 'Are discussed within a clinical team where appropriate')], cols=4) +
            '<div class="dx-includes"><h3>Every Refocus psychiatric assessment includes:</h3>' + ul(['A developmental history appointment with parents/carers', 'Review of emotional, behavioural, social, and educational functioning', 'Evidence-based questionnaires completed by parents/carers and the young person (where age-appropriate)', 'A one-to-one mental state examination with the child or young person', 'Clear formulation linking symptoms, development, and environment']) + '</div>', center=True, dark=True),
        sec('dx-adv', 'tools-title', 'Screening tools', 'Evidence-based screening tools we use', 'These tools support clinical judgement and help track patterns over time.',
            tools([('SDQ', 'Strengths and Difficulties Questionnaire', '<p>Completed by parents/carers and, where appropriate, young people.</p><p><strong>It helps screen for:</strong></p>' + ul(['Emotional symptoms', 'Conduct difficulties', 'Hyperactivity/inattention', 'Peer relationship challenges', 'Prosocial strengths'])),
                   ('RCADS', 'Revised Children’s Anxiety and Depression Scale', '<p>Completed by parents and young people.</p><p><strong>It provides structured insight into:</strong></p>' + ul(['Anxiety disorders (including panic and social anxiety)', 'Depressive symptoms', 'Severity and functional impact']))]), deco=wave('right')),
        sec('dx-conditions', 'cond-title', 'Conditions we assess', 'Conditions we assess', 'Our generic psychiatric assessments can explore and diagnose a wide range of conditions, including:',
            ul(['Anxiety disorders and panic disorder', 'Depressive disorders', 'Selective mutism', 'Tic disorders and Tourette’s syndrome', 'OCD', 'PTSD and trauma-related difficulties', 'Emotional and behavioural difficulties', 'School refusal'], 'dx-cond'), center=True),
        sec('dx-how', 'how-title', 'Booking', 'How do our general psychiatry assessments work?', 'At Refocus, we offer comprehensive child and adolescent mental health (CAMHS) psychiatric assessments, delivered exclusively by experienced consultant child and adolescent psychiatrists. Our assessments follow NICE and NHS standards and high-quality, evidence-based assessment.',
            split('<div class="dx-how-copy"><p>During the appointment, the psychiatrist will take a developmental, emotional, and mental health history, explore current concerns in depth, and consider strengths, vulnerabilities, and protective factors.</p><p><strong>Depending on the reason for referral, pre-assessment questionnaires will be requested from:</strong></p>' + ul(['Parents or carers', 'The young person themselves (age-appropriate)']) + '<p>School information is not routinely required at the pre-assessment stage, but may be requested later if clinically indicated.</p><p>Following the assessment, families receive clear verbal feedback, diagnostic impressions where appropriate, and written recommendations to guide next steps and support.</p></div>',
                  price_box('Child &amp; adolescent psychiatric assessment', [('Virtual or face-to-face', '£370', '£500')]), cls='dx-how-split')),
        talk_band(),
    ]
    page('diagnosis-main-page/child-adolescent-psychiatric', 'Child &amp; Teen Psychiatric Assessment Manchester | Refocus',
         'Private psychiatric assessment for children and teenagers in Manchester - anxiety, OCD, tics and Tourette’s, selective mutism and school refusal.',
         '/img/hero-psychiatric.webp',
         H('/img/hero-psychiatric.webp', 'A teenage girl talks with a consultant psychiatrist in a calm room', 'Children &amp; young people psychiatric assessments',
           'Children &amp; young people psychiatric assessments', 'Comprehensive mental-health assessment at Refocus The Brain Hub.'), sections)


# ================================================================ Adult ADHD
def adult_adhd():
    sections = [
        intro(['At Refocus, our goal is not simply to diagnose ADHD, but to deeply understand how your brain works, how your experiences have evolved over time, and what support is most likely to help you move forward.',
               'All Refocus assessments are Consultant-led, NHS-recognised, and aligned with NICE guidelines and the Adult ADHD Assessment Quality Assurance Standard (AQAS).'],
              '/img/intro-man.webp', 'A man deep in thought at his desk', 'Adult ADHD', 'Understanding how your brain works', sat='/img/framework-refocus.webp'),
        sec('dx-signs', 'signs-title', 'Is it ADHD?', 'Is an ADHD assessment right for me?', 'ADHD in adulthood can look very different from the stereotypes many people expect. Some adults are visibly hyperactive and impulsive. Others appear highly capable externally while privately struggling with:',
            chips(['Mental fatigue', 'Executive dysfunction', 'Emotional overwhelm', 'Procrastination and paralysis', 'Difficulties managing everyday life'], 'dx-chips dx-chips-lg') +
            '<p class="dx-note">Many adults — particularly women — develop strong masking strategies and only seek support after years of burnout, anxiety, or feeling persistently misunderstood.</p>'
            '<h3 class="dx-sub">Symptoms commonly overlap with:</h3>' + chips(['Anxiety and chronic stress', 'Low mood or depression', '<a href="/adult-autism-assessment/">Autism spectrum differences</a>', 'Trauma or attachment difficulties', 'Sleep difficulties and emotional dysregulation', '<a href="/care-main-page/adhd-assessments-for-women-approaching-perimenopause/">Hormonal transitions such as perimenopause</a>']) +
            statement('If you’ve spent years feeling that “something doesn’t fully fit” or traditional approaches have not brought clarity, a specialist adult ADHD assessment can help provide answers and direction.')),
        sec('dx-matters', 'matters-title', 'Why it matters', 'Why accurate diagnosis matters', 'Adults with undiagnosed ADHD often internalise years of struggle and self-criticism.',
            contrast('Over time, this can impact:', ['Confidence and self-esteem', 'Relationships and family life', 'Work performance and career progression', 'Physical and mental burnout', 'Emotional wellbeing and resilience'],
                     'A thoughtful, evidence-based diagnosis can:', ['Reduce shame', 'Increase self-understanding', 'Open the door to more effective support strategies'],
                     'For many people, understanding ADHD is not about “finding a label.” It is about finally understanding why life has felt harder than it should have.'), deco=wave('left')),
        sec('dx-approach', 'approach-title', 'Our approach', 'Our approach at Refocus: beyond questionnaires', 'ADHD is a complex neurodevelopmental condition, which is why meaningful assessment requires more than screening forms alone. At Refocus, we combine gold-standard clinical assessment methods with a holistic understanding of the brain, mental health, and lived experience.',
            features([('i-shield', 'Consultant Psychiatrist', 'Assessment by an experienced Consultant Psychiatrist with extensive experience in adult neurodevelopmental disorders'),
                      ('i-book', 'Full History', 'Developmental, psychosocial, educational, and mental-health history.'),
                      ('i-people', 'Structured DIVA-5 Interview', 'Conducted during the appointment as a gold-standard diagnostic tool.'),
                      ('i-doc', 'Pre-assessment Questionnaires', 'Evidence-based forms completed by you and an observer who knows you well — ideally one who knew you in childhood.'),
                      ('i-layers', 'Screening for co-occurring conditions', 'Anxiety, mood difficulties, autism traits, burnout and emotional dysregulation.')]), center=True, dark=True),
        sec('dx-tool-sec', 'tool-title', 'The gold standard', 'What is the DIVA-5?', '',
            split('<img class="dx-single reveal-img" src="/img/dr-report.webp" alt="A consultant psychiatrist reviewing a written assessment report" loading="lazy">',
                  '<p class="lede">The DIVA-5 (Diagnostic Interview for ADHD in Adults) is a gold-standard, NICE-aligned structured diagnostic interview based on DSM-5 ADHD criteria.</p><p>It:</p>' +
                  ul(['Explores symptoms in both childhood and adulthood', 'Assesses how ADHD impacts work, relationships, daily functioning, and emotional wellbeing', 'Uses real-life examples rather than simple tick-box questions', 'Helps differentiate ADHD from other conditions that can present similarly']) +
                  '<p class="ab-pull">Using the DIVA-5 ensures the assessment is structured, clinically robust, and evidence-based, while still allowing space for your individual story and lived experience.</p>')),
        sec('dx-pre', 'pre-title', 'Before you meet us', 'Pre-assessment questionnaires', 'Before your appointment, you will complete a series of evidence-based screening tools through our secure patient portal. These may include:',
            split('<ul class="dx-q">' + ''.join(f'<li><strong>{a}</strong>{b}</li>' for a, b in [('ASRS v1.1', 'Adult ADHD Self-Report Scale'), ('DASS-10', 'Depression, Anxiety and Stress Scale'), ('BAARS', 'Barkley Adult ADHD Rating Scale'), ('History forms', 'Additional developmental and psychosocial history forms')]) + '</ul>',
                  '<div class="dx-observer"><h3>Observer input — a key part of the assessment</h3><p>As part of a gold-standard diagnostic process, we also invite observer input from someone who knows you well now and, where possible, someone who knew you during childhood (such as a parent, close family member, long-term partner, or close friend). This helps us:</p>' +
                  ul(['Build a more objective and balanced understanding of your experiences', 'Explore how patterns may have been present across different stages of life', 'Meet diagnostic standards requiring evidence of childhood onset']) +
                  '<p class="ab-pull">At Refocus, we do not rely on self-report alone.</p><p>We integrate multiple perspectives to ensure your assessment is clinically robust, evidence-based, and truly reflective of how your brain works.</p></div>'), deco=wave('right')),
        sec('dx-adv', 'adv-title', 'Beyond the interview', 'Advanced tools we may include', 'Depending on presentation and clinical complexity, we may also recommend additional neuroscience-informed assessments.',
            split('<img class="dx-single reveal-img" src="/img/framework-map.webp" alt="A clinician fits a qEEG brain mapping headset on a patient" loading="lazy">',
                  f'<h3>qEEG Brain Mapping <small>(when clinically indicated)</small></h3><p><strong>{QEEG_NOTE}</strong></p><p>qEEG is not required for diagnosis, but in selected cases it can:</p>' +
                  ul(['Provide additional neurobiological insight', 'Support understanding of attention, regulation, and cognitive processing patterns', 'Help guide personalised recommendations and future interventions']) +
                  '<p>We are transparent about when qEEG is helpful and when it is not, and it is never used in isolation for diagnosis.</p><a class="text-link" href="/neuroscience-main-page/qeeg-brain-mapping/">About qEEG brain mapping <svg><use href="#i-right"/></svg></a>', reverse=True)),
        sec('dx-process', 'process-title', 'Step by step', 'The assessment process', '',
            steps([('Step 1', 'Before the appointment', '<p>Once a deposit is paid, patients receive secure access to our electronic health record patient portal.</p><p>You will receive:</p>' + ul(['Pre-assessment questionnaires', 'Observer forms', 'Developmental and mental-health screening tools', 'Consent and background forms']) + '<p>Our clinicians carefully review all information before the appointment so your consultation is focused, efficient, and meaningful.</p>'),
                   ('Step 2', 'During the assessment', ul(['Appointments typically last up to 90 min', 'You will meet with a senior Consultant Psychiatrist experienced in adult ADHD and neurodevelopmental conditions']) + '<p>The session includes the structured DIVA-5 interview alongside exploration of:</p>' + ul(['Childhood development and educational history', 'Work and occupational functioning', 'Relationships and emotional wellbeing', 'Strengths, coping strategies, and masking patterns', 'Mental health and overlapping conditions']) + '<p>We understand that ADHD rarely exists in isolation, which is why we take time to understand the wider picture — not just symptoms in isolation.</p><p>Where appropriate, we will share our clinical impression during the appointment and discuss next steps together.</p>'),
                   ('Step 3', 'After the assessment', '<p>You will receive a comprehensive, clear, and practical report including:</p>' + ul(['Diagnostic outcome (where criteria are met)', 'Differential diagnoses considered', 'Personalised recommendations for workplace or educational adjustments, psychological therapies or coaching, lifestyle and environmental strategies, and emotional wellbeing support', 'Medication guidance (if appropriate), including discussion around NHS shared-care pathways']) + '<p>We understand many adults wish to continue aspects of care through the NHS, and we will support you in understanding your options while being transparent about local GP variability regarding shared care.</p>')],
                  img='/img/consultation.webp')),
        sec('dx-how', 'how-title', 'Booking', 'Book a private Adult ADHD assessment', '',
            '<div class="dx-promises"><p>At Refocus, assessments are:</p>' + chips(['Clinically robust', 'Neurodevelopmentally informed', 'Compassionate and personalised', 'Focused on the whole person']) + '</div>' +
            split(booking(STD_BOOKING, 'This process allows us to prepare thoroughly and ensures every patient receives the right assessment, at the right time, with the right clinician.'),
                  price_box('Adult ADHD assessment', [('Virtual assessment', '£750', '£850'), ('Face-to-face assessment', '£850', '£1,050')]), cls='dx-how-split')),
        talk_band(),
    ]
    page('adult-adhd-assessment', 'Private Adult ADHD Assessment Manchester &amp; Online | Refocus',
         'Consultant psychiatrist-led adult ADHD assessment using DIVA-5, with optional qEEG brain mapping. NICE-aligned report for your GP. Online or in Manchester.',
         '/img/hero-adult-adhd.webp',
         H('/img/hero-adult-adhd.webp', 'A man pauses to think at a desk covered in sticky notes', 'Adult ADHD assessment',
           'Adult ADHD assessment at Refocus The Brain Hub', 'A neuroscience-informed, personalised assessment for adults.'), sections)


# ================================================================ Adult autism
def adult_asd():
    sections = [
        intro(['At Refocus, our goal is not simply to identify autism, but to understand how your mind works, how you have adapted over a lifetime, and what support will genuinely help.',
               'Every assessment is Consultant-led and follows NICE guideline CG142 on autism diagnosis in adults, using the structured tools NICE recommends — the ADI-R developmental interview and the ADOS-2 observation.'],
              '/img/adult-autism-intro.webp', 'A man reading in an armchair at home, headphones around his neck', 'Adult autism', 'How your mind works, and how you have adapted', sat='/img/who-diagnosed.webp'),
        sec('dx-signs', 'signs-title', 'Is it autism?', 'Is an autism assessment right for me?', 'Autism in adulthood rarely looks the way people expect. Some adults recognise themselves the moment they read about it. Others have spent decades appearing to cope, while privately managing:',
            chips(['Exhaustion after ordinary social contact', 'Sensory overload — noise, light, texture, crowds', 'A real need for routine, and genuine distress when it breaks', 'Unwritten social rules that others seem to absorb effortlessly', 'Deep, focused interests that have always felt central'], 'dx-chips dx-chips-lg') +
            '<p class="dx-note">Many adults — particularly women, and those given a diagnosis of anxiety or depression first — develop sophisticated masking strategies, and only seek an assessment after years of burnout or feeling persistently misunderstood.</p>'
            '<h3 class="dx-sub">Autistic traits are commonly mistaken for:</h3>' + chips(['Anxiety and chronic stress', 'Low mood or depression', '<a href="/adult-adhd-assessment/">ADHD and executive function difficulties</a>', 'Trauma or attachment difficulties', 'Sleep difficulties and emotional dysregulation', 'Social anxiety or avoidant traits']) +
            statement('If you have spent years feeling that “something doesn’t quite fit”, or earlier explanations have never fully made sense, a specialist adult autism assessment can offer clarity and direction.')),
        sec('dx-matters', 'matters-title', 'Why it matters', 'Why accurate diagnosis matters', 'Adults who are autistic without knowing it often absorb years of self-blame for finding things harder than everyone else appeared to.',
            contrast('Over time, that can affect:', ['Confidence and self-esteem', 'Relationships and family life', 'Work, study and career progression', 'Autistic burnout and exhaustion', 'Emotional wellbeing and resilience'],
                     'A careful, evidence-based assessment can:', ['Reduce shame', 'Deepen self-understanding', 'Open the door to adjustments and support that actually fit'],
                     'For many people, an autism assessment is not about “getting a label.” It is about finally understanding why life has taken so much more effort than it seemed to for everyone else.'), deco=wave('left')),
        sec('dx-approach', 'approach-title', 'Our approach', 'Our approach at Refocus: beyond questionnaires', 'Autism is a lifelong difference in how the brain processes social information, sensory input and change — which is why a meaningful assessment needs far more than a screening questionnaire. At Refocus, we combine the structured tools NICE recommends with a holistic understanding of the brain, mental health and lived experience.',
            features([('i-shield', 'Consultant Psychiatrist', 'Assessment led by an experienced Consultant Psychiatrist trained in ADOS-2 and ADI-R — the tools NICE recommends for diagnosing autism.'),
                      ('i-book', 'Developmental History', 'Developmental, educational, psychosocial and mental-health history, explored in depth.'),
                      ('i-people', 'Structured ADI-R Interview', 'The Autism Diagnostic Interview–Revised, exploring early development with someone who knew you as a child.'),
                      ('i-doc', 'Pre-assessment Questionnaires', 'Evidence-based forms completed by you and, where possible, someone who has known you since childhood.'),
                      ('i-layers', 'Screening for co-occurring conditions', 'Anxiety, mood difficulties, ADHD traits, autistic burnout and emotional dysregulation.')]), center=True, dark=True),
        sec('dx-tool-sec', 'tool-title', 'The gold standard', 'What are the ADOS-2 and ADI-R?', '',
            split('<img class="dx-single reveal-img" src="/img/clinic/quiet-room.webp" alt="A calm, quiet assessment room at the Refocus clinic" loading="lazy">',
                  '<p class="lede">The ADOS-2 (Autism Diagnostic Observation Schedule) and the ADI-R (Autism Diagnostic Interview–Revised) are the structured assessment tools NICE recommends for diagnosing autism.</p><p>Together they:</p>' +
                  ul(['Observe social communication and interaction directly, rather than relying on self-report', 'Explore developmental history from early childhood through to the present', 'Examine patterns of behaviour, focused interests and sensory experiences', 'Help distinguish autism from conditions that can present similarly']) +
                  '<p class="ab-pull">Using the ADOS-2 and ADI-R together makes the assessment structured, clinically robust and evidence-based, while still leaving room for your own story and lived experience.</p>')),
        sec('dx-pre', 'pre-title', 'Before you meet us', 'Pre-assessment questionnaires', 'Before your appointment, you will complete a series of evidence-based screening tools through our secure patient portal. These may include:',
            split('<ul class="dx-q">' + ''.join(f'<li><strong>{a}</strong>{b}</li>' for a, b in [('AQ-10', 'Autism Spectrum Quotient, 10-item'), ('Wellbeing', 'Mood, anxiety and wellbeing screening tools'), ('Daily living', 'Sensory and daily-living questionnaires'), ('History forms', 'Additional developmental and psychosocial history forms')]) + '</ul>',
                  '<div class="dx-observer"><h3>Informant input — central to an autism assessment</h3><p>The ADI-R is an informant interview, so wherever possible we invite input from someone who knew you as a child — a parent, older sibling or close family member — alongside someone who knows you well now. Where no childhood informant is available, we adapt the assessment and tell you openly how that shapes it. Informant input helps us:</p>' +
                  ul(['Build a fuller, more balanced picture than self-report alone can give', 'Understand how traits were present in early development', 'Meet the diagnostic standard, which requires evidence of early developmental onset']) +
                  '<p>At Refocus we never rely on self-report alone. We bring several perspectives together so your assessment is clinically robust, evidence-based, and a true reflection of how your mind works.</p></div>'), deco=wave('right')),
        sec('dx-adv', 'adv-title', 'Beyond the interview', 'Advanced tools we may include', 'Depending on your presentation and clinical complexity, we may also recommend additional neuroscience-informed assessments.',
            split('<img class="dx-single reveal-img" src="/img/framework-map.webp" alt="A clinician fits a qEEG brain mapping headset on a patient" loading="lazy">',
                  f'<h3>qEEG Brain Mapping <small>(when clinically indicated)</small></h3><p><strong>{QEEG_NOTE}</strong></p><p>qEEG plays no part in diagnosing autism, but in selected cases it can:</p>' +
                  ul(['Give additional insight into how your brain regulates attention and arousal', 'Help make sense of sensory sensitivity, overload and fatigue', 'Guide personalised recommendations and any future neuroscience-led support']) +
                  '<p>NICE is explicit that no brain scan, blood test or genetic test diagnoses autism. We are equally clear about when qEEG adds something useful and when it does not — and it is never used to make a diagnosis.</p>', reverse=True)),
        sec('dx-process', 'process-title', 'Step by step', 'The assessment process', '',
            steps([('Step 1', 'Before the appointment', '<p>Once a deposit is paid, you receive secure access to our electronic health record patient portal.</p><p>You will receive:</p>' + ul(['Pre-assessment questionnaires', 'Informant forms', 'Developmental and mental-health screening tools', 'Consent and background forms']) + '<p>Our clinicians review everything before your appointment, so the session itself stays focused and meaningful.</p>'),
                   ('Step 2', 'During the assessment', ul(['You will meet a senior Consultant Psychiatrist trained in ADOS-2 and ADI-R', 'The ADOS-2 observation is carried out by a highly specialised ADOS-trained practitioner']) + '<p>The session explores:</p>' + ul(['Early development, childhood and education', 'Social communication and relationships', 'Sensory experiences and environment', 'Routines, focused interests, and how change feels', 'Masking, coping strategies, and what they cost', 'Mental health and any coexisting conditions']) + '<p>All clinical information is brought together in a multidisciplinary team discussion. Autism rarely exists in isolation — it frequently co-occurs with ADHD — which is why we take time to understand the wider picture rather than traits in isolation.</p><p>Where appropriate, we will share our clinical impression during the appointment and discuss next steps together.</p>'),
                   ('Step 3', 'After the assessment', '<p>You will receive a comprehensive, clear and practical report including:</p>' + ul(['Diagnostic outcome (where criteria are met)', 'Differential diagnoses considered', 'A profile of your strengths, needs and sensory world', 'Personalised recommendations for workplace or educational adjustments, psychological support and coaching, sensory and environmental strategies, and emotional wellbeing and burnout recovery', 'Guidance on any coexisting conditions identified, and how to take them forward']) + '<p>Support after an autism diagnosis is about understanding, adjustments and any coexisting conditions — not about treating autism itself. Your report is written to be used: with employers, universities, your GP and wider support services.</p>')],
                  img='/img/clinic/consult-room.webp')),
        sec('dx-how', 'how-title', 'Booking', 'Enquire about a private adult autism assessment', '',
            '<div class="dx-promises"><p>At Refocus, assessments are:</p>' + chips(['Clinically robust', 'Neurodevelopmentally informed', 'Compassionate and personalised', 'Focused on the whole person']) + '</div>' +
            split(booking([STD_BOOKING[0], STD_BOOKING[1], ('Complete online forms', 'Including your own and informant screening tools.'), STD_BOOKING[3], STD_BOOKING[4]], 'This process allows us to prepare thoroughly and ensures every patient receives the right assessment, at the right time, with the right clinician.'),
                  price_box('Adult autism assessment', [('Virtual assessment', '£1,500', None), ('Face-to-face assessment', '£1,800', None)], note='Ask about our current special offer prices on your free call.'), cls='dx-how-split')),
        talk_band(),
    ]
    page('adult-autism-assessment', 'Private Adult Autism Assessment Manchester | Refocus',
         'Consultant psychiatrist-led adult autism assessment using ADOS-2 and ADI-R, the tools NICE recommends. Online or in Manchester, with a report you can use.',
         '/img/hero-adult-asd.webp',
         H('/img/hero-adult-asd.webp', 'A woman wearing noise-cancelling headphones reads calmly in a quiet corner', 'Adult autism assessment',
           'Adult autism assessment at Refocus The Brain Hub', 'A structured, neurodiversity-informed autism assessment for adults.'), sections)


# ================================================================ Women & perimenopause
def women():
    inc = [('i-people', 'Clinical Interview &amp; Developmental Exploration', ['Detailed clinical interview exploring lifelong attention, organisation, and emotional regulation patterns', 'Mapping of symptoms across development, education, work, relationships, and parenting', 'Exploration of recent changes linked to hormonal transition']),
           ('i-doc', 'DIVA-5 Diagnostic Interview', ['Gold-standard structured diagnostic interview aligned with DSM-5 ADHD criteria', 'Assesses childhood and adult ADHD symptoms', 'Explores functional impairment across multiple life domains', 'Helps distinguish ADHD from anxiety, burnout, or mood disorders']),
           ('i-wave', 'MOXO AI ADHD Test', ['FDA-cleared computer-based test', 'Provides objective data on attention, impulsivity, hyperactivity, and timing', 'Tested under real-life distractors', 'Supports clinical decision-making alongside interview and history']),
           ('i-book', 'Adult Screening Questionnaires', ['ADHD symptom and impairment scales', 'Anxiety and mood screening', 'Functional and occupational impact measures', 'Informant questionnaires from partner, family member, or colleague']),
           ('i-venus', 'Perimenopause &amp; Menopause Screening', ['Menstrual and hormonal history', 'Vasomotor symptoms (hot flushes, night sweats)', 'Sleep disturbance assessment', 'Cognitive changes and brain fog evaluation', 'Optional blood tests and qEEG brain mapping when appropriate']),
           ('i-layers', 'MDT Discussion &amp; Formulation', ['All cases reviewed in MDT with Medical Director', 'Holistic consideration of neurodevelopmental history', 'Integration of hormonal transition and mental health context', 'Balanced, evidence-based, and individualised recommendations'])]
    inc_html = '<div class="dx-inc-grid">' + ''.join(f'<article class="dx-inc"><span class="ico"><svg><use href="#{i}"/></svg></span><h3>{t}</h3>{ul(items)}</article>' for i, t, items in inc) + '</div>'
    sections = [
        sec('dx-missed', 'missed-title', 'Why it’s missed', 'Why ADHD is often missed in women', 'Many women with ADHD are not identified in childhood. The signs can be subtle and easily attributed to personality traits or life circumstances.',
            split(collage('/img/woman-window.webp', '/img/who-woman.webp', 'A woman in her late forties sitting by a window, calm and reflective', 'A woman smiling on her sofa'),
                  features([('i-heart', 'Masking Difficulties', 'Girls often mask difficulties by overcompensating, presenting as anxious, perfectionistic, or emotionally sensitive rather than ‘hyperactive’.'),
                            ('i-book', 'Academic Performance', 'Many perform well academically until demands increase, making ADHD harder to identify in childhood.'),
                            ('i-venus', 'Hormonal Changes', 'As oestrogen levels fluctuate during perimenopause, dopamine regulation becomes more vulnerable, and ADHD traits may become unmasked or significantly worse.')], cols=1)), sid='start', deco=wave('right')),
        sec('dx-symptoms', 'sym-title', 'Recognise this?', 'Common symptoms during perimenopause', '',
            chips(['Brain fog and forgetfulness', 'Feeling overwhelmed', 'Coping strategies no longer working', 'Emotional lability', 'Concentration difficulties'], 'dx-chips dx-chips-lg') +
            '<p class="dx-note">These symptoms may reflect perimenopause, burnout, anxiety, sleep disturbance, or neurodevelopmental vulnerability interacting with hormonal change.</p>' +
            statement('This is why our approach is holistic and menopause-informed.') +
            '<div class="dx-right"><h3>Is this assessment right for you?</h3>' + ul(['A woman approaching or experiencing perimenopause', 'Not previously diagnosed with ADHD but now struggling with focus, organisation, or overwhelm', 'Unsure whether difficulties are due to ADHD, hormonal change, or both'], 'dx-tick-list') + '</div>', center=True),
        sec('dx-approach', 'approach-title', 'Our approach', 'Our Refocus women’s ADHD assessment approach', 'Assessments are led by our Advanced Nurse Practitioner, who has extensive experience in adult ADHD assessments, brings lived experience of ADHD, and is completing a PhD in perimenopause. She leads the Refocus Perimenopausal &amp; Menopausal Women’s Service. All cases are reviewed and discussed with the Medical Director as part of MDT governance.',
            features([('i-shield', 'NICE-Compliant', 'NHS-recognised assessments following national guidelines'), ('i-people', 'MDT-Led', 'Conducted within a multidisciplinary team'),
                      ('i-venus', 'Midlife-Focused', 'Designed specifically for women at midlife'), ('i-heart', 'Expert-Led', 'Led by specialists with lived experience')], cols=4) +
            team(['williams', 'vrajitoriu']), center=True, dark=True),
        sec('dx-includes-sec', 'inc-title', 'What’s included', 'What the assessment includes', 'A comprehensive, evidence-based assessment designed to understand your unique experience and provide clear answers.', inc_html, center=True, deco=wave('left')),
        sec('dx-after', 'after-title', 'After the assessment', 'After the assessment', 'You will receive a clear, comprehensive report with actionable recommendations tailored to your unique situation.',
            split('<img class="dx-single reveal-img" src="/img/woman-light.webp" alt="A woman with her eyes closed in warm sunlight" loading="lazy">',
                  features([('i-doc', 'Diagnostic Outcome', 'Clear ADHD diagnosis where criteria are met, with differential diagnoses considered'), ('i-brain', 'Personalised Formulation', 'Explaining how hormones, brain function, and mental health interact in your case'),
                            ('i-path', 'Treatment Pathways', 'ADHD-specific strategies, menopause-focused interventions, or psychological support'), ('i-compass', 'Workplace Adjustments', 'Recommendations for reasonable adjustments in your work environment')], cols=1))),
        sec('dx-how', 'how-title', 'Prices', 'Neuro-Hormone ADHD Pathway™ prices', '',
            split(booking([('Book online', 'Request a women’s ADHD assessment'), ('Pay deposit', '£250 deposit unlocks access to Medesk portal'), ('Complete questionnaires', 'Online screening and informant questionnaires'),
                           ('Assessment booked', 'With our Advanced Nurse Practitioner, with MDT oversight'), ('Final payment', 'Remaining balance paid before the appointment')]),
                  price_box('Neuro-Hormone ADHD Pathway™', [('Virtual: ADHD + mental health and perimenopause', '£750', '£900'), ('Face-to-face: ADHD + mental health and perimenopause', '£850', '£1,000')]), cls='dx-how-split')),
        f'''    <section class="section dx dx-info" aria-labelledby="info-title">
      <div class="wrap dx-info-grid">
        <div>
          <p class="kicker">Booking information</p>
          <h2 id="info-title">Who this clinic is for</h2>
          <p class="lede">This specialist clinic is for women aged 40+ who are experiencing ADHD-related difficulties that have worsened during perimenopause or menopause, such as changes in focus, emotional regulation, mental energy, and cognitive clarity.</p>
          <p>We focus on the interaction between ADHD, hormones, cognition, mood, energy, and executive functioning, for a holistic understanding and support.</p>
          <div class="dx-important"><h3>Important information</h3>{ul(['This clinic is not suitable for acute mental health presentations.', 'It does not assess or treat bipolar disorder, psychosis, or active suicidal ideation.'])}</div>
          <p>If you are happy to proceed, please complete the brief pre-booking screening.</p>
          <a class="btn btn-primary btn-lg" href="{FREE_CALL}">Book now</a>
        </div>
        <aside class="dx-safety" aria-labelledby="safety-title">
          <h3 id="safety-title">Important safety notice</h3>
          <p><strong>This clinic does not provide crisis or acute mental health care.</strong></p>
          <p>If you are currently experiencing:</p>
          {ul(['Suicidal thoughts', 'Significant risk to yourself', 'Acute psychiatric symptoms'])}
          <p>Please contact:</p>
          {ul(['<a href="tel:111">NHS 111</a> for urgent advice', 'Your GP or local mental health service', '<a href="tel:999">999</a> / A&amp;E in an emergency'])}
          <p class="pg-small">Refocus assessments are not an emergency service.</p>
        </aside>
      </div>
    </section>
''',
        talk_band(),
    ]
    page('care-main-page/adhd-assessments-for-women-approaching-perimenopause', 'ADHD Assessment for Women &amp; Perimenopause | Refocus',
         'ADHD in women often goes unrecognised until perimenopause. Consultant-led assessment exploring attention, brain fog, hormones and masking. Manchester.',
         '/img/hero-women.webp',
         H('/img/hero-women.webp', 'A woman in her late forties holds a coffee and gazes thoughtfully out of the kitchen window', 'Women’s ADHD &amp; perimenopause',
           'ADHD assessments for women approaching perimenopause', 'A holistic neuropsychiatric pathway designed for women at midlife. We recognise that ADHD, hormones, and mental health intersect—so you receive clarity rather than fragmented explanations.',
           [('Learn more', '#start', 'btn-primary'), ('Book now', FREE_CALL, 'btn-ghost')]), sections)


if __name__ == '__main__':
    hub()
    child_adhd()
    child_asd()
    combined()
    psychiatric()
    adult_adhd()
    adult_asd()
    women()
