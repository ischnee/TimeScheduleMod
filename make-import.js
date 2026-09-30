// Writes TimeScheduleMod.html, a bookmarks file Chrome can import (Bookmark Manager > ⋮ > Import bookmarks).
// The code after "javascript:" is percent-encoded so newlines and % signs survive.
const fs = require('fs'), path = require('path');
const raw = fs.readFileSync(path.join(__dirname, 'bookmarklet-timeschedulemod.js'), 'utf8');
if (!raw.startsWith('javascript:')) throw new Error('missing javascript: prefix');
const code = raw.slice('javascript:'.length), href = 'javascript:' + encodeURIComponent(code);
if (decodeURIComponent(href.slice('javascript:'.length)) !== code) throw new Error('round-trip mismatch');
fs.writeFileSync(path.join(__dirname, 'TimeScheduleMod.html'), `<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><A HREF="${href}">TimeScheduleMod</A>
</DL><p>
`);
console.log('wrote TimeScheduleMod.html', href.length, 'chars');
