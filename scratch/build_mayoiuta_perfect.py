import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Smart romaji distributor for charRomaji
def make_line(ja, romaji, ko, char_romaji=None):
    clean_ro = romaji.lower().replace(" ", "")
    # Strip spaces from ja for typing mapping, or keep ja for display
    # In typing page: currentLine.ja is displayed, charRomaji is per character of currentLine.ja
    # If ja has spaces, we should distribute over ja characters!
    if char_romaji is None:
        char_romaji = []
        pos = 0
        ja_len = len(ja)
        for i, ch in enumerate(ja):
            if ch == ' ' or ch == '　' or ch == '？' or ch == '?' or ch == '・':
                char_romaji.append('')
                continue
            remaining_ja = len([c for c in ja[i:] if c not in (' ', '　', '？', '?', '・')])
            remaining_ro = len(clean_ro) - pos
            take = max(1, round(remaining_ro / max(1, remaining_ja)))
            if remaining_ja == 1:
                take = remaining_ro
            char_romaji.append(clean_ro[pos:pos+take])
            pos += take
    return {
        "ja": ja,
        "romaji": clean_ro,
        "ko": ko,
        "charRomaji": char_romaji
    }

part1_lines = [
    make_line("交差点の真ん中 急ぐ人に紛れて", "kousatennomannakaisoguhitonimagirete", "교차로 한가운데 바쁘게 스쳐 가는 사람들 속에"),
    make_line("僕だけがあてもなく 漂うみたいだ", "bokudakegaatemonakutadayoumitaida", "나만 혼자 갈 곳 없이 떠도는 것 같아"),
    make_line("流行りの歌はいつも 僕のことは歌ってない", "hayarinoutahaitsumobokunokotohautattenai", "유행하는 노래들은 늘 나와는 상관 없는 이야기 같아"),
    make_line("ねえビジョンの中から 笑いかけないで", "neebijonnonakakarawaraikakenaide", "저기, 화면 속에서 웃지 말아줘"),
    make_line("また今日も声にならずに 飲み込んだ感情", "matakyoumokoeninarazuninomikondakanjou", "오늘도 또 입 밖으로 꺼내지 못하고 삼켜버린 감정들"),
    make_line("下書き埋め尽くして", "shitagakiumetsukushite", "글로만 적어내려가며"),
    make_line("ああ そうやって何千回夜を越える", "aasouyattenanzenkaiyoruwokoeru", "아아, 그렇게 몇 천 번의 밤을 보냈어"),
    make_line("僕のため それだけ それだけだったんだよ", "bokunotamesoredakesoredakedattandayo", "나를 위해, 그것뿐, 그것뿐이었어"),
    make_line("出口探し 溢れただけの言葉", "deguchisagashikoboretadakenokotoba", "출구를 찾아 헤매다 쏟아져 넘쳐버린 말들"),
    make_line("君の心へ届いて 隙間をちょっと埋めるなら", "kiminokokorohetodoitesukimawochottoumerunara", "만약 너의 마음에 닿아서 텅 빈 틈을 조금이라도 채울 수 있다면"),
    make_line("こんな僕でも ここにいる 叫ぶよ", "konnabokudemokokoniirusakebuyo", "이런 나라도 여기에 있다고 외칠게"),
    make_line("迷い星のうた", "mayoihoshinouta", "길잃은 별의 노래"),
]

part2_lines = [
    make_line("問われることは何故か 将来のことばかり", "towarerukotohanazekashourainokotobakari", "왜인지 사람들은 늘 내 장래에 대해서만 묻곤 해"),
    make_line("目の前にいる僕の 今はおざなりで", "menomaeniirubokunoimawaozanaride", "눈앞에 있는 지금의 나는 뒷전인 채로"),
    make_line("華やぎに馴染めない この心を無視して", "hanayagininajimenaikonokokorowomushishite", "화려함에 어울리지 못하는 이 마음을 외면하면서"),
    make_line("輝かしい明日を 推奨しないでくれ", "kagayakashiiashitawosuishoushinaidekure", "찬란한 내일만 강요하지 말아줘"),
    make_line("夜空にチカチカ光る 頼りない星屑", "yozoranichikachikahikarutayorinaihoshikuzu", "밤하늘에 반짝반짝 빛나는 의지할 수 없는 작은 별들"),
    make_line("躊躇いながらはぐれて", "tamerainagarahagurete", "망설이다가 길을 잃고"),
    make_line("ああ 彷徨っているそれが僕", "aasamayotteirusoregaboku", "아아, 그렇게 헤매는 게 바로 나야"),
    make_line("僕になる それしか それしかできないだろう", "bokuninarusoreshikasoreshikadekinaidarou", "나 자신이 될 거야, 그것밖에, 그것밖에 할 수 없잖아"),
    make_line("誰の真似も 上手くやれないんだ", "darenomanemoumakuyarenainda", "누구처럼 되는 것도 제대로 할 수 없어"),
    make_line("こんな痛い日々をなんで 退屈だって片付ける？", "konnaitaihibiwonandetaikutsudattekatazukeru", "이 고통스러운 날들을 어떻게 지루하다고 넘길 수 있겠어?"),
    make_line("よろめきながらでも もがいているんだよ", "yoromekinagarademomogaiteirundayo", "비틀거리면서도 발버둥치고 있는 거야"),
    make_line("迷い星のうた", "mayoihoshinouta", "길잃은 별의 노래"),
]

part3_lines = [
    make_line("僕のため それだけ それだけだったんだよ", "bokunotamesoredakesoredakedattandayo", "나를 위해, 그것뿐, 그것뿐이었어"),
    make_line("涙流し やっと生まれた言葉", "namidanagashiyattoumaretakotoba", "눈물을 흘려 간신히 태어난 말들"),
    make_line("どこかで同じように ヒリヒリする胸抱えて", "dokokadeonajiyounihirihirisurumunekakaete", "어디선가 나처럼 아픈 마음을 안고"),
    make_line("震える君に 僕もいる 叫ぶよ", "furuerukiminibokumoirusakebuyo", "떨고 있을 너에게 나도 여기 있다고 외칠게"),
    make_line("迷い星のうた", "mayoihoshinouta", "길잃은 별의 노래"),
]

full_lines = part1_lines + part2_lines + part3_lines

mayoiuta_obj = {
    "id": "mayoiuta",
    "title": "迷星叫",
    "reading": "まよいうた",
    "category": "original",
    "album": "1st Single『迷星叫』, 1st Album『迷跡波』",
    "youtubeId": "w-Gvclnnfpc",
    "parts": [
        {
            "id": "part1",
            "name": "Part 1 (前半・1番)",
            "lines": part1_lines
        },
        {
            "id": "part2",
            "name": "Part 2 (後半・2番)",
            "lines": part2_lines
        },
        {
            "id": "part3",
            "name": "Part 3 (ラスト・Cメロ~完走)",
            "lines": part3_lines
        },
        {
            "id": "full",
            "name": "Part 4 (★全曲フル完走★)",
            "lines": full_lines
        }
    ]
}

print(f"Part 1 lines: {len(part1_lines)}")
print(f"Part 2 lines: {len(part2_lines)}")
print(f"Part 3 lines: {len(part3_lines)}")
print(f"Full lines: {len(full_lines)}")

with open('scratch/mayoiuta_perfect.json', 'w', encoding='utf-8') as f:
    json.dump(mayoiuta_obj, f, ensure_ascii=False, indent=2)

print("Saved to scratch/mayoiuta_perfect.json successfully!")
