# IP 스키마 — 348차원 (1챕터)

> 원작 소설 기반 IP 표준화 스키마. MVP 범위: 화전민 마을 + 주변 숲.
> 추후 IP 추가 시 동일한 구조를 따른다.

---

## 메타데이터

```json
{
  "ip_id": "dimension_348_v1",
  "title": "348차원",
  "version": "1.0",
  "genre": ["이세계", "헌터물", "중세판타지"],
  "user_entry_framing": "지구 멸망 생존자 — 이세계 전이자",
  "interface_system": true,
  "mvp_chapter": 1,
  "mvp_tick_range": "0 ~ 6",
  "mvp_sandbox": ["forest", "nameless_village"]
}
```

---

## 1. 세계관 물리법칙

```json
{
  "magic_system": {
    "type": "마나 + 서클 마법",
    "circles": [1, 2, 3, 4, "5+"],
    "description": "마나를 몸 안에 서클로 응축하여 마법 시전. 서클 수가 많을수록 고위 마법 가능.",
    "training_method": "심상공간(내면 세계) 수련"
  },
  "combat_system": {
    "tiers": ["일반인", "소드유저", "소드엑스퍼트", "소드마스터(오러소드)"],
    "description": "검술 수련으로 오러 각성. 오러소드는 마스터 경지 전유물."
  },
  "interface_system": {
    "exists_in_world": true,
    "visible_to": "지구인 생존자 전용",
    "components": ["레벨", "스탯", "스킬", "퀘스트", "칭호", "인도자"],
    "note": "348차원 원주민에게는 보이지 않음. 판정 결과를 인터페이스 알림으로 자연스럽게 출력 가능."
  },
  "stat_system": {
    "stats": ["근력", "민첩", "지구력", "마나", "맷집", "집중력", "근지구력"],
    "level_up_method": "전투(몬스터/인간 처치) 기반",
    "stat_up_method": "수련/행동 기반 (레벨과 별개 개념)"
  },
  "technology_level": "중세 (화약/총기 없음, 마법 존재, 영지제)",
  "communication": {
    "methods": [
      { "type": "직접 대화", "range": "근거리", "condition": "물리적 접촉 가능" },
      { "type": "전령", "range": "원거리", "delay": "1~7일 (거리 비례)" },
      { "type": "마법 통신", "range": "원거리", "condition": "고위 마법사, 관계 허용 시" },
      { "type": "인터페이스", "range": "무제한", "condition": "지구인 생존자 전용" },
      { "type": "심상공간", "range": "내면", "condition": "하준이 심상공간 진입 시 켄신과 소통" }
    ]
  }
}
```

---

## 2. 지역 데이터 (1챕터 샌드박스 범위)

```json
{
  "locations": [
    {
      "id": "forest",
      "name": "이름없는 숲",
      "type": "자연",
      "accessible": true,
      "description": "화전민 마을 주변 울창한 숲. 하운드 등 몬스터 출몰. 냇가 포함.",
      "adjacent": ["nameless_village"],
      "danger_level": "medium"
    },
    {
      "id": "nameless_village",
      "name": "이름없는 화전민 마을",
      "type": "은거지",
      "accessible": true,
      "description": "사연 있는 자들이 모여 사는 소규모 공동체. 헥터/조이 거주. 언덕 너머 로크빌 방향.",
      "adjacent": ["forest"],
      "danger_level": "low",
      "note": "헥터가 4년 전 정착 후 범죄자 소탕. 현재 치안 안정."
    }
  ],
  "out_of_bounds": [
    {
      "id": "rokville",
      "name": "로크빌",
      "distance": "도보 3일",
      "note": "1챕터 범위 외. 이동 시도 시 세계관 검증 에이전트가 제한."
    },
    {
      "id": "holy_capital",
      "name": "신성제국 수도",
      "distance": "수 주",
      "note": "1챕터 범위 외."
    }
  ]
}
```

---

## 3. 인물 데이터

### 3.1 하준 (주인공 / 유저 포지션)

