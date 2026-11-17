"""Build the Refocus neuroscience and care pages.

Usage: python3 tools/build_neuro.py .
Reuses the page shell in tools/build_pages.py and the building blocks in tools/build_diagnosis.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import build, hero, cta_band, FREE_CALL  # noqa: E402
from build_diagnosis import (REVIEWS, REGULATED, sec, wave, ul, chips, features, split, collage, contrast,  # noqa: E402
                             tools, steps, booking, team, price_box, statement, talk_band, faq, intro)

NEURO = '/neuroscience-main-page/'
QEEG = NEURO + 'qeeg-brain-mapping/'
EXO = NEURO + 'exomind/'
NF = NEURO + 'neurofeedback/'
PBM = NEURO + 'photobiomodulation/'
CARE = '/care-main-page/'
NHC = '/neurohormone-clinic/'
MEDS = CARE + 'adhd-medication-treatment-pathway/'
HRT = CARE + 'hrt-treatment-pathway/'
WOMEN = CARE + 'adhd-assessments-for-women-approaching-perimenopause/'


def page(slug, title, desc, hero_img, hero_html, sections, current):
    main = '  <main id="main">\n' + hero_html + ''.join(sections) + '  </main>\n'
    build(slug, title, desc, hero_img, main, current=current)


def H(img, alt, kicker, h1, sub, ctas=None):
    ctas = ctas or [('Explore our approach', '#start', 'btn-primary'), ('Book now', FREE_CALL, 'btn-ghost')]
    out = hero(img, alt, kicker, h1, sub, ctas, pos='78% center')
    return out.replace('<h1 id="pg-title">', '<h1 id="pg-title" class="is-long">') if len(h1) > 48 else out


def card(img, title, sub, text, tags, href, cta='Learn more', alt=''):
    t = chips(tags) if tags else ''
    s = f'<p class="nc-card-sub">{sub}</p>' if sub else ''
    return f'''<article class="dx-svc">
            <div class="dx-svc-media"><img src="{img}" alt="{alt}" loading="lazy"></div>
            <div class="dx-svc-body">
              <h3><a href="{href}">{title}</a></h3>{s}
              <p>{text}</p>
              {t}
              <div class="btn-row"><a class="btn btn-primary" href="{href}">{cta}</a><a class="text-link" href="{FREE_CALL}">Book now <svg><use href="#i-right"/></svg></a></div>
            </div>
          </article>'''


def cards(items, cols=3):
    return f'<div class="dx-svc-grid dx-svc-compact nc-grid-{cols}">' + ''.join(items) + '</div>'


def timeline(items):
    lis = ''.join(f'<li><span class="n">{k + 1:02d}</span><div><h3>{t}</h3>{x if x.startswith("<") else f"<p>{x}</p>"}</div></li>' for k, (t, x) in enumerate(items))
    return f'<ol class="dx-timeline">{lis}</ol>'


def safety(sid, h2, intro_ps, list_lead, items, outro_ps, img, alt, kicker='Safety first', btn='Book now'):
    ps = ''.join(f'<p class="{"lede" if i == 0 else ""}">{p}</p>' for i, p in enumerate(intro_ps))
    outro = ''.join(f'<p>{p}</p>' for p in outro_ps)
    return f'''    <section class="section dx nc-safety" id="{sid}" aria-labelledby="{sid}-title">
      <div class="wrap">
        {split(f'<img class="dx-single reveal-img" src="{img}" alt="{alt}" loading="lazy">',
               f'<p class="kicker">{kicker}</p><h2 id="{sid}-title">{h2}</h2>{ps}<div class="dx-important"><h3>{list_lead}</h3>{ul(items)}</div>{outro}<a class="btn btn-primary btn-lg" href="{FREE_CALL}">{btn}</a>', reverse=True)}
      </div>
    </section>
'''


def pathways_band():
    links = [('qEEG Brain Mapping', QEEG, 'i-brain'), ('Exomind TMS', EXO, 'i-wave'), ('Neurofeedback', NF, 'i-infinity'), ('Photobiomodulation', PBM, 'i-sun')]
    lis = ''.join(f'<li><a href="{h}"><span class="ico"><svg><use href="#{i}"/></svg></span>{t}<svg class="arr"><use href="#i-right"/></svg></a></li>' for t, h, i in links)
    return f'<ul class="nc-paths">{lis}</ul>'


NEURO_TALK = ('Not sure which route is right for you?', 'Start with a conversation. We’ll listen to your goals, explain honestly what each technique can and can’t do, and tell you whether brain mapping would add value first.')
QEEG_REDUCED = 'qEEG brain mapping costs £200 instead of £350 when booked alongside any Refocus service.'


# ================================================================ Neuroscience hub
def neuro_hub():
    faqs = [
        ('1. How safe are your neuroscience treatments and who are they suitable for?',
         '<p>At Refocus Neuroscience, safety and clinical integrity are central to everything we do.</p><p>We offer evidence-informed neuromodulation approaches including:</p>' + ul(['qEEG Brain Mapping', 'Exomind TMS', 'Neurofeedback', 'Transcranial Photobiomodulation (tPBM)']) +
         '<p>All treatments are delivered within a medically governed environment, with clinical screening completed prior to starting any programme.</p><p>Non-invasive neuromodulation techniques such as TMS, neurofeedback and photobiomodulation have strong safety profiles when delivered appropriately. Most people experience minimal side effects, which may include mild scalp discomfort, transient headache or temporary fatigue depending on the modality used.</p><p>Before starting, we assess:</p>' +
         ul(['Medical and psychiatric history', 'Medication use', 'Neurological considerations', 'Suitability for stimulation-based therapies']) +
         '<p>If a treatment is not appropriate, we will advise accordingly. Not everyone needs neuromodulation, and not everyone is suitable for every modality.</p><p>Our approach is measured, ethical and personalised.</p>'),
        ('2. Do I need a qEEG brain map before starting treatment?',
         '<p>Not always, but in many cases, it is highly beneficial.</p><p>qEEG brain mapping provides objective data about brainwave patterns, connectivity and functional regulation. It allows us to understand how your brain is operating before intervention.</p><p>Some individuals choose qEEG:</p>' +
         ul(['To guide neurofeedback protocols', 'To personalise stimulation targets', 'To better understand symptoms such as brain fog, attention difficulty or emotional dysregulation', 'To track progress over time']) +
         '<p>However, certain treatments, such as standard Exomind TMS protocols, can be delivered based on established clinical targeting without qEEG.</p><p>We will advise you on whether qEEG adds meaningful value in your specific situation. Our aim is precision, not unnecessary investigation.</p>'),
        ('3. Can treatments be combined, and how do they fit alongside psychiatric care?',
         '<p>Yes, and this is where Refocus is different.</p><p>We are structured as a Brain Hub, meaning neuroscience services sit alongside psychiatric diagnostics and ongoing care.</p><p>Depending on your goals, treatments may be:</p>' +
         ul(['Used independently', 'Integrated with ADHD medication', 'Combined sequentially (for example qEEG-guided neurofeedback with Exomind TMS)', 'Used as part of a wider wellbeing or cognitive optimisation plan']) +
         '<p>We carefully consider:</p>' + ul(['Clinical indication', 'Treatment timing', 'Neuroplasticity principles', 'Your personal capacity and schedule']) +
         '<p>Neuromodulation is not a replacement for psychiatric care where medication or therapy is indicated, nor is medication always the only solution.</p><p>Our role is to integrate both worlds responsibly.</p><p>You will always receive a clear plan outlining:</p>' +
         ul(['Recommended modality', 'Expected duration', 'Monitoring approach', 'Outcome tracking']) +
         '<p>The goal is measurable improvement, in mood, cognition, focus or emotional regulation, not simply completing sessions.</p>'),
    ]
    mods = cards([
        card('/img/svc-neuromod.webp', 'Exomind TMS', 'Network-level change', 'Best when we want to influence specific circuits linked to mood, drive, regulation, and cognitive control. It’s often used when someone feels stuck, like the brain can’t shift gears even when they’re doing ‘all the right things’.', ['Wellbeing', 'Mood', 'Focus', 'Control', 'Performance'], EXO),
        card('/img/nf-session.webp', 'Neurofeedback', 'Self-regulation training', 'Neurofeedback is like a gym for the nervous system. The brain receives feedback and gradually learns to spend more time in steadier, more efficient states, supporting regulation of attention, arousal, sleep and emotional reactivity.', ['Focus', 'Regulation', 'Resilience', 'Balance', 'Sleep'], NF),
        card('/img/hero-tpbm.webp', 'Photobiomodulation', 'Cellular support + recovery', 'Photobiomodulation uses specific wavelengths of light to support cellular energy processes, often positioned around recovery, resilience, and supporting brain function under strain.', ['Energy', 'Clarity', 'Repair', 'Longevity', 'Brain health'], PBM),
    ])
    sections = [
        f'''    <section class="dx-belief nc-belief" id="start" aria-label="Our principle">
      <div class="wrap"><p>Neuroplasticity is neutral. <span>It can build resilience or reinforce stress and burnout.</span></p>
      <p class="nc-belief-sub">We measure brain function first, then apply targeted, neuroscience-informed interventions to support healthier patterns.</p></div>
    </section>
''',
        sec('nc-plastic', 'plastic-title', 'What we mean by “neuroplasticity”', 'The brain’s natural ability to change', 'Neuroplasticity is the brain’s natural ability to change, adapt and re-organise itself through life.',
            split('<img class="dx-single reveal-img" src="/img/neuroplasticity.webp" alt="A glowing network of neural pathways forming around the outline of a head" loading="lazy">',
                  features([('i-spark', 'New neural pathways', 'When you learn or experience something new'),
                            ('i-layers', 'Stronger connections', 'Practised activities or behaviours make pathways stronger and more efficient'),
                            ('i-leaf', 'Unused pathways fade', 'Underused networks gradually weaken and fade'),
                            ('i-flask', 'Cellular-level changes', 'Changes in brain signalling, neurotransmitters and how brain cells communicate')], cols=1)) +
            '<div class="nc-influence"><p>In everyday life, neuroplasticity is influenced by things like</p>' + chips(['Stress', 'Sleep', 'Emotions', 'Learning', 'Attention', 'Exercise', 'New experiences'], 'dx-chips dx-chips-lg') + '</div>' +
            statement('Refocus exists to help people use neuroplasticity on purpose, especially when life has pushed the brain into patterns that no longer serve them.'), deco=wave('right')),
        sec('nc-why', 'why-title', 'Why Refocus is different', 'Why Refocus combines qEEG brain mapping with neuromodulation', 'Many services start with symptoms. <strong>We start with brain-based insight.</strong>',
            '<div class="nc-two">'
            f'<article class="nc-stage"><span class="nc-stage-k">Step 1</span><img src="/img/qeeg-tablet.webp" alt="An iSyncWave qEEG headset beside a tablet showing colourful brain maps" loading="lazy"><div><h3>qEEG brain mapping</h3><p>qEEG helps us understand how your brain is functioning right now, your baseline patterns, strengths, and areas under strain. It can help us make your plan more precise.</p><p>For example, clarifying whether the brain looks more like it’s:</p>{ul(["Stuck in over-arousal / threat mode", "Running on low energy / low activation", "Struggling with attention regulation", "Showing signs of cognitive fatigue / overload"])}<p class="nc-result"><strong>Result:</strong> a clearer picture to guide the “what next” choice.</p><a class="text-link" href="{QEEG}">About qEEG brain mapping <svg><use href="#i-right"/></svg></a></div></article>'
            f'<article class="nc-stage"><span class="nc-stage-k">Step 2</span><img src="/img/svc-neuromod.webp" alt="A patient relaxes during an Exomind session with a clinician at the console" loading="lazy"><div><h3>Neuromodulation</h3><p>Neuromodulation is how we deliver targeted input to help the brain practise healthier patterns, supporting neuroplasticity in a structured way.</p><p>At Refocus, we chose three complementary techniques because they work at different “levels” of the system:</p><ul class="check-list"><li><strong>Exomind TMS</strong> - targeted stimulation of specific brain networks</li><li><strong>Neurofeedback</strong> - training the brain to self-regulate</li><li><strong>Photobiomodulation</strong> - supporting brain energy &amp; recovery</li></ul></div></article>'
            '</div>', center=True, dark=True),
        sec('nc-mods', 'mods-title', 'Because “one size fits none” in neuroscience', 'Why we chose three techniques', 'Each technique works at a different level of the system, so your plan can match what your brain actually needs.', mods, deco=wave('left')),
        sec('nc-decide', 'decide-title', 'Your personalised plan', 'How we decide what you need', 'A step-by-step approach to understanding your brain and creating your personalised plan.',
            timeline([('Discovery &amp; clinical context', 'We understand your goals, symptoms, history, sleep, stress load and what ‘better’ could look like.'),
                            ('qEEG brain mapping', 'When appropriate, we map patterns and identify likely drivers of symptoms.'),
                            ('Personalised plan', 'We recommend the most suitable route: Exomind TMS, Neurofeedback, Photobiomodulation or a sequenced combination.'),
                            ('Progress tracking', 'We track outcomes (and repeat mapping when useful) so your plan stays responsive.')]), center=True),
        f'''    <section class="section nc-next on-dark" aria-labelledby="next-title">
      <img src="/img/hero-neuro.webp" alt="" loading="lazy" data-parallax>
      <div class="wrap nc-next-inner">
        <p class="kicker">Choose your next step</p>
        <h2 id="next-title">Ready to understand your brain and create a plan that works for you?</h2>
        <div class="btn-row"><a class="btn btn-primary btn-lg" href="{FREE_CALL}">Book now</a></div>
        <p class="nc-next-or">Or go straight to a pathway</p>
        {pathways_band()}
      </div>
    </section>
''',
        REVIEWS,
        faq(faqs, 'FAQ'),
        REGULATED,
        cta_band('Not sure where to start?', 'Start with a free 15-minute call', NEURO_TALK[1]),
    ]
    page('neuroscience-main-page', 'Brain Mapping, TMS &amp; Neurofeedback Manchester | Refocus',
         'Brain mapping, TMS, neurofeedback and photobiomodulation in Manchester. Psychiatry and neuroscience combined to support focus, mood and brain health.',
         '/img/hero-neuro.webp',
         H('/img/hero-neuro.webp', 'A woman relaxes with her eyes closed while wearing an iSyncWave brain mapping headset', 'Refocus Neuroscience · Neuroplasticity',
           'Brain mapping &amp; targeted neuromodulation for meaningful, lasting change',
           'At Refocus, our Neuroscience arm is grounded in a single, evidence-based principle: the brain is capable of change. Through neuroplasticity, neural networks can strengthen, reorganise, or quieten in response to repeated patterns of attention, behaviour, and experience. This adaptive capacity underpins learning, recovery, and regulation across the lifespan.'),
         sections, NEURO)


# ================================================================ qEEG
def qeeg():
    who = [('i-peak', 'Neurotypical brains seeking performance &amp; clarity', ['Focus, speed, mental stamina', 'Cognitive sharpness and resilience', 'Professional, academic, and athletic optimisation']),
           ('i-puzzle', 'Neurodivergent &amp; complex minds', ['ADHD, autism, learning differences', 'Girls and women who mask or are under-recognised', 'Mixed presentations that don’t fit neat diagnostic boxes', 'When symptoms don’t match ability']),
           ('i-people', 'Children &amp; adolescents', ['Understanding cognitive age vs chronological age', 'Identifying learning readiness and attention capacity', 'Informing school, home, and therapeutic pathways']),
           ('i-lifespan', 'Adults &amp; cognitive health monitoring', ['Identifying EEG markers linked to Mild Cognitive Impairment (MCI) and early Alzheimer’s detection', 'Differentiating stress, neurodivergence, and early cognitive change'])]
    who_html = '<div class="dx-inc-grid nc-who">' + ''.join(f'<article class="dx-inc"><span class="ico"><svg><use href="#{i}"/></svg></span><h3>{t}</h3>{ul(x)}</article>' for i, t, x in who) + '</div>'
    sections = [
        intro(['iSyncWave™, a 2022 Red Dot Award winner, is an intelligent brain-mapping system for modern neuroscience.',
               'At Refocus, it helps us see how a brain actually functions, beyond questionnaires, labels, or self-reports, revealing connectivity, efficiency, and processing speed.'],
              '/img/qeeg-tablet.webp', 'An iSyncWave headset on a desk beside a tablet showing colourful qEEG brain maps', 'Winner · 2022 Red Dot Award', 'Why iSyncWave™ at Refocus is different', sat='/img/framework-map.webp'),
        sec('nc-db', 'db-title', 'Global qEEG intelligence', 'Powered by a global qEEG intelligence database', 'Unlike traditional EEGs, iSyncWave™ compares your brain data to thousands of qEEGs across age groups and brain profiles, enabling us to:',
            features([('i-compass', 'Spot subtle patterns', 'Identify subtle patterns missed by standard assessments'),
                      ('i-wave', 'Read the effort', 'Understand compensation, fatigue, and neural efficiency'),
                      ('i-heart', 'Neuroaffirming', 'Contextualise neurodivergence rather than pathologise it'),
                      ('i-path', 'Track change', 'Track cognitive change over time')], cols=4) +
            statement('This is especially important when questionnaires are inconclusive, contradictory, or fail to capture lived experience.'), center=True, dark=True),
        sec('nc-who-sec', 'who-title', 'Who it’s for', 'Who is iSyncWave™ for?', '', who_html, center=True, deco=wave('left')),
        sec('nc-explain', 'explain-title', 'Explained simply', 'iSyncWave™ brain mapping explained simply', '',
            split('<img class="dx-single reveal-img" src="/img/framework-map.webp" alt="A clinician fits an iSyncWave headset on a patient" loading="lazy">',
                  '<h3>What is iSyncWave™?</h3><p class="lede">iSyncWave™ is a comfortable, non-invasive EEG brain scan that measures how your brain works, including attention, processing speed, and how different brain areas communicate.</p>' +
                  chips(['No needles', 'No radiation', 'No discomfort']) +
                  '<h3>Why isn’t a questionnaire enough?</h3><p>Questionnaires rely on memory, self-awareness and how symptoms look on the outside. But many people, especially children, women, and neurodivergent individuals, mask or compensate.</p><p>iSyncWave™ allows us to:</p>' +
                  ul(['Look directly at brain activity', 'Understand why things feel hard', 'Explain strengths as well as challenges'], 'dx-tick-list'))),
        sec('nc-show', 'show-title', 'What it can show', 'What can it show?', '',
            tools([('In children', 'Development &amp; learning', ul(['Cognitive development compared to age expectations', 'Attention and learning patterns', 'Emotional regulation and processing load'])),
                   ('In adults', 'Efficiency &amp; load', ul(['Focus and mental efficiency', 'Signs of overload or burnout', 'Patterns linked to Mild Cognitive Impairment (MCI)'])),
                   ('In everyone', 'Strengths &amp; strain', ul(['Unique brain strengths', 'Areas where the brain is working harder than it should', 'Where support or optimisation may help']))]), center=True, deco=wave('right')),
        sec('nc-after', 'after-title', 'Your results', 'What happens after the scan?', 'Your results are interpreted by Refocus clinicians, integrated with clinical assessment and used to guide personalised recommendations.',
            split(collage('/img/brainmap-consult.webp', '/img/qeeg-tablet.webp', 'A clinician talks a patient through her qEEG brain map'),
                  '<p>These may include:</p>' + ul([f'<a href="{NF}">Neurofeedback</a>', f'<a href="{EXO}">Transcranial magnetic stimulation (TMS)</a>', f'<a href="{PBM}">Photobiomodulation (tPBM)</a>', 'Brain optimisation or recovery pathways', 'Education and practical strategies'], 'dx-tick-list') +
                  price_box('qEEG brain mapping', [('qEEG brain mapping with clinical interpretation', '£350', None), ('Booked alongside any Refocus service', '£200', '£350')], note='Also £200 if you go on to a recommended assessment or treatment plan following your brain mapping.'))),
        safety('safe', 'Is qEEG brain mapping safe?',
               ['qEEG is considered very safe and is widely used in both clinical and research settings with children, young people, and adults. The sensors only record activity - nothing is sent into the brain.',
                'Most people experience no side effects. Occasionally, some may notice mild and temporary effects such as tiredness, a mild headache, or brief scalp sensitivity from the sensors.'],
               'qEEG may be postponed or adapted if someone is experiencing:',
               ['Acute mental health distress (such as severe agitation or psychosis)', 'A recent head injury or concussion', 'Scalp conditions or infections that prevent sensor placement'],
               ['At Refocus, every qEEG assessment is completed within a clinically governed framework and interpreted by experienced clinicians. qEEG is often used as a gateway into our neuroscience programmes, helping to guide personalised neurofeedback, photobiomodulation, or Exomind pathways, and to support deeper understanding in complex diagnostic assessments.'],
               '/img/hero-qeeg.webp', 'A clinician explains colourful brain maps to a patient'),
        REVIEWS,
        talk_band(*NEURO_TALK),
    ]
    page('neuroscience-main-page/qeeg-brain-mapping', 'qEEG Brain Mapping Manchester with iSyncWave | Refocus',
         'Non-invasive qEEG brain mapping with iSyncWave: see how your brain activity relates to focus, sleep and mood. Standalone or with an ADHD/autism assessment.',
         '/img/hero-qeeg.webp',
         H('/img/hero-qeeg.webp', 'A clinician points to colourful qEEG brain maps on a monitor while a patient looks on', 'qEEG brain mapping with iSyncWave™',
           'See the brain. Understand the mind.',
           'At Refocus The Brain Hub, we use iSyncWave™, a next-generation EEG brain-mapping system designed to go far beyond questionnaires and symptom checklists. This is neuroscience that helps us see how a brain is actually functioning, from high-performing neurotypical adults seeking sharper cognition, to children and adults with complex neurodivergent profiles where standard tools often fall short.',
           [('Learn more', '#start', 'btn-primary'), ('Book now', FREE_CALL, 'btn-ghost')]),
         sections, NEURO)


# ================================================================ Exomind
def exomind():
    benefit = [('i-heart', 'Mood &amp; motivation', ['Low mood, emotional blunting, loss of motivation', 'High stress load, burnout, mental fatigue', 'Brain fog and difficulty concentrating']),
               ('i-venus', 'Perimenopause', ['Cognitive and emotional strain during hormonal transition', 'High-functioning women whose usual coping strategies are no longer enough', 'Integrated support with hormone-aware care']),
               ('i-puzzle', 'Neurodivergent adults', ['ADHD traits with cognitive overwhelm', 'Autism traits with emotional load', 'Years of compensatory effort leading to exhaustion']),
               ('i-peak', 'High performers', ['Athletes, leaders, and professionals', 'After appropriate clinical screening', 'Mental clarity under sustained pressure'])]
    benefit_html = '<div class="dx-inc-grid nc-who">' + ''.join(f'<article class="dx-inc"><span class="ico"><svg><use href="#{i}"/></svg></span><h3>{t}</h3>{ul(x)}</article>' for i, t, x in benefit) + '</div>'
    sections = [
        intro(['We use EXOMIND™, powered by BTL’s ExoTMS® technology, to support healthier brain activity linked to mood, cognition, and self-control.',
               'Unlike one-size-fits-all TMS, our clinician-led programme is tailored using symptoms, history, and, when appropriate, brain mapping and broader medical context.'],
              '/img/svc-neuromod.webp', 'A man relaxes in the Exomind chair while a clinician uses the console', 'EXOMIND™ · BTL ExoTMS®', 'A programme designed for real life', sat='/img/clinic/exomind-room.webp'),
        sec('nc-what', 'what-title', 'The technology', 'What is EXOMIND™ (ExoTMS®)?', 'EXOMIND is a non-invasive transcranial magnetic stimulation (TMS) system that delivers magnetic pulses to stimulate nerve cells in specific brain regions.',
            features([('i-compass', 'Targeted stimulation', 'Magnetic pulses precisely target key brain networks linked to mood regulation, cognitive function and self-control.'),
                      ('i-spark', 'Neuroplasticity support', 'The aim is to support neuroplasticity, helping brain networks “reset” and communicate more effectively over time.'),
                      ('i-shield', 'FDA-cleared', 'EXOMIND’s ExoTMS® technology is FDA-cleared for the treatment of depression in the context of its marketed indications.')]), center=True, dark=True),
        sec('nc-diff', 'diff-title', 'Why EXOMIND is different', 'Not just crisis intervention', 'Unlike traditional TMS pathways, we deliver a holistic, clinician-led programme tailored to your unique brain and life.',
            split('<img class="dx-single reveal-img" src="/img/hero-exomind.webp" alt="A woman relaxes during an Exomind session" loading="lazy">',
                  features([('i-leaf', 'A mental wellness programme', 'EXOMIND has been developed with a broader wellbeing and performance lens, aiming to support mood, motivation, cognitive clarity and resilience, especially relevant for busy, high-demand lives.'),
                            ('i-heart', 'Comfort-forward delivery', 'EXOMIND is designed to be comfortable and accessible, making it easier to complete a full course consistently, an important ingredient for meaningful change.'),
                            ('i-layers', 'Integrated diagnostics', 'At Refocus, EXOMIND can be part of a wider plan that may include qEEG brain mapping, psychological strategies, medication review, and lifestyle-aware care.')], cols=1)), deco=wave('right')),
        sec('nc-who-sec', 'who-title', 'Who may benefit', 'Who may benefit', 'EXOMIND may be suitable for adults looking for a non-invasive, medication-free (or medication-supportive) approach to improving brain network functioning.',
            benefit_html + '<p class="dx-note"><strong>Important:</strong> suitability depends on clinical screening and safety checks. We’ll assess your individual circumstances during consultation.</p>', center=True),
        sec('nc-research', 'res-title', 'Evidence', 'What the research says', '',
            tools([('Mental wellness', 'An expanding evidence base', '<p>Repetitive Transcranial Magnetic Stimulation (rTMS) has an expanding evidence base beyond clinical disorders, with growing research exploring its role in mental wellness, cognitive performance, and stress resilience.</p><p>Studies suggest that targeted prefrontal stimulation may support improvements in cognitive function, mental clarity, emotional regulation, and fatigue, symptoms commonly reported in burnout, brain fog, perimenopause, and high cognitive load states.</p>'),
                   ('Depression', 'Established and robust', '<p>rTMS has an established and robust evidence base in depression, particularly for individuals who have not responded adequately to antidepressant medication.</p><p>NICE guidelines support the use of rTMS for treatment-resistant depression when delivered using approved protocols and appropriate clinical governance, and rTMS is also FDA-approved for Major Depressive Disorder in adults.</p>'),
                   ('Binge eating &amp; OCD', 'Emerging evidence', '<p>rTMS has emerging evidence in binge eating and obsessive-compulsive disorder (OCD), particularly through its effects on impulse control, cognitive flexibility, and fronto-striatal circuits.</p><p>Clinical studies suggest that targeted prefrontal stimulation may reduce binge frequency, food cravings, and the intensity of intrusive or repetitive thoughts, with generally good tolerability.</p>'),
                   ('ADHD symptoms', 'Emerging evidence', '<p>rTMS has an emerging evidence base in ADHD, particularly in relation to attention regulation, executive functioning, and emotional control.</p><p>Research studies suggest that targeted prefrontal stimulation may support improvements in attention, impulsivity, and cognitive control, especially in individuals who experience persistent symptoms despite standard interventions.</p>')]), deco=wave('left')),
        sec('nc-gov', 'gov-title', 'Evidence, safety &amp; governance', 'Evidence, safety &amp; governance', 'As a CQC-ready service, we maintain the highest standards of clinical governance and patient safety.',
            features([('i-shield', 'NICE guidance', 'NICE has published guidance on rTMS for depression, noting no major safety concerns when used with appropriate governance.'),
                      ('i-book', 'Published outcomes', 'EXOMIND’s ExoTMS has published early clinical outcomes in a peer-reviewed journal reporting improvements in mental wellbeing measures.'),
                      ('i-doc', 'Clear criteria', 'Careful screening and clear suitability criteria, with referral pathways when needs are more complex.'),
                      ('i-path', 'Outcome tracking', 'Validated scales and patient goals are tracked throughout treatment.')], cols=4), center=True, dark=True),
        sec('nc-expect', 'expect-title', 'Step by step', 'What to expect at Refocus', '',
            steps([('Step 1', 'Clinical screening &amp; goals', '<p>We assess your symptoms, history, medications, sleep, hormones, and neurodevelopmental profile to understand your unique situation.</p>'),
                   ('Step 2', 'Optional qEEG mapping', f'<p>Brain mapping to better understand your baseline brain patterns and guide a personalised treatment approach.</p><p><strong>{QEEG_REDUCED}</strong></p>'),
                   ('Step 3', 'Structured EXOMIND course', '<p>A comfortable, clinician-led programme delivered in our clinic with sessions designed around your schedule.</p>'),
                   ('Step 4', 'Progress reviews', '<p>Regular reviews and plan refinement, including wider support where needed to ensure lasting improvement.</p>')],
                  img='/img/clinic/exomind-room.webp')),
        sec('dx-how', 'how-title', 'Prices', 'Start your EXOMIND programme', '',
            split('<div class="dx-how-copy"><p class="lede">Your first session includes a medic appointment, so we can confirm EXOMIND is safe and suitable for you before your course begins.</p><p>If you continue to a six-session course, the cost of your first session is deducted.</p></div>',
                  price_box('EXOMIND TMS', [('First session with medic appointment', '£350', None), ('6-session course (first session deducted)', '£1,000', '£1,800')]), cls='dx-how-split')),
        safety('safe', 'Is EXOMIND safe?',
               ['EXOMIND is a non-invasive brain stimulation treatment based on established transcranial magnetic stimulation (TMS) technology. It is generally well tolerated and does not involve medication or sedation.'],
               'For safety reasons, EXOMIND cannot be offered to individuals who:',
               ['Have a history of epilepsy or seizures', 'Are pregnant or breastfeeding', 'Have metal implants near the head or implanted electronic devices (such as pacemakers)', 'Have experienced psychotic episodes or have certain severe mental health conditions', 'Are under 16 years of age'],
               ['At Refocus, safety always comes first. Every EXOMIND programme is delivered within a medically governed framework, with access to consultant psychiatrists and neuroscience-informed care pathways.'],
               '/img/clinic/tms-room.webp', 'The Refocus treatment room with the Exomind chair'),
        REVIEWS,
        talk_band(*NEURO_TALK),
    ]
    page('neuroscience-main-page/exomind', 'EXOMIND TMS Manchester | Non-Invasive Brain Stimulation | Refocus',
         'Non-invasive transcranial magnetic stimulation (TMS) in Manchester, clinician-led and guided by qEEG brain mapping. NICE-supported option for depression.',
         '/img/hero-exomind.webp',
         H('/img/hero-exomind.webp', 'A woman relaxes in the Exomind chair while a clinician sets up her session', 'Refocus Neuroscience',
           'EXOMIND™ ExoTMS at Refocus',
           'A modern, non-invasive brain stimulation programme for depression, mental wellbeing, focus and resilience, designed for real life, not just crisis care.'),
         sections, NEURO)


# ================================================================ Neurofeedback
def neurofeedback():
    sections = [
        intro(['Neurofeedback (also called EEG biofeedback) is a form of brain training.',
               'Small sensors sit on the scalp and read brainwave activity. Software translates those signals into feedback, often through sound or visuals, so your brain can “notice” patterns and gradually adjust.'],
              '/img/nf-session.webp', 'A woman relaxes in an armchair with small sensors and earbuds during a neurofeedback session', 'Brain training', 'What is neurofeedback?'),
        sec('nc-loop', 'loop-title', 'How it works', 'Measure. Analyse. Feedback. Learn.', '' + chips(['Non-invasive', 'No medication', 'Brain training']),
            timeline([('Measure', 'We measure brain activity (EEG) using sensors on the scalp.'),
                      ('Analyse', 'The system analyses patterns in real time (hundreds of readings per second).'),
                      ('Feedback', 'You receive feedback (audio/visual changes) linked to what your brain is doing in that moment.'),
                      ('Learn', 'Your brain learns through repetition, reinforcing helpful states and reducing “stuck” patterns, over time.')]) +
            statement('This is why neurofeedback is often described as training rather than “treatment”: we’re supporting the brain’s capacity to self-regulate, not forcing it to do anything.'), center=True, dark=True),
        sec('nc-nopt', 'nopt-title', 'Why NeurOptimal®', 'Why we use NeurOptimal® at Refocus', '',
            split('<img class="dx-single reveal-img" src="/img/hero-neurofeedback.webp" alt="A man relaxes with his eyes closed during a NeurOptimal session" loading="lazy">',
                  '<p class="lede">NeurOptimal® offers a gentle, non-invasive form of Dynamical Neurofeedback® designed to support flexibility, resilience and self-regulation.</p><p>During a session, small sensors placed on the scalp and ears monitor moment-to-moment electrical activity while you relax and listen to music. When the system detects a change in the activity it is monitoring, the music briefly pauses, providing real-time feedback that acts like a mirror for the brain.</p><p>There is no difficult task to complete, and the system does not push the brain towards a fixed target. The sensors only record activity; they do not deliver electricity or magnetic stimulation. People choose NeurOptimal® as part of their wellbeing routine to explore greater calm, focus, adaptability and resilience in everyday life. Experiences and outcomes vary, and NeurOptimal® is offered as a general wellness brain training system rather than a diagnostic test or treatment for a medical or mental health condition.</p>') +
            features([('i-wave', 'Real-time feedback', 'NeurOptimal® continuously monitors your brain activity and reflects subtle shifts back to the central nervous system so your brain can self-adjust.'),
                      ('i-leaf', 'Non-directive and gentle', 'The system does not push the brain toward specific targets or frequencies; instead, it mirrors your brain’s activity and supports its own adaptive processes.'),
                      ('i-brain', 'Whole-system focus', 'Because NeurOptimal® engages the brain as a whole, many people notice benefits across stress resilience, sleep, emotional balance, and focus.'),
                      ('i-doc', 'No diagnosis required', 'NeurOptimal® is a brain training tool, not a medical treatment, and does not diagnose or treat specific disorders.')], cols=4) +
            statement('In practice, you sit comfortably, engage with subtle feedback cues (often sound or visual), and your brain does the work, with no conscious effort needed on your part.'), deco=wave('right')),
        sec('nc-cbt', 'cbt-title', 'CBT and neurofeedback', 'CBT and neurofeedback: how they fit together', 'Cognitive Behavioural Therapy (CBT) is a structured psychological therapy that helps people identify patterns of thought and behaviour that contribute to distress and learn new, more adaptive ways of thinking and acting. It’s one of the most evidence-supported therapies for anxiety, mood and stress-related conditions.',
            tools([('Enhancing learning readiness', 'Calmer, more focused', '<p>Neurofeedback supports brain regulation and calm focus, which can make the cognitive work in CBT (e.g., restructuring thoughts, practising new behaviours) easier and more effective. Some research suggests that when the brain is less dysregulated, people may engage more consistently with therapeutic exercises.</p>'),
                   ('Addressing physiological patterns', 'Mind and nervous system', '<p>While CBT tackles thought and behaviour patterns, neurofeedback directly engages the brain’s self-regulatory networks. Together they can offer a whole-person approach, addressing what you think and how your nervous system responds.</p>'),
                   ('Adjunct outcomes', 'Better together', '<p>Studies have found that neurofeedback can be effective alongside CBT in reducing symptoms like anxiety and improving emotional regulation, supporting the idea that combining them can be more impactful than either alone for some clients.</p>')]) +
            statement('At Refocus, we integrate neurofeedback seamlessly with therapeutic work (including CBT, coaching, or other supports) so your brain and behaviour both have space to shift.'), center=True),
        sec('nc-help', 'help-title', 'What it can help with', 'What neurofeedback can help with', 'Neurofeedback is used by many people to support:',
            split(collage('/img/svc-coaching.webp', '/img/performer.webp', 'Two people smiling while planning together at a table', 'A runner at sunrise beside a canal'),
                  features([('i-compass', 'Focus and mental stamina', ''), ('i-heart', 'Emotional regulation and reactivity', ''), ('i-sun', 'Sleep quality and recovery', ''), ('i-shield', 'Stress resilience and coping', '')], cols=1) +
                  '<p>Because neurofeedback supports regulation, it can be relevant for people with neurodivergent profiles (e.g., ADHD/autistic traits), performance goals, or anyone aiming for steadier functioning.</p><p class="dx-note"><strong>Important note:</strong> outcomes vary by person. We do not guarantee cures or specific results.</p>', reverse=True), deco=wave('left')),
        sec('nc-path', 'path-title', 'Step by step', 'The Refocus neurofeedback pathway', '',
            steps([('Step 1', 'Discovery + goals', '<p>We clarify your priorities - focus, stress, sleep, emotional recovery, performance.</p>'),
                   ('Step 2', 'Optional brain mapping (qEEG)', '<p>A qEEG helps tailor training where appropriate.</p>'),
                   ('Step 3', 'NeurOptimal® training sessions', '<p>Comfortable, relaxed sessions where sensors monitor brain activity and provide real-time feedback, with your brain leading the adaptation.</p>'),
                   ('Step 4', 'Progress reviews &amp; integration', '<p>We measure change in how you think, feel, and function, and integrate that insight with CBT or other supports.</p>')],
                  img='/img/clinic/quiet-room.webp')),
        sec('dx-how', 'how-title', 'Prices', 'Neurofeedback programmes', '',
            split('<div class="dx-how-copy"><p class="lede">Every neurofeedback programme starts with qEEG brain mapping, so your training is grounded in how your brain is working today.</p><p>Many people begin with 10 sessions and review progress with their clinician before deciding whether to continue.</p></div>',
                  price_box('Neurofeedback', [('10 sessions + qEEG brain mapping', '£950', None), ('20 sessions + qEEG brain mapping', '£1,350', None)], note='Sessions take place at our Manchester clinic.'), cls='dx-how-split')),
        safety('safe', 'Is neurofeedback safe?',
               ['Neurofeedback is a non-invasive brain training approach that uses EEG sensors to help the brain learn healthier regulation patterns.', 'It is generally safe for children and adults of all ages.'],
               'Some individuals may need additional clinical review or tailored protocols, particularly those with:',
               ['A history of seizures', 'Complex trauma', 'Severe mental health conditions'],
               ['At Refocus, neurofeedback is always delivered within a clinically governed framework, ensuring safety, adaptability, and evidence-informed care.'],
               '/img/clinic/lounge-brain.webp', 'A calm lounge at the Refocus clinic'),
        REVIEWS,
        talk_band(*NEURO_TALK),
    ]
    page('neuroscience-main-page/neurofeedback', 'NeurOptimal Neurofeedback Manchester | Refocus',
         'NeurOptimal neurofeedback therapy in Manchester to support focus, sleep and emotional regulation, guided by qEEG brain mapping. For ADHD, anxiety and more.',
         '/img/hero-neurofeedback.webp',
         H('/img/hero-neurofeedback.webp', 'A man relaxes in an armchair with earbuds and small sensors during a neurofeedback session', 'Neurofeedback at Refocus',
           'Train your brain. Support self-regulation. Build resilience.',
           'Your brain is always generating electrical activity. Neurofeedback uses gentle, real-time feedback from that activity to help your brain practise regulation, the same way a mirror helps you adjust posture. At Refocus, neurofeedback sits inside our wider Brain Hub approach: measure → understand → train → integrate.',
           [('Learn more', '#start', 'btn-primary'), ('Book now', FREE_CALL, 'btn-ghost')]),
         sections, NEURO)


# ================================================================ Photobiomodulation
def tpbm():
    sections = [
        intro(['Photobiomodulation (tPBM) uses specific wavelengths of red and near-infrared (NIR) light to support cellular energy production and recovery. In the brain, tPBM is being researched for its potential effects on mitochondrial function (ATP/energy), neuroinflammation pathways, and neurovascular coupling, the relationship between brain activity and blood flow.',
               'At Refocus, we deliver tPBM using iSyncWave, a dry-EEG headset that integrates brain mapping with built-in NIR tPBM, allowing us to tailor sessions using objective brain data rather than “one-size-fits-all” settings.'],
              '/img/framework-map.webp', 'A clinician fits an iSyncWave headset on a patient', 'Photobiomodulation with iSyncWave', 'Brain energy, blood flow and neuroplasticity', sat='/img/qeeg-tablet.webp'),
        sec('nc-diff', 'diff-title', 'What makes it different', 'What makes iSyncWave tPBM different?', '',
            tools([('tPBM guided by your brain data', 'qEEG-informed', '<p>iSyncWave combines wireless dry EEG with tPBM light therapy, designed so tPBM can be guided by qEEG patterns and tracked over time.</p>' + ul(['Identify patterns linked to fatigue, stress load, focus issues or cognitive slowdown', 'Build a tPBM plan that matches your brain profile', 'Monitor trends and adjust your programme as your brain changes'])),
                   ('Near-infrared tPBM built into the headset', 'One device', ul(['Delivers targeted near-infrared light directly to the scalp, without the need for separate external devices.', 'Allows consistent, repeatable tPBM sessions that integrate seamlessly into brain-mapping and neuromodulation pathways.'])),
                   ('A recognised, award-winning medical design', 'Red Dot Award 2022', ul(['Developed with a strong focus on safety, comfort, and clinical usability in real-world healthcare settings.', 'Combines advanced neuroscience technology with an intuitive design to support regular, monitored use.'])),
                   ('Cleared as a medical device in the US', 'FDA-cleared', ul(['Cleared by the FDA in the United States as a medical device, reflecting established safety and manufacturing standards.', 'Used internationally in clinical and research settings as part of supervised brain-health and wellbeing programmes.']))]), center=True, dark=True),
        sec('nc-reasons', 'reasons-title', 'Who tends to choose it', 'What tPBM may help with', 'People come to Refocus for tPBM for two broad reasons:',
            '<div class="nc-two">'
            f'<article class="nc-stage"><span class="nc-stage-k">1</span><img src="/img/performer.webp" alt="A runner at sunrise beside a canal" loading="lazy"><div><h3>Brain performance &amp; resilience</h3><p>For high-achievers, founders, clinicians, students, athletes, and anyone who feels their brain is “running hot”:</p>{ul(["Mental fatigue and brain fog", "Focus/attention strain", "Stress load, sleep disruption, burnout patterns", "Wanting to support neuroplasticity alongside coaching, CBT, or lifestyle changes"])}</div></article>'
            f'<article class="nc-stage"><span class="nc-stage-k">2</span><img src="/img/brainmap-consult.webp" alt="A clinician talks a patient through her brain map" loading="lazy"><div><h3>Brain health support when questionnaires aren’t enough</h3><p>For people who want objective insight, especially when symptoms are mixed or complex:</p>{ul(["Cognitive complaints (slowed processing, forgetfulness, not as sharp)", "Post-viral / post-stress cognitive fatigue patterns", "Neurodivergent brains where symptoms overlap (ADHD/anxiety/sleep)", "Early cognitive change monitoring as part of a wider clinical plan"])}</div></article>'
            '</div>' + statement('tPBM is not a diagnosis or a cure. We position it as part of a wider clinical, neuroscience-led plan.'), center=True, deco=wave('left')),
        sec('nc-prog', 'prog-title', 'Step by step', 'What a tPBM programme looks like at Refocus', '',
            steps([('Step 1', 'Baseline brain mapping', '<p>We start with a structured intake and a baseline measurement (qEEG / iSyncWave scan) to understand your brain pattern and goals.</p>'),
                   ('Step 2', 'Personalised tPBM plan', '<p>A tPBM plan tailored to your profile, with optional neurofeedback, CBT strategies, sleep optimisation, and clinician support.</p>'),
                   ('Step 3', 'Sessions + tracking', '<p>Sessions are non-invasive, comfortable, quiet, and tracked over time to reveal trends, not just daily feelings.</p>'),
                   ('Step 4', 'Review &amp; next steps', '<p>We review progress to continue tPBM, integrate neurofeedback, or escalate to medical review or diagnostics.</p>')],
                  img='/img/hero-tpbm.webp')),
        sec('dx-how', 'how-title', 'Prices', 'tPBM programmes', '',
            split('<div class="dx-how-copy"><p class="lede">Every in-clinic tPBM programme includes qEEG brain mapping, so your sessions are guided by your own brain data.</p><p>Prefer to continue at home? Our <a href="/at-home-brain-therapy-2/">at-home brain therapy helmets</a> let you keep up regular sessions between clinic reviews.</p></div>',
                  price_box('Photobiomodulation (tPBM)', [('10 tPBM sessions with qEEG brain mapping', '£950', None), ('20 tPBM sessions with qEEG brain mapping', '£1,350', None)], note='Clinic sessions take place in Manchester.'), cls='dx-how-split')),
        safety('safe', 'Is tPBM safe?',
               ['Transcranial photobiomodulation (tPBM) is a non-invasive light-based therapy that uses carefully controlled red and near-infrared light to support brain health and function. It does not involve medication, injections, or electrical stimulation.',
                'tPBM is generally well tolerated, and most people experience no or only mild, temporary side effects, such as a brief headache, lightheadedness, or changes in sleep following early sessions.'],
               'tPBM is not suitable for everyone. For safety reasons, it may not be recommended for individuals who:',
               ['Have conditions causing sensitivity to light', 'Have a history of light-triggered seizures', 'Are pregnant', 'Have implanted electronic medical devices (such as pacemakers)', 'Have known or suspected cancer in the area being treated'],
               ['At Refocus, all patients complete a short safety screening before booking tPBM. Where additional considerations are identified, a clinician will review the information to ensure the therapy is safe and appropriately tailored.',
                'tPBM at Refocus is delivered within a clinically governed neuroscience framework, with protocols adjusted carefully and conservatively to prioritise safety, comfort, and individual brain needs.'],
               '/img/hero-neuro.webp', 'A woman relaxes wearing an iSyncWave headset'),
        REVIEWS,
        talk_band(*NEURO_TALK),
    ]
    page('neuroscience-main-page/photobiomodulation', 'Photobiomodulation (tPBM) Manchester | Refocus',
         'Transcranial photobiomodulation: red and near-infrared light therapy supporting brain energy, focus and recovery. Clinic sessions in Manchester or at home.',
         '/img/hero-tpbm.webp',
         H('/img/hero-tpbm.webp', 'A woman relaxes with her eyes closed wearing an iSyncWave headset with a soft near-infrared glow', 'Photobiomodulation (tPBM) with iSyncWave',
           'A gentle, science-led way to support brain energy, blood flow and neuroplasticity',
           'Red and near-infrared light, guided by your own brain data, delivered within a clinically governed neuroscience programme at Refocus.',
           [('Learn more', '#start', 'btn-primary'), ('Book now', FREE_CALL, 'btn-ghost')]),
         sections, NEURO)


# ================================================================ Care hub
CARE_FAQS = [
    ('1. What is Refocus Care and who is it designed for?',
     '<p>Refocus Care is our ongoing clinical pathway for individuals who require structured, medically led follow-up after assessment.</p><p>It includes:</p>' +
     ul(['Women’s Neurohormone Assessments', 'ADHD / Neurodevelopmental Medication Pathway (pending CQC registration)', 'Hormone Replacement Therapy (HRT) pathway']) +
     '<p>Refocus Care is designed for:</p>' + ul(['Women experiencing cognitive, emotional or attentional changes linked to hormonal transition', 'Individuals diagnosed with ADHD who require medication initiation or ongoing monitoring', 'Patients seeking integrated psychiatric and hormonal support']) +
     '<p>Our approach recognises that brain function, hormones and mental health are interconnected. Rather than treating symptoms in isolation, we take a whole-brain, whole-person perspective.</p><p>Every care plan is personalised, structured and consultant-led.</p>'),
    ('2. How do the Women’s Neurohormone and HRT pathways work?',
     '<p>Our Women’s Neurohormone pathway is a specialist consultation service exploring the interaction between:</p>' +
     ul(['ADHD and female presentation', 'Perimenopause and menopause', 'Mood changes and emotional regulation', 'Brain fog and cognitive shifts', 'Sleep disruption and burnout']) +
     '<p>The assessment includes:</p>' + ul(['Detailed clinical and hormonal history', 'Review of previous treatments', 'Risk assessment and medical screening', 'Individualised formulation']) +
     '<p>Where appropriate, treatment options may include:</p>' + ul(['ADHD medication optimisation', 'HRT discussion and prescribing (pending CQC registration)', 'Lifestyle and sleep regulation strategies', 'Cognitive and brain-health recommendations']) +
     '<p>HRT prescribing follows recognised UK clinical guidance and includes careful risk screening and monitoring.</p><p>Our focus is safety, clarity and evidence-informed decision-making, not trend-driven treatment.</p>'),
    ('3. How will ADHD medication management work at Refocus Care?',
     '<p>For individuals diagnosed with ADHD, we offer a structured medication pathway (pending CQC approval).</p><p>This includes:</p>' +
     ul(['Medication discussion and informed consent', 'Careful initiation and titration', 'Regular monitoring appointments', 'Side-effect and response tracking', 'Communication with your GP regarding shared care where appropriate']) +
     '<p>We follow national prescribing standards and ensure:</p>' + ul(['Physical health screening prior to initiation', 'Ongoing safety monitoring', 'Clear documentation', 'Transparent pricing and review structure']) +
     '<p>Shared care agreements depend on local GP policies, and we will guide you through this process.</p><p>Our aim is stability, safety and sustainable improvement, not rushed prescribing.</p>'),
]


def soon_tag():
    return '<span class="nc-soon">Coming soon</span>'


def care_hub():
    svc = cards([
        card('/img/woman-light.webp', 'Women’s Neuro-Hormone Assessments', '', 'Specialist assessments exploring how hormonal transitions, including early perimenopause and menopause, interact with brain function, emotional regulation, cognition, and ADHD traits. These assessments are particularly designed for women whose symptoms are complex, overlapping, or previously misunderstood.',
             ['Neurodivergence informed', 'Brain &amp; hormone aware', 'Mood, cognition, sleep considered', 'Menopause specialists'], NHC),
        card('/img/svc-medication.webp', 'Refocus Neurodevelopmental Medication Pathway', soon_tag(), 'Safe, structured ADHD prescribing across adolescence and adulthood, with collaborative, individualised medication decisions.',
             ['ADHD prescribing', 'Health screening', 'Regular review &amp; monitoring', 'Neuroscience service'], MEDS),
        card('/img/woman-window.webp', 'Refocus Neuro-Hormone Medication Pathway', soon_tag(), 'Individualised hormone prescribing prioritising brain health, safety, and long-term wellbeing, recognising links between hormones, cognition, mood, and neurodivergence in perimenopause and menopause.',
             ['Individualised HRT', 'Health &amp; risk assessment', 'Ongoing monitoring', 'Neurodivergence informed care'], HRT),
    ])
    sections = [
        f'''    <section class="dx-belief" id="start" aria-label="Our promise">
      <div class="wrap"><p>At Refocus, the assessment is only the beginning. <span>This is where support continues.</span></p></div>
    </section>
''',
        sec('nc-covers', 'covers-title', 'What Refocus Care covers', 'Structured clinical pathways, not one-off appointments', 'All services are clinician-led, evidence-based, and aligned with NICE guidance while remaining responsive to emerging neuroscience and real-world patient needs.', svc, deco=wave('right')),
        sec('nc-phil', 'phil-title', 'Our philosophy', 'Brains don’t exist in isolation', 'They exist within bodies, relationships, careers, and changing hormonal landscapes.',
            split(collage('/img/hero-care.webp', '/img/svc-medication.webp', 'A consultant and a patient smile during a relaxed conversation', 'A nurse practitioner talks with a patient'),
                  '<p class="lede">That’s why Refocus does not separate psychiatry, neuroscience, and hormone health into silos.</p><p>We prioritise thoughtful medicine, shared decision-making, and care that adapts as lives evolve. We bring together psychiatry, advanced nursing practice, neuroscience, and hormone-brain expertise to deliver thoughtful, ethical, and long-term clinical care.</p>' +
                  '<div class="nc-hub"><p>Refocus is designed as a connected hub</p><ol><li><a href="/diagnosis-main-page/">Diagnostics</a></li><li><a href="/care-main-page/">Care</a></li><li><a href="/neuroscience-main-page/">Neuroscience</a></li></ol></div>')),
        sec('nc-pillars', 'pillars-title', 'Our standards', 'Every Refocus Care pathway is:', '',
            features([('i-person', 'Clinician-led', 'Consultant psychiatrists and advanced nurse practitioners lead every pathway.'),
                      ('i-flask', 'Evidence-based', 'Aligned with NICE guidance and recognised UK prescribing standards.'),
                      ('i-heart', 'Neurodivergence-affirming', 'Care that respects how your brain works, rather than trying to change who you are.'),
                      ('i-shield', 'Ethically governed', 'Careful screening, clear documentation and transparent decision-making.'),
                      ('i-infinity', 'Designed for the long term', 'Built for sustainable, long-term outcomes, not quick fixes.')]), center=True, dark=True),
        sec('dx-team-sec', 'team-title', 'Meet the team', 'The clinicians behind Refocus Care', '', team(['vrajitoriu', 'williams', 'mcguinness'])),
        REVIEWS,
        faq(CARE_FAQS, 'FAQ'),
        REGULATED,
        cta_band('Not sure what comes next?', 'Start with a free 15-minute call', 'Whether you have just been diagnosed or are navigating hormonal change, we’ll help you find the right pathway and the right clinician.'),
    ]
    page('care-main-page', 'ADHD Treatment &amp; Ongoing Care Manchester | Refocus',
         'Ongoing care after an ADHD diagnosis: medication pathway, personalised support and neuroscience options, led by consultant psychiatrists. NICE-aligned.',
         '/img/hero-care.webp',
         H('/img/hero-care.webp', 'A consultant talks warmly with a patient in a calm clinic room', 'Refocus Care',
           'Ongoing support for modern minds',
           'Refocus Care is our continuity-of-care service, designed to support individuals after diagnosis, between life stages, and through periods of neurological and hormonal change. This is where personalised treatment begins and support continues.'),
         sections, CARE)


# ================================================================ Neurohormone clinic
def neurohormone():
    who = ['Brain fog, memory lapses, poor concentration', 'Sleep disruption, fatigue, burnout', 'Noticing worsening ADHD traits or wondering if ADHD has been missed',
           'Feeling that symptoms are being dismissed as ‘just stress’ or ‘just hormones’', 'Emotional volatility, anxiety, low mood, irritability', 'Loss of confidence or sense of identity', 'Recognising lifelong autistic traits becoming harder to mask']
    sections = [
        intro(['Perimenopause and menopause can impact mood, sleep, focus, and resilience, even in high-achieving women.',
               'At Refocus NeuroHormone Clinic™, we specialise in mental health where hormones, brain function, and neurodiversity intersect. This is not a “one-size-fits-all” menopause service. We look deeply at how hormonal transition interacts with mental health, cognition, ADHD traits, autistic masking, and stress physiology, and we build a plan that makes sense for you.'],
              '/img/who-woman.webp', 'A woman smiling as she relaxes on her sofa', 'Refocus NeuroHormone Clinic™', 'When hormones change, the brain changes too', sat='/img/woman-window.webp'),
        sec('nc-who-sec', 'who-title', 'Who it’s for', 'Who is this service for?', 'This clinic is designed for women who are in early perimenopause, perimenopause, or menopause and experiencing:',
            ul(who, 'dx-cards-list') + statement('You do not need a formal menopause diagnosis to be seen.'), deco=wave('right')),
        sec('nc-approach', 'approach-title', 'Our neurohormone approach', 'Moving beyond labels and into clarity', 'At Refocus, we understand the intricate connection between hormones, mental health, and neurodiversity.',
            features([('i-venus', 'Hormonal understanding', 'Hormones influence brain networks, not just physical symptoms.'),
                      ('i-puzzle', 'Neurodiversity screening', 'ADHD and autism are often identified for the first time during perimenopause.'),
                      ('i-heart', 'Mental health assessment', 'Burnout can look like depression, but requires a very different response.'),
                      ('i-brain', 'Objective brain data', f'<a href="{QEEG}">qEEG brain mapping</a> where helpful for deeper clarity.')], cols=4), center=True, dark=True),
        sec('nc-assess', 'assess-title', 'Step by step', 'What happens in a Refocus neurohormone assessment', '',
            steps([('Step 1', 'Book your virtual assessment', '<p>Book online with secure access to your Medesk patient portal. Questionnaires are sent automatically before your appointment. Appointments are delivered virtually and led by our Advanced Nurse Practitioner and Women’s NeuroHormone Service Lead (PhD in perimenopause).</p>'),
                   ('Step 2', 'Screening questionnaires', '<p>Your questionnaires help us map symptoms properly before we meet. This includes:</p>' + ul(['Menopause &amp; hormonal symptom mapping (MRS, Greene Scale, MENQOL)', 'Mental health screening (PHQ-9, GAD-7)', 'Stress &amp; burnout assessment', 'Neurodiversity screening (ADHD &amp; autism)', 'Sleep &amp; cognitive impact assessments'])),
                   ('Step 3', 'Your virtual clinical assessment', '<p>Your 60-75 minute consultation focuses on symptom onset, cognitive changes, sleep, stress, and neurodevelopmental traits. By the end, you’ll have a clear working formulation, an understanding of what may be hormonal, neurodivergent, or stress-related, and a personalised care plan.</p>'),
                   ('Step 4', 'Home blood tests (if appropriate)', '<p>Where blood tests add value, we arrange hormone home testing through Forth. Results are reviewed and interpreted in context, not in isolation.</p>'),
                   ('Step 5', 'Optional qEEG brain mapping', '<p>For women with significant cognitive symptoms, emotional dysregulation, or neurodiversity questions, qEEG brain mapping may be recommended. It helps us understand attention networks, stress circuits, cognitive fatigue patterns, and brain features often seen in ADHD-like profiles.</p>'),
                   ('Step 6', 'Integrated NeuroHormone plan', f'<p>We bring together clinical history, questionnaire profiles, blood results, and qEEG findings. Your plan may include hormonal pathway guidance, neurodivergent women’s support, brain-based interventions (<a href="{NF}">neurofeedback</a>, <a href="{PBM}">photobiomodulation</a>, <a href="{EXO}">Exomind TMS</a>), and psychological strategies.</p>')],
                  img='/img/hero-neurohormone.webp')),
        sec('nc-why', 'why-title', 'Why Refocus', 'Why choose Refocus NeuroHormone Clinic™?', '',
            split(team(['williams']),
                  ul(['Neurodiversity-aware menopause care', 'Evidence-based questionnaires and formulation', 'Integrated care across Refocus Care, Neuroscience &amp; Diagnostics', 'Mental health-led, not symptom-dismissive', 'Optional objective brain mapping', 'Designed for women who want answers, not assumptions'], 'dx-tick-list'), cls='nc-why-split'), deco=wave('left')),
        sec('dx-how', 'how-title', 'Book your assessment', 'Book your assessment', 'If you feel like your brain has changed, and you want a thoughtful explanation that fits your experience, we’re here.',
            split(booking([('Complete a short screening', 'So we match you to the most appropriate service.'),
                           ('Pay a £100 deposit', 'This unlocks secure access to our clinical portal (Medesk).'),
                           ('Complete online forms', 'Screening questionnaires and forms through your portal.'),
                           ('Clinical review &amp; allocation', 'Our admin team reviews the information and books you with the right clinician.'),
                           ('Final payment', 'The remaining balance is paid before the appointment.')],
                          'This process helps us prepare thoroughly and ensures you receive the right assessment, at the right time, with the right clinician.'),
                  price_box('NeuroHormone assessment', [('Virtual assessment', '£300', None)], note='') +
                  f'<aside class="nc-credit"><p class="kicker">Refocus NeuroHormone → ADHD continuity credit</p><p>If an ADHD assessment is recommended following the NeuroHormone Clinic and you choose to continue care at Refocus, a <strong>£100 discount</strong> is applied.</p><p class="nc-credit-p">ADHD assessment price: <strong>£650</strong></p><a class="text-link" href="{WOMEN}">About our women’s ADHD assessment <svg><use href="#i-right"/></svg></a></aside>', cls='dx-how-split')),
        f'''    <section class="section dx dx-info" aria-labelledby="info-title">
      <div class="wrap dx-info-grid">
        <div>
          <p class="kicker">Booking information</p>
          <h2 id="info-title">Who this clinic is for</h2>
          <p class="lede">This clinic is for women aged 40+ who are experiencing changes in mood, cognition, energy, or emotional regulation linked to perimenopause, menopause, or post-menopause.</p>
          <p>The focus is on understanding the interaction between brain, hormones, and wellbeing, rather than acute mental health care.</p>
          <a class="btn btn-primary btn-lg" href="{FREE_CALL}">Book a NeuroHormone assessment</a>
        </div>
        <aside class="dx-safety" aria-labelledby="safety-title">
          <h3 id="safety-title">Important safety information</h3>
          <p><strong>This clinic does not provide crisis or emergency mental health care.</strong></p>
          <p>If you are experiencing:</p>
          {ul(['Suicidal thoughts', 'Significant risk to yourself', 'Acute psychiatric symptoms'])}
          <p>Please contact:</p>
          {ul(['<a href="tel:111">NHS 111</a>', 'Your GP', 'A&amp;E or <a href="tel:999">999</a> in an emergency'])}
          <p class="pg-small">Refocus appointments are not an emergency service.</p>
        </aside>
      </div>
    </section>
''',
        REVIEWS,
        talk_band(),
    ]
    page('neurohormone-clinic', 'Neurohormone Clinic Manchester | Perimenopause Mental Health | Refocus',
         'Neurohormone support in Manchester: ongoing brain health, assessments and ADHD medication pathways within a joined-up, medically-led approach.',
         '/img/hero-neurohormone.webp',
         H('/img/hero-neurohormone.webp', 'A woman in her late forties on a video consultation at her kitchen table', 'Perimenopause &amp; menopause mental health assessments',
           'Refocus Neurohormone Clinic™',
           'Specialist mental health assessments at the intersection of hormones, brain function, and neurodiversity.'),
         sections, CARE)


# ================================================================ Coming-soon pathways
def notify_form(subject, sid):
    return f'''<form class="pg-form nc-notify" data-mailto="hello@refocushub.co.uk" data-subject="{subject}" novalidate>
            <div class="form-grid">
              <div class="field"><label for="{sid}-name">Your name</label><input id="{sid}-name" name="name" autocomplete="name" required><span class="err" aria-live="polite"></span></div>
              <div class="field"><label for="{sid}-email">Your email</label><input id="{sid}-email" name="email" type="email" autocomplete="email" required><span class="err" aria-live="polite"></span></div>
            </div>
            <button class="btn btn-primary btn-lg" type="submit">Notify me</button>
            <p class="pg-form-status" role="status" hidden></p>
            <p class="pg-small">We’ll only use your details to tell you when this pathway opens. See our <a href="https://refocushub.co.uk/privacy-policy/">privacy policy</a>.</p>
          </form>'''


def soon_section(sid, title, text, subject):
    return f'''    <section class="section dx nc-soon-sec" id="{sid}" aria-labelledby="{sid}-title">
      <div class="wrap nc-soon-grid">
        <div>
          <p class="kicker">Coming soon</p>
          <h2 id="{sid}-title">{title}</h2>
          <p class="lede">{text}</p>
        </div>
        <div class="nc-soon-card">{notify_form(subject, sid)}</div>
      </div>
    </section>
'''


def meds():
    sections = [
        soon_section('start', 'This pathway is opening soon', 'Our ADHD medication pathway is pending CQC registration. Leave your details and we’ll let you know as soon as it opens. In the meantime, our team is happy to talk through your options.', 'ADHD medication pathway: notify me'),
        sec('nc-what', 'what-title', 'What the pathway will include', 'Safe, structured ADHD prescribing', 'For individuals diagnosed with ADHD, we will offer a structured medication pathway across adolescence and adulthood, with collaborative, individualised medication decisions.',
            split(collage('/img/svc-medication.webp', '/img/svc-coaching.webp', 'A nurse practitioner talks through a care plan with a patient', 'Two people smiling while planning together with sticky notes'),
                  features([('i-doc', 'Discussion &amp; informed consent', 'Medication discussion and informed consent, so every decision is shared.'),
                            ('i-path', 'Careful initiation &amp; titration', 'Starting gently and adjusting carefully to find what works for you.'),
                            ('i-calendar', 'Regular monitoring', 'Regular monitoring appointments with side-effect and response tracking.'),
                            ('i-people', 'GP shared care', 'Communication with your GP regarding shared care where appropriate.')], cols=1)), deco=wave('right')),
        sec('nc-standards', 'std-title', 'Our standards', 'We follow national prescribing standards', 'Our aim is stability, safety and sustainable improvement, not rushed prescribing.',
            features([('i-heart', 'Physical health screening', 'Physical health screening prior to initiation.'),
                      ('i-shield', 'Ongoing safety monitoring', 'Blood pressure, heart rate, weight and wellbeing reviewed throughout.'),
                      ('i-book', 'Clear documentation', 'Clear records you and your GP can rely on.'),
                      ('i-gift', 'Transparent pricing', 'A transparent pricing and review structure.')], cols=4) +
            '<p class="dx-note">Shared care agreements depend on local GP policies, and we will guide you through this process.</p>', center=True, dark=True),
        sec('dx-team-sec', 'team-title', 'Meet the lead', 'Led by our ADHD Medication Pathway Lead', '', team(['mcguinness', 'vrajitoriu'])),
        sec('nc-first', 'first-title', 'Not diagnosed yet?', 'Start with an assessment', 'Medication is only ever considered after a thorough, consultant-led diagnosis.',
            cards([card('/img/who-adult.webp', 'Adult ADHD assessment', '', 'Consultant psychiatrist-led adult ADHD assessment using the structured DIVA-5 interview, with observer input and optional qEEG brain mapping.', [], '/adult-adhd-assessment/'),
                   card('/img/svc-adhd.webp', 'Child &amp; adolescent ADHD', '', 'A neuroscience-informed, child-centred ADHD assessment led by consultant child and adolescent psychiatrists.', [], '/diagnosis-main-page/child-adolescent-adhd/'),
                   card('/img/woman-light.webp', 'Women’s ADHD &amp; perimenopause', '', 'A holistic pathway for women at midlife, recognising that ADHD, hormones and mental health intersect.', [], WOMEN)]), center=True),
        faq([CARE_FAQS[2], CARE_FAQS[0]], 'FAQ'),
        talk_band(),
    ]
    page('care-main-page/adhd-medication-treatment-pathway', 'ADHD Medication &amp; Treatment Pathway Manchester | Refocus',
         'ADHD medication titration and ongoing treatment for adults and adolescents, led by consultant psychiatrists and advanced nurse practitioners. NICE-aligned.',
         '/img/hero-meds.webp',
         H('/img/hero-meds.webp', 'A nurse practitioner checks a patient’s blood pressure during a review appointment', 'Refocus Care · Coming soon',
           'ADHD medication treatment pathway',
           'Safe, structured ADHD prescribing across adolescence and adulthood, with careful titration, regular monitoring and collaborative decisions.',
           [('Notify me', '#start', 'btn-primary'), ('Book a free call', FREE_CALL, 'btn-ghost')]),
         sections, CARE)


def hrt():
    sections = [
        soon_section('start', 'This pathway is opening soon', 'Our Neuro-Hormone medication pathway is pending CQC registration. Leave your details and we’ll let you know as soon as it opens. You can already book a NeuroHormone assessment today.', 'HRT pathway: notify me'),
        sec('nc-what', 'what-title', 'What the pathway will include', 'Hormone prescribing that puts brain health first', 'Individualised hormone prescribing prioritising brain health, safety, and long-term wellbeing, recognising links between hormones, cognition, mood, and neurodivergence in perimenopause and menopause.',
            split(collage('/img/woman-window.webp', '/img/hero-hrt.webp', 'A woman sits calmly by a window', 'A woman walks through a park in autumn'),
                  features([('i-venus', 'Individualised HRT', 'Hormone options chosen around your history, symptoms and preferences.'),
                            ('i-shield', 'Health &amp; risk assessment', 'Careful risk screening before any prescribing, following recognised UK clinical guidance.'),
                            ('i-calendar', 'Ongoing monitoring', 'Regular reviews so your plan keeps pace with your body and brain.'),
                            ('i-puzzle', 'Neurodivergence-informed care', 'Care that understands how ADHD and autistic traits can change during hormonal transition.')], cols=1)), deco=wave('right')),
        sec('nc-today', 'today-title', 'Available now', 'Start with a NeuroHormone assessment', 'Our Women’s Neurohormone pathway is a specialist consultation service exploring how ADHD, perimenopause, mood, brain fog and sleep interact. Where appropriate, treatment options may include:',
            chips(['ADHD medication optimisation', 'HRT discussion and prescribing (pending CQC registration)', 'Lifestyle and sleep regulation strategies', 'Cognitive and brain-health recommendations'], 'dx-chips dx-chips-lg') +
            statement('Our focus is safety, clarity and evidence-informed decision-making, not trend-driven treatment.') +
            f'<div class="btn-row nc-center"><a class="btn btn-primary btn-lg" href="{NHC}">Visit the NeuroHormone Clinic</a><a class="text-link" href="{WOMEN}">ADHD and perimenopause <svg><use href="#i-right"/></svg></a></div>', center=True, dark=True),
        sec('dx-team-sec', 'team-title', 'Meet the lead', 'Led by our Women’s NeuroHormone Service Lead', '', team(['williams', 'vrajitoriu'])),
        faq([CARE_FAQS[1], CARE_FAQS[0]], 'FAQ'),
        talk_band(),
    ]
    page('care-main-page/hrt-treatment-pathway', 'HRT Treatment Pathway: Hormones &amp; Brain Health | Refocus',
         'Neurohormone assessments in Manchester supporting brain health during perimenopause and hormonal transitions, led by an advanced practitioner with expertise in perimenopause.',
         '/img/hero-hrt.webp',
         H('/img/hero-hrt.webp', 'A woman in her fifties walks confidently through a park in autumn light', 'Refocus Care · Coming soon',
           'HRT treatment pathway',
           'Individualised hormone care that prioritises brain health, safety and long-term wellbeing through perimenopause and menopause.',
           [('Notify me', '#start', 'btn-primary'), ('Book a free call', FREE_CALL, 'btn-ghost')]),
         sections, CARE)


if __name__ == '__main__':
    neuro_hub()
    qeeg()
    exomind()
    neurofeedback()
    tpbm()
    care_hub()
    neurohormone()
    meds()
    hrt()
