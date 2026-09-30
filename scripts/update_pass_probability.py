import sqlite3

def update_probability():
    conn = sqlite3.connect('database/jlpt_learning.db')
    c = conn.cursor()

    c.execute('DELETE FROM pass_probability_snapshots WHERE snapshot_date="2026-09-30"')

    reason_n2 = '[2026-09-30 제2회 실전모의고사(2023.12 기출 102문항) 완주 및 Voca 전 덱 완독 반영] 1) 제2회 기출 완본 실전모의고사 92/180점 합격 및 전 영역 과락 0건 달성. 역대 최고 난이도 불시험에서도 과락 없이 합격선을 방어함으로써 합격 하방 안전마진(Floor)을 실증. 2) 9/20 제1회(119점, 표준 난이도)와 이번 제2회(92점, 최상 난이도) 2회 연속 완본 실전 합격 실측치 확보로 통계적 신뢰도를 medium에서 high로 상향. 3) JLPT 한끝 Voca N5·N4·N3·N2 전권 미학습 0장 100% 완독 기반 확립. 현재 시점 합격 범위 55~72%(중간값 63.5%, +10~12%p), 12월 본시험 합격률 82%(+7%p)로 상향 조정.'
    reason_n3 = '[2026-09-30] N3 완독 및 N2 연속 합격 반영으로 N3 합격 확실성 96% 도달.'

    c.execute('''
        INSERT INTO pass_probability_snapshots (
            snapshot_date, level, current_low_pct, current_high_pct, projected_exam_pct, daily_change_pp, confidence, reason
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('2026-09-30', 'N2', 55.0, 72.0, 82.0, 7.0, 'high', reason_n2))

    c.execute('''
        INSERT INTO pass_probability_snapshots (
            snapshot_date, level, current_low_pct, current_high_pct, projected_exam_pct, daily_change_pp, confidence, reason
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('2026-09-30', 'N3', 75.0, 90.0, 96.0, 11.0, 'high', reason_n3))

    conn.commit()
    conn.close()
    print('Successfully inserted 2026-09-30 pass probability snapshots!')

if __name__ == '__main__':
    update_probability()
