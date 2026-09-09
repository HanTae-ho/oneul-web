from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Version — tolerate spacing around the assignment.
s,n=re.subn(r"const\s+BUILD\s*=\s*'V8\.2\.68'", "const BUILD='V8.2.69'", s, count=1)
if not n:
    assert re.search(r"const\s+BUILD\s*=\s*'V8\.2\.69'",s), 'BUILD anchor'

# SMART Recovery — insert immediately after NA in the existing GROUPS array.
if '한국 SMART Recovery' not in s:
    pat=re.compile(r"(\{n:'NA 익명의 약물중독자들',\s*d:'약물 · 지역별 모임 일정',\s*w:'https://nakr\.org/'\},)")
    s,n=pat.subn(r"\1\n  {n:'한국 SMART Recovery', d:'CBT 접근과 자기관리 기술을 활용하는 회복 자조모임',\n   w:'https://smartkr.org/'},",s,count=1)
    assert n==1, 'NA GROUPS entry not found'

# Reclaimed-summary accordion styling.
if '.reclaim-acc .acc-b' not in s:
    anchor='  .reclaim-wrap{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:15px;margin-bottom:14px}\n'
    assert anchor in s, 'reclaim CSS not found'
    s=s.replace(anchor,anchor+'  .reclaim-acc .acc-b{padding:2px 12px 12px}\n  .reclaim-acc .reclaim-wrap{border:0;margin:0;padding:0}\n',1)

if 'function reclaimToggle(btn)' not in s:
    anchor='function drawReclaim(){'
    assert anchor in s
    helper="""function reclaimToggle(btn){
  const acc=btn&&btn.closest?btn.closest('.acc'):null;
  if(!acc) return;
  const open=!acc.classList.contains('on');
  acc.classList.toggle('on',open);
  btn.setAttribute('aria-expanded',open?'true':'false');
}
"""
    s=s.replace(anchor,helper+anchor,1)

# Replace only drawReclaim's generated markup; all calculations above it remain untouched.
f0=s.index('function drawReclaim(){')
f1=s.index('function openReclaimSettings(){',f0)
chunk=s[f0:f1]
if 'class="acc reclaim-acc"' not in chunk:
    a0=chunk.index('  box.innerHTML=')
    a1=chunk.index("  const b=$('#rec-reclaim-settings')",a0)
    new_assign="""  const reclaimSummary=(type?('회복 '+dayValue):'회복일 설정 필요')+' · 회복 실천 '+habits+'회';
  box.innerHTML='<div class="acc reclaim-acc"><button class="acc-h" type="button" aria-expanded="false" onclick="reclaimToggle(this)"><span class="acc-n"><b>내가 되찾은 것</b><span>'+esc(reclaimSummary)+' · 눌러서 자세히 보기</span></span><svg class="acc-v" viewBox="0 0 24 24"><path d="M6.5 9.5l5.5 5.5 5.5-5.5"/></svg></button><div class="acc-b"><div class="reclaim-wrap"><div class="reclaim-head"><div><b>회복하면서 되찾은 것</b><span>손실이 아니라 회복하면서 내 삶에 다시 남은 것을 봅니다.</span></div><button type="button" class="reclaim-set" id="rec-reclaim-settings">기준 설정</button></div><div class="reclaim-grid">'+
    card('cal','회복일',dayValue,dayDesc,'',!type)+
    card('clock','되찾은 시간',timeValue,timeDesc,'',!timeReady)+
    card('wallet','지킨 비용',costValue,costDesc,'',gambling||!costReady)+
    card('sprout','회복 실천',habits+'회','내가 실천하고 기록한 회복 행동','habit',false)+
    '</div></div></div></div>';
"""
    chunk=chunk[:a0]+new_assign+chunk[a1:]
    s=s[:f0]+chunk+s[f1:]

# Locate balanced accordion blocks inside the general-user '나' page.
sec0=s.index('<section class="pg" id="p-my">')
sec1=s.index('</section>',sec0)+len('</section>')
sec=s[sec0:sec1]

