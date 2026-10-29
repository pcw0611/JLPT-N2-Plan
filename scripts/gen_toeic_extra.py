#!/usr/bin/env python3
"""Fill remaining Tier 1 to 500, then generate Tier 2 (500), Tier 3 (500), Grammar (220)."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ======================== TIER 1 REMAINING (~78 more) ========================
with open(r"scripts\toeic_tier1.json","r",encoding="utf-8") as f:
    t1 = json.load(f)
t1_seen = {w["Word"].lower() for w in t1}

t1_add = [
{"Word":"acquaint","PartOfSpeech":"verb","Meaning":"숙지시키다","Example":"New employees should acquaint themselves with company rules.","ExampleKo":"신입 직원은 회사 규정을 숙지해야 합니다.","Tier":"1-기초"},
{"Word":"acquisition","PartOfSpeech":"noun","Meaning":"인수, 취득","Example":"The acquisition of the smaller firm was completed last month.","ExampleKo":"소규모 회사의 인수가 지난달 완료되었습니다.","Tier":"1-기초"},
{"Word":"adapt","PartOfSpeech":"verb","Meaning":"적응하다","Example":"We need to adapt quickly to changes in the market.","ExampleKo":"시장 변화에 신속하게 적응해야 합니다.","Tier":"1-기초"},
{"Word":"adopt","PartOfSpeech":"verb","Meaning":"채택하다","Example":"The company adopted a new work-from-home policy.","ExampleKo":"회사가 새 재택근무 정책을 채택했습니다.","Tier":"1-기초"},
{"Word":"affordable","PartOfSpeech":"adjective","Meaning":"저렴한","Example":"The restaurant is known for its affordable menu.","ExampleKo":"그 레스토랑은 저렴한 메뉴로 알려져 있습니다.","Tier":"1-기초"},
{"Word":"aim","PartOfSpeech":"noun/verb","Meaning":"목표; 목표로 하다","Example":"The company aims to double its revenue within five years.","ExampleKo":"회사는 5년 내 매출을 두 배로 늘리는 것을 목표로 합니다.","Tier":"1-기초"},
{"Word":"anniversary","PartOfSpeech":"noun","Meaning":"기념일","Example":"The company is celebrating its 50th anniversary.","ExampleKo":"회사가 창립 50주년을 기념하고 있습니다.","Tier":"1-기초"},
{"Word":"anonymous","PartOfSpeech":"adjective","Meaning":"익명의","Example":"The survey responses are completely anonymous.","ExampleKo":"설문 응답은 완전히 익명입니다.","Tier":"1-기초"},
{"Word":"archive","PartOfSpeech":"noun/verb","Meaning":"보관소; 보관하다","Example":"Old files are stored in the company archive.","ExampleKo":"오래된 파일은 회사 보관소에 저장됩니다.","Tier":"1-기초"},
{"Word":"assurance","PartOfSpeech":"noun","Meaning":"보증, 확신","Example":"We give our assurance that all data will be kept secure.","ExampleKo":"모든 데이터가 안전하게 보관될 것임을 보장합니다.","Tier":"1-기초"},
{"Word":"belongings","PartOfSpeech":"noun","Meaning":"소지품","Example":"Please keep your personal belongings with you at all times.","ExampleKo":"개인 소지품을 항상 가지고 계세요.","Tier":"1-기초"},
{"Word":"blueprint","PartOfSpeech":"noun","Meaning":"설계도","Example":"The architect presented the blueprint for the new building.","ExampleKo":"건축가가 새 건물의 설계도를 발표했습니다.","Tier":"1-기초"},
{"Word":"clarify","PartOfSpeech":"verb","Meaning":"명확히 하다","Example":"Could you clarify the payment terms in the contract?","ExampleKo":"계약서의 지불 조건을 명확히 해주시겠어요?","Tier":"1-기초"},
{"Word":"commerce","PartOfSpeech":"noun","Meaning":"상업","Example":"E-commerce has grown rapidly in recent years.","ExampleKo":"전자상거래가 최근 몇 년간 급속히 성장했습니다.","Tier":"1-기초"},
{"Word":"commute","PartOfSpeech":"verb/noun","Meaning":"통근하다; 통근","Example":"Many employees commute by train.","ExampleKo":"많은 직원이 기차로 통근합니다.","Tier":"1-기초"},
{"Word":"consensus","PartOfSpeech":"noun","Meaning":"합의","Example":"The committee reached a consensus on the new policy.","ExampleKo":"위원회가 새 정책에 대한 합의에 도달했습니다.","Tier":"1-기초"},
{"Word":"delegate","PartOfSpeech":"verb/noun","Meaning":"위임하다; 대표","Example":"Managers should delegate tasks to team members.","ExampleKo":"매니저는 팀원에게 업무를 위임해야 합니다.","Tier":"1-기초"},
{"Word":"demographic","PartOfSpeech":"noun/adj","Meaning":"인구 통계(의)","Example":"The campaign targets a younger demographic.","ExampleKo":"캠페인은 젊은 인구 집단을 대상으로 합니다.","Tier":"1-기초"},
{"Word":"detect","PartOfSpeech":"verb","Meaning":"감지하다","Example":"The system can detect any security threats.","ExampleKo":"시스템이 모든 보안 위협을 감지할 수 있습니다.","Tier":"1-기초"},
{"Word":"diploma","PartOfSpeech":"noun","Meaning":"졸업장","Example":"A diploma in business administration is preferred.","ExampleKo":"경영학 졸업장이 선호됩니다.","Tier":"1-기초"},
{"Word":"drawback","PartOfSpeech":"noun","Meaning":"단점","Example":"One drawback of the plan is the high cost.","ExampleKo":"이 계획의 한 가지 단점은 높은 비용입니다.","Tier":"1-기초"},
{"Word":"duration","PartOfSpeech":"noun","Meaning":"기간","Example":"The duration of the training is three weeks.","ExampleKo":"교육 기간은 3주입니다.","Tier":"1-기초"},
{"Word":"elaborate","PartOfSpeech":"adjective/verb","Meaning":"정교한; 자세히 설명하다","Example":"Could you elaborate on your proposal?","ExampleKo":"제안에 대해 더 자세히 설명해 주시겠어요?","Tier":"1-기초"},
{"Word":"endorse","PartOfSpeech":"verb","Meaning":"보증하다, 지지하다","Example":"Several celebrities endorsed the new product.","ExampleKo":"여러 유명인이 새 제품을 지지했습니다.","Tier":"1-기초"},
{"Word":"enforce","PartOfSpeech":"verb","Meaning":"시행하다, 집행하다","Example":"The new parking rules will be strictly enforced.","ExampleKo":"새 주차 규정이 엄격히 시행될 것입니다.","Tier":"1-기초"},
{"Word":"enhance","PartOfSpeech":"verb","Meaning":"향상시키다","Example":"New lighting was installed to enhance the workspace.","ExampleKo":"작업 공간을 향상시키기 위해 새 조명이 설치되었습니다.","Tier":"1-기초"},
{"Word":"entrepreneur","PartOfSpeech":"noun","Meaning":"기업가","Example":"The entrepreneur founded three successful companies.","ExampleKo":"그 기업가는 성공적인 회사 3개를 설립했습니다.","Tier":"1-기초"},
{"Word":"evenly","PartOfSpeech":"adverb","Meaning":"고르게, 균등하게","Example":"Tasks should be distributed evenly among team members.","ExampleKo":"업무는 팀원들에게 균등하게 분배되어야 합니다.","Tier":"1-기초"},
{"Word":"fiscal","PartOfSpeech":"adjective","Meaning":"회계의, 재정의","Example":"The fiscal year ends in March.","ExampleKo":"회계연도는 3월에 끝납니다.","Tier":"1-기초"},
{"Word":"fluctuate","PartOfSpeech":"verb","Meaning":"변동하다","Example":"Stock prices tend to fluctuate throughout the day.","ExampleKo":"주가는 하루 동안 변동하는 경향이 있습니다.","Tier":"1-기초"},
{"Word":"grateful","PartOfSpeech":"adjective","Meaning":"감사하는","Example":"We are grateful for your continued support.","ExampleKo":"계속적인 지원에 감사드립니다.","Tier":"1-기초"},
{"Word":"hazard","PartOfSpeech":"noun","Meaning":"위험 요소","Example":"Fire hazards must be removed from the workplace.","ExampleKo":"화재 위험 요소는 작업장에서 제거해야 합니다.","Tier":"1-기초"},
{"Word":"hesitant","PartOfSpeech":"adjective","Meaning":"주저하는","Example":"Some investors were hesitant to commit funds.","ExampleKo":"일부 투자자들은 자금 투입을 주저했습니다.","Tier":"1-기초"},
{"Word":"imply","PartOfSpeech":"verb","Meaning":"암시하다","Example":"The data implies that consumer spending is declining.","ExampleKo":"데이터는 소비자 지출이 감소하고 있음을 암시합니다.","Tier":"1-기초"},
{"Word":"incentive","PartOfSpeech":"noun","Meaning":"인센티브, 장려금","Example":"The company offers incentives for meeting sales targets.","ExampleKo":"회사는 매출 목표 달성에 대한 인센티브를 제공합니다.","Tier":"1-기초"},
{"Word":"incur","PartOfSpeech":"verb","Meaning":"초래하다, 발생시키다","Example":"Late payments may incur additional fees.","ExampleKo":"연체 지불 시 추가 수수료가 발생할 수 있습니다.","Tier":"1-기초"},
{"Word":"integral","PartOfSpeech":"adjective","Meaning":"필수적인","Example":"Teamwork is an integral part of our company culture.","ExampleKo":"팀워크는 저희 기업 문화의 필수적인 부분입니다.","Tier":"1-기초"},
{"Word":"justify","PartOfSpeech":"verb","Meaning":"정당화하다","Example":"You must justify the additional expense with documentation.","ExampleKo":"추가 비용을 서류로 정당화해야 합니다.","Tier":"1-기초"},
{"Word":"markedly","PartOfSpeech":"adverb","Meaning":"현저히","Example":"Customer complaints have decreased markedly.","ExampleKo":"고객 불만이 현저히 감소했습니다.","Tier":"1-기초"},
{"Word":"mentorship","PartOfSpeech":"noun","Meaning":"멘토링","Example":"The company has a mentorship program for new employees.","ExampleKo":"회사에 신입 직원을 위한 멘토링 프로그램이 있습니다.","Tier":"1-기초"},
{"Word":"milestone","PartOfSpeech":"noun","Meaning":"이정표, 중요 시점","Example":"Reaching 1 million users was a major milestone.","ExampleKo":"사용자 100만 명 달성은 주요 이정표였습니다.","Tier":"1-기초"},
{"Word":"morale","PartOfSpeech":"noun","Meaning":"사기","Example":"Employee morale improved after the salary increase.","ExampleKo":"급여 인상 후 직원 사기가 향상되었습니다.","Tier":"1-기초"},
{"Word":"negotiate","PartOfSpeech":"verb","Meaning":"협상하다","Example":"We negotiated a better deal with the supplier.","ExampleKo":"공급업체와 더 나은 거래를 협상했습니다.","Tier":"1-기초"},
{"Word":"nominal","PartOfSpeech":"adjective","Meaning":"명목상의, 적은","Example":"There is a nominal fee for the service.","ExampleKo":"서비스에 소액의 수수료가 있습니다.","Tier":"1-기초"},
{"Word":"obligate","PartOfSpeech":"verb","Meaning":"의무를 지우다","Example":"The contract obligates both parties to fulfill their roles.","ExampleKo":"계약은 양측에 각자의 역할을 이행할 의무를 지웁니다.","Tier":"1-기초"},
{"Word":"occasionally","PartOfSpeech":"adverb","Meaning":"가끔","Example":"The CEO occasionally visits the regional offices.","ExampleKo":"CEO는 가끔 지역 사무소를 방문합니다.","Tier":"1-기초"},
{"Word":"overwhelm","PartOfSpeech":"verb","Meaning":"압도하다","Example":"The customer service team was overwhelmed with inquiries.","ExampleKo":"고객 서비스 팀이 문의로 압도당했습니다.","Tier":"1-기초"},
{"Word":"payroll","PartOfSpeech":"noun","Meaning":"급여 대장","Example":"Payroll will be processed on the 25th of each month.","ExampleKo":"급여는 매월 25일에 처리됩니다.","Tier":"1-기초"},
{"Word":"pedestrian","PartOfSpeech":"noun","Meaning":"보행자","Example":"A new pedestrian crossing was added near the office.","ExampleKo":"사무실 근처에 새 횡단보도가 추가되었습니다.","Tier":"1-기초"},
{"Word":"plumber","PartOfSpeech":"noun","Meaning":"배관공","Example":"A plumber was called to fix the leak in the office.","ExampleKo":"사무실 누수를 수리하기 위해 배관공이 호출되었습니다.","Tier":"1-기초"},
{"Word":"premiere","PartOfSpeech":"noun","Meaning":"첫 공개, 초연","Example":"The product premiere attracted major media coverage.","ExampleKo":"제품 첫 공개가 주요 언론의 관심을 끌었습니다.","Tier":"1-기초"},
{"Word":"prevalent","PartOfSpeech":"adjective","Meaning":"널리 퍼진","Example":"Remote work has become more prevalent since 2020.","ExampleKo":"2020년 이후 재택근무가 더 널리 퍼졌습니다.","Tier":"1-기초"},
{"Word":"proofread","PartOfSpeech":"verb","Meaning":"교정하다","Example":"Please proofread the document before printing.","ExampleKo":"인쇄 전에 문서를 교정해 주세요.","Tier":"1-기초"},
{"Word":"punctual","PartOfSpeech":"adjective","Meaning":"시간을 잘 지키는","Example":"Employees are expected to be punctual.","ExampleKo":"직원들은 시간을 잘 지킬 것이 기대됩니다.","Tier":"1-기초"},
{"Word":"questionnaire","PartOfSpeech":"noun","Meaning":"설문지","Example":"Please complete the questionnaire and return it.","ExampleKo":"설문지를 작성하고 반환해 주세요.","Tier":"1-기초"},
{"Word":"receptionist","PartOfSpeech":"noun","Meaning":"접수 담당자","Example":"The receptionist will direct you to the meeting room.","ExampleKo":"접수 담당자가 회의실로 안내해 드립니다.","Tier":"1-기초"},
{"Word":"reimburse","PartOfSpeech":"verb","Meaning":"환급하다","Example":"All approved expenses will be reimbursed promptly.","ExampleKo":"승인된 모든 경비는 신속히 환급됩니다.","Tier":"1-기초"},
{"Word":"renovation","PartOfSpeech":"noun","Meaning":"개보수","Example":"The store will reopen after renovation in September.","ExampleKo":"가게는 9월 개보수 후 재개장합니다.","Tier":"1-기초"},
{"Word":"renew","PartOfSpeech":"verb","Meaning":"갱신하다","Example":"Please renew your membership before it expires.","ExampleKo":"만료 전에 회원권을 갱신해 주세요.","Tier":"1-기초"},
{"Word":"respectively","PartOfSpeech":"adverb","Meaning":"각각","Example":"Tokyo and Seoul had 12 and 15 percent growth, respectively.","ExampleKo":"도쿄와 서울은 각각 12%와 15% 성장했습니다.","Tier":"1-기초"},
{"Word":"retail","PartOfSpeech":"noun","Meaning":"소매","Example":"The company operates over 200 retail stores.","ExampleKo":"회사는 200개 이상의 소매점을 운영하고 있습니다.","Tier":"1-기초"},
{"Word":"scarce","PartOfSpeech":"adjective","Meaning":"부족한, 드문","Example":"Skilled workers are becoming increasingly scarce.","ExampleKo":"숙련된 노동자가 점점 부족해지고 있습니다.","Tier":"1-기초"},
{"Word":"scrutinize","PartOfSpeech":"verb","Meaning":"면밀히 조사하다","Example":"Auditors will scrutinize the company's financial records.","ExampleKo":"감사관이 회사의 재무 기록을 면밀히 조사할 것입니다.","Tier":"1-기초"},
{"Word":"setback","PartOfSpeech":"noun","Meaning":"차질","Example":"The project experienced a minor setback due to bad weather.","ExampleKo":"악천후로 인해 프로젝트에 사소한 차질이 있었습니다.","Tier":"1-기초"},
{"Word":"simultaneously","PartOfSpeech":"adverb","Meaning":"동시에","Example":"The product was launched simultaneously in three countries.","ExampleKo":"제품이 3개국에서 동시에 출시되었습니다.","Tier":"1-기초"},
{"Word":"souvenir","PartOfSpeech":"noun","Meaning":"기념품","Example":"Souvenirs are available in the gift shop on the first floor.","ExampleKo":"1층 선물 가게에서 기념품을 구입할 수 있습니다.","Tier":"1-기초"},
{"Word":"specification","PartOfSpeech":"noun","Meaning":"사양, 명세","Example":"The product specifications are listed on the website.","ExampleKo":"제품 사양은 웹사이트에 나와 있습니다.","Tier":"1-기초"},
{"Word":"sponsor","PartOfSpeech":"noun/verb","Meaning":"후원자; 후원하다","Example":"The event was sponsored by a local bank.","ExampleKo":"행사는 지역 은행이 후원했습니다.","Tier":"1-기초"},
{"Word":"statistics","PartOfSpeech":"noun","Meaning":"통계","Example":"Recent statistics show a decline in unemployment.","ExampleKo":"최근 통계는 실업률 감소를 보여줍니다.","Tier":"1-기초"},
{"Word":"stringent","PartOfSpeech":"adjective","Meaning":"엄격한","Example":"The company has stringent quality control measures.","ExampleKo":"회사는 엄격한 품질 관리 조치를 시행합니다.","Tier":"1-기초"},
{"Word":"surpass","PartOfSpeech":"verb","Meaning":"능가하다","Example":"Revenue surpassed expectations by 20 percent.","ExampleKo":"수익이 예상치를 20% 능가했습니다.","Tier":"1-기초"},
{"Word":"tenant","PartOfSpeech":"noun","Meaning":"세입자","Example":"Tenants must give 30 days notice before moving out.","ExampleKo":"세입자는 이사 전 30일 전에 통보해야 합니다.","Tier":"1-기초"},
{"Word":"thorough","PartOfSpeech":"adjective","Meaning":"철저한","Example":"Please conduct a thorough review of the data.","ExampleKo":"데이터에 대한 철저한 검토를 수행해 주세요.","Tier":"1-기초"},
{"Word":"toll-free","PartOfSpeech":"adjective","Meaning":"수신자 부담의","Example":"Call our toll-free number for customer support.","ExampleKo":"고객 지원을 위해 수신자 부담 번호로 전화하세요.","Tier":"1-기초"},
{"Word":"turnover","PartOfSpeech":"noun","Meaning":"이직률; 매출액","Example":"Employee turnover has been high this year.","ExampleKo":"올해 직원 이직률이 높았습니다.","Tier":"1-기초"},
{"Word":"unanimous","PartOfSpeech":"adjective","Meaning":"만장일치의","Example":"The board made a unanimous decision to approve the plan.","ExampleKo":"이사회가 만장일치로 계획을 승인했습니다.","Tier":"1-기초"},
{"Word":"venture","PartOfSpeech":"noun","Meaning":"벤처, 사업","Example":"The joint venture was announced at the press conference.","ExampleKo":"합작 사업이 기자 회견에서 발표되었습니다.","Tier":"1-기초"},
{"Word":"warranty","PartOfSpeech":"noun","Meaning":"보증","Example":"Extended warranty options are available at checkout.","ExampleKo":"계산 시 연장 보증 옵션을 이용할 수 있습니다.","Tier":"1-기초"},
{"Word":"worthwhile","PartOfSpeech":"adjective","Meaning":"가치 있는","Example":"The investment turned out to be very worthwhile.","ExampleKo":"투자가 매우 가치 있는 것으로 판명되었습니다.","Tier":"1-기초"},
]

for w in t1_add:
    k = w["Word"].lower()
    if k not in t1_seen:
        t1_seen.add(k)
        t1.append(w)

t1 = t1[:500]
print(f"Tier 1: {len(t1)} words")
with open(r"scripts\toeic_tier1.json","w",encoding="utf-8") as f:
    json.dump(t1, f, ensure_ascii=False, indent=2)
print("Tier 1 saved.")
