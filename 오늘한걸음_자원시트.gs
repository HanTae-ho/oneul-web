/**
 * 오늘 한 걸음 — 자원 목록 서버
 *
 * 이 스크립트가 하는 일은 하나뿐이다.
 * 스프레드시트에 적어둔 자조모임·센터·병원·상담전화 목록을 JSON 으로 내어준다.
 *
 * ★ 절대 하지 않는 것 ★
 *   회복 기록(감정·충동·재발·HALT)은 이곳으로 오지 않는다. 받지도 않는다.
 *   그것들은 각자의 휴대폰 안에만 있다.
 *   그래서 이 웹앱 주소가 남에게 알려져도 새어나갈 개인정보가 없다.
 *
 * 쓰는 법
 *   1. 구글 스프레드시트를 하나 만든다
 *   2. 확장 프로그램 → Apps Script → 이 파일을 통째로 붙여넣는다
 *   3. SHEET_ID 를 그 시트 주소의 /d/ 와 /edit 사이 글자로 바꾼다
 *   4. 편집기에서 MAKE_SHEETS 를 한 번 실행한다 (탭 네 개와 제목줄이 만들어진다)
 *   5. 배포 → 새 배포 → 웹 앱
 *        실행 사용자: 나
 *        액세스 권한: 모든 사용자
 *      → 나오는 주소를 앱의 [내 정보 → 자원 목록]에 붙여넣는다
 *
 * ★ 고칠 때 조심할 것 ★
 *   두 번째부터는 '새 배포'를 누르지 마라. 주소가 바뀌어 모든 기기가 멈춘다.
 *   배포 → 배포 관리 → 연필(편집) → 버전: 새 버전 → 배포   ○
 *   배포 → 새 배포                                        ✗
 */

const SHEET_ID = '여기에_스프레드시트_ID를_넣으세요';

/* 탭 이름과 열 구성 */
const TABS = {
  lines:   { title: '상담전화', cols: ['n', 't', 'd', 'u'] },
  groups:  { title: '자조모임', cols: ['n', 'd', 'w'] },
  centers: { title: '중독센터', cols: ['n', 'd', 'w'] },
  hosp:    { title: '전문병원', cols: ['n', 'd', 'w'] }
};

/* 열 뜻
     n  이름          예) 자살예방 상담전화 / AA 광주모임 / 다사랑병원
     t  전화번호      예) 109        (상담전화 탭에만 있음)
     d  한 줄 설명    예) 24시간 · 무료
     w  링크 주소     예) https://...   (지도 링크를 넣어도 된다)
     u  급함 표시     1 을 적으면 앱에서 빨간 카드로 크게 보인다 (상담전화 탭에만)
*/

function doGet() {
  const out = {};
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    Object.keys(TABS).forEach(function (key) {
      out[key] = readTab_(ss, key);
    });
    out.ok = true;
  } catch (e) {
    out.ok = false;
    out.error = String(e);
  }
  return ContentService
    .createTextOutput(JSON.stringify(out))
    .setMimeType(ContentService.MimeType.JSON);
}

function readTab_(ss, key) {
  const sh = ss.getSheetByName(TABS[key].title);
  if (!sh) return [];
  const v = sh.getDataRange().getValues();
  if (v.length < 2) return [];

  const head = v[0].map(function (x) { return String(x).trim(); });
  const rows = [];

  for (let i = 1; i < v.length; i++) {
    const row = {};
    let any = false;
    TABS[key].cols.forEach(function (c) {
      const j = head.indexOf(c);
      if (j < 0) return;
      const val = String(v[i][j] == null ? '' : v[i][j]).trim();
      if (val) { row[c] = (c === 'u') ? 1 : val; any = true; }
    });
    if (any && row.n) rows.push(row);
  }
  return rows;
}

/** 시트 네 개와 제목줄을 만들어 준다. 처음 한 번만 실행하면 된다. */
function MAKE_SHEETS() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  Object.keys(TABS).forEach(function (key) {
    const t = TABS[key];
    let sh = ss.getSheetByName(t.title);
    if (!sh) sh = ss.insertSheet(t.title);
    if (sh.getLastRow() === 0) {
      sh.getRange(1, 1, 1, t.cols.length).setValues([t.cols]).setFontWeight('bold');
      sh.setFrozenRows(1);
    }
  });

  /* 상담전화 탭이 비어 있으면 기본값을 넣어둔다 */
  const sh = ss.getSheetByName(TABS.lines.title);
  if (sh.getLastRow() <= 1) {
    sh.getRange(2, 1, 6, 4).setValues([
      ['자살예방 상담전화', '109',        '24시간 · 무료 · 죽고 싶은 마음이 들 때', 1],
      ['응급 신고',        '119',        '손떨림·경련·환각 등 금단 증상이 있을 때', 1],
      ['정신건강 상담전화', '1577-0199',  '24시간 · 지역 정신건강복지센터 연결',   ''],
      ['도박문제 헬프라인', '1336',       '24시간 · 한국도박문제예방치유원',       ''],
      ['보건복지상담센터',  '129',        '복지·의료 서비스 안내',                 ''],
      ['마약류 중독 상담',  '1899-0893',  '식약처 · 상담 및 치료 연계 안내',       '']
    ]);
  }
  SpreadsheetApp.getUi().alert('시트를 준비했습니다. 이제 목록을 채워넣으세요.');
}

/** 지금 무엇이 나가고 있는지 확인용. 편집기에서 실행하고 실행 기록을 본다. */
function SHOW_OUTPUT() {
  Logger.log(doGet().getContent());
}