```json
{
  "character_id": "hajun",
  "name": "하준",
  "tier": "protagonist",
  "origin": "지구 생존자 (한국, 23세)",
  "persona": {
    "motivation": "지구와 348차원을 구하는 계약 이행, 포식자 강림 저지",
    "values": ["의리", "침착함", "성장"],
    "background": "고아 출신, 은사(딸: 은혜)에게 키워짐. 취직 직전 지구 멸망 생존.",
    "speech_style": "현대적, 솔직함, 가끔 유머. 속마음은 인터페이스로 독백."
  },
  "stats_chapter1_start": {
    "level": 1, "근력": 12, "민첩": 14, "지구력": 14, "마나": 0, "서클": 0
  },
  "stats_chapter1_end": {
    "level": 3, "근력": 30, "민첩": 25, "지구력": 25, "마나": "초기", "서클": 1
  },
  "skills": [
    { "id": "interface_ex", "name": "권능-인터페이스(EX)", "grade": "EX", "desc": "레벨/스탯/퀘스트/칭호 시스템 사용 가능" },
    { "id": "indomitable_spirit", "name": "불굴의 정신(S)", "grade": "S", "desc": "정신계 마법 면역, 저주 면역, 극한 상황 침착" },
    { "id": "growth_blessing", "name": "성장의 축복(S)", "grade": "S", "desc": "수련 효과 상승" },
    { "id": "communication_blessing", "name": "소통의 축복(C)", "grade": "C", "desc": "언어 자동 습득" }
  ],
  "relations": {
    "kenshin": { "type": "인도자/스승", "level": 90, "note": "심상공간에서만 소통" },
    "joy_josephine": { "type": "보호 대상/동생같은 존재", "level": 80 },
    "hector": { "type": "은인/신뢰", "level": 75 },
    "matthew": { "type": "우호적 주민", "level": 60 }
  },
  "initial_state": {
    "location": "forest",
    "alive": true,
    "condition": "부상 (첫 진입 시)",
    "special": "인터페이스 보유, 인도자 오류 상태 (tick 5 이전)"
  }
}
```

### 3.2 켄신 (인도자)

```json
{
  "character_id": "kenshin",
  "name": "켄신",
  "title": "패배한 세계의 초월자",
  "tier": "primary",
  "origin": "불명 (다른 차원 패배 세계의 초월자)",
  "persona": {
    "motivation": "하준 성장 지원을 통한 포식자 저지",
    "values": ["실력주의", "냉철함", "성장"],
    "speech_style": "오만함, 반말, 무심한 독설. 인정할 땐 나지막하게.",
    "example_lines": [
      "- 네가는 반말이고, 꼬맹아. 인도자님이시다. -",
      "- 방심은 실전에서 바로 죽음으로 이어지지. -",
      "그래도 어느정도 쓸 만해졌군."
    ]
  },
  "combat_ability": "초월자급. 하준 스탯 올라갈수록 맞춰 수준 상승.",
  "location": "심상공간 (하준 내면)",
  "activation_condition": "하준이 심상공간 진입 시 또는 위기 상황 자동 개입 (tick 5~)",
  "initial_state": {
    "alive": true,
    "accessible": false,
    "error_state": true,
    "note": "tick 5 이전: 인터페이스에 오류로 표기. tick 5: 슈네드 전투 위기에서 자동 각성."
  }
}
```

### 3.3 조이 (조세핀 폰 아시오네)

```json
{
  "character_id": "joy_josephine",
  "name": "조이 / 조세핀 폰 아시오네",
  "tier": "primary",
  "origin": "신성제국 황녀 (4황녀)",
  "age": 16,
  "persona": {
    "motivation": "신분 숨기고 생존. 수도 귀환 목표 (tick 6 이후).",
    "values": ["은혜", "신뢰", "용기"],
    "background": "4년 전 황실 내부 사정으로 헥터와 도주. 이름없는 마을에서 은거.",
    "speech_style": "밝고 활발. 예절 배어있음. 헥터 앞에서 강단있음.",
    "example_lines": [
      "도망치세요!",
      "헥터 아저씨! 보고만 있지 말고 어서 도와주세요!",
      "제 이름은 조이가 아닌 조세핀이에요."
    ]
  },
  "secret": "신성제국 4황녀 조세핀. 1황자의 여동생. tick 6에 정체 공개.",
  "relations": {
    "hector": { "type": "보호자/아버지 같은 존재", "level": 95 },
    "hajun": { "type": "은인/오빠", "level": 80 },
    "first_prince": { "type": "오빠 (1황자)", "level": 70, "note": "하준을 죽은 줄 알고 있음" }
  },
  "initial_state": {
    "location": "forest",
    "alive": true,
    "accessible": true,
    "identity_hidden": true,
    "note": "tick 2에 숲에서 하운드에게 쫓기다 하준과 조우."
  }
}
```

