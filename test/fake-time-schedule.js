// A made-up PHIL department's Time Schedule page, in the real page's format, for the tests. Every name and number is invented.
// page(quarter, shift) returns the page; shift nudges lecture enrollments so past quarters differ.
const fs = require('fs');
const courses = [
  ['100', 'INTRODUCTION TO PHILOSOPHY', '(A&H/SSc)', [[180, 200], [96, 100]]],
  ['102', 'CONTEMPORARY MORAL PROBLEMS', '(A&H/SSc)', [[141, 150], [48, 60]]],
  ['114', 'PHILOSOPHICAL ISSUES IN THE LAW', '(A&H/SSc)', [[117, 120]]],
  ['115', 'PRACTICAL REASONING', '(SSc)', [[88, 120]]],
  ['118', 'PHILOSOPHY OF RELIGION', '(A&H)', [[55, 60]]],
  ['120', 'INTRODUCTION TO LOGIC', '(NSc)', [[172, 180], [60, 60]]],
  ['160', 'SOME MAJOR FIGURES IN PHILOSOPHY', '(A&H)', [[42, 50]]],
  ['207', 'HISTORY OF MODERN PHILOSOPHY', '(A&H)', [[38, 45]]],
  ['240', 'INTRODUCTION TO ETHICS', '(A&H/SSc)', [[119, 120], [45, 50]]],
  ['241', 'TOPICS IN ETHICS', '(A&H/SSc)', [[30, 40]]],
  ['242', 'INTRODUCTION TO MEDICAL ETHICS', '(A&H/SSc)', [[149, 150]]],
  ['243', 'ENVIRONMENTAL ETHICS', '(A&H/SSc)', [[70, 80]]],
  ['267', 'INTRODUCTION TO PHILOSOPHY OF RELIGION', '(A&H)', [[31, 40]]],
  ['320', 'HISTORY OF ANCIENT PHILOSOPHY', '(A&H)', [[36, 40]]],
  ['322', 'MODERN PHILOSOPHY', '(A&H)', [[24, 40]]],
  ['338', 'PHILOSOPHY OF HUMAN RIGHTS', '(A&H/SSc)', [[40, 40]]],
  ['345', 'MORAL PSYCHOLOGY', '(A&H)', [[33, 30]]],
  ['360', 'INTRODUCTION TO SYMBOLIC LOGIC', '(NSc)', [[33, 40]]],
  ['401', 'PHILOSOPHICAL WRITING', '', [[12, 20]]],
  ['411', 'KANT', '(A&H)', [[18, 25]]],
  ['440', 'TOPICS IN POLITICAL PHILOSOPHY', '(A&H/SSc)', [[22, 25]]],
  ['450', 'EPISTEMOLOGY', '(A&H)', [[16, 25]]],
  ['460', 'PHILOSOPHY OF SCIENCE', '(A&H/NSc)', [[20, 25]]],
];
const names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi'];
// Quiz sections per lecture: [leader, enrolled]. leader is a TA's name, 'STAFF', 'TBA' (no meeting time or name),
// '' (blank) or 'PROF' (the lecture's own instructor). Worked out by hand, all courses: 12 named TAs; usual load 2
// (7 TAs lead 2, 3 lead 3, 1 leads 4, 1 leads 1); 16 sections with students but no TA, 1 of them taken by Kale
// (1 section, in a course where the usual is 2); ≈8 more TAs; 3 empty sections not counted; 47 quiz sections. ≈20 TAs.
const QUIZ = {
  '100 A': [['Aster', 24], ['Aster', 25], ['Birch', 23], ['Birch', 25], ['Cedar', 22], ['Cedar', 24], ['STAFF', 20], ['', 18]],
  '100 B': [['Dahlia', 24], ['Dahlia', 25], ['STAFF', 21], ['PROF', 19]],
  '102 A': [['Elm', 25], ['Elm', 24], ['Elm', 23], ['Fern', 22], ['Fern', 25], ['Fern', 24]],
  '120 A': [['Ginkgo', 25], ['Ginkgo', 24], ['Ginkgo', 23], ['Laurel', 25], ['Laurel', 22], ['Laurel', 21], ['Laurel', 20], ['STAFF', 22], ['STAFF', 12], ['', 9]],
  '240 A': [['Hazel', 25], ['Hazel', 24], ['STAFF', 0], ['STAFF', 0]],
  '242 A': [['Iris', 25], ['Iris', 25], ['Juniper', 24], ['TBA', 23], ['PROF', 22], ['', 0]],
  '115 A': [['Juniper', 22], ['Kale', 21], ['STAFF', 23], ['STAFF', 22]],
  '114 A': [['STAFF', 24], ['STAFF', 24], ['STAFF', 23], ['', 23], ['TBA', 23]],
};
function page(quarter, shift) {
  let sln = 20100, out = `<html><head><title>PHIL ${quarter}</title></head><body><h1>PHILOSOPHY</h1>`;
  courses.forEach(([num, name, gened, secs], ci) => {
    out += `<br><table><tr><td><A NAME=phil${num}>PHIL&nbsp;&nbsp; ${num} </A>&nbsp;<A HREF=/course>${name}</A> ${gened}</td></tr></table>`;
    secs.forEach(([enrl0, lim], si) => {
      const enrl = Math.max(0, Math.min(lim + 5, enrl0 + shift * ((ci + si) % 3 - 1)));
      const sec = String.fromCharCode(65 + si), who = 'Instructor,' + names[(ci * 3 + si) % names.length];
      out += `<table><tr><td><pre><A HREF=/sln>${sln++}</A> ${sec}  5       MWF    1030-1120  SAV  264      ${who.padEnd(20)} Open     ${String(enrl).padStart(3)}/ ${lim}                      ${gened.replace(/[()]/g, '')}</pre></td></tr></table>`;
      (QUIZ[num + ' ' + sec] || []).forEach(([leader, qe], q) => {
        const id = sec + String.fromCharCode(65 + q);
        const meets = leader === 'TBA' ? 'to be arranged           ' : 'TTh    0930-1020  SAV  132';
        const person = leader === 'PROF' ? who : leader === 'STAFF' ? 'STAFF' : leader && leader !== 'TBA' ? 'Assistant,' + leader : '';
        out += `<table><tr><td><pre><A HREF=/sln>${sln++}</A> ${id} QZ      ${meets}      ${person.padEnd(20)} Open      ${String(qe).padStart(2)}/ 25</pre></td></tr></table>`;
      });
    });
  });
  return out + '</body></html>';
}
page.QUIZ = QUIZ; page.courses = courses; page.names = names;
module.exports = page;

