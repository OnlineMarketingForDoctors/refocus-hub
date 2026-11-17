"""Build Refocus blog article pages.

Usage: python3 tools/build_blog.py .
Each article keeps its live slug at the site root. Reuses the page shell in tools/build_pages.py.
Content is a list of blocks, so new articles only need a new ARTICLES entry.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import build, hero, cta_band, newsletter, FREE_CALL, POSTS, post_card, REPO  # noqa: E402

ICON = {'venus': 'i-venus', 'drop': 'i-drop', 'person': 'i-person', 'heart': 'i-heart', 'flask': 'i-flask', 'leaf': 'i-leaf',
        'shield': 'i-shield', 'brain': 'i-brain', 'doc': 'i-doc', 'compass': 'i-compass', 'layers': 'i-layers', 'path': 'i-path'}


def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', re.sub(r'<[^>]+>|&[a-z]+;', '', t).lower()).strip('-')


def render(blocks):
    """Return (article_html, toc) from a list of blocks."""
    out, toc = [], []
    for b in blocks:
        k = b[0]
        if k == 'p':
            out.append(f'<p>{b[1]}</p>')
        elif k == 'lede':
            out.append(f'<p class="ar-lede">{b[1]}</p>')
        elif k == 'h2':
            sid = slugify(b[1])
            toc.append((sid, b[1]))
            out.append(f'<h2 id="{sid}">{b[1]}</h2>')
        elif k == 'h3':
            out.append(f'<h3>{b[1]}</h3>')
        elif k == 'takeaways':
            out.append('<aside class="ar-takeaways" aria-label="Key takeaways"><p class="ar-k">In short</p><ul>' + ''.join(f'<li>{x}</li>' for x in b[1]) + '</ul></aside>')
        elif k == 'cards':  # (cols, [(icon, title, html, heading_level)])
            items = ''.join(f'<article class="ar-card"><span class="ico"><svg><use href="#{ICON[i]}"/></svg></span><{lvl}>{t}</{lvl}>{x}</article>' for i, t, x, lvl in b[2])
            out.append(f'<div class="ar-cards ar-cards-{b[1]}">{items}</div>')
        elif k == 'img':
            out.append(f'<figure class="ar-fig"><img src="{b[1]}" alt="{b[2]}" loading="lazy"><figcaption>{b[3]}</figcaption></figure>')
        elif k == 'quote':
            out.append(f'<blockquote class="ar-quote"><p>{b[1]}</p></blockquote>')
        elif k == 'callout':
            out.append(f'<aside class="ar-callout"><p class="ar-k">{b[1]}</p>{b[2]}</aside>')
        elif k == 'cta':  # (kicker, title, text, [(label, href, cls)])
            btns = ''.join(f'<a class="btn {c}" href="{h}">{l}</a>' for l, h, c in b[4])
            out.append(f'<aside class="ar-cta on-dark"><p class="kicker">{b[1]}</p><p class="ar-cta-t">{b[2]}</p><p>{b[3]}</p><div class="btn-row">{btns}</div></aside>')
        elif k == 'html':
            out.append(b[1])
    return '\n          '.join(out), toc


def share(url, title):
    from urllib.parse import quote
    full = 'https://refocushub.co.uk' + url
    u, t = quote(full, safe=''), quote(re.sub('&amp;', '&', title), safe='')
    return f'''<div class="ar-share" aria-label="Share this article">
            <span>Share</span>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url={u}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">in</a>
            <a href="https://www.facebook.com/sharer/sharer.php?u={u}" target="_blank" rel="noopener" aria-label="Share on Facebook">f</a>
            <a href="https://x.com/intent/post?url={u}&amp;text={t}" target="_blank" rel="noopener" aria-label="Share on X">X</a>
            <a href="mailto:?subject={t}&amp;body={u}" aria-label="Share by email"><svg><use href="#i-mail"/></svg></a>
            <button type="button" data-copy="{full}" aria-label="Copy link"><svg><use href="#i-doc"/></svg><span class="ar-copied" role="status"></span></button>
          </div>'''


def article(a):
    body, toc = render(a['blocks'])
    words = len(re.sub(r'<[^>]+>', ' ', body).split())
    mins = max(1, round(words / 230))
    toc_html = ''.join(f'<li><a href="#{i}">{re.sub(r"<[^>]+>", "", t)}</a></li>' for i, t in toc)
    related = ''.join(post_card(p) for p in POSTS if p[1] != a['url'] and p[2] in a['related'])
    main = '  <main id="main">\n' + '    <div class="ar-progress" aria-hidden="true"><span></span></div>\n' + hero(
        a['hero'], a['hero_alt'], f'Neuro blog · {a["cat"]}', a['title'], a['dek'],
        [('Read the article', '#start', 'btn-primary'), ('Book a free 15-minute call', FREE_CALL, 'btn-ghost')], pos='72% center').replace('<h1 id="pg-title">', '<h1 id="pg-title" class="is-long">' if len(a['title']) > 40 else '<h1 id="pg-title">') + f'''
    <section class="ar-meta-bar" id="start" aria-label="Article details">
      <div class="wrap ar-meta-inner">
        <nav class="ar-crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/neuro-blog/">Neuro blog</a><span aria-hidden="true">/</span><a href="/neuro-blog/?topic={a['cat']}">{a['cat']}</a></nav>
        <p class="ar-dates"><span>By {a['author']}</span><span>Published <time datetime="{a['iso']}">{a['date']}</time></span><span>Updated <time datetime="{a['mod_iso']}">{a['mod']}</time></span><span>{mins} min read</span></p>
      </div>
    </section>

    <section class="section ar-sec" aria-label="Article">
      <img class="deco deco-waves" src="/img/waves-side.svg" alt="" width="300" height="900" style="width:150px;right:0;top:80px" loading="lazy">
      <div class="wrap ar-layout">
        <aside class="ar-toc" aria-labelledby="toc-title">
          <details open>
            <summary id="toc-title">In this article</summary>
            <ol>{toc_html}</ol>
          </details>
          {share(a['url'], a['title'])}
        </aside>
        <article class="ar-body">
          {body}
          <footer class="ar-foot">
            <p class="ar-disclaimer"><strong>Medical disclaimer.</strong> This article is for general information and does not replace personalised medical advice. Speak to a qualified clinician before starting, stopping or changing any medication or hormone therapy.</p>
            {share(a['url'], a['title'])}
          </footer>
        </article>
      </div>
    </section>

    <section class="section ar-related" aria-labelledby="rel-title">
      <div class="wrap">
        <div class="split-head"><div><p class="kicker">Keep reading</p><h2 id="rel-title">Related articles</h2></div><a class="text-link" href="/neuro-blog/">All articles <svg><use href="#i-right"/></svg></a></div>
        <div class="bl-grid">{related}</div>
      </div>
    </section>
''' + newsletter() + cta_band('Not sure where to start?', 'Start with a free 15-minute call', a['cta_text']) + '  </main>\n'

    slug = a['url'].strip('/')
    build(slug, a['seo_title'], a['desc'], a['hero'], main, current='/learning-page/')
    ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': re.sub('&amp;', '&', a['title']),
          'description': a['desc'], 'image': 'https://refocushub.co.uk' + a['hero'], 'datePublished': a['iso'], 'dateModified': a['mod_iso'],
          'author': {'@type': 'Organization', 'name': 'Refocus The Brain Hub'},
          'publisher': {'@type': 'Organization', 'name': 'Refocus The Brain Hub', 'logo': {'@type': 'ImageObject', 'url': 'https://refocushub.co.uk/img/logo.webp'}},
          'mainEntityOfPage': 'https://refocushub.co.uk' + a['url']}
    path = f'{REPO}/{slug}/index.html'
    page = open(path, encoding='utf8').read()
    page = page.replace('</head>', f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n</head>', 1)
    open(path, 'w', encoding='utf8').write(page)


def ul(items):
    return '<ul class="check-list">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


HORMONES = {
    'url': '/can-hormone-therapy-improve-neurodivergent-symptoms/',
    'title': 'Can Hormone Therapy Improve Neurodivergent Symptoms?',
    'seo_title': 'Hormone Therapy &amp; Neurodivergent Symptoms | Refocus',
    'desc': 'How oestrogen affects dopamine, why ADHD and autism symptoms change with hormones, and when hormone therapy may help as part of a wider care plan.',
    'dek': 'How hormones shape dopamine, why ADHD and autism symptoms shift with puberty, the menstrual cycle and menopause, and where hormone therapy fits in a wider care plan.',
    'cat': 'Mindfulness', 'author': 'the Refocus team',
    'date': '25 June 2026', 'iso': '2026-06-25', 'mod': '10 November 2026', 'mod_iso': '2026-11-10',
    'hero': '/img/hero-blog-hormones.webp', 'hero_alt': 'A woman holding a mug of tea gazes thoughtfully out of a window in soft morning light',
    'related': ['perimenopause-adhd', 'adhd-burnout-masking', 'autism-adults'],
    'cta_text': 'If your symptoms shift with your cycle, after having a baby or in perimenopause, we’ll help you work out what is hormonal, what is neurodivergent, and what support will genuinely help.',
    'blocks': [
        ('lede', 'Even though the link between hormones and mood has been studied for over a century, it was only in the early 2000s that their direct influence over neurodivergent symptoms was recognised. For decades, women reported feeling overwhelmed, anxious and foggy during hormonal shifts, but these complaints were often perceived as psychological “hysteria” or weakness.'),
        ('p', 'Today, the medical community confirms that estrogen directly impacts the production and efficiency of dopamine and serotonin. As a result, hormone therapy can be used to improve neurodivergent symptoms, albeit indirectly, by normalising the brain’s neurochemical environment rather than by treating the neurodivergence itself.'),
        ('p', 'How exactly do hormonal changes affect neurodivergent symptoms? What does science say about the effect of hormone therapy on improving ADHD, autism or dyslexia? Below, you will find these answers and relevant information regarding how hormone regulation can improve neurodivergent care and support your brain health.'),
        ('takeaways', ['Hormone therapy does not treat ADHD or autism directly, but it can ease symptoms by stabilising hormone levels and preventing dopamine crashes.',
                       'Drops in estrogen, in the luteal phase, perimenopause and after childbirth, can make executive dysfunction, emotional dysregulation and sensory overload worse.',
                       'It works best as one part of a holistic plan alongside the right medication, neuroinclusive therapy and nutrition.']),
        ('h2', 'What Is the Connection Between Hormones and the Brain?'),
        ('p', 'The connection between hormones and the brain is a powerful, bidirectional communication network that forms the neuroendocrine system. While the brain acts as the master command centre, deciding how many hormones are produced, hormones, in turn, act as chemical messengers that fundamentally change how brain cells process information and regulate mood.'),
        ('p', 'Your ovaries, thyroid and adrenal glands can produce hormones only with a direct command from the brain. Consequently, hormones dictate how your brain’s neurochemicals do their job.'),
        ('cards', 3, [('flask', 'Estrogen', '<p>Responsible for the growth of new neurons and the connections between brain cells.</p>', 'h3'),
                      ('leaf', 'Progesterone', '<p>Calms the nervous system and reduces anxiety.</p>', 'h3'),
                      ('shield', 'Cortisol', '<p>Regulates alertness and helps you respond to danger.</p>', 'h3')]),
        ('h2', 'How Hormonal Changes Affect Neurodivergent Symptoms'),
        ('p', 'Hormonal changes, such as those during the menstrual cycle, pregnancy and menopause, seriously affect neurodivergent symptoms. Estrogen is a natural booster for dopamine and serotonin, while progesterone has a calming effect. When the levels of these hormones drop, it causes executive dysfunction, emotional dysregulation and increased sensitivity to sensory input.'),
        ('h3', 'Puberty and the Onset of More Visible Symptoms'),
        ('p', 'Puberty is a major diagnostic turning point for girls with ADHD. While boys often experience an improvement in their neurodivergent symptoms during adolescence, girls notice a significant exacerbation of theirs. Before puberty, estrogen levels are low and stable. However, once the menstrual cycle begins, they start to fluctuate and drop, causing a severe monthly dopamine deficit. Consequently, internal struggles with focus, attention and memory become visible.'),
        ('p', 'What was simply daydreaming in childhood turns into missing assignments or the inability to finish exams. Intense mood swings and severe frustration over minor setbacks make navigating daily life much harder. Because a young girl cannot understand why she cannot keep up with her peers, she internalises these struggles, often experiencing depression, anxiety or eating disorders.'),
        ('h3', 'The Menstrual Cycle and ADHD / Autism Symptoms'),
        ('p', 'The menstrual cycle causes a rise and fall in estrogen and progesterone levels that directly exacerbates ADHD and autism symptoms. During the first half of the cycle, high estrogen levels act as a natural cognitive booster. Conversely, in the second half (the luteal phase), the drop in hormones throws girls and women into severe executive dysfunction and emotional distress.'),
        ('img', '/img/blog-cycle-journal.webp', 'A woman tracks her monthly cycle in a journal at her kitchen table', 'Tracking how symptoms change across the cycle can help your clinician spot hormone-linked patterns.'),
        ('p', 'For those with ADHD, this frequently manifests as executive paralysis, struggling to initiate basic tasks, such as opening emails or doing laundry. Furthermore, they struggle with time estimation, often being late or panicking over deadlines.'),
        ('p', 'The luteal phase affects autistic women as well. They experience sensory overload due to the brain’s inability to filter out background noise. Additionally, they may temporarily lose their communication skills, finding themselves unable to engage in small talk. Since the menstrual cycle alters brain chemistry, psychiatrists may recommend specific medication adjustments rather than prescribing the same dosage all year round.'),
        ('h3', 'Perimenopause, Menopause and Cognitive Changes'),
        ('p', 'Perimenopause and menopause cause an estrogen decline that affects the coping mechanisms women with ADHD used to mask their symptoms, leading to serious cognitive changes. During perimenopause, estrogen levels rise and crash, which destabilises the prefrontal cortex and takes a heavy cognitive toll.'),
        ('p', 'Consequently, the brain no longer has the energy for masking, and coping mechanisms fail. Women face difficulty in following conversations, meeting project deadlines or being on time. However, because these symptoms overlap with the menopausal transition, they often lead to a misdiagnosis. Unfortunately, relying solely on Hormone Replacement Therapy cannot restore cognitive clarity without also addressing the underlying ADHD.'),
        ('h3', 'Testosterone and Neurodivergence in Men'),
        ('p', 'Testosterone directly protects and regulates dopamine, just like estrogen does. When testosterone drops, dopamine levels are affected, causing executive dysfunction. However, unlike estrogen in women, this decline is neither rapid nor monthly. Testosterone remains high and stable daily throughout adulthood. When andropause occurs, levels decline at a slow rate of 1-2% per year after the age of 30, offering men decades to adapt their coping strategies.'),
        ('h2', 'What Does the Research Say About Hormone Therapy and Neurodivergence?'),
        ('p', 'According to current research, hormone therapy does not treat neurodivergence directly. However, it improves symptoms by stabilising fluctuating hormone levels and preventing dopamine crashes.'),
        ('cards', 2, [('compass', 'The Current State of Research', '<p>The medical community increasingly recognises hormone therapy as an essential tool for balancing the nervous system. Notably, following the <a href="https://www.fda.gov/news-events/press-announcements/hhs-advances-womens-health-removes-misleading-fda-warnings-hormone-replacement-therapy" target="_blank" rel="noopener">FDA’s decision to update safety guidelines</a> for menopausal hormone therapies on 10 November 2025, psychiatrists and endocrinologists have begun exploring these treatments as preventative cognitive support for ageing neurodivergent women.</p><p>Furthermore, a study conducted in January 2026 by the University of Cambridge demonstrated that while hormone therapy acts as a powerful chemical stabiliser and cognitive protector during menopause, it cannot replace specialised neurodivergent care.</p>', 'h3'),
                      ('flask', 'What is Formally Proven', '<p>It is well-established that estrogen and testosterone are powerful neuromodulators. Estrogen stimulates dopamine synthesis, whereas progesterone calms the nervous system. Clinical data confirms that while hormone therapy cannot alter core neurodivergent traits, it regulates neurotransmitter levels, thereby improving executive functioning and working memory.</p><p>Clinical reviews also show that estrogen and testosterone directly interact with stimulant medications. Consequently, stabilising hormones through therapy enhances medication efficacy during the premenstrual week or perimenopause, when estrogen levels drop.</p>', 'h3'),
                      ('layers', 'What Remains Unclear', '<p>Despite recent advancements, a standardised dosing protocol for <a href="/neurohormone-clinic/">ADHD and hormones women</a> remains unavailable. It is still unclear whether a neurodivergent brain requires higher or lower doses of hormones compared to a neurotypical brain to achieve cognitive stability.</p><p>Additionally, while hormone therapy offers short-term improvements in reducing brain fog and enhancing working memory during menopause, it remains uncertain whether long-term hormone therapy permanently protects against cognitive decline in neurodivergent individuals.</p>', 'h3'),
                      ('doc', 'Limitations of Existing Studies', '<p>The greatest limitation of existing research is the lack of randomised controlled trials evaluating the safety and efficacy of combining neurodivergent medications with hormone therapies.</p><p>Furthermore, there is a historical deficit of clinical drug trials involving women. For decades, clinical drug trials and diagnostic tools for ADHD or autism were designed primarily around young men, leaving women completely overlooked.</p>', 'h3')]),
        ('h2', 'Who Might Benefit From Hormone Therapy?'),
        ('p', 'Hormone therapy can benefit individuals whose neurodivergent symptoms are exacerbated by hormonal shifts. Even though it cannot cure ADHD or autism, it acts as a neurochemical stabiliser that mitigates symptom severity. The following groups stand to benefit the most from hormone therapy:'),
        ('cards', 2, [('venus', 'Perimenopausal and menopausal women', '<p>Women in their 40s and 50s experience a dramatic decline in estrogen levels, which often worsens ADHD symptoms. Restoring estrogen levels through hormone therapy enhances the efficacy of standard ADHD stimulant medications and prevents severe executive paralysis.</p>', 'h3'),
                      ('drop', 'Neurodivergent women with Premenstrual Dysphoric Disorder (PMDD)', '<p>Approximately <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9344571/" target="_blank" rel="noopener">92% of autistic women</a> and 45% of women with ADHD experience significant estrogen drops and subsequent dopamine crashes due to PMDD. Utilising hormone therapy helps prevent these dopamine deficits, thereby reducing the frequency of sensory and emotional dysregulation.</p>', 'h3'),
                      ('person', 'Ageing men with executive burnout', '<p>Men who experience a testosterone drop due to ageing, chronic stress or illness may present with a sudden worsening of ADHD symptoms. Testosterone Replacement Therapy (TRT) can reduce these effects by optimising dopamine utilisation, which restores focus and working memory.</p>', 'h3'),
                      ('heart', 'Women in the postpartum period', '<p>Women going through the postpartum phase face an abrupt and significant drop in estrogen levels. When this occurs, they may feel unable to function or regulate their sensory system after childbirth, significantly increasing the risk of burnout and postpartum depression. Low doses of hormone therapy can prevent a collapse of the nervous system, allowing them to adapt more smoothly to motherhood.</p>', 'h3')]),
        ('cta', 'Refocus NeuroHormone Clinic™', 'Do your symptoms change with your hormones?', 'Our specialist assessments look at how hormonal transition interacts with mental health, cognition, ADHD traits and autistic masking, and build a plan that makes sense for you.',
         [('Visit the NeuroHormone Clinic', '/neurohormone-clinic/', 'btn-primary'), ('Book a free 15-minute call', FREE_CALL, 'btn-ghost')]),
        ('h2', 'Types of Hormone Therapy'),
        ('p', 'Although hormone therapy is not a primary treatment for ADHD or autism, symptoms can either improve or worsen depending on the precision of the treatment. The following are the primary types of hormone therapies utilised to alleviate neurodivergent traits during hormonal shifts:'),
        ('cards', 2, [('venus', 'Hormone Replacement Therapy (HRT)', '<p>Hormone Replacement Therapy is prescribed to manage the physical symptoms of menopause and prevent the subsequent estrogen drops and dopamine deficits. By ensuring a steady supply of estrogen, HRT prevents executive paralysis and restores the efficacy of stimulant medications.</p>', 'h3'),
                      ('flask', 'Bioidentical Hormones (BHRT)', '<p>Bioidentical hormones are chemical compounds that are molecularly identical to the hormones naturally produced by the human body. For the neurodivergent brain, BHRT is typically much better tolerated.</p><p>When administered transdermally (via gels or patches), these hormones bypass the liver’s first-pass metabolism entirely. This maximises their bioavailability, preventing the neurochemical fluctuations that cause executive paralysis, and safely restoring the efficacy of stimulant medications.</p>', 'h3'),
                      ('leaf', 'Natural Approaches to Hormonal Balance', '<p>Natural approaches to hormonal balance focus on improving the way the neurodivergent brain processes the hormones it already has. A specialist may recommend a low-glycaemic and high-protein diet that provides the necessary amino acids for synthesising dopamine and prevents insulin spikes that trigger ADHD paralysis.</p><p>Including high-fibre foods in your diet can prevent dysbiosis, which otherwise negatively affects hormonal balance. Additionally, certain vitamins and minerals, such as magnesium, zinc, iron and omega-3 fatty acids, support hormone synthesis and neurotransmitter production.</p>', 'h3'),
                      ('person', 'Testosterone Replacement Therapy (TRT)', '<p>Testosterone Replacement Therapy is recommended for men experiencing abnormally low hormone levels and transgender individuals undergoing gender-affirming care. By restoring proper dopamine regulation, it improves focus, working memory and executive functioning.</p><p>However, it is not recommended for age-related declines in testosterone without the presence of characteristic symptoms.</p>', 'h3')]),
        ('h2', 'What Hormone Therapy Cannot Do?'),
        ('callout', 'Worth knowing', '<p>While hormone therapy restores baseline dopamine and GABA levels, it cannot cure or alter core ADHD or autism traits. Furthermore, it cannot substitute on its own for specialised neurodivergent care. Even though it supports neuronal health and improves brain metabolism, it cannot change how the brain is wired.</p>'),
        ('p', 'When it comes to managing immediate cognitive symptoms, such as brain fog or hot flushes, hormone therapy is extremely effective; however, it does not halt the overall structural reductions in grey matter volume that take place during ageing. Consequently, there is no guarantee that individuals will feel exactly as they did in their 20s or 30s. For many, developing new post-menopausal coping mechanisms remains essential to effectively manage ADHD or autism.'),
        ('h2', 'A Holistic View: Hormones as One Piece of the Puzzle'),
        ('p', 'When viewing the health of a neurodivergent person from a holistic perspective, hormones are not the entire solution, but rather one vital piece of a complex puzzle. Long-term, effective management requires hormone therapy to stabilise the chemical baseline, combined with targeted ADHD or anxiety medications, neuroinclusive therapy that supports healthy unmasking, and high-protein nutrition to support dopamine and GABA levels.'),
        ('quote', 'Executive dysfunction is not a challenge that can be adequately addressed with neurotypical time management advice, especially when an underlying hormonal imbalance causes a severe dopamine deficit.'),
        ('p', 'Opting for a comprehensive, holistic approach that blends hormone therapy, stimulants or anxiolytics, specialised therapy and tailored nutrition is the most effective way to truly support the neurodivergent brain and enhance overall well-being.'),
        ('h2', 'When to Seek Professional Guidance'),
        ('p', 'When you struggle to manage neurodivergent symptoms during hormonal shifts, it is crucial to know when to seek professional guidance. You should consider asking for clinical support if:'),
        ('html', ul(['Your standard ADHD stimulant medications fail to work, or you experience severe monthly crashes during the luteal phase', 'You are in your 40s or 50s and experiencing a perimenopausal crash characterised by poor working memory, spatial confusion, emotional dysregulation or severe ADHD paralysis', 'You have recently given birth and find yourself suffering from severe executive dysfunction'])),
        ('p', 'Since a holistic approach is necessary, you do not have to rely on a single specialist. A psychiatrist specialised in adult female ADHD or autism can help you manage your neurodivergent diagnosis and monitor overlapping conditions like depression or PMDD. Simultaneously, you will need the support of a neuroendocrinologist who can safely evaluate and prescribe appropriate hormone therapy. Finally, a therapist or an ADHD coach can help you create structure, develop coping mechanisms and find safe ways to practise healthy unmasking.'),
        ('p', 'As clinical evidence shows, hormone therapy can improve neurodivergent symptoms, not independently, but as part of a complex, comprehensive treatment plan individualised to your specific needs. If you experience neurodivergent traits that worsen monthly, or if you are navigating perimenopause or the postpartum period and notice your struggles intensifying, undergoing a <a href="/diagnosis-main-page/">private ADHD diagnosis</a> can provide the clarity you deserve.'),
        ('p', 'Combining proper ADHD medication with specialised neurodivergent therapy, hormone regulation and a protein-rich diet offers a powerful therapeutic approach. This integration helps you navigate difficult hormonal shifts without compromising your neurological health. We are here to provide the exact support you need. Start with a free consultation at Refocus, and let us guide you through the next steps of your journey.'),
        ('cta', 'Start with a conversation', 'Ready for clarity?', 'Book a free 15-minute call with our team. We’ll listen, answer your questions and guide you to the right assessment or care pathway.',
         [('Book a free 15-minute call', FREE_CALL, 'btn-primary'), ('Explore assessments', '/diagnosis-main-page/', 'btn-ghost')]),
    ],
}

ARTICLES = [HORMONES]

if __name__ == '__main__':
    for a in ARTICLES:
        article(a)