### 3.4 헥터

```json
{
  "character_id": "hector",
  "name": "헥터",
  "alias": "철사자",
  "tier": "primary",
  "origin": "신성제국 출신 전직 최상급 소드 엑스퍼트",
  "persona": {
    "motivation": "조이 보호. 과거와 단절한 조용한 삶.",
    "values": ["책임감", "의리", "단순함"],
    "background": "한때 '철사자'로 이름 날린 최상급 소드 엑스퍼트. 조이를 데리고 도주 후 마을 정착. 이름 버림.",
    "speech_style": "호탕하고 여유로움. 조이 앞에서만 한없이 약해짐.",
    "example_lines": [
      "늙고 약한 놈이로군. 무리에서 배제되어 떠돌다 온 모양이야.",
      "철사자라…그 이름은 버린지 오래다. 지금은 그저 헥터다.",
      "조촐하지? 그래도 사람사는 곳이니."
    ]
  },
  "combat_ability": "소드마스터급 (오러소드 사용 가능)",
  "stats": {
    "combat": 95,
    "perception": 75,
    "charisma": 70,
    "stealth": 40
  },
  "relations": {
    "joy_josephine": { "type": "피보호자/딸 같은 존재", "level": 95 },
    "hajun": { "type": "인정하는 젊은이", "level": 75 },
    "shuned": { "type": "강한 적대", "level": 5 },
    "matthew": { "type": "우호적 동료", "level": 70 }
  },
  "initial_state": {
    "location": "nameless_village",
    "alive": true,
    "accessible": true,
    "note": "순찰 중 조이 위기 신호로 숲 진입. tick 3에 합류."
  }
}
```

### 3.5 슈네드

```json
{
  "character_id": "shuned",
  "name": "슈네드",
  "tier": "secondary",
  "origin": "신성제국 기사",
  "persona": {
    "motivation": "조세핀 황녀 포획 및 황실 귀환 명령 수행",
    "values": ["충성", "명예", "집념"],
    "speech_style": "성마름, 분노 조절 어려움. 헥터에 대한 강한 적개심.",
    "example_lines": [
      "헥터! 헥터! 헥터!",
      "그나저나 거기 계신건 조세핀 황녀님이 맞으십니까?"
    ]
  },
  "combat_ability": "소드 엑스퍼트 이상",
  "stats": {
    "combat": 75,
    "perception": 65,
    "charisma": 40,
    "stealth": 50
  },
  "relations": {
    "hector": { "type": "강한 적대", "level": 5 },
    "joy_josephine": { "type": "추격 대상", "level": 10 }
  },
  "initial_state": {
    "location": "unknown",
    "alive": true,
    "accessible": false,
    "state": "조이/헥터 추격 중",
    "activation_tick": 5,
    "note": "tick 5에 마을 인근 접근. 켄신 각성 트리거."
  }
}
```

### 3.6 매튜

```json
{
  "character_id": "matthew",
  "name": "매튜",
  "tier": "tertiary",
  "origin": "화전민 마을 주민",
  "persona": {
    "motivation": "마을 평화 유지",
    "values": ["소박함", "공동체"],
    "speech_style": "편안하고 솔직함. 뻐드렁니가 특징.",
    "example_lines": [
      "언덕너머에서 내려오는걸 보니 로크빌에서 오는모양이지?",
      "이 마을에 사연 없는 사람이 어디 있겠는가."
    ]
  },
  "stats": {
    "combat": 30,
    "perception": 50,
    "charisma": 60,
    "stealth": 35
  },
  "initial_state": {
    "location": "nameless_village",
    "alive": true,
    "accessible": true
  }
}
```

