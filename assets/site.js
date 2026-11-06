(() => {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = id => document.getElementById(id);

  // Logo animation from the brand guide, on a loop: a line travels in and coils toward the centre,
  // the two beams are drawn in from the space it leaves, they hold, then clear for the next pass.
  // No rotation, no shadow, and the two forms never join.
  const trace = $('trace'), c1 = $('c1r'), c2 = $('c2r');
  if (trace && c1 && c2) {
    const pts = [];
    for (let k = 0, n = 220, turns = 1.85; k <= n; k++) {
      const t = k / n, a = -Math.PI / 2 + t * turns * 2 * Math.PI, r = 56 - 50 * t;
      pts.push((60 + r * Math.cos(a)).toFixed(2) + ',' + (60 + r * Math.sin(a)).toFixed(2));
    }
    trace.setAttribute('d', 'M60,-30 L' + pts.join(' L'));
    const beams = (a, b) => {
      c1.setAttribute('height', (120 * a).toFixed(1));
      c2.setAttribute('y', (120 - 120 * b).toFixed(1)); c2.setAttribute('height', (120 * b).toFixed(1));
    };
    if (still) { beams(1, 1); trace.style.opacity = 0; }
    else {
      const L = trace.getTotalLength(), CYCLE = 7600;
      trace.style.strokeDasharray = L;
      const clamp = (v) => Math.min(1, Math.max(0, v)), span = (t, from, len) => clamp((t - from) / len);
      const inOut = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, out = t => 1 - Math.pow(1 - t, 3);
      let start = performance.now(), running = true, raf = 0;
      function frame(now) {
        const t = (now - start) % CYCLE;
        trace.style.strokeDashoffset = (L * (1 - inOut(span(t, 200, 1500)))).toFixed(1);
        trace.style.opacity = (1 - span(t, 1750, 650)).toFixed(3);
        const grow1 = out(span(t, 1600, 700)), grow2 = out(span(t, 1850, 700));
        const clear1 = inOut(span(t, 6100, 600)), clear2 = inOut(span(t, 6300, 600));
        beams(grow1 * (1 - clear1), grow2 * (1 - clear2));
        if (running) raf = requestAnimationFrame(frame);
      }
      raf = requestAnimationFrame(frame);
      // Pause when the logo is off screen or the tab is hidden, to save battery.
      const plate = trace.closest('.plate');
      const setRunning = on => {
        if (on === running) return;
        running = on;
        if (on) { start = performance.now() - ((performance.now() - start) % CYCLE); raf = requestAnimationFrame(frame); }
        else cancelAnimationFrame(raf);
      };
      let visible = true;
      new IntersectionObserver(es => { visible = es[0].isIntersecting; setRunning(visible && !document.hidden); }).observe(plate);
      document.addEventListener('visibilitychange', () => setRunning(visible && !document.hidden));
    }
  }

  // Statement lights up word by word as it scrolls through the screen.
  const st = $('statement');
  let words = [];
  if (st) {
    st.innerHTML = st.textContent.trim().split(/\s+/).map(w => `<span class="w">${w}</span>`).join(' ');
    words = [...st.querySelectorAll('.w')];
    if (still) words.forEach(w => w.classList.add('on'));
  }
  const fill = () => { const r = st.getBoundingClientRect(); return Math.min(1, Math.max(0, (innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.3))); };

  const top = $('top'), phone = $('phone');
  let ticking = false;
  function onScroll() {
    ticking = false;
    if (top) top.classList.toggle('lined', scrollY > 10);
    if (still) return;
    if (phone) {
      const r = phone.getBoundingClientRect(), p = Math.min(1, Math.max(0, 1.1 - r.top / innerHeight));
      phone.style.setProperty('--lift', (26 - p * 26).toFixed(1) + 'px');
    }
    if (st) { const n = Math.round(fill() * words.length); words.forEach((w, i) => w.classList.toggle('on', i < n)); }
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, {passive: true});
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), {rootMargin: '0px 0px -8% 0px'});
  document.querySelectorAll('.rv').forEach(el => io.observe(el));
  onScroll();
})();
