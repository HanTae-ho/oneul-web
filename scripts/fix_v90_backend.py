from pathlib import Path
p=Path('social-apps-script.gs')
s=p.read_text(encoding='utf-8')
old="""  const sh = sheet_(SOCIAL_SHEETS.profiles), data = rows_(SOCIAL_SHEETS.profiles);\n  const found = data.find(r => str_(r.userId) === userId);\n  const now = Date.now(), hash = hash_(token);\n"""
new="""  const sh = sheet_(SOCIAL_SHEETS.profiles), data = rows_(SOCIAL_SHEETS.profiles);\n  const found = data.find(r => str_(r.userId) === userId);\n  const sameNick = data.find(r => str_(r.status) === 'active' && str_(r.userId) !== userId && str_(r.nickname).toLowerCase() === nickname.toLowerCase());\n  if(sameNick) return {ok:false,error:'NICK_TAKEN',message:'이미 사용 중인 닉네임입니다.'};\n  const now = Date.now(), hash = hash_(token);\n"""
if s.count(old)!=1: raise SystemExit('profile anchor mismatch')
p.write_text(s.replace(old,new,1),encoding='utf-8')