---

## 4. 캐논 이벤트 타임라인 (1챕터)

```json
{
  "timeline_id": "canon_348_ch1",
  "events": [
    {
      "event_id": "earth_destruction",
      "tick": 0,
      "location": "void",
      "name": "지구 멸망 & 경계의 신과 계약",
      "description": "포식자 차원 충돌로 지구 파괴. 경계의 신이 1294명 생존자에게 권능 분배 후 소멸.",
      "importance": "critical",
      "divergence_possible": false,
      "involved_characters": ["hajun"],
      "canon_outcome": "하준 348차원 전이, 인터페이스 부여"
    },
    {
      "event_id": "forest_awakening",
      "tick": 1,
      "location": "forest",
      "name": "숲에서 깨어남 & 인터페이스 첫 확인",
      "description": "하준이 숲 공터에서 깨어나 인터페이스를 처음 확인. 인도자는 오류 상태.",
      "importance": "high",
      "divergence_possible": true,
      "involved_characters": ["hajun"],
      "canon_outcome": "냇가 방향으로 이동 시작",
      "divergence_options": [
        "숲 깊이 들어간다 → Macro 스킵 후 마을 방향 재유도",
        "그 자리에서 기다린다 → 시간 경과, 몬스터 조우 위험"
      ]
    },
    {
      "event_id": "hound_encounter",
      "tick": 2,
      "location": "forest",
      "name": "조이와 하운드 조우",
      "description": "냇가에서 하운드에게 쫓기는 조이와 조우. 하준이 방패막이 역할.",
      "importance": "high",
      "divergence_possible": true,
      "involved_characters": ["hajun", "joy_josephine"],
      "canon_outcome": "하준이 조이를 먼저 도망치게 하고 하운드와 대치",
      "divergence_options": [
        "조이를 무시하고 도망친다 → 조이 사망 위험, 퀘스트 실패",
        "하운드를 단독으로 처치한다 → DC 70 판정 (저레벨엔 거의 불가)",
        "조이에게 먼저 도망치라 한다 → 캐논 진행"
      ]
    },
    {
      "event_id": "hector_arrival",
      "tick": 3,
      "location": "forest",
      "name": "헥터 합류 & 하운드 처치",
      "description": "조이가 헥터를 데리고 복귀. 헥터가 하운드 처치. 화전민 마을로 이동.",
      "importance": "high",
      "divergence_possible": true,
      "involved_characters": ["hajun", "joy_josephine", "hector"],
      "canon_outcome": "하운드 처치, 마을 도착, 헥터/조이의 호의 획득",
      "divergence_options": [
        "헥터 도착 전 하운드 대실패 → 하준 중상, 헥터가 구출하지만 신뢰도 하락",
        "마을 동행 거부 → 단독 행동 루트 (정보 없이 고난도)"
      ]
    },
    {
      "event_id": "village_daily_life",
      "tick": 4,
      "location": "nameless_village",
      "name": "마을 정착 & 일상 퀘스트",
      "description": "상처 치료, 매튜와 대화, 헥터의 부탁 수행. 세계관 파악 기간.",
      "importance": "medium",
      "divergence_possible": true,
      "involved_characters": ["hajun", "hector", "joy_josephine", "matthew"],
      "canon_outcome": "마을 정착. 인터페이스 시스템 파악. 레벨 2~3 달성.",
      "divergence_options": [
        "마을을 이탈한다 → 세계관 검증 에이전트가 제한 (장비/체력 부족)",
        "헥터에게 진실을 말한다 → 반응 분기 발생"
      ]
    },
    {
      "event_id": "kenshin_awakening",
      "tick": 5,
      "location": "nameless_village",
      "name": "켄신 각성 & 슈네드 등장",
      "description": "슈네드가 마을에 접근. 위기 상황에서 켄신이 인도자로 자동 각성. 첫 전투 지원.",
      "importance": "critical",
      "divergence_possible": true,
      "involved_characters": ["hajun", "kenshin", "hector", "shuned"],
      "canon_outcome": "켄신 각성, 소드엑스퍼트 격파, 칭호 <소드엑스퍼트를 쓰러트린 초보자> 획득",
      "divergence_options": [
        "슈네드와 대화로 해결한다 → 설득 판정 (DC 80, 매우 어려움)",
        "헥터에게 전부 맡긴다 → 헥터 단독 처리, 켄신 각성 지연",
        "켄신 도움으로 처치 → 캐논 진행"
      ]
    },
    {
      "event_id": "joy_identity_reveal",
      "tick": 6,
      "location": "nameless_village",
      "name": "조이 정체 공개 (1챕터 엔딩)",
      "description": "슈네드 사건 후 조이가 신성제국 황녀 조세핀임을 밝힘. 수도 귀환 계획 언급.",
      "importance": "critical",
      "divergence_possible": true,
      "involved_characters": ["hajun", "joy_josephine", "hector"],
      "canon_outcome": "하준이 조이의 정체를 알게 됨. 2챕터 수도 여정 복선.",
      "divergence_options": [
        "조이의 정체에 무관심하게 반응 → 관계도 소폭 하락",
        "신성제국 수배를 이유로 동행 거부 → 단독 루트 분기",
        "동행 결정 → 캐논 진행, 2챕터 개방"
      ]
    }
  ]
}
```