def acc_block(text,label):
    target=text.index('<b>'+label+'</b>')
    start=text.rfind('<div class="acc">',0,target)
    assert start>=0, label+' accordion start'
    token=re.compile(r'<div\b[^>]*>|</div>')
    depth=0
    for m in token.finditer(text,start):
        if m.group(0).startswith('</div'):
            depth-=1
            if depth==0:
                return start,m.end(),text[start:m.end()]
        else:
            depth+=1
    raise AssertionError(label+' accordion end')

if '<b>관리자</b>' in sec or sec.index('<b>앱에 바라는 점</b>') < sec.index('<b>지원 및 안내</b>'):
    fs,fe,feedback=acc_block(sec,'앱에 바라는 점')
    ss,se,support=acc_block(sec,'지원 및 안내')
    ranges=[(fs,fe),(ss,se)]
    if '<b>관리자</b>' in sec:
        ads,ade,admin=acc_block(sec,'관리자')
        ranges.append((ads,ade))
    base=sec
    for a,b in sorted(ranges,reverse=True):
        base=base[:a]+base[b:]
    insert=base.rfind('</section>')
    sec=base[:insert].rstrip()+'\n\n'+support+'\n\n'+feedback+'\n'+base[insert:]
    s=s[:sec0]+sec+s[sec1:]

# The dormant admin engine remains, but drawAdmin must tolerate the removed user card.
old="const b = $('#me-admin'); b.innerHTML = '';\n  $('#tab-admin').classList.add('hide');"
if old in s:
    s=s.replace(old,"const b = $('#me-admin');\n  $('#tab-admin').classList.add('hide');\n  if(!b) return;\n  b.innerHTML = '';",1)
assert "const b = $('#me-admin');\n  $('#tab-admin').classList.add('hide');\n  if(!b) return;" in s
s=s.replace('/* 관리자 화면은 내 정보에서만 엽니다. 하단 탭에는 표시하지 않습니다. */','/* 관리자 엔진은 유지하지만 일반 사용자 메뉴와 하단 탭에는 표시하지 않습니다. */',1)

# User-facing guide/manual alignment.
old_order='당사자 모드의 <b>나</b> 화면에는 위에서부터 <b>내가 되찾은 것 → 내 발자취 → 내 정보 · 설정 → 앱에 바라는 점 → 지원 및 안내 → 관리자</b>가 배치됩니다. 가족·보호자 모드에서는 당사자의 회복성과를 대신 계산하지 않도록 <b>내가 되찾은 것</b>은 표시하지 않습니다.'
new_order='당사자 모드의 <b>나</b> 화면에는 위에서부터 <b>내가 되찾은 것 → 내 발자취 → 내 정보 · 설정 → 지원 및 안내 → 앱에 바라는 점</b>이 배치됩니다. <b>내가 되찾은 것</b>은 기본적으로 접혀 있어 내 발자취와 설정이 바로 보이며, 필요할 때 눌러 자세히 펼칩니다. 가족·보호자 모드에서는 당사자의 회복성과를 대신 계산하지 않도록 표시하지 않습니다.'
if old_order in s:
    s=s.replace(old_order,new_order,1)
s=s.replace('      <p style="margin-top:8px">관리자는 일반 사용 기능과 분리되어 있으며 기존 관리자 접근 방식은 그대로 유지됩니다.</p>\n','',1)

old='당사자 모드에서는 <b>나</b> 화면 상단의 <b>내가 되찾은 것</b>에서 회복일·되찾은 시간·지킨 비용·회복 실천을 한눈에 볼 수 있습니다.'
if old in s:
    s=s.replace(old,'당사자 모드에서는 <b>나</b> 화면 상단의 접힌 <b>내가 되찾은 것</b>을 눌러 회복일·되찾은 시간·지킨 비용·회복 실천을 한눈에 볼 수 있습니다.',1)