/* A made-up CLAS department with a page for every quarter from Autumn 2016 to Autumn 2026 (Winter and Spring 2027 aren't
   published yet), for the Year, Decade and Summers views. Every name and number is invented.
   clas.sections(quarter) gives each lecture section, so the tests can add up what each view should show:
   - CLAS 101 A (lim 100), with four quiz sections led by two TAs (two each): 2 TAs every quarter but summer.
   - CLAS 210 A (lim 120) and CLAS 320 A (lim 40); CLAS 330 A (lim 30) only in Autumn 2018 and Spring 2019.
   - CLAS 484 A and B: independent study, "to be arranged", 1-5 credits, limit 5.
   - Summer: CLAS 101 A (lim 40, no quiz sections) and CLAS 484 A.
   Enrollments vary by quarter: i counts quarters from Autumn 2016. */
const CLAS_FIRST = 2016 * 4 + 3, QN = { WIN: 0, SPR: 1, SUM: 2, AUT: 3 };
function clasIndex(quarter) { return +quarter.slice(3) * 4 + QN[quarter.slice(0, 3)] - CLAS_FIRST; }
function clasSections(quarter) {
  const i = clasIndex(quarter);
  if (i < 0 || i > clasIndex('AUT2026')) return null;
  const tba = (sec, enrl) => ({ number: '484', name: 'INDEPENDENT READINGS', sec, cred: '1-5', meets: 'to be arranged', enrl, lim: 5, who: 'Instructor,Pi' });
  if (quarter.startsWith('SUM')) return [
    { number: '101', name: 'LATIN AND GREEK IN CURRENT USE', sec: 'A', cred: '5', meets: 'MTWTh  1030-1220  DEN  112', enrl: 25 + i % 10, lim: 40, who: 'Instructor,Rho' },
    tba('A', 1)];
  return [
    { number: '101', name: 'LATIN AND GREEK IN CURRENT USE', sec: 'A', cred: '5', meets: 'MWF    1030-1120  DEN  112', enrl: 60 + (i * 7) % 40, lim: 100, who: 'Instructor,Rho', quizzes: [['Ivy', 24], ['Ivy', 22], ['Oak', 20], ['Oak', 18]] },
    { number: '210', name: 'GREEK AND ROMAN MYTHOLOGY', sec: 'A', cred: '5', meets: 'MWF    0130-0220  DEN  211', enrl: 90 + (i * 5) % 30, lim: 120, who: 'Instructor,Sigma' },
    { number: '320', name: 'GREEK PHILOSOPHY', sec: 'A', cred: '5', meets: 'TTh    1130-1250  DEN  213', enrl: 20 + i % 15, lim: 40, who: 'Instructor,Tau' }]
    // A course last taught in Spring 2019, for the time series' "last taught".
    .concat(quarter === 'AUT2018' || quarter === 'SPR2019' ? [{ number: '330', name: 'GREEK TRAGEDY', sec: 'A', cred: '5', meets: 'MW     0230-0350  DEN  209', enrl: 18, lim: 30, who: 'Instructor,Upsilon' }] : [])
    .concat([tba('A', 1), tba('B', i % 2)]);
}
function clasPage(quarter) {
  const secs = clasSections(quarter);
  if (!secs) return null;
  let sln = 30000 + clasIndex(quarter) * 20, out = `<html><head><title>CLAS ${quarter}</title></head><body><h1>CLASSICS</h1>`, last = null;
  secs.forEach(s => {
    if (s.number !== last) { out += `<br><table><tr><td><A NAME=clas${s.number}>CLAS&nbsp;&nbsp; ${s.number} </A>&nbsp;<A HREF=/course>${s.name}</A> (A&H)</td></tr></table>`; last = s.number; }
    out += `<table><tr><td><pre><A HREF=/sln>${sln++}</A> ${s.sec}  ${s.cred.padEnd(8)}${s.meets.padEnd(31)}${s.who.padEnd(22)}Open     ${String(s.enrl).padStart(3)}/ ${s.lim}      A&H</pre></td></tr></table>`;
    (s.quizzes || []).forEach(([leader, qe], q) => {
      out += `<table><tr><td><pre><A HREF=/sln>${sln++}</A> ${s.sec}${String.fromCharCode(65 + q)} QZ      TTh    0930-1020  DEN  132      ${('Assistant,' + leader).padEnd(22)}Open      ${String(qe).padStart(2)}/ 25</pre></td></tr></table>`;
    });
  });
  return out + '</body></html>';
}
page.clas = { page: clasPage, sections: clasSections };

