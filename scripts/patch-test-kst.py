from pathlib import Path

p=Path('test.js')
s=p.read_text(encoding='utf-8')
old="""  const localYmd = d => {
    const z = n => String(n).padStart(2, '0');
    return d.getFullYear() + '-' + z(d.getMonth()+1) + '-' + z(d.getDate());
  };
  const daysAgo = n => {
    const d = new Date();
    d.setHours(12, 0, 0, 0);
    d.setDate(d.getDate() - n);
    return localYmd(d);
  };"""
new="""  // CI runner의 시스템 시간대(UTC)와 관계없이 앱과 같은 Asia/Seoul 날짜를 사용합니다.
  const kstYmd = d => {
    const parts = new Intl.DateTimeFormat('en-CA', {
      timeZone:'Asia/Seoul', year:'numeric', month:'2-digit', day:'2-digit'
    }).formatToParts(d);
    const v = Object.fromEntries(parts.map(x => [x.type, x.value]));
    return v.year + '-' + v.month + '-' + v.day;
  };
  const daysAgo = n => {
    const todayKst = kstYmd(new Date());
    const [y,m,d] = todayKst.split('-').map(Number);
    const x = new Date(Date.UTC(y, m-1, d));
    x.setUTCDate(x.getUTCDate() - n);
    const z = v => String(v).padStart(2, '0');
    return x.getUTCFullYear() + '-' + z(x.getUTCMonth()+1) + '-' + z(x.getUTCDate());
  };"""
if old not in s:
    raise SystemExit('stale local date helper not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('test.js KST date helper PASS')
