import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"scripts\toeic_tier2.json", "r", encoding="utf-8") as f:
    t2 = json.load(f)

seen = {w["Word"].lower() for w in t2}
with open(r"scripts\toeic_tier1.json", "r", encoding="utf-8") as f:
    t1 = json.load(f)
for w in t1:
    seen.add(w["Word"].lower())

more_words = [
    ("adversely", "adv", "불리하게, 부정적으로", "Supply chain delays adversely affected our quarterly revenue.", "공급망 지연은 당사의 분기 매출에 부정적인 영향을 미쳤습니다."),
    ("allegedly", "adv", "주장하는 바에 따르면, 전해진 바에 의하면", "The company allegedly concealed audit findings from regulators.", "회사가 규제 당국으로부터 감사 결과를 은폐했다는 주장이 제기되었습니다."),
    ("altogether", "adv", "완전히, 전적으로", "The airline decided to discontinue meal service altogether on short flights.", "그 항공사는 단거리 노선에서 기내식 제공을 완전히 중단하기로 결정했습니다."),
    ("anonymously", "adv", "익명으로", "Whistleblowers can submit violation tips anonymously online.", "내부고발자는 위반 제보를 온라인으로 익명 제출할 수 있습니다."),
    ("apparently", "adv", "겉보기에, 분명히", "The shipment was apparently misrouted to the Chicago sorting center.", "화물이 겉보기에 시카고 분류 센터로 잘못 발송된 것으로 보입니다."),
    ("approximately", "adv", "대략, 약", "The construction will take approximately fourteen business days.", "공사에는 대략 14 영업일이 소요될 것입니다."),
    ("arguably", "adv", "단언컨대, 거의 틀림없이", "This is arguably the most fuel-efficient delivery vehicle on the market.", "이것은 단언컨대 시장에서 가장 연비가 좋은 배송 차량입니다."),
    ("authentically", "adv", "진정으로, 진짜답게", "The marketing campaign authentically connected with urban youth.", "그 마케팅 캠페인은 도시 청년층과 진정성 있게 연결되었습니다."),
    ("barely", "adv", "간신히, 가까스로", "We barely met the filing deadline before the state office closed.", "저희는 주 정부 청사가 문을 닫기 직전에 가까스로 서류 제출 마감일을 맞췄습니다."),
    ("chronically", "adv", "만성적으로", "The municipal airport has been chronically congested for years.", "그 시립 공항은 수년간 만성적으로 혼잡을 겪어 왔습니다."),
    ("collaboratively", "adv", "협력하여", "Engineers and designers worked collaboratively to craft the interface.", "엔지니어들과 디자이너들은 협력하여 인터페이스를 제작했습니다."),
    ("comparatively", "adv", "비교적, 상대적으로", "Electric delivery trucks have comparatively low maintenance costs.", "전기 배송 트럭은 상대적으로 유지보수 비용이 적게 듭니다."),
    ("compatibly", "adv", "호환되게, 양립하여", "Ensure all components run compatibly within the cloud framework.", "모든 구성 요소가 클라우드 프레임워크 내에서 호환되어 실행되도록 하십시오."),
    ("competently", "adv", "유능하게, 능숙하게", "The junior project manager handled the crisis competently.", "주니어 프로젝트 관리자는 위기를 유능하게 수습했습니다."),
    ("comprehensively", "adv", "포괄적으로, 철저히", "The handbook explains corporate benefits comprehensively.", "그 편람은 기업의 복리후생 제도를 포괄적으로 설명하고 있습니다."),
    ("concurrently", "adv", "동시에", "Two high-priority software patches were deployed concurrently.", "두 개의 최우선 소프트웨어 패치가 동시에 배포되었습니다."),
    ("confidentiality", "noun", "기밀성, 비밀 유지", "The non-disclosure agreement guarantees absolute client confidentiality.", "비밀유지계약서는 고객에 대한 절대적인 기밀 유지를 보장합니다."),
    ("conspicuously", "adv", "눈에 띄게, 두드러지게", "Exit routes must be conspicuously marked on every floor.", "비상구 경로는 각 층마다 눈에 띄게 표시되어야 합니다."),
    ("continually", "adv", "계속해서, 끊임없이", "Developers continually iterate on customer suggestions.", "개발자들은 고객 제안 사항을 바탕으로 계속해서 제품을 개선합니다."),
    ("customarily", "adv", "관례적으로, 통상적으로", "Board elections are customarily held during the second quarter.", "이사회 선거는 관례적으로 2분기 중에 개최됩니다."),
    ("decisively", "adv", "결단력 있게, 단호하게", "The board acted decisively to replace underperforming management.", "이사회는 실적이 저조한 경영진을 교체하기 위해 단호하게 조치했습니다."),
    ("definitely", "adv", "분명히, 틀림없이", "Automation will definitely decrease human manufacturing error.", "자동화는 인간에 의한 제조 실수를 분명히 줄여줄 것입니다."),
    ("deliberately", "adv", "의도적으로, 신중하게", "The firm deliberately slowed hiring to manage operating margins.", "그 기업은 영업이익률을 관리하기 위해 의도적으로 채용 속도를 늦췄습니다."),
    ("diligently", "adv", "부지런히, 성실하게", "The compliance auditor worked diligently through the weekend.", "규정 준수 감사관은 주말 내내 성실하게 근무했습니다."),
    ("directly", "adv", "직접, 곧바로", "Direct all customer inquiries directly to the tier-two helpdesk.", "모든 고객 문의는 2차 헬프데스크로 곧바로 전달해 주십시오."),
    ("discreetly", "adv", "신중하게, 조심스럽게", "HR handled the executive transition discreetly to prevent panic.", "인사부는 혼란을 방지하기 위해 임원 교체를 신중하게 처리했습니다."),
    ("drastically", "adv", "과감하게, 급격하게", "Energy consumption dropped drastically after solar array installation.", "태양광 집열판 설치 후 에너지 소비량이 급격하게 감소했습니다."),
    ("effectively", "adv", "효과적으로, 실질적으로", "The new workflow effectively halved project completion turnaround.", "새로운 업무 흐름은 프로젝트 완료 소요 시간을 실질적으로 절반으로 줄였습니다."),
    ("efficiently", "adv", "효율적으로, 능률적으로", "Modern sorting facilities process packages three times more efficiently.", "현대식 분류 시설은 택배 물품을 3배 더 효율적으로 처리합니다."),
    ("elaborately", "adv", "정교하게, 공들여", "The exhibition booth was elaborately decorated to mirror a cafe.", "전시 부스는 카페를 재현하기 위해 정교하게 꾸며졌습니다."),
    ("eminently", "adv", "대단히, 현저하게", "She is an eminently qualified candidate for the director position.", "그녀는 이사직에 대단히 자격을 갖춘 적임자입니다."),
    ("entirely", "adv", "전적으로, 완전히", "The plant operates entirely on hydro-electric power.", "그 공장은 전적으로 수력 발전에 의존하여 가동됩니다."),
    ("equitably", "adv", "공평하게", "Annual bonus pools were distributed equitably across departments.", "연간 보너스 재원은 부서 전반에 걸쳐 공평하게 분배되었습니다."),
    ("essentially", "adv", "본질적으로, 기본적으로", "The revised policy is essentially identical to last year's draft.", "개정된 정책은 본질적으로 작년 초안과 동일합니다."),
    ("evidently", "adv", "분명히, 눈에 띄게", "The advertising push was evidently successful, doubling web visits.", "광고 캠페인은 분명히 성공적이었으며, 웹사이트 방문자 수를 두 배로 늘렸습니다."),
    ("exceptionally", "adv", "특출나게, 예외적으로", "The laptop processor runs exceptionally cool under heavy load.", "그 노트북 프로세서는 고부하 작업 중에도 특출나게 낮은 온도를 유지합니다."),
    ("exclusively", "adv", "독점적으로, 오로지", "Executive suites are reserved exclusively for visiting dignitaries.", "이그제큐티브 스위트룸은 외빈 방문객 전용으로만 예약됩니다."),
    ("explicitly", "adv", "명시적으로, 명백하게", "The warranty explicitly excludes damage caused by water immersion.", "보증서에는 침수로 인한 손상은 명시적으로 제외된다고 적혀 있습니다."),
    ("exponentially", "adv", "기하급수적으로", "Cloud storage demands have grown exponentially over five years.", "클라우드 저장소 수요는 5년에 걸쳐 기하급수적으로 증가했습니다."),
    ("extensively", "adv", "광범위하게, 널리", "The new medication was tested extensively across five countries.", "새 약품은 5개국에 걸쳐 광범위하게 임상 테스트를 거쳤습니다."),
    ("firmly", "adv", "확고하게, 단호히", "Management firmly believes in cultivating internal employee leadership.", "경영진은 사내 직원의 리더십을 육성하는 것을 확고하게 신뢰합니다."),
    ("formally", "adv", "공식적으로, 격식 있게", "The international merger was formally announced at the stock exchange.", "국제 합병은 증권거래소에서 공식적으로 발표되었습니다."),
    ("fundamentally", "adv", "근본적으로", "Artificial intelligence fundamentally transformed our data analysis.", "인공지능은 당사의 데이터 분석 방식을 근본적으로 변화시켰습니다."),
    ("gradually", "adv", "점진적으로, 서서히", "Consumer confidence gradually recovered following the rate cuts.", "금리 인하 이후 소비자 신뢰 지수는 서서히 회복되었습니다."),
    ("hardly", "adv", "거의 ~않다", "We could hardly keep up with the unexpected surge in orders.", "저희는 예상치 못한 주문 급증을 거의 따라잡기 힘들었습니다."),
    ("highly", "adv", "대단히, 매우", "The cloud management software comes highly recommended by auditors.", "그 클라우드 관리 소프트웨어는 감사관들에 의해 대단히 추천받고 있습니다."),
    ("immediately", "adv", "즉시, 곧바로", "Defective components must be pulled from the conveyor line immediately.", "결함이 있는 부품은 즉시 컨베이어 라인에서 제거해야 합니다."),
    ("immensely", "adv", "엄청나게, 대단히", "Her previous logistics experience helped the startup immensely.", "그녀의 이전 물류 경험은 스타트업에 엄청난 도움이 되었습니다."),
    ("inadvertently", "adv", "의도치 않게, 부주의로", "The billing department inadvertently charged the client twice.", "청구 부서는 부주의로 고객에게 두 번 요금을 청구했습니다."),
    ("increasingly", "adv", "점점 더, 갈수록", "Online security has become an increasingly urgent priority.", "온라인 보안은 갈수록 더욱 시급한 최우선 과제가 되었습니다."),
    ("indefinitely", "adv", "무기한으로", "Factory operations were paused indefinitely pending environmental clearance.", "공장 가동은 환경 승인이 날 때까지 무기한 중단되었습니다."),
    ("initially", "adv", "처음에는, 초기에", "The team was initially skeptical of transitioning to agile sprints.", "팀은 처음에는 애자일 스프린트로 전환하는 것에 회의적이었습니다."),
    ("instantly", "adv", "즉각, 즉시", "Subscribers can access digital editions instantly upon publication.", "구독자들은 출간 즉시 디지털 판에 접속할 수 있습니다."),
    ("invariably", "adv", "변함없이, 언제나", "Friday afternoon meetings invariably run longer than anticipated.", "금요일 오후 회의는 변함없이 예상보다 길어지곤 합니다."),
    ("mutually", "adv", "상호 간에, 서로", "Both firms signed a mutually advantageous distribution agreement.", "두 회사는 상호 유리한 유통 계약에 서명했습니다."),
    ("notably", "adv", "특히, 현저하게", "Several regional branches, notably Chicago, beat their sales goals.", "몇몇 지역 지사들, 특히 시카고 지사는 판매 목표를 초과 달성했습니다."),
    ("officially", "adv", "공식적으로", "The new high-speed rail corridor officially opens this Friday.", "새로운 고속철도 노선은 이번 주 금요일에 공식 개통합니다."),
    ("ordinarily", "adv", "보통, 대체로", "Travel reimbursements are processed within five business days ordinarily.", "출장비 환급은 통상적으로 5 영업일 이내에 처리됩니다."),
    ("overwhelmingly", "adv", "압도적으로", "Stockholders overwhelmingly supported the green energy initiative.", "주주들은 친환경 에너지 추진안을 압도적으로 지지했습니다."),
    ("particularly", "adv", "특히, 각별히", "The software performs particularly well on older tablet devices.", "그 소프트웨어는 특히 구형 태블릿 기기에서 뛰어난 성능을 발휘합니다."),
    ("periodically", "adv", "주기적으로, 정기적으로", "Security keys are periodically refreshed to thwart cyber intruders.", "사이버 침입자를 차단하기 위해 보안 키는 주기적으로 갱신됩니다."),
    ("permanently", "adv", "영구적으로", "The downtown satellite branch will be closed permanently in March.", "시내 위성 지사는 3월에 영구 폐쇄될 예정입니다."),
    ("potentially", "adv", "잠재적으로, 어쩌면", "The patent litigation could potentially cost the firm millions.", "그 특허 소송은 잠재적으로 기업에 수백만 달러의 비용을 치르게 할 수 있습니다."),
    ("predominantly", "adv", "주로, 대개", "Our manufacturing footprint is predominantly located in North America.", "당사의 제조 시설은 주로 북미 지역에 위치해 있습니다."),
    ("previously", "adv", "이전에, 미리", "She previously served as senior vice president of supply chain.", "그녀는 이전에 공급망 담당 수석 부사장을 역임했습니다."),
    ("primarily", "adv", "주로, 기본적으로", "Revenue growth was driven primarily by overseas enterprise software sales.", "매출 성장은 주로 해외 기업용 소프트웨어 판매에 의해 견인되었습니다."),
    ("promptly", "adv", "신속하게, 즉시", "Invoices must be settled promptly within thirty calendar days.", "청구서는 30일 이내에 신속히 정산되어야 합니다."),
    ("properly", "adv", "제대로, 적절하게", "Ensure all chemical containers are sealed and properly labeled.", "모든 화학물질 용기가 밀봉되고 제대로 라벨이 부착되었는지 확인하십시오."),
    ("rapidly", "adv", "급속히, 빠르게", "Digital payment adoption expanded rapidly among small business merchants.", "소상공인들 사이에서 디지털 결제 도입이 급속히 확산되었습니다."),
    ("readily", "adv", "손쉽게, 기꺼이", "Spare replacement filters are readily available at retail hardware stores.", "교체용 예비 필터는 철물 소매점에서 손쉽게 구할 수 있습니다."),
    ("regularly", "adv", "정기적으로, 자주", "Inspect backup generators regularly to verify emergency readiness.", "비상 대비 태세를 확인하기 위해 비상 발전기를 정기적으로 점검하십시오."),
    ("reluctantly", "adv", "마지못해, 꺼려하며", "The council reluctantly accepted the tax assessment increase.", "시의회는 마지못해 세금 평가액 인상을 수용했습니다."),
    ("remarkably", "adv", "놀랍게도, 두드러지게", "The factory operated remarkably smoothly despite supply chain headwinds.", "공장은 공급망 역풍에도 불구하고 놀라울 정도로 순조롭게 가동되었습니다."),
    ("repeatedly", "adv", "반복적으로, 거듭", "Technicians repeatedly tested the elevator emergency brake cables.", "기술자들은 엘리베이터 비상 브레이크 케이블을 거듭 테스트했습니다."),
    ("routinely", "adv", "일상적으로, 판에 박힌 듯", "All incoming email attachments are routinely scanned for trojans.", "수신되는 모든 이메일 첨부파일은 일상적으로 악성코드 검사를 받습니다."),
    ("scrupulously", "adv", "꼼꼼하게, 양심적으로", "The research team scrupulously tracked every statistical anomaly.", "연구팀은 모든 통계적 이상 징후를 꼼꼼하게 추적했습니다."),
    ("seamlessly", "adv", "매끄럽게, 빈틈없이", "The upgraded database integrated seamlessly with the analytics suite.", "업그레이드된 데이터베이스는 분석 프로그램과 매끄럽게 연동되었습니다."),
    ("sharply", "adv", "날카롭게, 급격하게", "Corporate earnings dropped sharply following the sudden currency devaluation.", "갑작스러운 통화 가치 하락 이후 기업 순이익이 급격하게 감소했습니다."),
    ("significantly", "adv", "상당히, 의미 있게", "The new robotic arms significantly improved warehouse sorting accuracy.", "새 로봇 팔은 물류창고의 분류 정확도를 상당히 향상시켰습니다."),
    ("simultaneously", "adv", "동시에", "The game app launched simultaneously on PC and mobile formats.", "그 게임 앱은 PC와 모바일 플랫폼에 동시에 출시되었습니다."),
    ("specifically", "adv", "구체적으로, 명확히", "The contract specifically assigns copyright ownership to the publisher.", "계약서는 저작권 소유권을 출판사에 명확히 귀속시키고 있습니다."),
    ("strictly", "adv", "엄격히, 오로지", "Visitors are strictly prohibited from photographing lab prototypes.", "방문객은 실험실 시제품을 촬영하는 것이 엄격히 금지됩니다."),
    ("substantially", "adv", "상당히, 실질적으로", "Switching to LED fixtures substantially decreased monthly electric bills.", "LED 조명으로 교체한 후 월간 전기 요금이 상당히 줄어들었습니다."),
    ("successfully", "adv", "성공적으로", "The enterprise successfully raised $50 million in Series B funding.", "그 기업은 시리즈 B 투자에서 5천만 달러 유치에 성공했습니다."),
    ("thoroughly", "adv", "철저하게, 완전히", "Inspectors thoroughly examined every seam of the pressure vessel.", "검사관들은 압력 용기의 모든 이음매를 철저하게 검사했습니다."),
    ("ultimately", "adv", "궁극적으로, 결국", "Customer satisfaction ratings will ultimately dictate the product's longevity.", "고객 만족도 평가는 궁극적으로 제품의 수명을 결정할 것입니다."),
    ("unanimously", "adv", "만장일치로", "The city council voted unanimously to designate the district an enterprise zone.", "시의회는 그 구역을 기업 특구로 지정하는 안을 만장일치로 통과시켰습니다."),
    ("undoubtedly", "adv", "의심할 여지 없이, 틀림없이", "This breakthrough technology is undoubtedly our greatest intellectual asset.", "이 획기적인 기술은 의심할 여지 없이 저희의 가장 큰 지적 자산입니다."),
    ("unexpectedly", "adv", "예기치 않게, 뜻밖에", "Foreign exchange fluctuations unexpectedly boosted fourth quarter margins.", "환율 변동은 뜻밖에 4분기 마진을 증가시켰습니다."),
    ("uniformly", "adv", "균일하게, 일률적으로", "The quality control standard must be applied uniformly across all plants.", "품질 관리 기준은 모든 공장에 균일하게 적용되어야 합니다.")
]

for w, pos, m, ex, ex_ko in more_words:
    if w.lower() not in seen:
        seen.add(w.lower())
        t2.append({
            "Word": w,
            "PartOfSpeech": pos,
            "Meaning": m,
            "Example": ex,
            "ExampleKo": ex_ko,
            "Tier": "2-중급"
        })

print(f"Tier 2 count after adding: {len(t2)}")
t2 = t2[:500]
print(f"Tier 2 final count (capped at 500): {len(t2)}")

with open(r"scripts\toeic_tier2.json", "w", encoding="utf-8") as f:
    json.dump(t2, f, ensure_ascii=False, indent=2)

print("Tier 2 successfully capped at 500!")