/* A made-up MATH department the size of a big one, for a stress test (Oct 2026: TSMod crashed on the real MATH, whose pages
   we can't see without a UW NetID). Every name and number is invented. Per quarter, Autumn 2016 to Autumn 2026: about 150
   lecture sections and 300 quiz sections; seminars (SM) and labs (LB); independent study, thesis and dissertation courses
   with dozens of sections each, so their IDs run past Z (AA, AB...), some typed IS and some untyped; sections with no seats;
   variable credits; and long course notes in plain text (the lines that froze TSMod on the real MATH: Ben's section-row
   pattern took exponentially long on them). */
function mathSections(quarter) {
  const i = clasIndex(quarter);
  if (i < 0 || i > clasIndex('AUT2026')) return null;
  const summer = quarter.startsWith('SUM'), out = [];
  const ids = n => Array.from({ length: n }, (_, k) => k < 26 ? String.fromCharCode(65 + k) : String.fromCharCode(64 + Math.floor(k / 26)) + String.fromCharCode(65 + k % 26));
  // Renumbered in Autumn 2019 (as on the real MATH pages: 207 was 307, 208 was 308, 224 was 324); o.lim may grow with the quarter.
  const renumbered = i < clasIndex('AUT2019'), num = n => renumbered && { 207: '307', 208: '308', 224: '324' }[n] || n;
  const add = (number, name, lectures, quizzes, o = {}) => ids(summer ? Math.max(1, Math.ceil(lectures / 4)) : lectures).forEach((sec, k) => out.push(Object.assign({
    number: num(number), name, sec, type: o.type || '', cred: o.cred || '5', meets: o.meets || 'MWF    0930-1020  SMI  120', enrl: Math.max(0, (typeof o.lim === 'function' ? o.lim(i) : o.lim || 160) - 12 - (i + k * 7) % 25), lim: typeof o.lim === 'function' ? o.lim(i) : o.lim || 160,
    who: o.who === undefined ? 'Instructor,' + names[(+number + k) % names.length] : o.who, quizzes: summer ? 0 : quizzes }, o.extra || {})));
  add('098', 'INTERMEDIATE ALGEBRA', 2, 0, { lim: 40 });
  add('102', 'PRE-ALGEBRA', 1, 0, { lim: 40 });
  add('103', 'INTRODUCTION TO ELEMENTARY FUNCTIONS', 1, 0, { lim: 40 });
  add('111', 'ALGEBRA WITH APPLICATIONS', 4, 4, { lim: 120 });
  add('112', 'BUSINESS CALCULUS', 3, 3, { lim: 120 });
  add('120', 'PRECALCULUS', 6, 4, { lim: 120 });
  add('124', 'CALCULUS WITH ANALYTIC GEOMETRY I', 12, 6, { lim: q => 160 + 2 * q });
  add('125', 'CALCULUS WITH ANALYTIC GEOMETRY II', 8, 6);
  add('126', 'CALCULUS WITH ANALYTIC GEOMETRY III', 6, 6);
  add('134', 'ACCELERATED (HONORS) CALCULUS', 1, 2, { lim: 60 });
  ['207', '208', '209', '224'].forEach((n, k) => add(n, ['INTRODUCTION TO DIFFERENTIAL EQUATIONS', 'MATRIX ALGEBRA WITH APPLICATIONS', 'LINEAR ANALYSIS', 'ADVANCED MULTIVARIABLE CALCULUS'][k], [6, 6, 2, 4][k], k < 2 ? 3 : 0,
    { lim: [q => 50 + 5 * q, q => 50 + 8 * q, () => 100, q => 50 + 6 * q][k] }));
  ['300', '309', '318', '327', '328', '334', '340', '380', '394'].forEach((n, k) => add(n, 'UPPER DIVISION TOPIC ' + n, [3, 2, 2, 2, 2, 1, 2, 1, 1][k], 0, { lim: 50, meets: 'TTh    1030-1150  PDL  C38' }));
  add('381', 'DISCRETE MATHEMATICAL MODELING I', 1, 0, { lim: 40 });
  add('382', 'DISCRETE MATHEMATICAL MODELING II', 1, 0, { lim: 40 });
  ['402', '403', '407', '409', '411', '424', '425', '427', '435', '441', '464', '491'].forEach((n, k) => add(n, 'ADVANCED TOPIC ' + n, 1 + k % 2, 0, { lim: 40, meets: 'MWF    1130-1220  PDL  C36' }));
  add('480', 'MATHEMATICS LAB', 2, 0, { type: 'LB', lim: 24, cred: '3' });
  add('498', 'SPECIAL TOPICS IN MATHEMATICS', 3, 0, { lim: 30, cred: '1-5' });
  add('499', 'UNDERGRADUATE RESEARCH', 30, 0, { lim: 5, cred: '1-5', meets: 'to be arranged' });
  ['504', '505', '524', '534', '544', '554', '564', '574'].forEach(n => add(n, 'GRADUATE COURSE ' + n, 1, 0, { lim: 25, cred: '3' }));
  ['581', '582', '590'].forEach(n => add(n, 'SEMINAR ' + n, 2, 0, { type: 'SM', lim: 20, cred: '1-3' }));
  add('600', 'INDEPENDENT STUDY OR RESEARCH', 45, 0, { type: 'IS', lim: 5, cred: '*', meets: 'to be arranged' });
  add('700', 'MASTERS THESIS', 10, 0, { lim: 5, cred: '*', meets: 'to be arranged' });
  add('800', 'DOCTORAL DISSERTATION', 40, 0, { lim: 5, cred: '*', meets: 'to be arranged' });
  add('495', 'MATHEMATICS CONTEST PREPARATION', 1, 0, { lim: 0, cred: '1' });   // no seats
  return out;
}
function mathPage(quarter) {
  const secs = mathSections(quarter);
  if (!secs) return null;
  let sln = 40000 + clasIndex(quarter) * 900, out = `<html><head><title>MATH ${quarter}</title></head><body><h1>MATHEMATICS</h1>`, last = null;
  secs.forEach(s => {
    if (s.number !== last) { out += `<br><table><tr><td><A NAME=math${s.number}>MATH&nbsp;&nbsp; ${s.number} </A>&nbsp;<A HREF=/course>${s.name}</A> (NSc)</td></tr></table>`; last = s.number; }
    out += `<table><tr><td><pre><A HREF=/sln>${sln++}</A> ${s.sec.padEnd(2)} ${s.type.padEnd(2)}  ${s.cred.padEnd(6)}${s.meets.padEnd(31)}${s.who.padEnd(22)}Open     ${String(s.enrl).padStart(3)}/ ${s.lim}      NSc${s.quizzes ? '\n                        STUDENTS MUST ALSO REGISTER FOR A QUIZ SECTION OF THIS COURSE AND ATTEND ALL MEETINGS IN PERSON' : ''}${s.number === '600' ? '\n                        CONTACT THE INSTRUCTOR BEFORE REGISTERING; ENTRY CODES ARE GIVEN ONLY WITH THE ADVISER\'S APPROVAL' : ''}</pre></td></tr></table>`;
    for (let q = 0; q < s.quizzes; q++) out += `<table><tr><td><pre><A HREF=/sln>${sln++}</A> ${s.sec}${String.fromCharCode(65 + q)} QZ      TTh    0930-1020  SMI  211      ${('Assistant,' + names[(q + +s.number) % names.length]).padEnd(22)}Open      ${String(20 + q).padStart(2)}/ 25</pre></td></tr></table>`;
  });
  return out + '</body></html>';
}
page.math = { page: mathPage, sections: mathSections };

