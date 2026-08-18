const express = require('express');
const child_process = require('child_process');
const app = express();

const API_KEY = "sk_test_12345";

app.get('/search', (req, res) => {
  const q = req.query.q || '';
  res.send(`<h1>Results for ${q}</h1>`);
});

app.get('/calc', (req, res) => {
  const expr = req.query.expr || '1+1';
  res.send(String(eval(expr)));
});

app.get('/ping', (req, res) => {
  const host = req.query.host || '127.0.0.1';
  const out = child_process.execSync(`ping -c 1 ${host}`).toString();
  res.send(out);
});

app.get('/token', (req, res) => {
  const token = 'tok-' + Math.random();
  res.send(`<script>localStorage.setItem('token', '${token}');</script>`);
});

app.listen(3000, () => console.log('insecure app listening on 3000'));
