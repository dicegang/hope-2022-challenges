const crypto = require('crypto');
const fs = require('fs');
const http = require('http');

const wait = (time) => new Promise((res) => setTimeout(res, time));
const unindent = (data) => {
  const lines = data.split('\n').filter((v) => v);
  const indent = lines[0].search(/\S/);
  return lines.map((v) => v.slice(indent)).join('\n');
};

const routes = new Map();
const server = http.createServer((req, res) => {
  req.url = new URL(`a:${req.url}`);
  (routes.get(req.url.pathname) ?? routes.get('/'))?.(req, res);
});

const test = fs.readFileSync('public/test.js').toString();
const script = fs.readFileSync('public/script.js').toString();
const approvals = new Map();
const verifications = new Map();
routes.set('/', async (req, res) => {
  const id = crypto.randomBytes(8).toString('hex');

  res.setHeader('set-cookie', [`i=${id}`]);

  const initial = unindent(`
    <!doctype html>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
        font-family: sans-serif;
      }

      body {
        background-image: url("background.jpg");
      }

      .incorrect {
        animation: shake 0.25s;
      }

      .content {
        transform: scale(4);
        background-color: white;
        padding: 2rem;
        border-radius: 0.5rem;
      }

      .container {
        height: 100%;
        display: grid;
        place-items: center;
      }

      @keyframes shake {
        0% { transform: rotate(0deg); }
        25% { transform: rotate(5deg); }
        50% { transform: rotate(0eg); }
        75% { transform: rotate(-5deg); }
        100% { transform: rotate(0deg); }
      }
    </style>
    <script>
      window.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        e.stopPropagation();
      });

      window.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
          e.preventDefault();
          e.stopPropagation();
        }
      });
    </script>
    <span></span>
  `);
  res.write(initial);

  const chrome = req.headers['sec-ch-ua']?.includes('Google Chrome');
  if (!chrome) {
    const unsupported = unindent(`
      <div class="container">
        <div class="content">sorry, only chrome is supported!</div>
      </div>
    `);
    return res.end(unsupported);
  }

  const approved = await Promise.race([
    new Promise((res) => approvals.set(id, res)),
    wait(1500),
  ]);
  approvals.delete(id);

  if (!approved) {
    const cheating = unindent(`
      <div class="container">
        <div class="content">hey, no cheating!</div>
      </div>
    `);
    return res.end(cheating);
  }

  res.write(`<script>${test}</script>`);

  const verified = await Promise.race([
    new Promise((res) => verifications.set(id, res)),
    wait(1500),
  ]);
  verifications.delete(id);

  if (verified) {
    const content = unindent(`
      <div class="container">
        <form class="content">
          <input type="text" placeholder="Password..."/>
          <input type="submit" value="Check!" />
        </form>
      </div>
    `);
    res.write(content);
    res.write(`<script>${script}</script>`);
  }

  res.end();
});

const background = fs.readFileSync('public/background.jpg');
routes.set('/background.jpg', (req, res) => {
  const id = req.headers.cookie?.split('=')[1];
  approvals.get(id)?.(true);
  res.end(background);
});

routes.set('/load', (req, res) => {
  const id = req.headers.cookie?.split('=')[1];
  verifications.get(id)?.(true);
  res.end();
});

// no favicon
routes.set('/favicon.ico', (_req, res) => {
  res.end();
});

server.listen(80);
