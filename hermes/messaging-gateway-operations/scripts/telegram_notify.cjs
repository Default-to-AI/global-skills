
const fs = require('fs');
const https = require('https');

const envPath = 'C:/Users/Tiger/AppData/Local/hermes/.env';
const env = fs.readFileSync(envPath, 'utf8');
const tokenLine = env.split('\n').find(line => line.startsWith('TELEGRAM_BOT_TOKEN=*** (!tokenLine) throw new Error('missing TELEGRAM_BOT_TOKEN');
const token = tokenLine.split('=').slice(1).join('=').trim();
const chatId = '8137298532';
const text = process.argv.length > 2 ? process.argv[2] : '✅ Hermes backup complete';
const postData = JSON.stringify({ chat_id: chatId, text });
const options = {
  hostname: 'api.telegram.org',
  path: `/bot${token}/sendMessage`,
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

const req = https.request(options, res => {
  let data = '';
  res.on('data', chunk => { data += chunk; });
  res.on('end', () => {
    const body = JSON.parse(data);
    if (body.ok !== true) throw new Error(JSON.stringify(body));
    if (!body.result || typeof body.result.message_id !== 'number') throw new Error(JSON.stringify(body));
    console.log(body.result.message_id);
  });
});

req.on('error', error => {
  console.error(error);
  process.exit(1);
});
req.write(postData);
req.end();
