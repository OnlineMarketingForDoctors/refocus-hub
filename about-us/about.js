(function () {
  'use strict';

  /* ---------- Read more toggles (founder profile and message) ---------- */
  document.querySelectorAll('.ab-more-btn').forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    var label = btn.querySelector('span');
    var closedText = label.textContent;
    btn.addEventListener('click', function () {
      var open = !panel.classList.contains('is-open');
      panel.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
      label.textContent = open ? 'Show less' : closedText;
    });
  });

  /* ---------- Team filter ---------- */
  var filters = document.querySelectorAll('.ab-filter button');
  var people = document.querySelectorAll('.ab-person');
  filters.forEach(function (f) {
    f.addEventListener('click', function () {
      var group = f.getAttribute('data-filter');
      filters.forEach(function (o) { o.setAttribute('aria-pressed', String(o === f)); });
      people.forEach(function (p) { p.hidden = group !== 'all' && p.getAttribute('data-group') !== group; });
    });
  });

  /* ---------- Profile dialog ---------- */
  var dlg = document.querySelector('.ab-dialog');
  if (!dlg || typeof dlg.showModal !== 'function') return;
  var dImg = dlg.querySelector('.ab-dialog-head img');
  var dName = dlg.querySelector('#dlg-name');
  var dRole = dlg.querySelector('.ab-dialog-head .role');
  var dCreds = dlg.querySelector('.ab-dialog-head .creds');
  var dBody = dlg.querySelector('.ab-dialog-body');
  var opener = null;

  document.querySelectorAll('.ab-person-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var card = btn.closest('.ab-person');
      opener = btn;
      dImg.src = card.querySelector('.photo img').getAttribute('src');
      dName.textContent = card.querySelector('h3').textContent;
      dRole.textContent = card.querySelector('.role').textContent;
      dCreds.textContent = card.querySelector('.creds').textContent;
      dBody.innerHTML = card.querySelector('.ab-bio').innerHTML;
      dlg.showModal();
      dlg.querySelector('.ab-dialog-inner').scrollTop = 0;
      dlg.scrollTop = 0;
    });
  });
  dlg.querySelector('.ab-dialog-close').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener('close', function () { if (opener) opener.focus(); });
})();
