(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Prices: audience tabs ---------- */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.pr-tab'));
  function selectTab(i, focus) {
    tabs.forEach(function (t, j) {
      var on = i === j;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tabs[i].focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { selectTab(i); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') selectTab((i + 1) % tabs.length, true);
      if (e.key === 'ArrowLeft') selectTab((i - 1 + tabs.length) % tabs.length, true);
    });
  });

  /* ---------- Prices: category sub-nav follows the section in view ---------- */
  var subLinks = Array.prototype.slice.call(document.querySelectorAll('.pr-subnav a'));
  if (subLinks.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        subLinks.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    subLinks.forEach(function (a) { var s = document.querySelector(a.getAttribute('href')); if (s) spy.observe(s); });
  }

  /* ---------- Prices: offer countdown ---------- */
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    var end = new Date(cd.getAttribute('data-countdown')).getTime();
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var tick = function () {
      var m = Math.floor(Math.max(0, end - Date.now()) / 60000);
      cd.querySelector('[data-d]').textContent = pad(Math.floor(m / 1440));
      cd.querySelector('[data-h]').textContent = pad(Math.floor((m % 1440) / 60));
      cd.querySelector('[data-m]').textContent = pad(m % 60);
    };
    tick();
    setInterval(tick, 30000);
  }

  /* ---------- Filter chips (neuro blog) ---------- */
  var grid = document.querySelector('[data-blog-grid]');
  if (grid) {
    var chips = Array.prototype.slice.call(document.querySelectorAll('.bl-filter button'));
    var cards = Array.prototype.slice.call(grid.children);
    var empty = document.querySelector('.bl-empty');
    var apply = function (cat) {
      var shown = 0;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-filter') === cat)); });
      cards.forEach(function (c) { var on = cat === 'All' || c.getAttribute('data-cat') === cat; c.hidden = !on; if (on) shown++; });
      if (empty) empty.hidden = shown > 0;
    };
    document.querySelectorAll('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () { apply(b.getAttribute('data-filter')); });
    });
    var topic = new URLSearchParams(location.search).get('topic');
    if (topic && chips.some(function (c) { return c.getAttribute('data-filter') === topic; })) {
      apply(topic);
      var list = document.querySelector('.bl-list');
      if (list) setTimeout(function () { list.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' }); }, 300);
    }
  }

  /* ---------- At-home: front / inside product views ---------- */
  document.querySelectorAll('.ah-prod').forEach(function (prod) {
    var imgs = prod.querySelectorAll('[data-views] img');
    var btns = prod.querySelectorAll('[data-view]');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var i = +b.getAttribute('data-view');
        btns.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        imgs.forEach(function (img, j) { img.classList.toggle('is-active', i === j); });
      });
    });
  });

  /* ---------- Contact: clinic photo lightbox ---------- */
  var lb = document.querySelector('.ct-lightbox');
  if (lb && typeof lb.showModal === 'function') {
    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('p');
    var opener = null;
    document.querySelectorAll('.ct-shot').forEach(function (shot) {
      shot.addEventListener('click', function () {
        opener = shot;
        var img = shot.querySelector('img');
        lbImg.src = shot.getAttribute('data-full');
        lbImg.alt = img.alt;
        lbCap.textContent = img.alt;
        lb.showModal();
      });
    });
    lb.querySelector('.ct-lb-close').addEventListener('click', function () { lb.close(); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('close', function () { if (opener) opener.focus(); });
  }

  /* ---------- Forms: validate, then open the visitor's email app with the message filled in ---------- */
  var messages = { name: 'Enter your name.', first: 'Enter your first name.', last: 'Enter your last name.', email: 'Enter an email address like name@example.com.', phone: 'Enter a phone number we can reach you on.', source: 'Choose how you heard about us.', message: 'Tell us a little about your question.' };
  document.querySelectorAll('form[data-mailto]').forEach(function (form) {
    var status = form.querySelector('.pg-form-status');
    function validate(el) {
      var ok = el.checkValidity();
      var field = el.closest('.field');
      if (field) {
        field.classList.toggle('has-error', !ok);
        var err = field.querySelector('.err');
        if (err) err.textContent = ok ? '' : messages[el.name] || 'Check this field.';
      }
      el.setAttribute('aria-invalid', String(!ok));
      return ok;
    }
    form.querySelectorAll('[required]').forEach(function (el) {
      el.addEventListener('blur', function () { if (el.value) validate(el); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = null;
      form.querySelectorAll('[required]').forEach(function (el) { if (!validate(el) && !bad) bad = el; });
      if (bad) {
        if (!bad.closest('.field') && status) {
          status.className = 'pg-form-status is-error';
          status.textContent = messages[bad.name] || 'Check this field.';
          status.hidden = false;
        }
        bad.focus();
        return;
      }
      var lines = [];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || !el.value) return;
        var label = form.querySelector('label[for="' + el.id + '"]');
        lines.push((label ? label.textContent.replace(/\(optional\)/, '').trim() : el.name) + ': ' + el.value);
      });
      var href = 'mailto:' + form.getAttribute('data-mailto') +
        '?subject=' + encodeURIComponent(form.getAttribute('data-subject') || 'Website enquiry') +
        '&body=' + encodeURIComponent(lines.join('\n\n'));
      window.location.href = href;
      if (status) {
        status.className = 'pg-form-status';
        status.innerHTML = 'Your email app should open with your message ready to send. If it doesn’t, email <a href="mailto:hello@refocushub.co.uk">hello@refocushub.co.uk</a> or call <a href="tel:+441614707093">0161 470 7093</a>.';
        status.hidden = false;
      }
    });
  });
})();

/* ---------- Assessment pages: expandable process steps ---------- */
(function () {
  'use strict';
  document.querySelectorAll('[data-steps]').forEach(function (list) {
    var items = Array.prototype.slice.call(list.querySelectorAll('.dx-step'));
    items.forEach(function (item) {
      var btn = item.querySelector('.dx-step-btn');
      btn.addEventListener('click', function () {
        var open = !item.classList.contains('is-open');
        items.forEach(function (o) {
          var on = o === item ? open : false;
          o.classList.toggle('is-open', on);
          o.querySelector('.dx-step-btn').setAttribute('aria-expanded', String(on));
        });
      });
    });
  });
})();

/* ---------- Blog article: reading progress, contents tracking, copy link ---------- */
(function () {
  'use strict';
  var body = document.querySelector('.ar-body');
  if (!body) return;
  var bar = document.querySelector('.ar-progress span');
  var ticking = false;
  function update() {
    var r = body.getBoundingClientRect();
    var total = r.height - window.innerHeight * 0.6;
    var p = Math.min(1, Math.max(0, -r.top / (total > 0 ? total : 1)));
    if (bar) bar.style.transform = 'scaleX(' + p + ')';
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  update();

  var links = Array.prototype.slice.call(document.querySelectorAll('.ar-toc a'));
  if (links.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    links.forEach(function (a) { var h = document.getElementById(a.getAttribute('href').slice(1)); if (h) spy.observe(h); });
  }
  var toc = document.querySelector('.ar-toc details');
  if (toc && window.matchMedia('(max-width: 1000px)').matches) toc.open = false;

  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var tip = btn.querySelector('.ar-copied');
      var done = function () { if (tip) { tip.textContent = 'Link copied'; tip.classList.add('is-on'); setTimeout(function () { tip.classList.remove('is-on'); }, 1800); } };
      if (navigator.clipboard) navigator.clipboard.writeText(btn.getAttribute('data-copy')).then(done, done); else done();
    });
  });
})();