---

## 5. 세계관 검증 규칙

### 금지 행동

```json
[
  { "action": "화약/총기 사용", "reason": "이 세계에 존재하지 않는 기술 수준" },
  { "action": "전기/현대 기기 사용", "reason": "현대 기술 부재" },
  { "action": "인터페이스를 타인에게 공개", "reason": "타인에게 보이지 않는 지구인 전용 시스템" },
  { "action": "1챕터 범위 외 지역 즉시 이동", "reason": "거리/장비/체력 제한" },
  { "action": "서클 초과 마법 사용", "reason": "현재 서클 수 초과 불가" }
]
```

### 가능 행동 (예시)

```json
[
  "마나 마법 (보유 서클 범위 내)",
  "검술/근접전 (숙련도 범위 내)",
  "인터페이스 활용 (퀘스트/스탯 확인)",
  "심상공간 진입 (켄신과 수련, tick 5 이후)",
  "NPC 설득/거래/협박/전투",
  "마을 내 자유 이동",
  "숲 탐색 (몬스터 조우 위험)"
]
```

### 스탯 → DC 매핑

| 행동 유형 | 관련 스탯 |
|---|---|
| 전투 | 근력, 민첩, 집중력 vs 상대 combat/defense |
| 잠입/은신 | 민첩, 집중력 vs 상대 perception |
| 설득/협상 | 칭호, 관계도, 상황 보정 |
| 마법 시전 | 마나, 서클, 집중력 |
| 도주 | 민첩, 지구력 vs 상대 민첩 |

---

## 6. 근접 에이전트 활성화 맵 (1챕터)

| tick | 유저 위치 | 활성화 에이전트 | 비활성 |
|---|---|---|---|
| 0~1 | forest | hajun (단독) | 전체 |
| 2 | forest | joy_josephine | hector, shuned |
| 3 | forest → village | hector, joy_josephine | shuned, matthew |
| 4 | nameless_village | hector, joy_josephine, matthew | shuned |
| 5 | nameless_village | hector, joy_josephine, kenshin, **shuned** | matthew |
| 6 | nameless_village | hector, joy_josephine | shuned (처리됨) |

---

## 7. RAG 인덱싱 단위

| 청크 타입 | 내용 | 주요 검색 키 |
|---|---|---|
| `character` | 인물 페르소나, 관계, 상태 | character_id, faction, location |
| `event_canon` | 캐논 이벤트 | tick, importance, location |
| `event_dynamic` | 분기 이후 발생 이벤트 | session_id, branch_id, tick |
| `relation` | 인물 간 관계 | character_a, character_b |
| `world_rule` | 세계관 물리법칙, 마법 체계 | category |
| `location` | 지역 정보, 인접 지역, 이동 거리 | location_id |
| `interface_log` | 인터페이스 알림 기록 | tick, character_id |