/* The Enrollment Summary (sdb.admin.uw.edu .../tsstat.asp) for any of the made-up Time Schedule pages above: every section
   on the page, with a room size and denied requests made up from its SLN, and quiz sections with no one in them withdrawn,
   as the real summary marks them. Laid out like the real page: SLN, Course (two cells), Type, Title, Current Enrollment,
   Limit, Room Capacity, Space Available, Denied Requests, Notes. */
function summaryRows(tsHtml) {
  const out = [];
  for (const m of tsHtml.matchAll(/<A HREF=\/sln>(\d+)<\/A> (\w+) +(QZ|LB|SM|IS)?[^<\n]*?(\d+)\/ *(\d+)/g)) {
    const sln = +m[1], type = m[3] || 'LC', enrl = +m[4], lim = +m[5], quiz = type === 'QZ';
    out.push({ sln: String(sln), id: m[2], type, enrl, lim, room: lim + (sln % 4) * 10, withdrawn: quiz && enrl === 0,
      denied: quiz ? (sln % 3 === 0 ? 1 : 0) : sln % 5 + (enrl >= lim - 2 ? 5 : 0) });
  }
  return out;
}
function summaryPage(tsHtml, prefix, quarter) {
  const rows = summaryRows(tsHtml);
  return `<html><head><title>Enrollment Summary</title></head><body><h1>${quarter} Enrollment Summary</h1><h2>${prefix}</h2><ul><li>To display section details, click the Schedule Line Number (SLN)</li></ul>`
    + '<table border=1><tr><th>SLN</th><th colspan=2>Course</th><th>Type</th><th>Title</th><th>Current<br>Enrollment</th><th>Limit</th><th>Room<br>Capacity</th><th>Space<br>Available</th><th>Denied<br>Requests</th><th>Notes</th></tr>'
    + rows.map(r => `<tr><td><a href="/sln">${r.sln}</a></td><td>${prefix} 100</td><td>${r.id}</td><td>${r.type}</td><td>A TITLE</td><td>${r.withdrawn ? 0 : r.enrl}</td><td>${r.withdrawn ? '' : r.lim}</td><td>${r.room}</td><td>${r.withdrawn ? '' : Math.max(0, r.lim - r.enrl)}</td><td>${r.denied}</td><td>${r.withdrawn ? '**Section Withdrawn**' : ''}</td></tr>`).join('')
    + '</table></body></html>';
}
page.summary = { rows: summaryRows, page: summaryPage };
