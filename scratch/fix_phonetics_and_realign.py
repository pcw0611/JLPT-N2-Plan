import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m_pre = re.search(r'^(.*?export const SONGS:\s*Song\[\]\s*=\s*)', text, re.DOTALL)
preamble = m_pre.group(1)

m_json = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
songs = json.loads(m_json.group(1))

# Dictionary of line corrections
# (song_id, ja_substring): new_romaji
CORRECTIONS = {
    ('mayoiuta', '交差点の真ん中急ぐ人に紛れて'): 'kousatennomannakaisoguhitonimagirete',
    ('haruhikage', '悴んだ心ふるえる眼差し'): 'kajikandakokorofuruerumanazashi',
    ('swim', '息を切らして笑い合える日まで'): 'ikiwokirashitewaraiaeruhimade',
    ('kageiromai', '前衛的シルエットダンス'): 'konrinzaidaremoshiranaiyorubokunoyazeneitekishiruettodansu',
    ('hitoshizuku', 'ビニール越しの空からこぼれ落ちる音響いて'): 'biniirukoshinosorakarakoboreochiruotohibiite',
    ('shiori', '不器用で空回って傷つくことから逃げている'): 'bukiyoudekaramawatteikizutsukukotokaranigeteiru',
    ('shiori', '人の顔色を窺いながら流されるままに衣食住'): 'hitonokaoirowoukagainagaranagasarerumamaniishokujuu',
    ('tanebi', '言葉になんてしたところで戸惑う人の目が怖かった'): 'kotobaninanteshitatokorodetomadouhitonomegakowakatta',
    ('hekitenbansou', '十分君はもう頑張ってる'): 'juubunkimihamouganbatteru',
    ('utaimashou', '心臓の音響かせて'): 'shinzounootohibikasete',
    ('noroshi', '僕と君なのに叫びたい想いが重なる'): 'bokutokiminanonisakebitaiomoigakasanaru',
    ('kaisoufu', '幾重にも重なる想いの層を突き破り'): 'ikuenimokasanaruomoinosouwotsukiyaburi',
    ('egakumirai', '意地悪な人の空に'): 'ijiwarunahitonosorani',
    ('nisokuhokou', 'ねえママ僕好きな人が出来たんだ'): 'neemamabokusukinahitogadekitanda',
    ('moshimoinochi', '大切な人を笑顔にするため'): 'taisetsunahitowoegaonisurutame',
}

from test_all_989_lines import align_line_to_romaji

corrected_count = 0
for s in songs:
    s_id = s['id']
    for p in s['parts']:
        for line in p['lines']:
            ja = line['ja']
            for (cid, cja), new_ro in CORRECTIONS.items():
                if cid == s_id and cja in ja:
                    print(f"Correcting [{s_id}] {ja}:")
                    print(f"  Old RO: {line['romaji']}")
                    print(f"  New RO: {new_ro}")
                    line['romaji'] = new_ro
                    corrected_count += 1
            # Recompute charRomaji
            cr = align_line_to_romaji(line['ja'], line['romaji'])
            assert len(cr) == len(line['ja']), f"Length mismatch on {line['ja']}"
            assert "".join(cr) == line['romaji'], f"Content mismatch on {line['ja']}"
            line['charRomaji'] = cr

print(f"Successfully applied {corrected_count} phonetic corrections and realigned all lines!")

new_songs_ts = preamble + json.dumps(songs, ensure_ascii=False, indent=2) + ";\n"
with open('jlpt-calendar-site/app/typing/songs.ts', 'w', encoding='utf-8') as f:
    f.write(new_songs_ts)

print("Saved updated songs.ts!")
