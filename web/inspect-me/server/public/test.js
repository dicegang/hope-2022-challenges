(() => {
  const m = {
    log: console.log,
    clear: console.clear,
    table: console.table,
    now: performance.now.bind(performance),
  };

  const a = Array(100).fill(document.createElement('a'));

  const detector = {
    state: undefined,
    listeners: [],
    worst: 1e-3,
    addListener(func) {
      this.listeners.push(func);
    },

    // loop
    update() {
      let start = m.now();
      m.log(a);
      const log = m.now() - start;
      m.table(a);
      const table = m.now() - start - log;

      m.clear();

      this.worst = Math.max(log, this.worst);

      const logging = table > 10 * this.worst;

      const threshold = 160;
      const size =
        window.outerWidth - window.innerWidth > threshold ||
        window.outerHeight - window.innerHeight > threshold;

      const next = size || logging;
      if (next === this.state) return;
      this.state = next;
      this.listeners.forEach((func) => func(this.state));
    },
  };

  setInterval(() => {
    detector.update();
    m.log('hey, no cheating!');
  }, 100);

  const state = {
    reloadOnClose: false,
    reloadOnOpen: false,
  };

  const opened = () => {
    state.reloadOnClose = true;
    if (state.reloadOnOpen) {
      window.location.reload();
    }
    document.body.innerHTML = `
      <div class="container">
        <div class="content">hey, no cheating!</div>
      </div>
    `;
  };

  const closed = () => {
    state.reloadOnOpen = true;
    if (state.reloadOnClose) {
      window.location.reload();
    } else {
      navigator.sendBeacon('load');
    }
  };

  detector.addListener((state) => (state ? opened() : closed()));
})();
