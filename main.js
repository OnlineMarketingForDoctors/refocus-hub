(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Header state, nav, back to top ---------- */
  var header = document.querySelector('.site-header');
  var toTop = document.querySelector('.to-top');
  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 60);
    toTop.classList.toggle('is-visible', y > 900);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }); });

  /* ---------- Hero video ---------- */
  var heroVideo = document.querySelector('.hero-video');
  var videoToggle = document.querySelector('.video-toggle');
  if (heroVideo && videoToggle) {
    var setPaused = function (paused) {
      videoToggle.classList.toggle('is-paused', paused);
      videoToggle.setAttribute('aria-label', paused ? 'Play background video' : 'Pause background video');
    };
    videoToggle.hidden = false;
    heroVideo.addEventListener('play', function () { setPaused(false); });
    heroVideo.addEventListener('pause', function () { setPaused(true); });
    videoToggle.addEventListener('click', function () {
      if (heroVideo.paused) heroVideo.play(); else heroVideo.pause();
    });
    setPaused(true);
    if (!reduceMotion) {
      var attempt = heroVideo.play();
      if (attempt && attempt.catch) attempt.catch(function () { setPaused(true); });
    }
  }

  /* ---------- qEEG video: plays muted while in view ---------- */
  var qVideo = document.querySelector('.qeeg-video');
  if (qVideo) {
    var qPlay = document.querySelector('[data-vid-play]');
    var qSound = document.querySelector('[data-vid-sound]');
    var userPaused = false;
    qVideo.addEventListener('play', function () { qPlay.classList.add('is-playing'); qPlay.setAttribute('aria-label', 'Pause video'); });
    qVideo.addEventListener('pause', function () { qPlay.classList.remove('is-playing'); qPlay.setAttribute('aria-label', 'Play video'); });
    qPlay.addEventListener('click', function () {
      userPaused = !qVideo.paused;
      if (qVideo.paused) qVideo.play(); else qVideo.pause();
    });
    qSound.addEventListener('click', function () {
      qVideo.muted = !qVideo.muted;
      qSound.classList.toggle('is-on', !qVideo.muted);
      qSound.setAttribute('aria-pressed', String(!qVideo.muted));
      qSound.setAttribute('aria-label', qVideo.muted ? 'Turn sound on' : 'Turn sound off');
      if (!qVideo.muted && qVideo.paused) { userPaused = false; qVideo.play(); }
    });
    if (!reduceMotion && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting && !userPaused) {
            var attempt = qVideo.play();
            if (attempt && attempt.catch) attempt.catch(function () {});
          } else if (!e.isIntersecting) {
            qVideo.pause();
          }
        });
      }, { threshold: 0.4 }).observe(qVideo);
    }
  }

  var nav = document.getElementById('main-nav');
  var toggle = document.querySelector('.menu-toggle');
  function setMenu(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    toggle.querySelector('use').setAttribute('href', open ? '#i-close' : '#i-menu');
  }
  toggle.addEventListener('click', function () { setMenu(!nav.classList.contains('is-open')); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  /* ---------- EEG traces ---------- */
  function eegPath(width, height, points, seed, spikes) {
    var rnd = function () { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
    var mid = height / 2, d = 'M0,' + mid.toFixed(1);
    for (var i = 1; i <= points; i++) {
      var x = (i / points) * width;
      var amp = (Math.sin(i * 0.35) * 0.5 + 0.6) * (height * 0.22);
      if (spikes && rnd() > 0.93) amp = height * 0.46;
      var y = mid + (i % 2 ? -1 : 1) * amp * (0.4 + rnd() * 0.6);
      d += ' L' + x.toFixed(1) + ',' + y.toFixed(1);
    }
    return d;
  }
  var miniEeg = document.getElementById('eeg-mini');
  if (miniEeg) miniEeg.setAttribute('d', eegPath(400, 46, 90, 3, true));

  /* ---------- Carousels ---------- */
  document.querySelectorAll('[data-carousel]').forEach(function (root) {
    var track = root.querySelector('.carousel-track');
    var items = Array.prototype.slice.call(track.children);
    var dotsWrap = root.querySelector('[data-dots]');
    var delay = parseInt(root.getAttribute('data-autoplay'), 10) || 0;
    var timer = null, paused = false;

    function step() { return items.length > 1 ? items[1].offsetLeft - items[0].offsetLeft : track.clientWidth; }
    function index() { return Math.round(track.scrollLeft / step()); }
    function maxIndex() { return Math.max(0, Math.round((track.scrollWidth - track.clientWidth) / step())); }
    function go(i) {
      var max = maxIndex();
      if (i > max) i = 0;
      if (i < 0) i = max;
      track.scrollTo({ left: i * step(), behavior: reduceMotion ? 'auto' : 'smooth' });
    }

    var dots = [];
    function buildDots() {
      if (!dotsWrap) return;
      dotsWrap.innerHTML = '';
      dots = [];
      for (var i = 0; i <= maxIndex(); i++) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('aria-label', 'Go to slide ' + (i + 1));
        b.addEventListener('click', go.bind(null, i));
        dotsWrap.appendChild(b);
        dots.push(b);
      }
      syncDots();
    }
    function syncDots() {
      var cur = index();
      dots.forEach(function (d, i) { d.setAttribute('aria-current', i === cur ? 'true' : 'false'); });
    }

    root.querySelector('[data-prev]').addEventListener('click', function () { go(index() - 1); });
    root.querySelector('[data-next]').addEventListener('click', function () { go(index() + 1); });
    var raf;
    track.addEventListener('scroll', function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(syncDots); }, { passive: true });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(index() + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(index() - 1); }
    });

    function start() { if (delay && !reduceMotion && !timer) timer = setInterval(function () { if (!paused) go(index() + 1); }, delay); }
    ['mouseenter', 'focusin', 'touchstart'].forEach(function (ev) { root.addEventListener(ev, function () { paused = true; }, { passive: true }); });
    ['mouseleave', 'focusout'].forEach(function (ev) { root.addEventListener(ev, function () { paused = false; }); });

    buildDots();
    window.addEventListener('resize', buildDots);
    if (delay && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) start(); else { clearInterval(timer); timer = null; } });
      }).observe(root);
    }
  });

  /* ---------- Review "read more" ---------- */
  function checkClamps() {
    document.querySelectorAll('.review-card').forEach(function (card) {
      var text = card.querySelector('.review-text');
      var btn = card.querySelector('.read-more');
      if (card.classList.contains('is-expanded')) return;
      btn.hidden = text.scrollHeight <= text.clientHeight + 2;
    });
  }
  document.querySelectorAll('.review-card .read-more').forEach(function (btn) {
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function () {
      var card = btn.closest('.review-card');
      var open = card.classList.toggle('is-expanded');
      btn.textContent = open ? 'Read less' : 'Read more';
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  window.addEventListener('load', checkClamps);
  window.addEventListener('resize', checkClamps);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(checkClamps);

  /* ---------- Accordion ---------- */
  document.querySelectorAll('[data-accordion] .acc-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.acc-item');
      var open = !item.classList.contains('is-open');
      item.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
  });

  /* ---------- Image reveals and parallax ---------- */
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { threshold: 0.15 });
    document.querySelectorAll('.reveal-img').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal-img').forEach(function (el) { el.classList.add('is-in'); });
  }
  var pars = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
  if (pars.length && !reduceMotion) {
    var parTick = function () {
      pars.forEach(function (el) {
        var r = el.parentElement.getBoundingClientRect();
        if (r.bottom > 0 && r.top < window.innerHeight) {
          var p = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
          el.style.transform = 'translate3d(0,' + (p * -6).toFixed(2) + '%,0)';
        }
      });
    };
    window.addEventListener('scroll', function () { requestAnimationFrame(parTick); }, { passive: true });
    parTick();
  }

  /* ---------- 8 billion: focus lens follows the pointer, drifts on its own otherwise ---------- */
  var lens = document.querySelector('[data-lens]');
  if (lens) {
    var cur = { x: 62, y: 46 }, target = { x: 62, y: 46 };
    var pointerActive = false, lensVisible = false, t0 = performance.now(), lensRaf = null;
    var setLens = function () {
      lens.style.setProperty('--x', cur.x.toFixed(2) + '%');
      lens.style.setProperty('--y', cur.y.toFixed(2) + '%');
    };
    var lensLoop = function (now) {
      if (!pointerActive) {
        var t = (now - t0) / 1000;
        target.x = 58 + Math.sin(t * 0.23) * 26;
        target.y = 42 + Math.sin(t * 0.37 + 1.2) * 16;
      }
      cur.x += (target.x - cur.x) * 0.08;
      cur.y += (target.y - cur.y) * 0.08;
      setLens();
      lensRaf = lensVisible ? requestAnimationFrame(lensLoop) : null;
    };
    lens.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'touch') return;
      var r = lens.getBoundingClientRect();
      pointerActive = true;
      target.x = ((e.clientX - r.left) / r.width) * 100;
      target.y = ((e.clientY - r.top) / r.height) * 100;
      if (reduceMotion) { cur.x = target.x; cur.y = target.y; setLens(); }
    });
    lens.addEventListener('pointerleave', function () { pointerActive = false; t0 = performance.now() - 4000; });
    if (!reduceMotion && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        lensVisible = entries[0].isIntersecting;
        if (lensVisible && !lensRaf) lensRaf = requestAnimationFrame(lensLoop);
      }).observe(lens);
    }
  }

  /* ---------- Approach: the step in the middle of the screen drives the image ---------- */
  var ap = document.querySelector('[data-approach]');
  if (ap && 'IntersectionObserver' in window) {
    var apSteps = Array.prototype.slice.call(ap.querySelectorAll('[data-ap-step]'));
    var apImgs = ap.querySelectorAll('[data-ap-img]');
    var apBar = ap.querySelector('[data-ap-bar]');
    var apSet = function (i) {
      apSteps.forEach(function (s, j) { s.classList.toggle('is-active', i === j); });
      apImgs.forEach(function (img) { img.classList.toggle('is-active', img.getAttribute('data-ap-img') === String(i)); });
      if (apBar) apBar.style.width = ((i + 1) / apSteps.length * 100) + '%';
    };
    var apIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) apSet(apSteps.indexOf(e.target)); });
    }, { rootMargin: '-45% 0px -45% 0px' });
    apSteps.forEach(function (s) { apIo.observe(s); });
  }
})();
