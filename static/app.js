const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
let shown = 0, me = null, filter = 'all', timer;

async function api(path, data) {
  const r = await fetch('/api/' + path, {
    method: data === undefined ? 'GET' : 'POST',
    headers: {'Content-Type': 'application/json'},
    body: data === undefined ? undefined : JSON.stringify(data)
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw Object.assign(new Error(j.error || 'Something went wrong.'), {status: r.status});
  return j;
}
function toast(msg, err) {
  const t = $('#toast'); t.textContent = msg; t.className = 'show' + (err ? ' err' : '');
  clearTimeout(timer); timer = setTimeout(() => t.className = '', 3200);
}
const money = n => n.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
function countTo(v) {
  const from = shown, t0 = performance.now();
  (function step(t) {
    const p = Math.min((t - t0) / 500, 1);
    shown = from + (v - from) * p; $('#bal').textContent = money(shown);
    if (p < 1) requestAnimationFrame(step);
  })(t0);
}
function renderHistory() {
  const items = me.history.filter(h => filter === 'all' || h.kind === filter);
  $('#hist').innerHTML = items.length ? items.map(h => {
    const amt = h.kind === 'info' ? '' : `<b class="${h.kind}">${h.kind === 'in' ? '+' : '-'}${money(h.amount)}</b>`;
    return `<li><span>${h.text}<small>${h.time}</small></span>${amt}</li>`;
  }).join('') : '<li class="muted">No transactions yet.</li>';
}
function show(data) {
  me = data; const on = !!data;
  $('#auth').hidden = on; $('#dash').hidden = !on; $('#who').hidden = !on;
  if (!on) { shown = 0; return; }
  $('#who').textContent = data.name; $('#accno').textContent = data.account_number;
  countTo(data.balance); renderHistory();
}
$$('.tab').forEach(b => b.onclick = () => {
  const g = b.dataset.group;
  $$(`.tab[data-group=${g}]`).forEach(x => x.classList.toggle('on', x === b));
  $$(`form[data-group=${g}]`).forEach(f => f.hidden = f.dataset.panel !== b.dataset.tab);
});
$$('form').forEach(f => f.onsubmit = async e => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(f)), act = f.dataset.action;
  try {
    const res = await api(act, data);
    f.reset();
    if (act === 'register') {
      $('#newacc').hidden = false;
      $('#newacc').innerHTML = `Account created. Your account number is <b>${res.account_number}</b>. Save it to log in.`;
      $('[data-tab=login]').click(); $('[data-panel=login] [name=account]').value = res.account_number;
      toast('Account created');
    } else { show(res); toast(f.dataset.ok || 'Welcome back, ' + res.name); }
  } catch (err) { if (err.status === 401 && act !== 'login') show(null); toast(err.message, true); }
});
$$('[data-add]').forEach(b => b.onclick = () => {
  const i = b.closest('form').amount; i.value = ((parseFloat(i.value) || 0) + +b.dataset.add).toFixed(2);
});
$$('[data-all]').forEach(b => b.onclick = () => b.closest('form').amount.value = me.balance.toFixed(2));
$$('.f').forEach(b => b.onclick = () => {
  filter = b.dataset.f; $$('.f').forEach(x => x.classList.toggle('on', x === b)); renderHistory();
});
$('#logout').onclick = async () => { await api('logout', {}); show(null); toast('Logged out'); };
$('#copy').onclick = () => navigator.clipboard.writeText(me.account_number).then(() => toast('Account number copied'));
api('me').then(show).catch(() => show(null));
