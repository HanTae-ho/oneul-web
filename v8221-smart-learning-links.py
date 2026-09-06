from pathlib import Path

p=Path('learning-data.js')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    s=s.replace(old,new,1)

once('/* 오늘 한 걸음 — 회복학습 데이터 V8.2.13','/* 오늘 한 걸음 — 회복학습 데이터 V8.2.21','learning data version')
once('"longDescription": "사용자가 번역한 SMART Recovery 핸드북의 4-Point Program과 도구 체계를 바탕으로 모바일 학습용으로 요약·재구성했습니다. 네 가지 Point는 순서대로 끝내는 단계가 아니라, 지금 필요한 영역의 도구를 골라 반복해서 사용하는 회복의 틀입니다.",','"longDescription": "SMART Recovery 핸드북의 4-Point Program과 도구 체계를 바탕으로 모바일 학습용으로 요약·재구성했습니다. 네 가지 Point는 순서대로 끝내는 단계가 아니라, 지금 필요한 영역의 도구를 골라 반복해서 사용하는 회복의 틀입니다.",','SMART long description')
once('"sourceNote": "사용자 번역 SMART Recovery 핸드북 기반 — 앱용 요약·재구성",','"sourceNote": "SMART Recovery 핸드북 기반 — 앱용 요약·재구성",','SMART source note')

old='''        "actions": [
          {
            "type": "smart-abc",
            "label": "ABC 문제 해결 작성하기"
          }
        ]
      },
      {
        "id": "smart-point4",'''
new='''        "actions": [
          {
            "type": "smart-abc",
            "label": "ABC 문제 해결 작성하기"
          },
          {
            "type": "smart-dibs",
            "label": "DIBS 생각 반박하기"
          },
          {
            "type": "smart-thinking-styles",
            "label": "도움이 되지 않는 사고방식 점검하기"
          },
          {
            "type": "smart-problem-solving",
            "label": "문제 해결 · 5단계 작성하기"
          }
        ]
      },
      {
        "id": "smart-point4",'''
once(old,new,'Point 3 actions')

old='''        "practice": "이번 주에 삶의 균형을 위해 늘리고 싶은 활동 하나와 줄이고 싶은 활동 하나를 정해보세요."
      }
    ]
  }
];'''
new='''        "practice": "이번 주에 삶의 균형을 위해 늘리고 싶은 활동 하나와 줄이고 싶은 활동 하나를 정해보세요.",
        "actions": [
          {
            "type": "smart-balance-pie",
            "label": "라이프스타일 밸런스 파이 작성하기"
          }
        ]
      }
    ]
  }
];'''
once(old,new,'Point 4 action')

for token in ['"type": "smart-abc"','"type": "smart-dibs"','"type": "smart-thinking-styles"','"type": "smart-problem-solving"','"type": "smart-balance-pie"']:
    if token not in s:
        raise SystemExit(f'missing action token: {token}')

p.write_text(s,encoding='utf-8')