old='당사자 모드에서는 나 화면 상단의 <b>내가 되찾은 것</b>에서 회복일·되찾은 시간·지킨 비용·회복 실천을 확인하고, <b>나 → 내 발자취</b>에서 저장한 기록과 변화 흐름을 확인합니다.'
if old in s:
    s=s.replace(old,'당사자 모드에서는 나 화면 상단의 접힌 <b>내가 되찾은 것</b>을 필요할 때 펼쳐 회복일·되찾은 시간·지킨 비용·회복 실천을 확인하고, <b>나 → 내 발자취</b>에서 저장한 기록과 변화 흐름을 확인합니다.',1)
old='<p style="margin-top:8px"><b>앱에 바라는 점 · 지원 및 안내 · 관리자</b>는 <b>내 정보 · 설정</b> 안이 아니라 <b>나</b> 화면에서 바로 이용합니다. 관리자 기능의 기존 접근 방식은 그대로 유지됩니다.</p>'
if old in s:
    s=s.replace(old,'<p style="margin-top:8px"><b>지원 및 안내</b>와 <b>앱에 바라는 점</b>은 <b>내 정보 · 설정</b> 안이 아니라 <b>나</b> 화면에서 바로 이용하며, 앱에 바라는 점은 지원 및 안내 아래에 배치됩니다.</p>',1)

# Structural checks before saving index.
sec0=s.index('<section class="pg" id="p-my">'); sec1=s.index('</section>',sec0); sec=s[sec0:sec1]
assert '<b>관리자</b>' not in sec
assert sec.index('<b>내 발자취</b>') < sec.index('<b>내 정보 · 설정</b>') < sec.index('<b>지원 및 안내</b>') < sec.index('<b>앱에 바라는 점</b>')
assert '한국 SMART Recovery' in s and 'https://smartkr.org/' in s
p.write_text(s,encoding='utf-8')

# Service worker/version surfaces.
p=Path('sw.js'); s=p.read_text(encoding='utf-8')
s=s.replace("const APP_VERSION = 'V8.2.68';","const APP_VERSION = 'V8.2.69';",1)
s=s.replace("const V = 'ohg-v8268-reminder-music-audited';","const V = 'ohg-v8269-me-smart';",1)
assert "const APP_VERSION = 'V8.2.69';" in s and 'ohg-v8269-me-smart' in s
p.write_text(s,encoding='utf-8')

for name in ('privacy.html','legal.html'):
    p=Path(name); s=p.read_text(encoding='utf-8')
    s=s.replace('<span class="ver">V8.2.68</span>','<span class="ver">V8.2.69</span>',1)
    assert '<span class="ver">V8.2.69</span>' in s
    p.write_text(s,encoding='utf-8')

p=Path('README.md'); s=p.read_text(encoding='utf-8')
if '## V8.2.69 — 나 화면 단순화 · 한국 SMART Recovery 연결' not in s:
    marker='## V8.2.68'
    assert marker in s
    note="""## V8.2.69 — 나 화면 단순화 · 한국 SMART Recovery 연결
- `나` 화면의 `내가 되찾은 것`을 기본 접힘 요약으로 바꿔 `내 발자취`와 `내 정보 · 설정`이 바로 보이도록 정리했습니다. 상세 회복일·되찾은 시간·지킨 비용·회복 실천 계산은 그대로 유지합니다.
- `지원 및 안내`를 `앱에 바라는 점`보다 먼저 배치하고, 일반 사용자 화면의 `관리자` 진입 카드는 제거했습니다. 내부 관리자 엔진은 삭제하지 않아 운영 기능에는 영향을 주지 않습니다.
- `자조모임 찾기 → 단체 공식 안내`에 `한국 SMART Recovery`를 추가하고 한국 사이트(https://smartkr.org/)로 연결합니다. 설명은 `CBT 접근과 자기관리 기술을 활용하는 회복 자조모임`으로 표시합니다.
- `DATA_SCHEMA=6`, 저장키 `ohg.v1`, 회복기록 구조, V8.2.68의 알림 동기화, Android 정확알림·화면 OFF·부팅 재예약·복약/외래/생활/습관 알림·마음프로 TTS·이완 TTS 엔진은 변경하지 않습니다.

"""
    s=s.replace(marker,note+marker,1)
p.write_text(s,encoding='utf-8')
