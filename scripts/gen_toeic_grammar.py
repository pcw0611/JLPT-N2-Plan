import json, sys

sys.stdout.reconfigure(encoding='utf-8')

items = [
    # ===== 1. Parts of Speech (품사 구분) — 30 items =====
    {"Word": "명사 vs 동사 어형 구분 (-tion/-ment)", "PartOfSpeech": "grammar", "Meaning": "명사 접미사 -tion, -ment, -ness, -ity 등으로 품사를 구분한다", "Example": "The implementation of the new policy requires board approval.", "ExampleKo": "새 정책의 시행은 이사회 승인이 필요하다.", "Tier": "문법"},
    {"Word": "형용사 자리: be동사/감각동사 + 형용사", "PartOfSpeech": "grammar", "Meaning": "be동사, look, seem, remain 뒤에는 형용사가 온다 (부사 X)", "Example": "The quarterly results look promising for investors.", "ExampleKo": "분기 실적이 투자자들에게 유망해 보인다.", "Tier": "문법"},
    {"Word": "부사 자리: 동사/형용사/부사 수식", "PartOfSpeech": "grammar", "Meaning": "동사, 형용사, 다른 부사를 수식할 때 부사를 쓴다", "Example": "Sales have increased significantly over the past quarter.", "ExampleKo": "매출이 지난 분기 동안 크게 증가했다.", "Tier": "문법"},
    {"Word": "-ly 형용사 vs -ly 부사 혼동", "PartOfSpeech": "grammar", "Meaning": "friendly, costly, timely 등은 -ly이지만 형용사이다", "Example": "The manager provided timely feedback on the proposal.", "ExampleKo": "관리자가 제안서에 대해 시기적절한 피드백을 제공했다.", "Tier": "문법"},
    {"Word": "명사 자리: 관사/소유격 + ___ + 동사", "PartOfSpeech": "grammar", "Meaning": "관사(a/the)나 소유격(his/our) 뒤, 동사 앞은 명사 자리이다", "Example": "Our participation in the trade fair boosted brand awareness.", "ExampleKo": "무역 박람회 참가가 브랜드 인지도를 높였다.", "Tier": "문법"},
    {"Word": "-ive / -ous / -al / -ful → 형용사 접미사", "PartOfSpeech": "grammar", "Meaning": "-ive, -ous, -al, -ful은 형용사를 만드는 접미사이다", "Example": "The innovative design attracted many potential customers.", "ExampleKo": "혁신적인 디자인이 많은 잠재 고객을 끌어들였다.", "Tier": "문법"},
    {"Word": "-ize / -ify / -en → 동사 접미사", "PartOfSpeech": "grammar", "Meaning": "-ize, -ify, -en은 동사를 만드는 접미사이다", "Example": "The company plans to modernize its manufacturing facilities.", "ExampleKo": "회사는 제조 시설을 현대화할 계획이다.", "Tier": "문법"},
    {"Word": "명사 + 명사 복합어 (compound nouns)", "PartOfSpeech": "grammar", "Meaning": "명사가 명사를 수식할 때 앞의 명사는 단수형을 쓴다", "Example": "Please submit the expense report by Friday.", "ExampleKo": "금요일까지 경비 보고서를 제출해 주세요.", "Tier": "문법"},
    {"Word": "형용사 vs 부사 선택: 동사 + 목적어 + ___", "PartOfSpeech": "grammar", "Meaning": "동사를 수식하면 부사, 보어 역할이면 형용사를 쓴다", "Example": "The technician carefully inspected the equipment.", "ExampleKo": "기술자가 장비를 주의 깊게 점검했다.", "Tier": "문법"},
    {"Word": "-ness / -ity → 추상 명사 접미사", "PartOfSpeech": "grammar", "Meaning": "-ness, -ity는 형용사에서 추상 명사를 만든다", "Example": "The effectiveness of the training program was evaluated.", "ExampleKo": "교육 프로그램의 효과가 평가되었다.", "Tier": "문법"},
    {"Word": "consider / find / make + 목적어 + 형용사 (목적보어)", "PartOfSpeech": "grammar", "Meaning": "consider, find, make 등은 목적어 뒤에 형용사 보어를 취한다", "Example": "The committee found the proposal acceptable.", "ExampleKo": "위원회는 그 제안을 수용 가능하다고 판단했다.", "Tier": "문법"},
    {"Word": "enough + 명사 / 형용사 + enough", "PartOfSpeech": "grammar", "Meaning": "enough는 명사 앞, 형용사·부사 뒤에 위치한다", "Example": "We have enough resources to complete the project on time.", "ExampleKo": "프로젝트를 제때 완료할 충분한 자원이 있다.", "Tier": "문법"},
    {"Word": "수량 형용사: many/much/few/little 가산·불가산 구분", "PartOfSpeech": "grammar", "Meaning": "many/few는 가산, much/little은 불가산 명사에 쓴다", "Example": "There is little information available about the merger.", "ExampleKo": "합병에 대해 이용 가능한 정보가 거의 없다.", "Tier": "문법"},
    {"Word": "-able / -ible → '~할 수 있는' 형용사", "PartOfSpeech": "grammar", "Meaning": "-able/-ible은 '가능한'을 뜻하는 형용사를 만든다", "Example": "All conference rooms are accessible to employees with disabilities.", "ExampleKo": "모든 회의실은 장애가 있는 직원도 이용할 수 있다.", "Tier": "문법"},
    {"Word": "동사 자리 확인: 주어 + ___ (동사 필요)", "PartOfSpeech": "grammar", "Meaning": "주어 뒤에 동사가 없으면 문장이 성립하지 않는다", "Example": "The marketing team develops strategies for new product launches.", "ExampleKo": "마케팅 팀은 신제품 출시 전략을 개발한다.", "Tier": "문법"},
    {"Word": "-ment / -tion / -ance / -ence → 명사 접미사", "PartOfSpeech": "grammar", "Meaning": "동사에 -ment, -tion, -ance, -ence를 붙여 명사를 만든다", "Example": "Employee attendance at the workshop is mandatory.", "ExampleKo": "직원의 워크숍 참석은 의무이다.", "Tier": "문법"},
    {"Word": "형용사 자리: 명사 앞 수식 (attributive)", "PartOfSpeech": "grammar", "Meaning": "명사 바로 앞에서 수식하는 위치에는 형용사가 온다", "Example": "The annual conference will be held in November.", "ExampleKo": "연례 회의가 11월에 개최될 것이다.", "Tier": "문법"},
    {"Word": "복합 형용사 (hyphenated adjective)", "PartOfSpeech": "grammar", "Meaning": "두 단어 이상이 명사 앞에서 수식할 때 하이픈으로 연결한다", "Example": "This is a well-known brand in the electronics industry.", "ExampleKo": "이것은 전자 산업에서 잘 알려진 브랜드이다.", "Tier": "문법"},
    {"Word": "명사 뒤치 수식: 형용사구/분사구/전치사구", "PartOfSpeech": "grammar", "Meaning": "형용사구, 분사구, 전치사구는 명사 뒤에서 수식한다", "Example": "Candidates interested in the position should apply online.", "ExampleKo": "해당 직위에 관심 있는 지원자는 온라인으로 지원해야 한다.", "Tier": "문법"},
    {"Word": "so + 형용사/부사, such + (a) + 명사", "PartOfSpeech": "grammar", "Meaning": "so는 형용사·부사 앞, such는 명사(구) 앞에 쓴다", "Example": "It was such a successful event that we plan to repeat it.", "ExampleKo": "너무 성공적인 행사여서 다시 개최할 계획이다.", "Tier": "문법"},
    {"Word": "no vs not 구분", "PartOfSpeech": "grammar", "Meaning": "no + 명사, not + 동사/형용사/부사로 부정을 나타낸다", "Example": "There are no vacancies in the accounting department.", "ExampleKo": "회계 부서에 빈자리가 없다.", "Tier": "문법"},
    {"Word": "almost / nearly + 형용사·부사·동사 수식", "PartOfSpeech": "grammar", "Meaning": "almost, nearly는 부사로서 형용사·동사 등을 수식한다", "Example": "The project is almost complete and ready for review.", "ExampleKo": "프로젝트가 거의 완료되어 검토 준비가 되었다.", "Tier": "문법"},
    {"Word": "even / still + 비교급 강조", "PartOfSpeech": "grammar", "Meaning": "even, still, much, far, a lot은 비교급을 강조한다", "Example": "The revised estimate is even higher than the original one.", "ExampleKo": "수정된 견적이 원래 것보다 훨씬 더 높다.", "Tier": "문법"},
    {"Word": "complete(형) vs completely(부) 품사 구분", "PartOfSpeech": "grammar", "Meaning": "complete는 형용사(완전한), completely는 부사(완전히)이다", "Example": "The renovation has been completely finished ahead of schedule.", "ExampleKo": "보수 공사가 일정보다 앞서 완전히 끝났다.", "Tier": "문법"},
    {"Word": "economy / economic / economical / economically", "PartOfSpeech": "grammar", "Meaning": "economy(경제/명사), economic(경제의), economical(절약적인), economically(경제적으로)", "Example": "The economic outlook for the region remains positive.", "ExampleKo": "그 지역의 경제 전망은 여전히 긍정적이다.", "Tier": "문법"},
    {"Word": "success / successful / successfully / succeed", "PartOfSpeech": "grammar", "Meaning": "success(성공/명사), successful(성공적인), successfully(성공적으로), succeed(성공하다)", "Example": "The product launch was successfully carried out last month.", "ExampleKo": "제품 출시가 지난달 성공적으로 진행되었다.", "Tier": "문법"},
    {"Word": "주격 보어 자리: S + V + ___ (형용사/명사)", "PartOfSpeech": "grammar", "Meaning": "become, remain, appear 등의 보어로 형용사나 명사를 쓴다", "Example": "The CEO remained confident about the company's growth.", "ExampleKo": "CEO는 회사의 성장에 대해 자신감을 유지했다.", "Tier": "문법"},
    {"Word": "depend / dependable / dependent / dependence", "PartOfSpeech": "grammar", "Meaning": "depend(의존하다), dependable(믿을 만한), dependent(의존적인), dependence(의존)", "Example": "Our company's dependence on a single supplier is risky.", "ExampleKo": "우리 회사가 단일 공급업체에 의존하는 것은 위험하다.", "Tier": "문법"},
    {"Word": "접미사 -ward(s): 방향 부사", "PartOfSpeech": "grammar", "Meaning": "-ward(s)는 '~쪽으로'라는 방향 부사를 만든다 (forward, afterward)", "Example": "Going forward, all invoices must be submitted electronically.", "ExampleKo": "앞으로 모든 청구서는 전자적으로 제출해야 한다.", "Tier": "문법"},
    {"Word": "접두사 의미 구분 (un-/re-/pre-/over-)", "PartOfSpeech": "grammar", "Meaning": "un-(부정), re-(다시), pre-(미리), over-(과도)로 의미가 변한다", "Example": "The contract was renegotiated to include better terms.", "ExampleKo": "더 나은 조건을 포함하도록 계약이 재협상되었다.", "Tier": "문법"},

    # ===== 2. Verb Tenses (시제) — 20 items =====
    {"Word": "현재 시제: 일반적 사실·반복 행위", "PartOfSpeech": "grammar", "Meaning": "습관, 사실, 규칙적 일정을 나타낼 때 현재 시제를 쓴다", "Example": "The store opens at 9 a.m. every weekday.", "ExampleKo": "가게는 평일 매일 오전 9시에 문을 연다.", "Tier": "문법"},
    {"Word": "현재 진행: be + -ing (진행 중)", "PartOfSpeech": "grammar", "Meaning": "지금 진행 중이거나 일시적 상황을 나타낸다", "Example": "The IT team is currently upgrading the server.", "ExampleKo": "IT 팀이 현재 서버를 업그레이드하고 있다.", "Tier": "문법"},
    {"Word": "과거 시제: 과거의 완료된 동작", "PartOfSpeech": "grammar", "Meaning": "과거에 시작되어 끝난 동작에 과거 시제를 쓴다", "Example": "The company relocated its headquarters last year.", "ExampleKo": "회사는 작년에 본사를 이전했다.", "Tier": "문법"},
    {"Word": "현재완료: have/has + p.p. (과거~현재)", "PartOfSpeech": "grammar", "Meaning": "과거에 시작되어 현재까지 관련되는 동작·상태에 쓴다", "Example": "We have received numerous inquiries about the new product.", "ExampleKo": "우리는 신제품에 대해 수많은 문의를 받아왔다.", "Tier": "문법"},
    {"Word": "현재완료 + since / for 구분", "PartOfSpeech": "grammar", "Meaning": "since + 시점(since 2020), for + 기간(for three years)과 함께 쓴다", "Example": "Ms. Park has worked here since 2018.", "ExampleKo": "박 씨는 2018년부터 여기서 근무해 왔다.", "Tier": "문법"},
    {"Word": "현재완료 + recently / already / yet / just", "PartOfSpeech": "grammar", "Meaning": "recently, already, yet, just는 현재완료와 자주 쓰인다", "Example": "The shipment has already been dispatched to the warehouse.", "ExampleKo": "화물은 이미 창고로 발송되었다.", "Tier": "문법"},
    {"Word": "과거완료: had + p.p. (과거보다 이전)", "PartOfSpeech": "grammar", "Meaning": "과거의 한 시점보다 더 이전에 완료된 동작을 나타낸다", "Example": "By the time the manager arrived, the meeting had already started.", "ExampleKo": "관리자가 도착했을 때, 회의는 이미 시작되어 있었다.", "Tier": "문법"},
    {"Word": "미래 시제: will + 동사원형", "PartOfSpeech": "grammar", "Meaning": "미래의 예정·의지·예측을 나타낸다", "Example": "The new branch will open in March.", "ExampleKo": "새 지점은 3월에 개장할 것이다.", "Tier": "문법"},
    {"Word": "be going to + 동사원형 (계획된 미래)", "PartOfSpeech": "grammar", "Meaning": "이미 결정된 계획이나 의도를 나타낸다", "Example": "The company is going to launch a new marketing campaign.", "ExampleKo": "회사는 새 마케팅 캠페인을 시작할 예정이다.", "Tier": "문법"},
    {"Word": "미래완료: will have + p.p.", "PartOfSpeech": "grammar", "Meaning": "미래의 특정 시점까지 완료될 동작을 나타낸다", "Example": "By next Friday, we will have completed the audit.", "ExampleKo": "다음 주 금요일까지 감사를 완료할 것이다.", "Tier": "문법"},
    {"Word": "시간 부사절에서 현재 시제 (미래 대용)", "PartOfSpeech": "grammar", "Meaning": "when, before, after, until, once 절에서는 미래 대신 현재 시제를 쓴다", "Example": "Once the contract is signed, production will begin immediately.", "ExampleKo": "계약이 체결되면, 생산이 즉시 시작될 것이다.", "Tier": "문법"},
    {"Word": "과거 진행: was/were + -ing", "PartOfSpeech": "grammar", "Meaning": "과거의 특정 시점에 진행 중이던 동작을 나타낸다", "Example": "The team was reviewing the budget when the director called.", "ExampleKo": "이사가 전화했을 때 팀은 예산을 검토하고 있었다.", "Tier": "문법"},
    {"Word": "현재완료 진행: have been + -ing", "PartOfSpeech": "grammar", "Meaning": "과거부터 현재까지 계속 진행 중인 동작을 강조한다", "Example": "The engineers have been working on the prototype for months.", "ExampleKo": "엔지니어들이 수개월간 시제품 작업을 해오고 있다.", "Tier": "문법"},
    {"Word": "시제 일치: 주절 과거 → 종속절 과거/과거완료", "PartOfSpeech": "grammar", "Meaning": "주절이 과거이면 종속절도 과거나 과거완료를 쓴다", "Example": "The manager said that the deadline had been extended.", "ExampleKo": "관리자는 마감일이 연장되었다고 말했다.", "Tier": "문법"},
    {"Word": "used to + 동사원형 (과거 습관)", "PartOfSpeech": "grammar", "Meaning": "과거에 했지만 지금은 안 하는 습관·상태를 나타낸다", "Example": "The company used to manufacture parts domestically.", "ExampleKo": "회사는 예전에 부품을 국내에서 제조했었다.", "Tier": "문법"},
    {"Word": "be used to + -ing (현재 익숙함)", "PartOfSpeech": "grammar", "Meaning": "'~에 익숙하다'는 뜻으로 be used to + 동명사를 쓴다", "Example": "She is used to handling multiple tasks simultaneously.", "ExampleKo": "그녀는 여러 업무를 동시에 처리하는 데 익숙하다.", "Tier": "문법"},
    {"Word": "would + 동사원형 (과거의 반복 동작)", "PartOfSpeech": "grammar", "Meaning": "과거에 반복적으로 했던 동작을 나타낸다", "Example": "The founder would visit every branch office each quarter.", "ExampleKo": "설립자는 매 분기마다 각 지사를 방문하곤 했다.", "Tier": "문법"},
    {"Word": "현재완료 vs 과거 시제 선택", "PartOfSpeech": "grammar", "Meaning": "명확한 과거 시점(yesterday, last year)이 있으면 과거, 없으면 현재완료를 쓴다", "Example": "I submitted the report yesterday. / I have submitted the report.", "ExampleKo": "나는 어제 보고서를 제출했다. / 나는 보고서를 제출했다(완료).", "Tier": "문법"},
    {"Word": "be about to + 동사원형 (곧 ~하려는)", "PartOfSpeech": "grammar", "Meaning": "바로 직전에 일어나려는 동작을 나타낸다", "Example": "The presentation is about to begin, so please take your seats.", "ExampleKo": "발표가 곧 시작되니 자리에 앉아 주세요.", "Tier": "문법"},
    {"Word": "be to + 동사원형 (예정·의무)", "PartOfSpeech": "grammar", "Meaning": "공식 일정이나 의무를 나타낼 때 쓴다", "Example": "The delegation is to arrive at the airport at noon.", "ExampleKo": "대표단은 정오에 공항에 도착할 예정이다.", "Tier": "문법"},

    # ===== 3. Subject-Verb Agreement (주어-동사 일치) — 15 items =====
    {"Word": "every / each + 단수 동사", "PartOfSpeech": "grammar", "Meaning": "every, each 뒤의 명사는 단수 취급하여 단수 동사를 쓴다", "Example": "Every employee is required to attend the safety training.", "ExampleKo": "모든 직원은 안전 교육에 참석해야 한다.", "Tier": "문법"},
    {"Word": "주어 + 전치사구 + 동사: 전치사구 무시", "PartOfSpeech": "grammar", "Meaning": "주어와 동사 사이의 전치사구는 수 일치에 영향을 주지 않는다", "Example": "The list of candidates has been narrowed down.", "ExampleKo": "후보자 명단이 좁혀졌다.", "Tier": "문법"},
    {"Word": "either A or B / neither A nor B → B에 일치", "PartOfSpeech": "grammar", "Meaning": "either...or, neither...nor에서 동사는 B(가까운 주어)에 일치한다", "Example": "Neither the manager nor the employees were informed.", "ExampleKo": "관리자도 직원들도 통보받지 못했다.", "Tier": "문법"},
    {"Word": "불가산 명사 + 단수 동사", "PartOfSpeech": "grammar", "Meaning": "information, equipment, furniture 등은 단수 취급한다", "Example": "The equipment was delivered to the construction site.", "ExampleKo": "장비가 건설 현장에 배달되었다.", "Tier": "문법"},
    {"Word": "the number of + 복수명사 + 단수 동사", "PartOfSpeech": "grammar", "Meaning": "the number of는 '~의 수'이므로 단수 동사를 쓴다", "Example": "The number of applicants has increased this year.", "ExampleKo": "지원자 수가 올해 증가했다.", "Tier": "문법"},
    {"Word": "a number of + 복수명사 + 복수 동사", "PartOfSpeech": "grammar", "Meaning": "a number of는 '많은'이라는 뜻이므로 복수 동사를 쓴다", "Example": "A number of employees have volunteered for the project.", "ExampleKo": "많은 직원이 그 프로젝트에 자원했다.", "Tier": "문법"},
    {"Word": "동명사/to부정사 주어 + 단수 동사", "PartOfSpeech": "grammar", "Meaning": "동명사구나 to부정사구가 주어이면 단수 동사를 쓴다", "Example": "Reducing costs is a top priority for this fiscal year.", "ExampleKo": "비용 절감이 이번 회계연도의 최우선 과제이다.", "Tier": "문법"},
    {"Word": "both A and B + 복수 동사", "PartOfSpeech": "grammar", "Meaning": "both A and B는 항상 복수 취급한다", "Example": "Both the CEO and the CFO are attending the summit.", "ExampleKo": "CEO와 CFO 모두 정상회의에 참석한다.", "Tier": "문법"},
    {"Word": "집합 명사 (staff, committee) 수 일치", "PartOfSpeech": "grammar", "Meaning": "집합 명사는 하나의 단위면 단수, 개별 구성원이면 복수 취급한다", "Example": "The committee has reached a unanimous decision.", "ExampleKo": "위원회가 만장일치 결정에 도달했다.", "Tier": "문법"},
    {"Word": "There is/are 구문: 뒤의 명사에 일치", "PartOfSpeech": "grammar", "Meaning": "There 구문에서 동사는 뒤에 오는 실제 주어의 수에 일치한다", "Example": "There are several issues that need to be addressed.", "ExampleKo": "해결해야 할 여러 문제가 있다.", "Tier": "문법"},
    {"Word": "one of the + 복수명사 + 단수 동사", "PartOfSpeech": "grammar", "Meaning": "one of the 다음에 복수명사가 오지만 주어는 one이므로 단수 동사를 쓴다", "Example": "One of the suppliers has failed to meet the deadline.", "ExampleKo": "공급업체 중 하나가 마감을 맞추지 못했다.", "Tier": "문법"},
    {"Word": "주어와 동사 사이 삽입절 무시", "PartOfSpeech": "grammar", "Meaning": "주어와 동사 사이의 삽입구(관계절 등)는 수 일치에 영향을 주지 않는다", "Example": "The report, along with the appendices, was submitted on time.", "ExampleKo": "보고서가 부록과 함께 제때 제출되었다.", "Tier": "문법"},
    {"Word": "복수형 고유명사/단체명 + 단수 동사", "PartOfSpeech": "grammar", "Meaning": "회사명, 국가명 등은 형태가 복수라도 단수 취급한다", "Example": "Global Industries has announced a new partnership.", "ExampleKo": "Global Industries가 새로운 파트너십을 발표했다.", "Tier": "문법"},
    {"Word": "금액/거리/시간 + 단수 동사", "PartOfSpeech": "grammar", "Meaning": "금액, 거리, 시간 등을 하나의 단위로 보면 단수 취급한다", "Example": "Five thousand dollars is the estimated cost of repairs.", "ExampleKo": "5천 달러가 수리 예상 비용이다.", "Tier": "문법"},
    {"Word": "what 절 주어의 수 일치", "PartOfSpeech": "grammar", "Meaning": "what 절이 주어일 때 보어의 수에 따라 단수/복수 동사를 쓴다", "Example": "What we need is a comprehensive marketing strategy.", "ExampleKo": "우리에게 필요한 것은 종합적인 마케팅 전략이다.", "Tier": "문법"},

    # ===== 4. Active/Passive Voice (능동/수동태) — 15 items =====
    {"Word": "수동태 기본: be + p.p.", "PartOfSpeech": "grammar", "Meaning": "주어가 동작을 받을 때 be + 과거분사를 쓴다", "Example": "All employees are required to wear identification badges.", "ExampleKo": "모든 직원은 신분증을 착용해야 한다.", "Tier": "문법"},
    {"Word": "수동태 + by + 행위자", "PartOfSpeech": "grammar", "Meaning": "행위자를 밝힐 때 by + 행위자를 추가한다", "Example": "The report was prepared by the accounting department.", "ExampleKo": "보고서는 회계 부서에 의해 작성되었다.", "Tier": "문법"},
    {"Word": "수동태 진행형: be being + p.p.", "PartOfSpeech": "grammar", "Meaning": "현재 진행 중인 수동을 나타낸다", "Example": "The building is being renovated to meet safety standards.", "ExampleKo": "건물이 안전 기준에 맞게 보수되고 있다.", "Tier": "문법"},
    {"Word": "수동태 완료형: have been + p.p.", "PartOfSpeech": "grammar", "Meaning": "완료된 수동을 나타낸다", "Example": "Several new policies have been implemented this quarter.", "ExampleKo": "이번 분기에 여러 새 정책이 시행되었다.", "Tier": "문법"},
    {"Word": "조동사 + be + p.p. (조동사 수동태)", "PartOfSpeech": "grammar", "Meaning": "can/will/should/must 등 조동사 뒤 수동은 be + p.p.이다", "Example": "The issue should be resolved before the end of the week.", "ExampleKo": "그 문제는 주말 전에 해결되어야 한다.", "Tier": "문법"},
    {"Word": "자동사는 수동태 불가", "PartOfSpeech": "grammar", "Meaning": "happen, occur, exist 등 자동사는 수동태로 쓸 수 없다", "Example": "The accident occurred during the night shift. (수동 불가)", "ExampleKo": "사고는 야간 근무 중에 발생했다.", "Tier": "문법"},
    {"Word": "4형식 수동태: 간접목적어/직접목적어 주어 전환", "PartOfSpeech": "grammar", "Meaning": "give, offer, send 등은 두 목적어 모두 수동태 주어가 될 수 있다", "Example": "All participants were given a certificate of completion.", "ExampleKo": "모든 참가자에게 수료증이 수여되었다.", "Tier": "문법"},
    {"Word": "5형식 수동태: be + p.p. + 목적보어", "PartOfSpeech": "grammar", "Meaning": "call, name, elect, consider 등의 수동태에서 보어가 남는다", "Example": "Mr. Lee was appointed team leader last month.", "ExampleKo": "이 씨가 지난달 팀장으로 임명되었다.", "Tier": "문법"},
    {"Word": "get + p.p. (구어적 수동태)", "PartOfSpeech": "grammar", "Meaning": "be 대신 get을 써서 수동을 나타낼 수 있다 (구어적)", "Example": "Several items got damaged during shipping.", "ExampleKo": "여러 물품이 배송 중에 파손되었다.", "Tier": "문법"},
    {"Word": "능동 vs 수동 선택 기준", "PartOfSpeech": "grammar", "Meaning": "주어가 동작의 주체면 능동, 대상이면 수동을 쓴다", "Example": "The company launched a new product. / A new product was launched.", "ExampleKo": "회사가 신제품을 출시했다. / 신제품이 출시되었다.", "Tier": "문법"},
    {"Word": "be supposed to + 동사원형 (~하기로 되어 있다)", "PartOfSpeech": "grammar", "Meaning": "예정·기대·의무를 나타내는 수동 표현이다", "Example": "The package is supposed to arrive by tomorrow.", "ExampleKo": "소포는 내일까지 도착하기로 되어 있다.", "Tier": "문법"},
    {"Word": "be expected to + 동사원형 (~할 것으로 예상되다)", "PartOfSpeech": "grammar", "Meaning": "예상·기대를 나타내는 수동 표현이다", "Example": "Revenue is expected to increase by 15 percent.", "ExampleKo": "수입이 15% 증가할 것으로 예상된다.", "Tier": "문법"},
    {"Word": "be required to + 동사원형 (~해야 한다)", "PartOfSpeech": "grammar", "Meaning": "의무·필수를 나타내는 수동 표현이다", "Example": "Visitors are required to sign in at the front desk.", "ExampleKo": "방문객은 안내 데스크에서 등록해야 한다.", "Tier": "문법"},
    {"Word": "be known for / be known as 구분", "PartOfSpeech": "grammar", "Meaning": "be known for + 이유(~로 유명한), be known as + 명칭(~로 알려진)", "Example": "The city is known for its vibrant tech industry.", "ExampleKo": "그 도시는 활기찬 기술 산업으로 유명하다.", "Tier": "문법"},
    {"Word": "be + p.p. vs be + 형용사 구분", "PartOfSpeech": "grammar", "Meaning": "같은 형태라도 동작이면 수동태, 상태이면 형용사 보어이다", "Example": "The door was closed at 6 p.m. (동작) / The door was closed. (상태)", "ExampleKo": "문이 오후 6시에 닫혔다. (동작) / 문이 닫혀 있었다. (상태)", "Tier": "문법"},

    # ===== 5. Gerunds vs Infinitives (동명사 vs 부정사) — 15 items =====
    {"Word": "동명사를 목적어로 취하는 동사 (enjoy, avoid, consider...)", "PartOfSpeech": "grammar", "Meaning": "enjoy, avoid, consider, mind, finish, suggest 등은 동명사를 목적어로 쓴다", "Example": "The board considered expanding into the Asian market.", "ExampleKo": "이사회는 아시아 시장 진출을 고려했다.", "Tier": "문법"},
    {"Word": "to부정사를 목적어로 취하는 동사 (want, plan, decide...)", "PartOfSpeech": "grammar", "Meaning": "want, plan, decide, agree, expect, hope 등은 to부정사를 목적어로 쓴다", "Example": "The firm decided to relocate its headquarters.", "ExampleKo": "회사는 본사를 이전하기로 결정했다.", "Tier": "문법"},
    {"Word": "동명사/to부정사 둘 다 가능 (뜻 같음): like, start, begin", "PartOfSpeech": "grammar", "Meaning": "like, love, hate, start, begin, continue는 둘 다 가능하며 의미 차이가 거의 없다", "Example": "He started reviewing / to review the contract.", "ExampleKo": "그는 계약서를 검토하기 시작했다.", "Tier": "문법"},
    {"Word": "stop + -ing vs stop + to부정사", "PartOfSpeech": "grammar", "Meaning": "stop -ing(~하던 것을 멈추다), stop to(~하기 위해 멈추다)", "Example": "He stopped checking his email to attend the meeting.", "ExampleKo": "그는 회의에 참석하기 위해 이메일 확인을 멈췄다.", "Tier": "문법"},
    {"Word": "remember/forget + -ing vs to부정사", "PartOfSpeech": "grammar", "Meaning": "remember -ing(과거에 한 것을 기억), remember to(앞으로 할 것을 기억)", "Example": "Please remember to submit the form before the deadline.", "ExampleKo": "마감 전에 양식을 제출하는 것을 기억해 주세요.", "Tier": "문법"},
    {"Word": "전치사 + 동명사 (-ing)", "PartOfSpeech": "grammar", "Meaning": "전치사 뒤에는 동명사(명사)를 쓴다 (to부정사 X)", "Example": "We look forward to hearing from you soon.", "ExampleKo": "곧 연락 주시기를 기대합니다.", "Tier": "문법"},
    {"Word": "to부정사의 부사적 용법 (목적)", "PartOfSpeech": "grammar", "Meaning": "to부정사로 '~하기 위해'라는 목적을 나타낸다", "Example": "She attended the seminar to learn about digital marketing.", "ExampleKo": "그녀는 디지털 마케팅에 대해 배우기 위해 세미나에 참석했다.", "Tier": "문법"},
    {"Word": "to부정사의 형용사적 용법 (명사 수식)", "PartOfSpeech": "grammar", "Meaning": "to부정사가 명사 뒤에서 수식하는 형용사 역할을 한다", "Example": "There are many issues to discuss at the next meeting.", "ExampleKo": "다음 회의에서 논의할 문제가 많다.", "Tier": "문법"},
    {"Word": "동명사의 주어 역할", "PartOfSpeech": "grammar", "Meaning": "동명사(구)가 문장의 주어로 쓰인다", "Example": "Attending the workshop is highly recommended for all staff.", "ExampleKo": "모든 직원에게 워크숍 참석이 강력히 권장된다.", "Tier": "문법"},
    {"Word": "it ... to부정사 가주어 구문", "PartOfSpeech": "grammar", "Meaning": "가주어 it을 쓰고 진주어 to부정사를 뒤에 둔다", "Example": "It is important to review the terms before signing.", "ExampleKo": "서명 전에 조건을 검토하는 것이 중요하다.", "Tier": "문법"},
    {"Word": "suggest / recommend + (that) + 주어 + 동사원형", "PartOfSpeech": "grammar", "Meaning": "suggest, recommend, insist 등 뒤의 that절에서 동사원형(가정법 현재)을 쓴다", "Example": "The consultant suggested that the company hire more analysts.", "ExampleKo": "컨설턴트는 회사가 분석가를 더 고용할 것을 제안했다.", "Tier": "문법"},
    {"Word": "allow / permit / enable + 목적어 + to부정사", "PartOfSpeech": "grammar", "Meaning": "allow, permit, enable은 목적어 + to부정사 구조를 취한다", "Example": "The software enables users to track their expenses easily.", "ExampleKo": "이 소프트웨어는 사용자가 경비를 쉽게 추적할 수 있게 한다.", "Tier": "문법"},
    {"Word": "spend + 시간/돈 + -ing", "PartOfSpeech": "grammar", "Meaning": "spend 뒤에 시간/돈 + 동명사 구조를 쓴다", "Example": "The team spent three weeks developing the prototype.", "ExampleKo": "팀은 시제품 개발에 3주를 보냈다.", "Tier": "문법"},
    {"Word": "be worth + -ing (~할 가치가 있다)", "PartOfSpeech": "grammar", "Meaning": "be worth 뒤에 동명사를 쓰며 수동 의미이다", "Example": "The conference is worth attending for networking opportunities.", "ExampleKo": "그 회의는 네트워킹 기회를 위해 참석할 가치가 있다.", "Tier": "문법"},
    {"Word": "have difficulty / trouble + -ing", "PartOfSpeech": "grammar", "Meaning": "have difficulty/trouble 뒤에 동명사를 쓴다 (to부정사 X)", "Example": "Some employees had difficulty adapting to the new system.", "ExampleKo": "일부 직원들은 새 시스템에 적응하는 데 어려움을 겪었다.", "Tier": "문법"},

    # ===== 6. Relative Clauses (관계절) — 15 items =====
    {"Word": "who: 사람 주격 관계대명사", "PartOfSpeech": "grammar", "Meaning": "선행사가 사람이고 관계절에서 주어 역할일 때 who를 쓴다", "Example": "Employees who complete the training will receive a certificate.", "ExampleKo": "교육을 이수한 직원은 수료증을 받는다.", "Tier": "문법"},
    {"Word": "whom: 사람 목적격 관계대명사", "PartOfSpeech": "grammar", "Meaning": "선행사가 사람이고 관계절에서 목적어 역할일 때 whom을 쓴다", "Example": "The applicant whom we interviewed was highly qualified.", "ExampleKo": "우리가 면접한 지원자는 매우 자격이 뛰어났다.", "Tier": "문법"},
    {"Word": "which: 사물 관계대명사", "PartOfSpeech": "grammar", "Meaning": "선행사가 사물·동물일 때 which를 쓴다", "Example": "The proposal, which was submitted last week, has been approved.", "ExampleKo": "지난주에 제출된 제안서가 승인되었다.", "Tier": "문법"},
    {"Word": "that: 제한적 관계대명사 (사람/사물)", "PartOfSpeech": "grammar", "Meaning": "제한적(한정적) 관계절에서 사람·사물 모두에 that을 쓸 수 있다", "Example": "The products that meet our standards will be shipped.", "ExampleKo": "기준을 충족하는 제품이 배송될 것이다.", "Tier": "문법"},
    {"Word": "whose: 소유격 관계대명사", "PartOfSpeech": "grammar", "Meaning": "선행사의 소유를 나타낼 때 whose를 쓴다 (사람·사물)", "Example": "The client whose order was delayed received a full refund.", "ExampleKo": "주문이 지연된 고객은 전액 환불을 받았다.", "Tier": "문법"},
    {"Word": "where: 장소 관계부사", "PartOfSpeech": "grammar", "Meaning": "선행사가 장소이고 관계절에서 부사 역할일 때 where를 쓴다", "Example": "This is the office where the marketing team works.", "ExampleKo": "여기가 마케팅 팀이 일하는 사무실이다.", "Tier": "문법"},
    {"Word": "when: 시간 관계부사", "PartOfSpeech": "grammar", "Meaning": "선행사가 시간이고 관계절에서 부사 역할일 때 when을 쓴다", "Example": "July is the month when most employees take vacations.", "ExampleKo": "7월은 대부분의 직원이 휴가를 가는 달이다.", "Tier": "문법"},
    {"Word": "계속적 용법: , which / , who (비제한적)", "PartOfSpeech": "grammar", "Meaning": "콤마 + which/who는 부가 정보를 제공하며 that으로 대체 불가", "Example": "Mr. Kim, who joined last year, has been promoted.", "ExampleKo": "작년에 입사한 김 씨가 승진했다.", "Tier": "문법"},
    {"Word": "전치사 + 관계대명사 (in which, for which)", "PartOfSpeech": "grammar", "Meaning": "전치사를 관계대명사 앞에 두는 격식체 표현이다", "Example": "The department in which she works is being restructured.", "ExampleKo": "그녀가 근무하는 부서가 구조조정되고 있다.", "Tier": "문법"},
    {"Word": "관계대명사 what (선행사 포함)", "PartOfSpeech": "grammar", "Meaning": "what은 선행사를 포함하여 'the thing(s) that'의 의미이다", "Example": "What the company needs is a stronger online presence.", "ExampleKo": "회사에 필요한 것은 더 강한 온라인 입지이다.", "Tier": "문법"},
    {"Word": "관계대명사 생략 (목적격)", "PartOfSpeech": "grammar", "Meaning": "목적격 관계대명사(whom, which, that)는 생략 가능하다", "Example": "The candidate (that) we selected starts next Monday.", "ExampleKo": "우리가 선발한 후보가 다음 주 월요일에 출근한다.", "Tier": "문법"},
    {"Word": "복합관계대명사: whoever / whichever / whatever", "PartOfSpeech": "grammar", "Meaning": "whoever(누구든), whichever(어느 것이든), whatever(무엇이든)", "Example": "Whoever finishes the task first will receive a bonus.", "ExampleKo": "과제를 먼저 끝내는 사람은 누구든 보너스를 받는다.", "Tier": "문법"},
    {"Word": "why: 이유 관계부사 (the reason why)", "PartOfSpeech": "grammar", "Meaning": "선행사가 the reason일 때 why를 쓴다 (생략 가능)", "Example": "That is the reason why the project was postponed.", "ExampleKo": "그것이 프로젝트가 연기된 이유이다.", "Tier": "문법"},
    {"Word": "관계절 내 주어-동사 일치", "PartOfSpeech": "grammar", "Meaning": "관계절 동사는 선행사의 수에 일치해야 한다", "Example": "Applicants who have experience in sales are preferred.", "ExampleKo": "영업 경험이 있는 지원자가 우대된다.", "Tier": "문법"},
    {"Word": "which로 앞 문장 전체 수식", "PartOfSpeech": "grammar", "Meaning": "콤마 + which가 앞 문장 전체를 선행사로 받을 수 있다", "Example": "Sales rose by 20%, which exceeded our expectations.", "ExampleKo": "매출이 20% 올랐는데, 이는 기대를 초과했다.", "Tier": "문법"},

    # ===== 7. Conditionals (조건문) — 10 items =====
    {"Word": "if + 현재, will + 동사원형 (1차 조건문)", "PartOfSpeech": "grammar", "Meaning": "실현 가능한 미래 조건을 나타낸다", "Example": "If you register by Friday, you will receive an early-bird discount.", "ExampleKo": "금요일까지 등록하면, 조기 등록 할인을 받을 것이다.", "Tier": "문법"},
    {"Word": "if + 과거, would + 동사원형 (2차 조건문)", "PartOfSpeech": "grammar", "Meaning": "현재 사실과 반대되는 가정을 나타낸다", "Example": "If we had a larger budget, we would expand overseas.", "ExampleKo": "예산이 더 크면, 해외로 확장할 텐데.", "Tier": "문법"},
    {"Word": "if + had p.p., would have p.p. (3차 조건문)", "PartOfSpeech": "grammar", "Meaning": "과거 사실과 반대되는 가정을 나타낸다", "Example": "If we had started earlier, we would have met the deadline.", "ExampleKo": "더 일찍 시작했더라면, 마감을 맞추었을 텐데.", "Tier": "문법"},
    {"Word": "unless = if ... not (만약 ~하지 않으면)", "PartOfSpeech": "grammar", "Meaning": "unless는 '~하지 않는 한'이라는 부정 조건을 나타낸다", "Example": "Unless the payment is received, the order will be canceled.", "ExampleKo": "결제가 접수되지 않으면, 주문이 취소될 것이다.", "Tier": "문법"},
    {"Word": "provided (that) / providing (that)", "PartOfSpeech": "grammar", "Meaning": "'~한다는 조건으로'라는 뜻의 조건 접속사이다", "Example": "You may work remotely, provided that you meet all deadlines.", "ExampleKo": "모든 마감을 지킨다는 조건으로 원격 근무가 가능하다.", "Tier": "문법"},
    {"Word": "as long as (~하는 한)", "PartOfSpeech": "grammar", "Meaning": "'~하는 동안/한'이라는 조건을 나타낸다", "Example": "As long as the quality standards are met, the supplier will be retained.", "ExampleKo": "품질 기준이 충족되는 한, 공급업체는 유지될 것이다.", "Tier": "문법"},
    {"Word": "in case (of) + 명사/절 (~에 대비하여)", "PartOfSpeech": "grammar", "Meaning": "'~할 경우에 대비하여'라는 뜻이다", "Example": "Bring an umbrella in case it rains during the outdoor event.", "ExampleKo": "야외 행사 중 비가 올 경우를 대비해 우산을 가져가세요.", "Tier": "문법"},
    {"Word": "otherwise (그렇지 않으면)", "PartOfSpeech": "grammar", "Meaning": "앞 문장의 조건이 아니면 어떤 결과가 생긴다는 뜻이다", "Example": "Submit the application today; otherwise, you may miss the deadline.", "ExampleKo": "오늘 지원서를 제출하세요; 그렇지 않으면 마감을 놓칠 수 있다.", "Tier": "문법"},
    {"Word": "even if vs even though 구분", "PartOfSpeech": "grammar", "Meaning": "even if(설사 ~하더라도/가정), even though(~에도 불구하고/사실)", "Example": "Even if the price increases, demand is likely to remain strong.", "ExampleKo": "가격이 올라도, 수요는 강세를 유지할 가능성이 높다.", "Tier": "문법"},
    {"Word": "should 도치 조건문 (격식체 if 대체)", "PartOfSpeech": "grammar", "Meaning": "격식체에서 If S should → Should S 도치로 쓸 수 있다", "Example": "Should you have any questions, please contact our helpdesk.", "ExampleKo": "질문이 있으시면, 헬프데스크로 연락해 주세요.", "Tier": "문법"},

    # ===== 8. Prepositions (전치사) — 25 items =====
    {"Word": "by + 기한 (~까지)", "PartOfSpeech": "grammar", "Meaning": "기한·마감을 나타낼 때 by를 쓴다 ('~까지')", "Example": "Please submit the report by the end of the month.", "ExampleKo": "월말까지 보고서를 제출해 주세요.", "Tier": "문법"},
    {"Word": "until + 시점 (~까지 계속)", "PartOfSpeech": "grammar", "Meaning": "어떤 시점까지 계속되는 동작에 until을 쓴다", "Example": "The office will remain open until 8 p.m. during the sale.", "ExampleKo": "세일 기간에는 사무실이 오후 8시까지 열려 있을 것이다.", "Tier": "문법"},
    {"Word": "by vs until 구분", "PartOfSpeech": "grammar", "Meaning": "by는 기한(완료), until은 계속(지속)을 나타낸다", "Example": "Finish the task by 5 p.m. / Wait until 5 p.m.", "ExampleKo": "오후 5시까지 과제를 끝내세요. / 오후 5시까지 기다리세요.", "Tier": "문법"},
    {"Word": "during + 명사 (~동안)", "PartOfSpeech": "grammar", "Meaning": "특정 기간 동안을 나타낼 때 during + 명사를 쓴다", "Example": "Sales increased significantly during the holiday season.", "ExampleKo": "매출이 연휴 기간 동안 크게 증가했다.", "Tier": "문법"},
    {"Word": "for + 기간 (~동안)", "PartOfSpeech": "grammar", "Meaning": "기간의 길이를 나타낼 때 for + 숫자/기간을 쓴다", "Example": "The warranty is valid for two years from the date of purchase.", "ExampleKo": "보증은 구매일로부터 2년간 유효하다.", "Tier": "문법"},
    {"Word": "in + 시간 (~후에 / ~안에)", "PartOfSpeech": "grammar", "Meaning": "미래의 시점('~후에') 또는 기간 이내를 나타낸다", "Example": "The package will arrive in three business days.", "ExampleKo": "소포는 영업일 기준 3일 후에 도착할 것이다.", "Tier": "문법"},
    {"Word": "on + 날짜/요일, in + 월/년, at + 시각", "PartOfSpeech": "grammar", "Meaning": "on은 날짜·요일, in은 월·계절·년, at은 시각과 쓴다", "Example": "The meeting is scheduled on Monday at 10 a.m. in January.", "ExampleKo": "회의는 1월 월요일 오전 10시에 예정되어 있다.", "Tier": "문법"},
    {"Word": "in charge of (~을 담당하여)", "PartOfSpeech": "grammar", "Meaning": "'~을 담당하다/책임지다'라는 뜻의 전치사구이다", "Example": "Ms. Chen is in charge of the customer service department.", "ExampleKo": "Chen 씨가 고객 서비스 부서를 담당하고 있다.", "Tier": "문법"},
    {"Word": "in addition to (~에 더하여)", "PartOfSpeech": "grammar", "Meaning": "'~에 더하여, 게다가'라는 뜻이며 뒤에 명사/동명사가 온다", "Example": "In addition to the salary, the position offers health benefits.", "ExampleKo": "급여에 더하여, 이 직위는 건강 보험 혜택을 제공한다.", "Tier": "문법"},
    {"Word": "in accordance with (~에 따라서)", "PartOfSpeech": "grammar", "Meaning": "규정·법률 등에 따라서라는 뜻이다", "Example": "All procedures must be followed in accordance with company policy.", "ExampleKo": "모든 절차는 회사 방침에 따라 준수해야 한다.", "Tier": "문법"},
    {"Word": "due to / because of + 명사 (~때문에)", "PartOfSpeech": "grammar", "Meaning": "이유를 나타내는 전치사구이며 뒤에 명사(구)가 온다", "Example": "The flight was delayed due to severe weather conditions.", "ExampleKo": "항공편이 악천후로 인해 지연되었다.", "Tier": "문법"},
    {"Word": "instead of + 명사/동명사 (~대신에)", "PartOfSpeech": "grammar", "Meaning": "'~대신에'라는 뜻이며 뒤에 명사나 동명사가 온다", "Example": "We chose to videoconference instead of traveling to the client.", "ExampleKo": "고객에게 출장 가는 대신 화상회의를 선택했다.", "Tier": "문법"},
    {"Word": "prior to + 명사/동명사 (~이전에)", "PartOfSpeech": "grammar", "Meaning": "'~이전에'라는 뜻의 격식체 전치사이다", "Example": "Prior to the merger, both companies operated independently.", "ExampleKo": "합병 이전에, 두 회사는 독립적으로 운영되었다.", "Tier": "문법"},
    {"Word": "regardless of + 명사 (~에 관계없이)", "PartOfSpeech": "grammar", "Meaning": "'~에 관계없이, 상관없이'라는 뜻이다", "Example": "All applicants are welcome regardless of experience level.", "ExampleKo": "경험 수준에 관계없이 모든 지원자를 환영한다.", "Tier": "문법"},
    {"Word": "with regard to / regarding (~에 관하여)", "PartOfSpeech": "grammar", "Meaning": "'~에 관하여'라는 뜻으로 비즈니스 서신에서 자주 쓴다", "Example": "I am writing with regard to the invoice dated March 5.", "ExampleKo": "3월 5일자 청구서에 관하여 편지를 드립니다.", "Tier": "문법"},
    {"Word": "on behalf of (~을 대신하여/~을 대표하여)", "PartOfSpeech": "grammar", "Meaning": "'~을 대신/대표하여'라는 뜻이다", "Example": "On behalf of the team, I would like to thank you.", "ExampleKo": "팀을 대표하여, 감사 인사를 드립니다.", "Tier": "문법"},
    {"Word": "in response to (~에 대한 응답으로)", "PartOfSpeech": "grammar", "Meaning": "'~에 대한 응답/대응으로'라는 뜻이다", "Example": "In response to customer feedback, we updated the menu.", "ExampleKo": "고객 피드백에 대응하여, 메뉴를 업데이트했다.", "Tier": "문법"},
    {"Word": "at the request of (~의 요청에 따라)", "PartOfSpeech": "grammar", "Meaning": "'~의 요청으로'라는 뜻이다", "Example": "The meeting was rescheduled at the request of the director.", "ExampleKo": "이사의 요청에 따라 회의 일정이 변경되었다.", "Tier": "문법"},
    {"Word": "as of + 날짜/시점 (~부터/~현재)", "PartOfSpeech": "grammar", "Meaning": "'~부터, ~현재로'라는 뜻으로 시점을 명시한다", "Example": "As of January 1, the new pricing policy will take effect.", "ExampleKo": "1월 1일부로, 새 가격 정책이 발효될 것이다.", "Tier": "문법"},
    {"Word": "except for (~을 제외하고)", "PartOfSpeech": "grammar", "Meaning": "'~을 제외하고'라는 뜻이다", "Example": "All departments met their targets except for sales.", "ExampleKo": "영업부를 제외하고 모든 부서가 목표를 달성했다.", "Tier": "문법"},
    {"Word": "according to (~에 따르면)", "PartOfSpeech": "grammar", "Meaning": "'~에 따르면, ~에 의하면'이라는 뜻이다", "Example": "According to the survey, customer satisfaction has improved.", "ExampleKo": "설문조사에 따르면, 고객 만족도가 향상되었다.", "Tier": "문법"},
    {"Word": "throughout + 명사 (~전체에 걸쳐)", "PartOfSpeech": "grammar", "Meaning": "공간적·시간적으로 '~전체에 걸쳐'라는 뜻이다", "Example": "The company has offices throughout the Asia-Pacific region.", "ExampleKo": "회사는 아시아 태평양 지역 전체에 사무소를 두고 있다.", "Tier": "문법"},
    {"Word": "between vs among 구분", "PartOfSpeech": "grammar", "Meaning": "between은 둘 사이, among은 셋 이상 사이에 쓴다", "Example": "The partnership between the two firms was announced today.", "ExampleKo": "두 회사 간의 파트너십이 오늘 발표되었다.", "Tier": "문법"},
    {"Word": "be responsible for (~에 책임이 있다)", "PartOfSpeech": "grammar", "Meaning": "'~에 대해 책임이 있다'라는 뜻이다", "Example": "Each manager is responsible for their team's performance.", "ExampleKo": "각 관리자는 자기 팀의 성과에 책임이 있다.", "Tier": "문법"},
    {"Word": "be subject to (~의 대상이 되다)", "PartOfSpeech": "grammar", "Meaning": "'~의 대상이다, ~에 따른다'라는 뜻이다", "Example": "The offer is subject to availability.", "ExampleKo": "이 제안은 재고 상황에 따른다.", "Tier": "문법"},

    # ===== 9. Conjunctions and Connectors (접속사/연결어) — 20 items =====
    {"Word": "although / though + 절 (~에도 불구하고)", "PartOfSpeech": "grammar", "Meaning": "양보를 나타내는 접속사로 뒤에 절(주어+동사)이 온다", "Example": "Although the economy slowed, the company maintained its profits.", "ExampleKo": "경제가 둔화되었음에도 불구하고, 회사는 수익을 유지했다.", "Tier": "문법"},
    {"Word": "despite / in spite of + 명사/동명사", "PartOfSpeech": "grammar", "Meaning": "'~에도 불구하고'이며 뒤에 명사(구)/동명사가 온다 (절 X)", "Example": "Despite the rain, the outdoor event was a success.", "ExampleKo": "비에도 불구하고, 야외 행사는 성공적이었다.", "Tier": "문법"},
    {"Word": "although vs despite 구분", "PartOfSpeech": "grammar", "Meaning": "although 뒤에는 절, despite 뒤에는 명사(구)가 온다", "Example": "Although it rained, ... / Despite the rain, ...", "ExampleKo": "비가 왔지만, ... / 비에도 불구하고, ...", "Tier": "문법"},
    {"Word": "whereas / while (~인 반면)", "PartOfSpeech": "grammar", "Meaning": "대조를 나타내는 접속사이다 ('~인 반면에')", "Example": "Sales rose in Asia, whereas they declined in Europe.", "ExampleKo": "아시아에서 매출이 올랐지만, 유럽에서는 감소했다.", "Tier": "문법"},
    {"Word": "however / nevertheless / nonetheless (그럼에도 불구하고)", "PartOfSpeech": "grammar", "Meaning": "앞 문장과 대조되는 내용을 이끄는 부사(접속부사)이다", "Example": "The product was expensive; however, it sold very well.", "ExampleKo": "제품은 비쌌다; 그러나, 매우 잘 팔렸다.", "Tier": "문법"},
    {"Word": "therefore / consequently / as a result (따라서)", "PartOfSpeech": "grammar", "Meaning": "인과 관계를 나타내는 접속부사이다 ('따라서, 그 결과')", "Example": "The company cut costs; therefore, profits increased.", "ExampleKo": "회사가 비용을 절감했다; 따라서, 수익이 증가했다.", "Tier": "문법"},
    {"Word": "moreover / furthermore / in addition (게다가)", "PartOfSpeech": "grammar", "Meaning": "앞 내용에 정보를 추가하는 접속부사이다 ('게다가')", "Example": "The hotel is affordable; moreover, it is centrally located.", "ExampleKo": "호텔은 가격이 합리적이다; 게다가, 중심부에 위치해 있다.", "Tier": "문법"},
    {"Word": "not only A but also B (A뿐만 아니라 B도)", "PartOfSpeech": "grammar", "Meaning": "'A뿐만 아니라 B도'라는 뜻이며 동사는 B에 일치한다", "Example": "Not only the price but also the quality has improved.", "ExampleKo": "가격뿐만 아니라 품질도 향상되었다.", "Tier": "문법"},
    {"Word": "both A and B (A와 B 둘 다)", "PartOfSpeech": "grammar", "Meaning": "'A와 B 둘 다'라는 뜻이며 복수 취급한다", "Example": "Both the design and the functionality have been upgraded.", "ExampleKo": "디자인과 기능 둘 다 업그레이드되었다.", "Tier": "문법"},
    {"Word": "either A or B (A 또는 B)", "PartOfSpeech": "grammar", "Meaning": "'A 또는 B 중 하나'라는 뜻이다", "Example": "Employees can choose either the morning or the afternoon shift.", "ExampleKo": "직원들은 오전 또는 오후 근무를 선택할 수 있다.", "Tier": "문법"},
    {"Word": "neither A nor B (A도 B도 아닌)", "PartOfSpeech": "grammar", "Meaning": "'A도 B도 아닌'이라는 뜻이다", "Example": "Neither the CEO nor the board members have commented.", "ExampleKo": "CEO도 이사진도 의견을 밝히지 않았다.", "Tier": "문법"},
    {"Word": "so that + 절 (~하기 위해/~하도록)", "PartOfSpeech": "grammar", "Meaning": "목적이나 결과를 나타내는 접속사이다", "Example": "We revised the schedule so that everyone could attend.", "ExampleKo": "모두가 참석할 수 있도록 일정을 수정했다.", "Tier": "문법"},
    {"Word": "접속사 vs 전치사 vs 접속부사 구분", "PartOfSpeech": "grammar", "Meaning": "접속사(절+절), 전치사(+명사), 접속부사(세미콜론/마침표 후) 구분이 중요하다", "Example": "Because it rained, ... / Because of the rain, ... / It rained; therefore, ...", "ExampleKo": "비가 와서 ... / 비 때문에 ... / 비가 왔다; 따라서 ...", "Tier": "문법"},
    {"Word": "once (~하자마자, 일단 ~하면)", "PartOfSpeech": "grammar", "Meaning": "'일단 ~하면'이라는 조건/시간 접속사이다", "Example": "Once the renovation is complete, the office will reopen.", "ExampleKo": "보수 공사가 완료되면, 사무실이 다시 열 것이다.", "Tier": "문법"},
    {"Word": "as well as + 명사 (~뿐만 아니라)", "PartOfSpeech": "grammar", "Meaning": "'~뿐만 아니라'라는 뜻이며 동사는 앞의 주어에 일치한다", "Example": "The manager, as well as the staff, was present at the event.", "ExampleKo": "직원뿐만 아니라 관리자도 행사에 참석했다.", "Tier": "문법"},
    {"Word": "now that (~이므로, ~이니까)", "PartOfSpeech": "grammar", "Meaning": "'이제 ~이므로'라는 이유·원인을 나타내는 접속사이다", "Example": "Now that the merger is finalized, we can begin integration.", "ExampleKo": "이제 합병이 확정되었으니, 통합을 시작할 수 있다.", "Tier": "문법"},
    {"Word": "in order to + 동사원형 (~하기 위해)", "PartOfSpeech": "grammar", "Meaning": "'~하기 위하여'라는 목적을 나타낸다", "Example": "She enrolled in the course in order to improve her skills.", "ExampleKo": "그녀는 기술을 향상시키기 위해 그 과정에 등록했다.", "Tier": "문법"},
    {"Word": "in order that + 절 (~하기 위해 / ~하도록)", "PartOfSpeech": "grammar", "Meaning": "격식체에서 목적을 나타내는 접속사이다", "Example": "The guidelines were updated in order that employees could comply.", "ExampleKo": "직원들이 준수할 수 있도록 지침이 업데이트되었다.", "Tier": "문법"},
    {"Word": "whether (or not) (~인지 아닌지)", "PartOfSpeech": "grammar", "Meaning": "'~인지 아닌지'를 나타내며 명사절을 이끈다", "Example": "We have not yet decided whether to accept the offer.", "ExampleKo": "우리는 아직 그 제안을 수락할지 결정하지 못했다.", "Tier": "문법"},
    {"Word": "as soon as (~하자마자)", "PartOfSpeech": "grammar", "Meaning": "'~하자마자'라는 뜻의 시간 접속사이다", "Example": "As soon as the contract is signed, construction will start.", "ExampleKo": "계약이 체결되자마자, 공사가 시작될 것이다.", "Tier": "문법"},

    # ===== 10. Comparative and Superlative (비교급/최상급) — 10 items =====
    {"Word": "비교급 + than (비교급 기본)", "PartOfSpeech": "grammar", "Meaning": "두 대상을 비교할 때 -er/more + than을 쓴다", "Example": "This quarter's revenue is higher than last quarter's.", "ExampleKo": "이번 분기 매출이 지난 분기보다 높다.", "Tier": "문법"},
    {"Word": "the + 최상급 + in/of (최상급 기본)", "PartOfSpeech": "grammar", "Meaning": "셋 이상 중 가장 ~한 것을 나타낸다", "Example": "This is the most efficient process in the entire factory.", "ExampleKo": "이것은 공장 전체에서 가장 효율적인 공정이다.", "Tier": "문법"},
    {"Word": "as + 원급 + as (원급 비교: ~만큼 ~한)", "PartOfSpeech": "grammar", "Meaning": "두 대상이 같은 정도임을 나타낸다", "Example": "The new model is as durable as the previous one.", "ExampleKo": "새 모델은 이전 것만큼 내구성이 있다.", "Tier": "문법"},
    {"Word": "not as/so + 원급 + as (~만큼 ~하지 않은)", "PartOfSpeech": "grammar", "Meaning": "두 대상의 차이를 나타내는 부정 비교이다", "Example": "The branch office is not as large as the headquarters.", "ExampleKo": "지사는 본사만큼 크지 않다.", "Tier": "문법"},
    {"Word": "the + 비교급, the + 비교급 (~할수록 더 ~한)", "PartOfSpeech": "grammar", "Meaning": "'~하면 할수록 더 ~하다'라는 비례 관계를 나타낸다", "Example": "The more experience you have, the higher salary you can expect.", "ExampleKo": "경험이 많을수록, 더 높은 급여를 기대할 수 있다.", "Tier": "문법"},
    {"Word": "much / far / even / still + 비교급 강조", "PartOfSpeech": "grammar", "Meaning": "비교급 앞에 much, far, even, still을 써서 강조한다", "Example": "The new software is far more efficient than the old version.", "ExampleKo": "새 소프트웨어는 이전 버전보다 훨씬 더 효율적이다.", "Tier": "문법"},
    {"Word": "one of the + 최상급 + 복수명사", "PartOfSpeech": "grammar", "Meaning": "'가장 ~한 것 중 하나'라는 뜻이다", "Example": "It is one of the most successful product launches this year.", "ExampleKo": "올해 가장 성공적인 제품 출시 중 하나이다.", "Tier": "문법"},
    {"Word": "less + 원급 + than (열등 비교)", "PartOfSpeech": "grammar", "Meaning": "'~보다 덜 ~한'이라는 뜻이다", "Example": "This option is less expensive than the alternative.", "ExampleKo": "이 옵션은 대안보다 덜 비싸다.", "Tier": "문법"},
    {"Word": "비교급 혼동: good-better-best / bad-worse-worst", "PartOfSpeech": "grammar", "Meaning": "불규칙 비교급·최상급 형태를 정확히 알아야 한다", "Example": "The company's financial performance is better than expected.", "ExampleKo": "회사의 재무 성과가 예상보다 더 좋다.", "Tier": "문법"},
    {"Word": "배수 표현: 배수 + as + 원급 + as", "PartOfSpeech": "grammar", "Meaning": "'~의 몇 배'를 나타낼 때 배수 + as 원급 as를 쓴다", "Example": "The new warehouse is three times as large as the old one.", "ExampleKo": "새 창고는 이전 것의 세 배 크기이다.", "Tier": "문법"},

    # ===== 11. Articles and Determiners (관사/한정사) — 10 items =====
    {"Word": "a/an (부정관사): 처음 언급하는 단수 가산", "PartOfSpeech": "grammar", "Meaning": "처음 언급하거나 불특정한 단수 가산명사 앞에 a/an을 쓴다", "Example": "We are looking for a qualified candidate for the position.", "ExampleKo": "우리는 그 직위에 적합한 후보를 찾고 있다.", "Tier": "문법"},
    {"Word": "the (정관사): 특정·유일·이미 언급된 대상", "PartOfSpeech": "grammar", "Meaning": "특정하거나 유일하거나 이미 언급된 대상 앞에 the를 쓴다", "Example": "The conference room on the third floor is reserved.", "ExampleKo": "3층 회의실은 예약되어 있다.", "Tier": "문법"},
    {"Word": "무관사 + 불가산명사/복수명사 (일반적 의미)", "PartOfSpeech": "grammar", "Meaning": "일반적·추상적 의미일 때 불가산·복수명사에 관사를 쓰지 않는다", "Example": "Information about the program is available on our website.", "ExampleKo": "프로그램에 대한 정보는 웹사이트에서 확인할 수 있다.", "Tier": "문법"},
    {"Word": "another + 단수명사 (또 다른 하나)", "PartOfSpeech": "grammar", "Meaning": "'또 다른 하나'라는 뜻으로 단수 가산명사 앞에 쓴다", "Example": "The team needs to hire another designer for the project.", "ExampleKo": "팀은 프로젝트를 위해 디자이너를 한 명 더 고용해야 한다.", "Tier": "문법"},
    {"Word": "other + 복수명사 / the other + 단수/복수", "PartOfSpeech": "grammar", "Meaning": "other + 복수(다른 것들), the other(나머지), the others(나머지 전부)", "Example": "Some employees prefer remote work, while others prefer the office.", "ExampleKo": "일부 직원은 원격 근무를, 나머지는 사무실을 선호한다.", "Tier": "문법"},
    {"Word": "each / every + 단수명사", "PartOfSpeech": "grammar", "Meaning": "each, every 뒤에는 단수 가산명사가 온다", "Example": "Each department is responsible for its own budget.", "ExampleKo": "각 부서는 자체 예산에 대한 책임이 있다.", "Tier": "문법"},
    {"Word": "all / most / some + 복수명사/불가산명사", "PartOfSpeech": "grammar", "Meaning": "all, most, some은 복수명사 또는 불가산명사와 쓴다", "Example": "Most employees participated in the annual health screening.", "ExampleKo": "대부분의 직원이 연례 건강 검진에 참여했다.", "Tier": "문법"},
    {"Word": "few vs a few / little vs a little", "PartOfSpeech": "grammar", "Meaning": "few/little(거의 없는-부정), a few/a little(약간의-긍정)", "Example": "A few changes were made to the original design.", "ExampleKo": "원래 디자인에 약간의 변경이 있었다.", "Tier": "문법"},
    {"Word": "the + 형용사 = 복수 의미 (~한 사람들)", "PartOfSpeech": "grammar", "Meaning": "the + 형용사로 '~한 사람들'을 나타낸다 (the elderly, the unemployed)", "Example": "The company donates 5% of profits to help the disadvantaged.", "ExampleKo": "회사는 수익의 5%를 소외 계층 돕기에 기부한다.", "Tier": "문법"},
    {"Word": "a/an vs the: TOEIC 빈칸 선택 전략", "PartOfSpeech": "grammar", "Meaning": "첫 언급·불특정이면 a/an, 이미 알려진·특정이면 the를 선택한다", "Example": "We opened a new branch. The branch is located downtown.", "ExampleKo": "새 지점을 열었다. 그 지점은 시내에 위치해 있다.", "Tier": "문법"},

    # ===== 12. Pronoun Reference (대명사) — 10 items =====
    {"Word": "it vs they/them: 단수/복수 대명사 일치", "PartOfSpeech": "grammar", "Meaning": "대명사는 선행 명사의 수(단수/복수)에 일치해야 한다", "Example": "The policy was updated because it no longer met current needs.", "ExampleKo": "현재 요구를 더 이상 충족하지 않아 정책이 업데이트되었다.", "Tier": "문법"},
    {"Word": "those who + 복수동사 (~하는 사람들)", "PartOfSpeech": "grammar", "Meaning": "'~하는 사람들'이라는 뜻으로 복수 취급한다", "Example": "Those who wish to participate should register in advance.", "ExampleKo": "참여를 원하는 사람들은 사전에 등록해야 한다.", "Tier": "문법"},
    {"Word": "재귀대명사: 주어와 목적어 같을 때 (himself, themselves)", "PartOfSpeech": "grammar", "Meaning": "주어와 목적어가 같은 대상일 때 재귀대명사를 쓴다", "Example": "The director himself approved the final design.", "ExampleKo": "이사가 직접 최종 디자인을 승인했다.", "Tier": "문법"},
    {"Word": "소유대명사: mine, yours, theirs, ours", "PartOfSpeech": "grammar", "Meaning": "소유대명사는 '소유격 + 명사'를 대신하며 뒤에 명사가 오지 않는다", "Example": "This office is ours; the one next door is theirs.", "ExampleKo": "이 사무실은 우리 것이고; 옆 것은 그들 것이다.", "Tier": "문법"},
    {"Word": "one / ones: 앞에 나온 명사 대용", "PartOfSpeech": "grammar", "Meaning": "이미 언급한 명사를 반복하지 않기 위해 one/ones를 쓴다", "Example": "The old printers are being replaced with new ones.", "ExampleKo": "구형 프린터가 새것으로 교체되고 있다.", "Tier": "문법"},
    {"Word": "that / those of: 비교 시 명사 반복 회피", "PartOfSpeech": "grammar", "Meaning": "비교 구문에서 앞의 명사 반복을 피할 때 that/those of를 쓴다", "Example": "Our sales figures exceed those of our competitors.", "ExampleKo": "우리 매출 수치가 경쟁사의 것을 초과한다.", "Tier": "문법"},
    {"Word": "대명사-선행사 일치: 성·수 일치", "PartOfSpeech": "grammar", "Meaning": "대명사는 선행사의 성별과 수에 일치해야 한다", "Example": "Each employee should submit his or her timesheet by Friday.", "ExampleKo": "각 직원은 금요일까지 근무 시간표를 제출해야 한다.", "Tier": "문법"},
    {"Word": "it의 비인칭 용법 (날씨, 시간, 거리)", "PartOfSpeech": "grammar", "Meaning": "날씨, 시간, 거리 등을 나타낼 때 비인칭 주어 it을 쓴다", "Example": "It is approximately 30 minutes from the hotel to the airport.", "ExampleKo": "호텔에서 공항까지 약 30분이다.", "Tier": "문법"},
    {"Word": "that 지시대명사 vs that 접속사 구분", "PartOfSpeech": "grammar", "Meaning": "that이 명사를 대신하면 지시대명사, 절을 이끌면 접속사이다", "Example": "The quality of this product is better than that of the competitor.", "ExampleKo": "이 제품의 품질이 경쟁사 제품보다 낫다.", "Tier": "문법"},
    {"Word": "부정대명사: anyone, someone, everyone + 단수 동사", "PartOfSpeech": "grammar", "Meaning": "anyone, someone, everyone, nobody 등은 단수 취급한다", "Example": "Everyone is expected to attend the annual company picnic.", "ExampleKo": "모든 사람이 연례 회사 야유회에 참석할 것으로 기대된다.", "Tier": "문법"},

    # ===== 13. Participles as Adjectives (분사 형용사) — 10 items =====
    {"Word": "현재분사(-ing) vs 과거분사(-ed) 형용사 기본", "PartOfSpeech": "grammar", "Meaning": "-ing는 '~하게 하는(원인)', -ed는 '~한 상태(감정 결과)'를 나타낸다", "Example": "The results were surprising. / The employees were surprised.", "ExampleKo": "결과가 놀라웠다. / 직원들이 놀랐다.", "Tier": "문법"},
    {"Word": "interesting vs interested", "PartOfSpeech": "grammar", "Meaning": "interesting(흥미로운-사물), interested(흥미를 느끼는-사람)", "Example": "Attendees were interested in the interesting presentation.", "ExampleKo": "참석자들은 흥미로운 발표에 관심을 보였다.", "Tier": "문법"},
    {"Word": "boring vs bored", "PartOfSpeech": "grammar", "Meaning": "boring(지루한-사물), bored(지루해하는-사람)", "Example": "The long meeting was boring, and everyone was bored.", "ExampleKo": "긴 회의가 지루했고, 모두가 지루해했다.", "Tier": "문법"},
    {"Word": "confusing vs confused", "PartOfSpeech": "grammar", "Meaning": "confusing(혼란스러운-사물), confused(혼란스러워하는-사람)", "Example": "The instructions were confusing, so the new hire was confused.", "ExampleKo": "지시가 혼란스러워서, 신입 사원이 당황했다.", "Tier": "문법"},
    {"Word": "satisfying vs satisfied", "PartOfSpeech": "grammar", "Meaning": "satisfying(만족스러운-사물), satisfied(만족한-사람)", "Example": "Customers are satisfied with the satisfying level of service.", "ExampleKo": "고객들은 만족스러운 수준의 서비스에 만족하고 있다.", "Tier": "문법"},
    {"Word": "disappointing vs disappointed", "PartOfSpeech": "grammar", "Meaning": "disappointing(실망스러운-사물), disappointed(실망한-사람)", "Example": "The quarterly earnings were disappointing to shareholders.", "ExampleKo": "분기 실적이 주주들에게 실망스러웠다.", "Tier": "문법"},
    {"Word": "exciting vs excited", "PartOfSpeech": "grammar", "Meaning": "exciting(흥분시키는-사물), excited(흥분한-사람)", "Example": "The team was excited about the exciting new partnership.", "ExampleKo": "팀은 흥미진진한 새 파트너십에 대해 흥분했다.", "Tier": "문법"},
    {"Word": "현재분사 vs 동명사 구분", "PartOfSpeech": "grammar", "Meaning": "같은 -ing 형태지만 형용사 역할이면 현재분사, 명사 역할이면 동명사이다", "Example": "The running cost is high. (분사) / Running is good exercise. (동명사)", "ExampleKo": "운영 비용이 높다. / 달리기는 좋은 운동이다.", "Tier": "문법"},
    {"Word": "분사구문: -ing(능동), p.p.(수동) + 주절", "PartOfSpeech": "grammar", "Meaning": "분사가 절을 축약하여 이유·때·조건 등을 나타낸다", "Example": "Located near the station, the hotel is convenient for travelers.", "ExampleKo": "역 근처에 위치해 있어서, 호텔은 여행자에게 편리하다.", "Tier": "문법"},
    {"Word": "overwhelming vs overwhelmed", "PartOfSpeech": "grammar", "Meaning": "overwhelming(압도적인-사물), overwhelmed(압도당한-사람)", "Example": "The response to the survey was overwhelming.", "ExampleKo": "설문조사에 대한 반응이 압도적이었다.", "Tier": "문법"},

    # ===== 14. Causative Verbs (사역동사) — 5 items =====
    {"Word": "have + 목적어 + 동사원형/p.p. (사역)", "PartOfSpeech": "grammar", "Meaning": "have + 사람 + 동사원형(시키다), have + 사물 + p.p.(시켜서 되게 하다)", "Example": "The manager had the assistant prepare the meeting agenda.", "ExampleKo": "관리자는 비서에게 회의 안건을 준비하게 했다.", "Tier": "문법"},
    {"Word": "make + 목적어 + 동사원형 (강제 사역)", "PartOfSpeech": "grammar", "Meaning": "make는 '~하게 만들다/시키다'이며 목적어 + 동사원형을 쓴다", "Example": "The new regulation made companies disclose their emissions data.", "ExampleKo": "새 규정이 기업들에게 배출 데이터를 공개하게 만들었다.", "Tier": "문법"},
    {"Word": "let + 목적어 + 동사원형 (허락 사역)", "PartOfSpeech": "grammar", "Meaning": "let은 '~하게 허락하다'이며 목적어 + 동사원형을 쓴다", "Example": "The supervisor let the team leave early on Friday.", "ExampleKo": "감독관이 금요일에 팀이 일찍 퇴근하도록 허락했다.", "Tier": "문법"},
    {"Word": "get + 목적어 + to부정사/p.p. (설득·의뢰)", "PartOfSpeech": "grammar", "Meaning": "get + 사람 + to부정사(설득하다), get + 사물 + p.p.(되게 하다)", "Example": "She got her colleague to review the draft before submission.", "ExampleKo": "그녀는 제출 전에 동료에게 초안을 검토하게 했다.", "Tier": "문법"},
    {"Word": "help + 목적어 + (to) 동사원형", "PartOfSpeech": "grammar", "Meaning": "help는 동사원형 또는 to부정사 둘 다 가능하다", "Example": "The new tool helps employees manage their schedules efficiently.", "ExampleKo": "새 도구는 직원들이 효율적으로 일정을 관리하도록 돕는다.", "Tier": "문법"},

    # ===== 15. Commonly Confused Words (혼동 어법) — 10 items =====
    {"Word": "affect (동사) vs effect (명사)", "PartOfSpeech": "grammar", "Meaning": "affect는 동사(영향을 미치다), effect는 명사(효과, 영향)", "Example": "The policy change will affect all departments. / The effect was immediate.", "ExampleKo": "정책 변경이 모든 부서에 영향을 미칠 것이다. / 효과는 즉각적이었다.", "Tier": "문법"},
    {"Word": "raise (타동사) vs rise (자동사)", "PartOfSpeech": "grammar", "Meaning": "raise는 타동사(~을 올리다), rise는 자동사(오르다)", "Example": "The company plans to raise prices. / Costs continue to rise.", "ExampleKo": "회사는 가격을 올릴 계획이다. / 비용이 계속 오르고 있다.", "Tier": "문법"},
    {"Word": "lay (타동사) vs lie (자동사)", "PartOfSpeech": "grammar", "Meaning": "lay는 타동사(~을 놓다, 과거 laid), lie는 자동사(놓여 있다, 과거 lay)", "Example": "Please lay the documents on the desk. / The factory lies near the highway.", "ExampleKo": "서류를 책상 위에 놓아 주세요. / 공장이 고속도로 근처에 있다.", "Tier": "문법"},
    {"Word": "principal (주요한/교장) vs principle (원칙)", "PartOfSpeech": "grammar", "Meaning": "principal은 형용사(주요한) 또는 명사(교장), principle은 명사(원칙)", "Example": "The principal reason for the change is cost reduction.", "ExampleKo": "변경의 주된 이유는 비용 절감이다.", "Tier": "문법"},
    {"Word": "assure / ensure / insure 구분", "PartOfSpeech": "grammar", "Meaning": "assure(사람에게 확신시키다), ensure(확실히 하다), insure(보험에 들다)", "Example": "Please ensure that all safety procedures are followed.", "ExampleKo": "모든 안전 절차가 준수되도록 확인해 주세요.", "Tier": "문법"},
    {"Word": "farther (거리) vs further (추가적인)", "PartOfSpeech": "grammar", "Meaning": "farther는 물리적 거리, further는 추가적·더 나아간 의미이다", "Example": "For further information, please visit our website.", "ExampleKo": "추가 정보는 저희 웹사이트를 방문해 주세요.", "Tier": "문법"},
    {"Word": "beside (옆에) vs besides (게다가)", "PartOfSpeech": "grammar", "Meaning": "beside는 전치사(~옆에), besides는 부사/전치사(~외에도, 게다가)", "Example": "Besides the main office, we have three regional branches.", "ExampleKo": "본사 외에도, 3개의 지역 지사가 있다.", "Tier": "문법"},
    {"Word": "complement (보완) vs compliment (칭찬)", "PartOfSpeech": "grammar", "Meaning": "complement(보완하다/보완물), compliment(칭찬하다/칭찬)", "Example": "The new software complements our existing system well.", "ExampleKo": "새 소프트웨어가 기존 시스템을 잘 보완한다.", "Tier": "문법"},
    {"Word": "precede (앞서다) vs proceed (진행하다)", "PartOfSpeech": "grammar", "Meaning": "precede(~에 앞서다), proceed(진행하다)", "Example": "A brief introduction will precede the main presentation.", "ExampleKo": "짧은 소개가 본 발표에 앞설 것이다.", "Tier": "문법"},
    {"Word": "stationary (정지한) vs stationery (문구류)", "PartOfSpeech": "grammar", "Meaning": "stationary(움직이지 않는), stationery(문구·사무용품)", "Example": "Please order more stationery for the office.", "ExampleKo": "사무실용 문구류를 더 주문해 주세요.", "Tier": "문법"},
]

# Validate count
print(f"Total items: {len(items)}")
assert len(items) == 220, f"Expected 220, got {len(items)}"

# Check for duplicates
words = [item["Word"] for item in items]
dupes = [w for w in words if words.count(w) > 1]
if dupes:
    print(f"WARNING: Duplicate words found: {set(dupes)}")
else:
    print("No duplicates found.")

# Validate all fields
required_fields = ["Word", "PartOfSpeech", "Meaning", "Example", "ExampleKo", "Tier"]
for i, item in enumerate(items):
    for field in required_fields:
        assert field in item, f"Item {i} missing field '{field}'"
    assert item["PartOfSpeech"] == "grammar", f"Item {i} PartOfSpeech is not 'grammar'"
    assert item["Tier"] == "문법", f"Item {i} Tier is not '문법'"

print("All validations passed!")

# Write JSON
output_path = r"c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan\scripts\toeic_grammar.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Written to {output_path}")
