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
