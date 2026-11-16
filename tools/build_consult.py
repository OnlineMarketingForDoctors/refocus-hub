"""Build the free 15-minute consultation page (/free-consultation/).

Usage: python3 tools/build_consult.py .
The form is a placeholder: it validates, then opens the visitor's email app with the details filled in (pages.js).
Swap it for the real booking or CRM form when that is ready.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import build, hero, cta_band  # noqa: E402
from build_diagnosis import REVIEWS, REGULATED, sec, steps, ul  # noqa: E402

SOURCES = ['Search Engines (Google, Bing, Yahoo)', 'Social media - Facebook, Instagram, Tiktok', 'From a friend/family member', 'From another doctor',
           'Newsletter', 'Text message', 'Influencer', 'Radio (incl. Podcasts)', 'AI Chats (ChatGPT, Gemini, Perplexity)', 'Other']


def field(fid, name, label, kind='text', auto='', full=False):
    a = f' autocomplete="{auto}"' if auto else ''
    return f'<div class="field{" full" if full else ""}"><label for="{fid}">{label}</label><input id="{fid}" name="{name}" type="{kind}"{a} required><span class="err" aria-live="polite"></span></div>'


def form():
    opts = '<option value="" selected disabled>Choose an option</option>' + ''.join(f'<option>{s}</option>' for s in SOURCES)
    return f'''<div class="form-card fc-form">
            <h3 id="form-title">Book your consultation</h3>
            <p class="sub">Complete the form below and our team will be in touch to schedule your session.</p>
            <form class="pg-form" data-mailto="hello@refocushub.co.uk" data-subject="Free 15-minute consultation request" novalidate>
              <div class="form-grid">
                {field('fc-first', 'first', 'First name', auto='given-name')}
                {field('fc-last', 'last', 'Last name', auto='family-name')}
                {field('fc-email', 'email', 'Email', 'email', 'email', full=True)}
                {field('fc-phone', 'phone', 'Phone', 'tel', 'tel', full=True)}
                <div class="field full"><label for="fc-source">How did you hear about us?</label><select id="fc-source" name="source" required>{opts}</select><span class="err" aria-live="polite"></span></div>
              </div>
              <button class="btn btn-primary btn-lg" type="submit">Book your consultation</button>
              <p class="pg-form-status" role="status" hidden></p>
              <p class="pg-small">Free and confidential. We’ll only use your details to arrange your call. See our <a href="https://refocushub.co.uk/privacy-policy/">privacy policy</a>.</p>
            </form>
          </div>'''


def page():
    who = [('i-compass', 'ADHD symptoms or attention difficulties'), ('i-heart', 'Anxiety or emotional overwhelm'), ('i-leaf', 'Burnout or chronic stress'),
           ('i-path', 'Difficulty focusing or staying productive'), ('i-brain', 'Brain fog or mental fatigue')]
    who_html = '<ul class="fc-who">' + ''.join(f'<li><span class="ico"><svg><use href="#{i}"/></svg></span>{t}</li>' for i, t in who) + '</ul>'
    sections = [
        f'''    <section class="section fc-form-sec" id="book" aria-labelledby="form-title">
      <img class="deco deco-waves" src="/img/waves-side.svg" alt="" width="300" height="900" style="width:160px;left:0;top:60px;transform:scaleX(-1)" loading="lazy">
      <div class="wrap fc-grid">
        <div class="fc-copy">
          <p class="kicker">Help us guide you to the right pathway</p>
          <h2>Speak directly with a specialist</h2>
          <p class="lede">At Refocus, we combine clinical expertise with advanced brain technologies to move beyond guesswork — and towards precision, personalised care.</p>
          <div class="fc-details">
            <p class="kicker">Consultation details</p>
            <h3>15-minute free online consultation</h3>
            <ul class="fc-facts"><li><strong>15</strong><span>minutes</span></li><li><strong>£0</strong><span>no cost</span></li><li><strong>Online</strong><span>from home</span></li></ul>
            {ul(['Speak directly with a specialist', 'Confidential conversation', 'Guidance on possible next steps'])}
          </div>
        </div>
        {form()}
      </div>
    </section>
''',
        sec('fc-who-sec', 'who-title', 'Who is this for?', 'A short call for anyone experiencing', 'Whether you’re experiencing difficulties with focus, anxiety, burnout or emotional regulation, this consultation will help you understand how our neuroscience-based approach may support you.', who_html, center=True),
        sec('fc-next', 'next-title', 'What to expect', 'How your free consultation works', '',
            steps([('Step 1', 'Send your details', '<p>Complete the short form with your name, contact details and how you heard about us.</p>'),
                   ('Step 2', 'We arrange your call', '<p>Our team gets in touch to find a time that suits you for your short online session.</p>'),
                   ('Step 3', 'Talk it through', '<p>A Refocus specialist listens to your concerns in a confidential conversation and explains how our approach may support you.</p>'),
                   ('Step 4', 'Your next steps', '<p>You leave with guidance on possible next steps — whether that is an assessment, brain mapping or ongoing care — with no obligation to book.</p>')],
                  img='/img/hero-consult.webp')),
        REVIEWS,
        REGULATED,
        cta_band('Prefer to talk now?', 'Call us on 0161 470 7093', 'Our team is happy to answer your questions by phone, Monday to Friday 9am to 6pm and Saturday 10am to 2pm.').replace('href="/free-consultation/"', 'href="#book"'),
    ]
    main = '  <main id="main">\n' + hero('/img/hero-consult.webp', 'A man smiles during a relaxed online video call on his laptop at home', 'Free · Confidential · Online',
                                        '15-minute free initial consultation',
                                        'Speak with a Refocus specialist in a short online session designed to understand your concerns and guide you toward the right next steps for your brain health.',
                                        [('Book your consultation', '#book', 'btn-primary'), ('Call 0161 470 7093', 'tel:+441614707093', 'btn-ghost')], pos='72% center').replace('href="#start"', 'href="#book"') + ''.join(sections) + '  </main>\n'
    build('free-consultation', 'Free 15-Minute Consultation | ADHD &amp; Autism | Refocus',
          'Book a free, confidential 15-minute call with the Refocus team to discuss ADHD, autism or brain health concerns and find the right assessment pathway.',
          '/img/hero-consult.webp', main)


if __name__ == '__main__':
    page()
