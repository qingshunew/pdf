const http = require('http');
const fs = require('fs');
const path = require('path');
const mime = {
  '.html': 'text/html; charset=utf-8',
  '.pdf': 'application/pdf',
  '.js': 'text/javascript',
  '.css': 'text/css'
};

http.createServer((req, res) => {
  let file = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
  if (fs.existsSync(file)) {
    let ext = path.extname(file);
    res.writeHead(200, { 'Content-Type': mime[ext] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
}).listen(8090, () => console.log('Server running on http://localhost:8090'));
