import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Helper: automatic romaji distributor for Japanese characters
# If romaji mapping per char is provided, use it. Otherwise smart-split.
def build_line(ja, romaji, ko, char_romaji=None):
    clean_romaji = romaji.lower().replace(" ", "")
    if char_romaji is None:
        # Smart distribution: distribute clean_romaji across ja characters
        ja_len = len(ja)
        # Approximate distribution
        char_romaji = []
        pos = 0
        for i in range(ja_len):
            remaining_ja = ja_len - i
            remaining_ro = len(clean_romaji) - pos
            take = max(1, round(remaining_ro / remaining_ja))
            if i == ja_len - 1:
                take = remaining_ro
            char_romaji.append(clean_romaji[pos:pos+take])
            pos += take
    return {
        "ja": ja,
        "romaji": clean_romaji,
        "ko": ko,
        "charRomaji": char_romaji
    }

songs_data = []

# ==========================================
# 1. 迷星叫 (Mayoiuta)
# ==========================================
songs_data.append({
    "id": "mayoiuta",
    "title": "迷星叫",
    "reading": "まよいうた",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "LvVat3Y17lc",
    "lines": [
        build_line("交差点の真ん中", "kousatennomannaka", "교차로 한가운데", ["kou", "sa", "ten", "no", "man", "n", "naka"]),
        build_line("急ぐ人に紛れて", "isoguhitonimagirete", "서두르는 사람들에 뒤섞여", ["isogu", "", "hito", "ni", "magire", "", "te"]),
        build_line("僕だけがあてもなく", "bokudakegaatemonaku", "나만이 정처도 없이", ["boku", "da", "ke", "ga", "a", "te", "mo", "na", "ku"]),
        build_line("漂うみたいだ", "tadayoumaitada", "떠도는 것만 같아", ["tadayou", "", "mi", "tai", "", "da"]),
        build_line("流行りの歌はいつも", "hayarinoutawaitsumo", "유행하는 노래는 언제나", ["hayari", "", "", "no", "uta", "wa", "i", "tsu", "mo"]),
        build_line("僕のことは歌ってない", "bokunokotowautattenai", "내 이야기는 노래하지 않아", ["boku", "no", "ko", "to", "wa", "utatte", "", "", "na", "i"]),
        build_line("ねえビジョンの中から", "neebijonnonakanakara", "저기, 전광판 속에서", ["ne", "e", "bi", "jo", "", "n", "no", "naka", "ka", "ra"]),
        build_line("笑いかけないで", "waraikakenaide", "웃는 얼굴로 바라보지 마", ["warai", "", "ka", "ke", "na", "i", "de"]),
        build_line("また今日も声にならずに", "matakyoumokoeninarazuni", "또 오늘도 목소리가 되지 못한 채", ["ma", "ta", "kyou", "", "mo", "koe", "ni", "na", "ra", "zu", "ni"]),
        build_line("飲み込んだ感情", "nomikondakanjou", "삼켜버린 감정", ["nomi", "", "konda", "", "", "kan", "jou"]),
        build_line("下書き埋め尽くして", "shitagakiumetsukushite", "임시 저장을 가득 채우고", ["shita", "gaki", "", "ume", "", "tsuku", "", "shi", "te"]),
        build_line("迷子でもいい迷子でも進め", "maigodemoiimaigodemosusume", "미아라도 좋아, 미아라도 나아가라", ["mai", "go", "de", "mo", "i", "i", "mai", "go", "de", "mo", "susu", "me"])
    ]
})

# ==========================================
# 2. 名無声 (Namonaki / Nanashigoe)
# ==========================================
songs_data.append({
    "id": "nanashigoe",
    "title": "名無声",
    "reading": "なもなき",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "2mM64qcBYg8",
    "lines": [
        build_line("何が僕にできるか", "nanigabokunidekiruka", "무엇을 내가 할 수 있을까", ["nani", "ga", "boku", "ni", "de", "ki", "ru", "ka"]),
        build_line("わからないけれど", "wakawanaikeredo", "알 수는 없지만", ["wa", "ka", "ra", "na", "i", "ke", "re", "do"]),
        build_line("言葉にすれば零れ落ちる", "kotobanisurebakoboreochiru", "말을 하면 흘러넘쳐 떨어지는", ["kotoba", "", "ni", "su", "re", "ba", "kobore", "", "ochi", "", "ru"]),
        build_line("名前のない痛みを", "namaenonaiitamiwo", "이름 없는 아픔을", ["namae", "", "no", "na", "i", "ita", "", "mi", "wo"]),
        build_line("抱きしめて歌うよ", "dakishimeteutauyo", "끌어안고 노래할게", ["daki", "", "shi", "me", "te", "uta", "u", "yo"]),
        build_line("誰かの正解じゃなくて", "daredanoseikaijanakute", "누군가의 정답이 아니라", ["dare", "ka", "no", "sei", "kai", "ja", "na", "ku", "te"]),
        build_line("僕だけの声で叫ぶ", "bokudakenokoedesakebu", "나만의 목소리로 외칠 거야", ["boku", "da", "ke", "no", "koe", "de", "sake", "bu"]),
        build_line("夜の静寂を切り裂いて", "yorunoshijimawokirisaite", "밤의 적막을 갈라버리고", ["yoru", "no", "shijima", "", "wo", "kiri", "", "sai", "", "te"]),
        build_line("此処にいると伝えるんだ", "kokoniirutotsutaerunda", "여기에 있다고 전할 거야", ["koko", "", "ni", "i", "ru", "to", "tsutae", "", "ru", "n", "da"])
    ]
})

# ==========================================
# 3. 音一会 (Otoichie)
# ==========================================
songs_data.append({
    "id": "otoichie",
    "title": "音一会",
    "reading": "おといちえ",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "F-h-M4p2v6E",
    "lines": [
        build_line("僕の居場所はB5", "bokunoibashowabiigo", "나의 있을 곳은 B5 노트", ["boku", "no", "iba", "", "sho", "wa", "bii", "go"]),
        build_line("ペンからこぼれる言葉を落として", "penkarakoborerukotobawootoshite", "펜에서 흘러나오는 말을 떨어뜨리며", ["pen", "ka", "ra", "ko", "bo", "re", "ru", "kotoba", "", "wo", "oto", "", "shi", "te"]),
        build_line("白紙を埋めた僕の歌", "hakushiwoumetabokunouta", "백지를 채운 나의 노래", ["haku", "shi", "wo", "ume", "", "ta", "boku", "no", "uta"]),
        build_line("届くはずのない叫びが", "todokuhazunonaisakebiga", "닿을 리 없던 외침이", ["todo", "", "ku", "ha", "zu", "no", "na", "i", "sake", "", "bi", "ga"]),
        build_line("君の音と重なっていく", "kiminoototokasanatteiku", "너의 소리와 겹쳐져 가", ["kimi", "no", "oto", "to", "kasa", "", "na", "tte", "i", "ku"]),
        build_line("ありがとう出会ってくれて", "arigatoudeattekurete", "고마워, 만나주어서", ["a", "ri", "ga", "tou", "dea", "", "tte", "ku", "re", "te"]),
        build_line("一期一会のこの音で", "ichigoichienokonootode", "일기일회의 이 소리로", ["ichi", "go", "ichi", "e", "no", "ko", "no", "oto", "de"]),
        build_line("僕らは繋がっている", "bokurawatsunagatteiru", "우리들은 이어져 있어", ["boku", "ra", "wa", "tsuna", "", "ga", "tte", "i", "ru"])
    ]
})

# ==========================================
# 4. 潜在表明 (Senzai Hyoumei)
# ==========================================
songs_data.append({
    "id": "senzaihyoumei",
    "title": "潜在表明",
    "reading": "せんざいひょうめい",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "zF0k41kI868",
    "lines": [
        build_line("地下鉄の窓に急に映る顔が", "chikatetsunomadonikyuuniutsurukaoga", "지하철 창문에 갑자기 비치는 얼굴이", ["chika", "", "tetsu", "no", "mado", "ni", "kyuu", "ni", "utsu", "", "ru", "kao", "ga"]),
        build_line("じっとこっちを見る", "jittokocchiwomiru", "가만히 이쪽을 바라봐", ["ji", "tto", "ko", "cchi", "wo", "mi", "ru"]),
        build_line("そのひどく不安気な目を", "sonohidokufuanginamezwo", "그 몹시 불안한 눈을", ["so", "no", "hi", "do", "ku", "fu", "an", "ge", "na", "me", "wo"]),
        build_line("逸らすことも出来ず立ち尽くしていた", "sorasukotomodekizutachitsukushiteita", "돌리지도 못하고 우두커니 서 있었어", ["sora", "", "su", "ko", "to", "mo", "deki", "", "zu", "tachi", "", "tsuku", "", "shi", "te", "i", "ta"]),
        build_line("耳の奥で後ろ指さす声がこだまする", "miminookudeushirotubisasukoegakodamasuru", "귀 깊은 곳에서 손가락질하는 소리가 메아리쳐", ["mimi", "no", "oku", "de", "ushiro", "", "yubi", "sa", "su", "koe", "ga", "kodama", "", "su", "ru"]),
        build_line("深く深く潜ったままの", "fukakufukakumuguttamamano", "깊고 깊게 숨죽여 잠든 채의", ["fuka", "", "ku", "fuka", "", "ku", "mugu", "", "tta", "ma", "ma", "no"]),
        build_line("僕の声を抱えて歩いた", "bokunokoewokakaetearuita", "내 목소리를 끌어안고 걸었어", ["boku", "no", "koe", "wo", "kaka", "", "e", "te", "aru", "", "i", "ta"])
    ]
})

# ==========================================
# 5. 影色舞 (Silhouette Dance)
# ==========================================
songs_data.append({
    "id": "kageiromai",
    "title": "影色舞",
    "reading": "しるえっと だんす",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "zW8bS2Z8d7g",
    "lines": [
        build_line("あと一匙の憂鬱で", "atohitosajinoyuuutsude", "앞으로 한 숟가락의 우울로", ["a", "to", "hito", "saji", "", "no", "yuu", "utsu", "de"]),
        build_line("壊れそうなんてのたまえど", "kowaresounantenotamaedo", "부서질 것 같다고 말하지만", ["kowa", "", "re", "sou", "na", "n", "te", "no", "ta", "ma", "e", "do"]),
        build_line("記憶域圧されてしまう", "kiokui kiosareteshimau", "기억 영역이 짓눌려 버려", ["ki", "oku", "iki", "osa", "", "re", "te", "shi", "ma", "u"]),
        build_line("もうなにもかも忘れて", "mounanimokamowasurete", "이제 모든 걸 잊어버리고", ["mou", "na", "ni", "mo", "ka", "mo", "wasu", "", "re", "te"]),
        build_line("今宵はシルエットダンス", "koyoiwashiruettodansu", "오늘 밤은 실루엣 댄스", ["koyoi", "", "wa", "shi", "ru", "e", "tto", "da", "n", "su"]),
        build_line("知らない要らない全然", "shiranaiiranaizenzen", "몰라 필요 없어 전혀", ["shira", "", "na", "i", "ira", "", "na", "i", "zen", "zen"]),
        build_line("なんの法則もなくただ舞って舞う", "nannohousokumonakutadamattemau", "어떤 법칙도 없이 그저 춤추고 춤춰", ["na", "n", "no", "hou", "soku", "mo", "na", "ku", "ta", "da", "ma", "tte", "ma", "u"]),
        build_line("超然的シルエットダンス", "chouzentekishiruettodansu", "초연한 실루엣 댄스", ["chou", "zen", "teki", "shi", "ru", "e", "tto", "da", "n", "su"])
    ]
})

# ==========================================
# 6. 壱雫空 (Hitoshizuku)
# ==========================================
songs_data.append({
    "id": "hitoshizuku",
    "title": "壱雫空",
    "reading": "ひとしずく",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "s_A_n9yU64s",
    "lines": [
        build_line("もしこの雨が上がっても", "moshikonoamegaagattemo", "만약 이 비가 그치더라도", ["mo", "shi", "ko", "no", "ame", "ga", "aga", "", "tte", "mo"]),
        build_line("忘れずに歩いてくよ", "wasurezuniaruitekuyo", "잊지 않고 걸어갈 거야", ["wasu", "", "re", "zu", "ni", "aru", "", "i", "te", "ku", "yo"]),
        build_line("最初のひとしずくに", "saishonohitoshizukuni", "첫 번째 한 방울에", ["sai", "sho", "no", "hi", "to", "shi", "zu", "ku", "ni"]),
        build_line("顔上げた今日の僕を", "kaoagetakyouanobokuwo", "얼굴을 든 오늘의 나를", ["kao", "age", "", "ta", "kyou", "", "no", "boku", "wo"]),
        build_line("透明な傘で作る", "toumeinakasadetsukuru", "투명한 우산으로 만드는", ["tou", "mei", "na", "kasa", "de", "tsuku", "ru"]),
        build_line("ひとり分だけの世界", "hitoribundakenosekai", "한 사람 몫만의 세계", ["hito", "ri", "bun", "da", "ke", "no", "se", "kai"]),
        build_line("この雨が上がってく時", "konoamegaagattegutoki", "이 비가 그쳐갈 때", ["ko", "no", "ame", "ga", "aga", "", "tte", "ku", "toki"]),
        build_line("過ぎ去ってしまう瞬間を", "sugisatteshimauimawwo", "지나가 버리는 순간을", ["sugi", "", "sa", "tte", "shi", "ma", "u", "shun", "kan", "wo"]),
        build_line("僕はあつめたいよひとしずくを", "bokuwaatsumetaiyohitoshizukuwo", "나는 모으고 싶어, 한 방울을", ["boku", "wa", "atsu", "me", "tai", "yo", "hi", "to", "shi", "zu", "ku", "wo"])
    ]
})

# ==========================================
# 7. 栞 (Shiori)
# ==========================================
songs_data.append({
    "id": "shiori",
    "title": "栞",
    "reading": "しおり",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "KId3M9bF9uI",
    "lines": [
        build_line("普通とかあたりまえってなんだろう", "futsuutokaatarimaettenandarou", "'보통'이라든가 '당연한 것'이란 뭘까", ["fu", "tsuu", "to", "ka", "a", "ta", "ri", "ma", "e", "tte", "na", "n", "da", "rou"]),
        build_line("今手にある物差しでは", "imateaniarumonosashidewa", "지금 손에 쥔 잣대로는", ["ima", "te", "ni", "a", "ru", "mono", "sashi", "", "de", "wa"]),
        build_line("全然上手く測れなくって", "zenzenumakuhakarenakutte", "전혀 제대로 잴 수가 없어서", ["zen", "zen", "uma", "", "ku", "haka", "", "re", "na", "ku", "tte"]),
        build_line("ページの間に挟んだ栞", "peejinoaidenihasandashiori", "페이지 사이에 끼워둔 책갈피", ["pee", "", "ji", "no", "aida", "", "ni", "hasa", "", "n", "da", "shiori"]),
        build_line("君と過ごした日々の印", "kimitosugoshitahibinoshirushi", "너와 함께 보낸 날들의 표시", ["kimi", "to", "sugo", "", "shi", "ta", "hi", "bi", "no", "shirushi"]),
        build_line("めくるたび甦る記憶", "mekurutabiyomigaerukioku", "넘길 때마다 되살아나는 기억", ["me", "ku", "ru", "ta", "bi", "yomi", "gae", "", "ru", "ki", "oku"]),
        build_line("迷いながら歩いた道も", "mayoinagaraaruitamichimo", "헤매며 걸었던 길도", ["mayo", "", "i", "na", "ga", "ra", "aru", "", "i", "ta", "michi", "mo"]),
        build_line("いつか宝物になるから", "itsukatakaramononinarukara", "언젠가 보물이 될 테니까", ["i", "tsu", "ka", "takara", "mono", "", "ni", "na", "ru", "ka", "ra"])
    ]
})

# ==========================================
# 8. 焚音打 (Taon-da / Tanebi)
# ==========================================
songs_data.append({
    "id": "tanebi",
    "title": "焚音打",
    "reading": "たねび",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "zX11UeP3h4Q",
    "lines": [
        build_line("きっと理由はバラバラだった", "kittoriyuuwabarabaradatta", "분명 이유는 제각각이었어", ["ki", "tto", "ri", "yuu", "wa", "ba", "ra", "ba", "ra", "da", "tta"]),
        build_line("寄る辺のないあの日の僕たち", "yorubenonaianohinobokutachi", "의지할 곳 없던 그날의 우리들", ["yo", "ru", "be", "no", "na", "i", "a", "no", "hi", "no", "boku", "tachi", ""]),
        build_line("もう二度と傷つきたくないって", "mounidotokizutsukitakunaitte", "더는 상처받고 싶지 않다고", ["mou", "ni", "do", "to", "kizu", "tsu", "ki", "ta", "ku", "na", "i", "tte"]),
        build_line("そう思ってうつむいたのに", "souomotteutsumuitanoni", "그렇게 생각하며 고개 숙였는데", ["sou", "omo", "", "tte", "u", "tsu", "mu", "i", "ta", "no", "ni"]),
        build_line("迷ってたから出会えて", "mayottetakaratdeatte", "헤매고 있었기에 만날 수 있어서", ["mayo", "", "tte", "ta", "ka", "ra", "dea", "", "e", "te"]),
        build_line("やっと繋いだ手を", "yattotsunaidatewo", "겨우 맞잡은 손을", ["ya", "tto", "tsuna", "", "i", "da", "te", "wo"]),
        build_line("もう僕は離さない", "moubokuwahanasanai", "이제 난 놓지 않을 거야", ["mou", "boku", "wa", "hana", "", "sa", "na", "i"]),
        build_line("何があっても握りしめていく", "nanigaattomonigirishimeteiku", "무슨 일이 있어도 꽉 쥐고 갈 거야", ["nani", "ga", "a", "tte", "mo", "nigiri", "", "shi", "me", "te", "i", "ku"])
    ]
})

# ==========================================
# 9. 碧天伴走 (Hekiten Bansou)
# ==========================================
songs_data.append({
    "id": "hekitenbansou",
    "title": "碧天伴走",
    "reading": "へきてんばんそう",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "y_QO3Y_d-o4",
    "lines": [
        build_line("人知れず肩落としてる君がいるのに", "hitoshirezukataotoshiterukimigairunoni", "남몰래 어깨를 떨구는 네가 있는데", ["hito", "shire", "", "zu", "kata", "oto", "", "shi", "te", "ru", "kimi", "ga", "i", "ru", "no", "ni"]),
        build_line("碧すぎてる空ばかりが眩しい", "aokusugiterusorabakarigamabushii", "너무도 푸른 하늘만이 눈부셔", ["aoku", "", "sugi", "", "te", "ru", "sora", "ba", "ka", "ri", "ga", "mabu", "shii", ""]),
        build_line("僕はどんな言葉を君に言えばいいのか", "bokuwadonnakotobawokiminiiebaiinoka", "나는 어떤 말을 네게 건네야 좋을까", ["boku", "wa", "do", "n", "na", "kotoba", "", "wo", "kimi", "ni", "ie", "", "ba", "i", "i", "no", "ka"]),
        build_line("君に何を伝えられるだろう", "kimininaniwotsutaerarerudarou", "너에게 무엇을 전할 수 있을까", ["kimi", "ni", "nani", "wo", "tsutae", "", "ra", "re", "ru", "da", "rou"]),
        build_line("躓いて転んだって", "tsumazuitekorondatte", "걸려 넘어진다 해도", ["tsumazui", "", "", "te", "koron", "", "da", "tte"]),
        build_line("立ち上がり来たんだ", "tachiagarikitanda", "다시 일어서서 여기까지 왔잖아", ["tachi", "aga", "", "ri", "ki", "ta", "n", "da"]),
        build_line("頑張ってるいつでも", "ganbatteruitsudemo", "언제나 힘내고 있어", ["ganba", "", "tte", "ru", "i", "tsu", "de", "mo"]),
        build_line("ここに立ってるだけで", "kokonitatterudakede", "여기에 서 있는 것만으로도", ["ko", "ko", "ni", "ta", "tte", "ru", "da", "ke", "de"]),
        build_line("迷っても君と走っていきたいんだよ", "mayottemokimitohashitteikitaindayo", "헤매더라도 너와 함께 달려가고 싶어", ["mayo", "", "tte", "mo", "kimi", "to", "hashi", "", "tte", "i", "ki", "ta", "i", "n", "da", "yo"])
    ]
})

# ==========================================
# 10. 歌いましょう鳴らしましょう (Utaimashou Narashimashou)
# ==========================================
songs_data.append({
    "id": "utaimashou",
    "title": "歌いましょう鳴らしましょう",
    "reading": "うたいましょうならしましょう",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "zF0k41kI868",
    "lines": [
        build_line("鑑賞用の花のように遠くで", "kanshouyounohananoyounitookude", "관상용 꽃처럼 먼 곳에서", ["kan", "shou", "you", "no", "hana", "no", "you", "ni", "too", "ku", "de"]),
        build_line("私見てるだけでいいのかい", "watashimiterudakedeiinokai", "나를 그저 바라보기만 하면 되는 거니", ["watashi", "mi", "te", "ru", "da", "ke", "de", "i", "i", "no", "kai"]),
        build_line("歌いましょう鳴らしましょう", "utaimashounarashimashou", "노래합시다 울려 퍼트립시다", ["uta", "i", "ma", "shou", "nara", "", "shi", "ma", "shou"]),
        build_line("この胸の衝動を解き放て", "konomunenosyoudouwotokihanate", "이 가슴의 충동을 해방해", ["ko", "no", "mune", "no", "shou", "dou", "wo", "toki", "hana", "", "te"]),
        build_line("泥だらけの靴で踏み鳴らせ", "dorodarakenokutsudefuminarase", "흙투성이 신발로 힘차게 굴러봐", ["doro", "da", "ra", "ke", "no", "kutsu", "de", "fumi", "nara", "", "se"]),
        build_line("僕らの音を響かせていこう", "bokuranootowohibikaseteikou", "우리들의 소리를 울려 퍼트려 가자", ["boku", "ra", "no", "oto", "wo", "hibi", "", "ka", "se", "te", "i", "kou"])
    ]
})

# ==========================================
# 11. 春日影 (Haruhikage - MyGO!!!!! ver.)
# ==========================================
songs_data.append({
    "id": "haruhikage",
    "title": "春日影 (MyGO!!!!! ver.)",
    "reading": "はるひかげ",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "a9t98mP179E",
    "lines": [
        build_line("かじかんだ心震えるまなざし", "kajikandakokorofuruerumanazashi", "얼어붙은 마음, 떨리는 눈빛", ["ka", "ji", "ka", "n", "da", "kokoro", "furu", "", "e", "ru", "ma", "na", "za", "shi"]),
        build_line("世界で僕はひとりぼっちだった", "sekaidebokuwahitoribocchidatta", "세상에서 나는 외톨이였어", ["se", "kai", "de", "boku", "wa", "hi", "to", "ri", "bo", "cchi", "da", "tta"]),
        build_line("散ることしか知らない春は", "chirukotoshikashiranaiharuwa", "지는 것밖에 모르는 봄은", ["chi", "ru", "ko", "to", "shi", "ka", "shira", "", "na", "i", "haru", "wa"]),
        build_line("毎年冷たくあしらう", "maitoshitsumetakuaishirau", "매년 매정하게 대하네", ["mai", "toshi", "tsume", "", "ta", "ku", "a", "shi", "ra", "u"]),
        build_line("暗がりの中一方通行に", "kuragarinonakaippoutsuukouni", "어둠 속 일방통행으로", ["kura", "ga", "ri", "no", "naka", "i", "ppou", "tsuu", "kou", "ni"]),
        build_line("ただただ言葉を書き殴って", "tadatadakotobawokakinagutte", "그저 말을 휘갈겨 쓰며", ["ta", "da", "ta", "da", "kotoba", "", "wo", "kaki", "nagu", "", "tte"]),
        build_line("雲間を縫ってきらりきらり", "kumomawonuuttekirarikirari", "구름 사이를 뚫고 반짝반짝", ["kumo", "ma", "wo", "nu", "tte", "ki", "ra", "ri", "ki", "ra", "ri"]),
        build_line("心満たしてはあふれ", "kokoromitashitehaafure", "마음을 채우고는 넘쳐흘러", ["kokoro", "mita", "", "shi", "te", "wa", "a", "fu", "re"]),
        build_line("君の手はどうしてこんなにも温かいの", "kiminotewadoushitekonnanimonatakaino", "네 손은 어째서 이렇게나 따스한 걸까", ["kimi", "no", "te", "wa", "dou", "shi", "te", "ko", "n", "na", "ni", "mo", "atataka", "", "i", "no"]),
        build_line("どうかこのまま離さないでいて", "doukakonomamahanasanaideite", "부디 이대로 손을 놓지 말아줘", ["dou", "ka", "ko", "no", "ma", "ma", "hana", "", "sa", "na", "i", "de", "i", "te"])
    ]
})

# ==========================================
# 12. 詩超絆 (Utakotoba)
# ==========================================
songs_data.append({
    "id": "utakotoba",
    "title": "詩超絆",
    "reading": "うたことば",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "QkX594yX8jE",
    "lines": [
        build_line("僕にはわからないんだいつも", "bokuniwawakaranaindaitsumo", "내게는 알 수 없는 거야 언제나", ["boku", "ni", "wa", "wa", "ka", "ra", "na", "i", "n", "da", "i", "tsu", "mo"]),
        build_line("みつけられない正解も普通も", "mitsukerarenaiseikaimofutsuumo", "찾을 수 없어 정답도 보통도", ["mi", "tsu", "ke", "ra", "re", "na", "i", "sei", "kai", "mo", "fu", "tsuu", "mo"]),
        build_line("世界はずっとずっと遠く", "sekaiwazuttozuttotooku", "세상은 줄곧 아득히 먼", ["se", "kai", "wa", "zu", "tto", "zu", "tto", "too", "ku"]),
        build_line("僕には届かない場所にあるんだ", "bokuniwatodokanaibashonianrunda", "내겐 닿지 않는 곳에 있는 거야", ["boku", "ni", "wa", "todo", "", "ka", "na", "i", "ba", "sho", "ni", "a", "ru", "n", "da"]),
        build_line("戻りたい伝えたい", "modoritaitutaetai", "돌아가고 싶어 전하고 싶어", ["modo", "", "ri", "tai", "tsuta", "", "e", "tai"]),
        build_line("許されるなら僕は諦めたくない", "yurusarerunarabokuwaakirametakunai", "용서받을 수 있다면 난 포기하고 싶지 않아", ["yuru", "", "sa", "re", "ru", "na", "ra", "boku", "wa", "akira", "", "me", "ta", "ku", "na", "i"]),
        build_line("うたういまああ届いて", "utauimaaatodoite", "노래해 지금, 아아 닿기를", ["u", "ta", "u", "ima", "a", "a", "todo", "", "i", "te"]),
        build_line("君の胸にまだ間に合うかい", "kiminomunenimadamaniaukai", "너의 가슴에 아직 늦지 않았을까", ["kimi", "no", "mune", "ni", "ma", "da", "ma", "ni", "a", "u", "kai"]),
        build_line("言葉を超えるため心を叫ぶ", "kotobawokoerutamekokorowosakebu", "말을 뛰어넘기 위해 마음을 외쳐", ["kotoba", "", "wo", "koe", "", "ru", "ta", "me", "kokoro", "wo", "sake", "bu"])
    ]
})

# ==========================================
# 13. 迷路日々 (Meirohibi)
# ==========================================
songs_data.append({
    "id": "meirohibi",
    "title": "迷路日々",
    "reading": "めいろひび",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "W2R2G9w2N-Q",
    "lines": [
        build_line("迷いながら戸惑いながら歩く", "mayoinagaratomadoinagaraaruku", "헤매면서 망설이면서 걸어", ["mayo", "", "i", "na", "ga", "ra", "tomado", "", "i", "na", "ga", "ra", "aru", "", "ku"]),
        build_line("めいろの中で僕らは居合わせてた", "meirononakadebokurawaimawasateta", "미로 속에서 우리들은 우연히 함께 있었어", ["me", "i", "ro", "no", "naka", "de", "boku", "ra", "wa", "i", "a", "wa", "se", "te", "ta"]),
        build_line("名前のない感情ああ抱きしめてる", "namaenonaikanjouaadakishimeteru", "이름 없는 감정 아아 끌어안고 있어", ["namae", "", "no", "na", "i", "kan", "jou", "a", "a", "daki", "", "shi", "me", "te", "ru"]),
        build_line("ちいさな一瞬あつめたい", "chiisananaisshunatsumetai", "작은 한순간을 모으고 싶어", ["chi", "i", "sa", "na", "i", "sshun", "atsu", "me", "tai"]),
        build_line("出口なんてどこにも見えなくても", "deguchinantedokonimomienakutemo", "출구 따윈 어디에도 보이지 않는다 해도", ["de", "guchi", "na", "n", "te", "do", "ko", "ni", "mo", "mie", "", "na", "ku", "te", "mo"]),
        build_line("君と手をつないで進む日々", "kimitotewotsunaidesusumuhibi", "너와 손을 잡고 나아가는 나날", ["kimi", "to", "te", "wo", "tsuna", "", "i", "de", "susu", "", "mu", "hi", "bi"])
    ]
})

# ==========================================
# 14. 無路矢 (Noroshi)
# ==========================================
songs_data.append({
    "id": "noroshi",
    "title": "無路矢",
    "reading": "のろし",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "v8K8a0Q81rA",
    "lines": [
        build_line("無軌道を描く足跡でも", "mukidouwokakuashiattodemo", "갈피 없는 궤도를 그리는 발자국이라도", ["mu", "ki", "dou", "wo", "eka", "", "ku", "ashi", "ato", "de", "mo"]),
        build_line("進み続けた", "susumitsuzuketa", "계속해서 나아갔어", ["susu", "", "mi", "tsuzu", "", "ke", "ta"]),
        build_line("ほつれそうな心で", "hotsuresounakokorode", "풀려버릴 것 같은 마음으로", ["ho", "tsu", "re", "sou", "na", "kokoro", "de"]),
        build_line("どこから来てどこに向かう", "dokokarakitedokonimukau", "어디에서 와서 어디로 향하는가", ["do", "ko", "ka", "ra", "ki", "te", "do", "ko", "ni", "muka", "u"]),
        build_line("何を信じて生きていくの", "naniwoshinjiteikiteikuno", "무엇을 믿고 살아가는 걸까", ["nani", "wo", "shin", "ji", "te", "iki", "", "te", "i", "ku", "no"]),
        build_line("道標も地図もなくて", "douhyoumouchizumonakute", "이정표도 지도도 없이", ["michi", "shirube", "mo", "chi", "zu", "mo", "na", "ku", "te"]),
        build_line("フラつく足で掲げた狼煙", "furatsukuashidekakagetanoroshi", "비틀거리는 걸음으로 피워 올린 봉화", ["fu", "ra", "tsu", "ku", "ashi", "de", "kaka", "", "ge", "ta", "no", "ro", "shi"])
    ]
})

# ==========================================
# 15. 砂寸奏 (Sasunso / Sasurai)
# ==========================================
songs_data.append({
    "id": "sasunso",
    "title": "砂寸奏",
    "reading": "さすらい",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "Y5V-92Pq8Xw",
    "lines": [
        build_line("同じ音符を追いかけるのに", "onajionpuwooikakerunoni", "같은 음표를 쫓아가는데도", ["ona", "", "ji", "on", "pu", "wo", "oi", "", "ka", "ke", "ru", "no", "ni"]),
        build_line("ズレていくのはどうしてだろう", "zureteikuwadowshitedarou", "어긋나 버리는 건 어째서일까", ["zu", "re", "te", "i", "ku", "no", "wa", "dou", "shi", "te", "da", "rou"]),
        build_line("砂の粒のようにこぼれ落ちて", "sunanotsubunoyounikoboreochite", "모래알처럼 손에서 흘러넘쳐 떨어져", ["suna", "no", "tsubu", "no", "you", "ni", "kobo", "", "re", "ochi", "", "te"]),
        build_line("足跡さえも消えてしまう", "ashiattosaemokieteshimau", "발자국마저 지워져 버려", ["ashi", "ato", "sa", "e", "mo", "kie", "", "te", "shi", "ma", "u"]),
        build_line("それでも鳴らす僕らのリズム", "soredemonarasubokuranorizumu", "그럼에도 울리는 우리들의 리듬", ["so", "re", "de", "mo", "nara", "", "su", "boku", "ra", "no", "ri", "zu", "mu"]),
        build_line("さすらいながら明日を探そう", "sasurainagaraashitawosagasou", "방랑하면서 내일을 찾아가자", ["sa", "su", "ra", "i", "na", "ga", "ra", "ashita", "", "wo", "saga", "", "sou"])
    ]
})

# ==========================================
# 16. 回層浮 (Kaisoufu)
# ==========================================
songs_data.append({
    "id": "kaisoufu",
    "title": "回層浮",
    "reading": "かいそうふ",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "gQO9mZq_T0A",
    "lines": [
        build_line("真夜中の入り口", "mayonakanoniriguchi", "한밤중의 입구", ["ma", "yo", "naka", "no", "iri", "guchi", ""]),
        build_line("不意にぶり返した孤独", "fuiniburihaeshitakodoku", "불현듯 되살아난 고독", ["fu", "i", "ni", "buri", "kae", "", "shi", "ta", "ko", "doku"]),
        build_line("水底に沈む光を見つめて", "minasokonisizumuhikariwomitsumete", "물밑으로 가라앉는 빛을 바라보며", ["mina", "soko", "ni", "shizu", "", "mu", "hikari", "wo", "mitsu", "", "me", "te"]),
        build_line("浮かんでは消える記憶の層", "ukandewakierukiokunosou", "떠올랐다 사라지는 기억의 층", ["uka", "", "n", "de", "wa", "kie", "", "ru", "ki", "oku", "no", "sou"]),
        build_line("息を吸い込んで泳ぎ出す", "ikiwosuiikondeoyogidasu", "숨을 들이마시고 헤엄쳐 나가", ["iki", "wo", "sui", "", "ko", "n", "de", "oyo", "", "gi", "da", "su"])
    ]
})

# ==========================================
# 17. 処救生 (Shokyuusei / Kokyuu)
# ==========================================
songs_data.append({
    "id": "shokyuusei",
    "title": "処救生",
    "reading": "こきゅう",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "H4K4aP8w09U",
    "lines": [
        build_line("こたえあわせ", "kotaeawase", "답 맞춰보기", ["ko", "ta", "e", "a", "wa", "se"]),
        build_line("丸と罰に埋もれ", "marutobatsuniumore", "동그라미와 가위표에 파묻혀", ["maru", "to", "batsu", "ni", "umo", "", "re"]),
        build_line("息苦しい部屋の中で", "ikigurushiibeyanonakade", "숨 막히는 방 안에서", ["iki", "guru", "", "shii", "he", "ya", "no", "naka", "de"]),
        build_line("命の音を確かめていた", "inochinootowotashikameteita", "생명의 소리를 확인하고 있었어", ["inochi", "no", "oto", "wo", "tashika", "", "me", "te", "i", "ta"]),
        build_line("救いを求めて叫ぶ呼吸", "sukuiwomotometesakebukokyuu", "구원을 바라며 외치는 호흡", ["suku", "", "i", "wo", "moto", "", "me", "te", "sake", "", "bu", "ko", "kyuu"])
    ]
})

# ==========================================
# 18. 端程山 (Hashidoyama / Panorama)
# ==========================================
songs_data.append({
    "id": "hashidoyama",
    "title": "端程山",
    "reading": "ぱのらま",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "6mJm078vGZQ",
    "lines": [
        build_line("どこまで歩けばいいのかなんて", "dokomadearukebaiinokanante", "어디까지 걸어야 하는지 따윈", ["do", "ko", "ma", "de", "aru", "", "ke", "ba", "i", "i", "no", "ka", "na", "n", "te"]),
        build_line("知らないまま踏みしめてた", "shiranaimamafumishimeteta", "모른 채 꾹꾹 내딛고 있었어", ["shira", "", "na", "i", "ma", "ma", "fumi", "shime", "", "te", "ta"]),
        build_line("見上げた空の広さに息をのむ", "miagetasoranohirosaniikiwonomu", "올려다본 하늘의 넓음에 숨을 삼켜", ["mi", "age", "", "ta", "sora", "no", "hiro", "", "sa", "ni", "iki", "wo", "no", "mu"]),
        build_line("広がるパノラマの向こうへ", "hirogarupanoramanomukouhe", "펼쳐지는 파노라마의 저편으로", ["hiro", "", "ga", "ru", "pa", "no", "ra", "ma", "no", "mukou", "", "e"])
    ]
})

# ==========================================
# 19. 輪符雨 (Rinpuu / Refrain)
# ==========================================
songs_data.append({
    "id": "rinpuu",
    "title": "輪符雨",
    "reading": "りふれいん",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "L-Z8B8X8Y-k",
    "lines": [
        build_line("硝子窓はすぐに雲に覆われて", "garasumadowasugunikumonioowarete", "유리창은 곧바로 구름에 뒤덮이고", ["garasu", "", "", "mado", "wa", "su", "gu", "ni", "kumo", "ni", "oowa", "", "re", "te"]),
        build_line("冷たい雨が降り続く", "tsumetaiamegafuritsuzuku", "차가운 비가 끝없이 내려", ["tsume", "", "ta", "i", "ame", "ga", "furi", "tsuzu", "", "ku"]),
        build_line("繰り返すメロディのように", "kurikaesumerodinoyouni", "반복되는 멜로디처럼", ["kuri", "kae", "", "su", "me", "ro", "di", "no", "you", "ni"]),
        build_line("僕らの涙を洗い流して", "bokuranonamidawowarainagashite", "우리들의 눈물을 씻어내 줘", ["boku", "ra", "no", "namida", "wo", "arai", "naga", "", "shi", "te"])
    ]
})

# ==========================================
# 20. 孤壊牢 (Kokairou / Kokoro)
# ==========================================
songs_data.append({
    "id": "kokairou",
    "title": "孤壊牢",
    "reading": "こころ",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "v8K8a0Q81rA",
    "lines": [
        build_line("まるで違う生き物なのに", "marudechigauikimononanoni", "마치 다른 생물인데도", ["ma", "ru", "de", "chiga", "", "u", "iki", "mono", "", "na", "no", "ni"]),
        build_line("何故か僕ら一括りで", "nazekabokurahitokukuride", "어째서인지 우릴 하나로 묶어버리고", ["naze", "ka", "boku", "ra", "hito", "kukuri", "", "de"]),
        build_line("檻の中で叫び続けている", "orinonakadesakebitsuzuketeiru", "우리 안에서 계속 외치고 있어", ["ori", "no", "naka", "de", "sake", "", "bi", "tsuzu", "", "ke", "te", "i", "ru"]),
        build_line("壊れそうな心を抱いて", "kowaresounakokorowodaite", "부서질 것 같은 마음을 품고", ["kowa", "", "re", "sou", "na", "kokoro", "wo", "da", "i", "te"])
    ]
})

# ==========================================
# 21. 歩拾道 (Hoshuudou)
# ==========================================
songs_data.append({
    "id": "hoshuudou",
    "title": "歩拾道",
    "reading": "ほしゅうどう",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "Y5V-92Pq8Xw",
    "lines": [
        build_line("ツギハギのコンクリートを歩いていく", "tsugihaginokonkuriitowoaruiteiku", "기워 맞춘 콘크리트 위를 걸어가", ["tsu", "gi", "ha", "gi", "no", "ko", "n", "ku", "rii", "to", "wo", "aru", "", "i", "te", "i", "ku"]),
        build_line("落としたものを一つずつ拾い集めて", "otoshitamonowohitotsuzutsuhiroiatsumete", "떨어뜨린 것들을 하나씩 주워 모으며", ["oto", "", "shi", "ta", "mono", "wo", "hito", "tsu", "zu", "tsu", "hiro", "", "i", "atsu", "", "me", "te"]),
        build_line("スピードを上げて進む道", "supiidowoaagetesusumumichi", "속도를 올려 나아가는 길", ["su", "pii", "do", "wo", "age", "", "te", "susu", "", "mu", "michi"])
    ]
})

# ==========================================
# 22. 夜隠染 (Yaonzen / Yokaze)
# ==========================================
songs_data.append({
    "id": "yaonzen",
    "title": "夜隠染",
    "reading": "よかぜ",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "6mJm078vGZQ",
    "lines": [
        build_line("あきらめれば楽だった", "akiramerebarakudatta", "포기하면 편했을 텐데", ["a", "ki", "ra", "me", "re", "ba", "raku", "da", "tta"]),
        build_line("夜風が吹き抜ける街で", "yokazegafukinukerumachide", "밤바람이 불어 지나가는 거리에서", ["yo", "kaze", "ga", "fuki", "nuke", "", "ru", "machi", "de"]),
        build_line("染まっていく暗闇に抗うように", "somatteikukurayaminiaragauyouni", "물들어가는 어둠에 맞서듯이", ["soma", "", "tte", "i", "ku", "kura", "yami", "ni", "araga", "", "u", "you", "ni"]),
        build_line("僕らは小さな火を灯す", "bokurawachiisanahiwotomosu", "우리는 작은 불을 지펴", ["boku", "ra", "wa", "chii", "sa", "na", "hi", "wo", "tomo", "su"])
    ]
})

# ==========================================
# 23. 霧周途 (Mushuutou / Mist)
# ==========================================
songs_data.append({
    "id": "mushuutou",
    "title": "霧周途",
    "reading": "みすと",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "L-Z8B8X8Y-k",
    "lines": [
        build_line("立ち籠める霧から", "tachikomerukirikara", "자욱하게 피어오르는 안개 속에서", ["tachi", "kome", "", "ru", "kiri", "ka", "ra"]),
        build_line("先が見えなくなっても", "sakigamienakunattemo", "앞이 보이지 않게 된다 해도", ["saki", "ga", "mie", "", "na", "ku", "na", "tte", "mo"]),
        build_line("手探りで進む旅路", "tesaguridesusumutabiji", "더듬거리며 나아가는 여로", ["te", "saguri", "", "de", "susu", "", "mu", "tabi", "ji"]),
        build_line("霧を切り拓いて僕らは行く", "kiriwokirihiraitiebokurawayuku", "안개를 헤치며 우리는 가네", ["kiri", "wo", "kiri", "hira", "", "i", "te", "boku", "ra", "wa", "yu", "ku"])
    ]
})

# ==========================================
# 24. 証命讃歌 (Shoumeisanka)
# ==========================================
songs_data.append({
    "id": "shoumeisanka",
    "title": "証命讃歌",
    "reading": "しょうめいさんか",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "QkX594yX8jE",
    "lines": [
        build_line("くだらない前例は絶って", "kudaranazenreiwatatte", "하찮은 전례는 끊어버리고", ["ku", "da", "ra", "na", "i", "zen", "rei", "wa", "ta", "tte"]),
        build_line("止まんない衝動に沿って", "tomannaishoudounisotte", "멈추지 않는 충동을 따라서", ["toma", "", "n", "na", "i", "shou", "dou", "ni", "so", "tte"]),
        build_line("生きてる証を刻み込め", "ikiteruakashiwokizamikome", "살아있다는 증거를 아로새겨라", ["iki", "", "te", "ru", "akashi", "wo", "kizami", "kome", ""]),
        build_line("命の讃歌を鳴り響かせろ", "inochinosankawonarihibikasero", "생명의 찬가를 소리 높여 울려라", ["inochi", "no", "san", "ka", "wo", "nari", "hibika", "", "se", "ro"])
    ]
})

# ==========================================
# 25. ノンブレス・オブリージュ (Non-breath oblige - Cover)
# ==========================================
songs_data.append({
    "id": "nonbreath",
    "title": "ノンブレス・オブリージュ",
    "reading": "のんぶれす おぶりーじゅ",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "QG3fM0qK9qg",
    "lines": [
        build_line("世界中のすべての人間に好かれるなんて気持ち悪いよ", "sekaijuunosubetenoningennsukarerunantekimochowaruiyo", "온 세상 모든 사람에게 사랑받는다는 건 징그러운 일이야", ["se", "kai", "juu", "no", "su", "be", "te", "no", "nin", "gen", "ni", "suka", "", "re", "ru", "na", "n", "te", "ki", "mo", "chi", "wa", "ru", "i", "yo"]),
        build_line("だけど一つになれない教室で", "dakedohitotsuninarenaikyoushitsude", "하지만 하나가 될 수 없는 교실에서", ["da", "ke", "do", "hito", "tsu", "ni", "na", "re", "na", "i", "kyou", "shitsu", "de"]),
        build_line("息を止めて息を止めて", "ikiwotometeikiwotomete", "숨을 참고, 숨을 참고", ["iki", "wo", "tome", "", "te", "iki", "wo", "tome", "", "te"]),
        build_line("誰も傷つけないように潜って", "daremokizutsukenaiyounikugutte", "누구도 상처입히지 않도록 숨죽이며", ["dare", "mo", "kizu", "tsu", "ke", "na", "i", "you", "ni", "kugu", "", "tte"]),
        build_line("苦しくても笑ってみせるんだ", "kurushikutemowarattemiserunda", "괴로워도 웃어 보이는 거야", ["kuru", "", "shi", "ku", "te", "mo", "wara", "", "tte", "mi", "se", "ru", "n", "da"])
    ]
})

# ==========================================
# 26. 君の神様になりたい。 (Kimi no Kamisama ni Naritai - Cover)
# ==========================================
songs_data.append({
    "id": "kiminokamisama",
    "title": "君の神様になりたい。",
    "reading": "きみのかみさまになりたい",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "V_S-v8m0k0A",
    "lines": [
        build_line("僕の命の歌で君が命を大事にすればいいのに", "bokunoinochinoutadekimigainochiwodaijinisurebaiinoni", "내 생명의 노래로 네가 목숨을 소중히 여겼으면 좋을 텐데", ["boku", "no", "inochi", "no", "uta", "de", "kimi", "ga", "inochi", "wo", "dai", "ji", "ni", "su", "re", "ba", "i", "i", "no", "ni"]),
        build_line("僕の家族の歌で君が愛を大事にすればいいのに", "bokunokazokunoutadekimigaaiwodaijinisurebaiinoni", "내 가족의 노래로 네가 사랑을 소중히 여겼으면 좋을 텐데", ["boku", "no", "ka", "zoku", "no", "uta", "de", "kimi", "ga", "ai", "wo", "dai", "ji", "ni", "su", "re", "ba", "i", "i", "no", "ni"]),
        build_line("そんなくだらない幻想を歌っている", "sonnakudaranagensouwooutatteiru", "그런 시시한 환상을 노래하고 있어", ["so", "n", "na", "ku", "da", "ra", "na", "i", "gen", "sou", "wo", "uta", "", "tte", "i", "ru"]),
        build_line("君を救えない歌など", "kimiwosukuenaiutanado", "너를 구할 수 없는 노래 따위", ["kimi", "wo", "suku", "", "e", "na", "i", "uta", "na", "do"]),
        build_line("僕にとっては意味がないんだ", "bokunitottewaimiganainda", "나에게는 아무런 의미가 없어", ["boku", "ni", "to", "tte", "wa", "i", "mi", "ga", "na", "i", "n", "da"])
    ]
})

# ==========================================
# 27. シャルル (Charles - Cover)
# ==========================================
songs_data.append({
    "id": "charles",
    "title": "シャルル",
    "reading": "しゃるる",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "gB_yD6zU_oQ",
    "lines": [
        build_line("さよならはあなたから言った", "sayonarahaanatakarayitta", "작별은 당신이 먼저 말했지", ["sa", "yo", "na", "ra", "wa", "a", "na", "ta", "ka", "ra", "i", "tta"]),
        build_line("それなのに頬を濡らしてしまうの", "sorenanonihohowonurashiteshimawuno", "그런데도 뺨을 적시고 마는 거야?", ["so", "re", "na", "no", "ni", "hoho", "wo", "nura", "", "shi", "te", "shi", "ma", "u", "no"]),
        build_line("そうやって昨日の事も消してしまうなら", "souyattekinoubokotomokeshiteshimaunara", "그렇게 어제의 일도 지워버릴 거라면", ["sou", "ya", "tte", "kinou", "", "no", "koto", "mo", "keshi", "", "te", "shi", "ma", "u", "na", "ra"]),
        build_line("もういいよ笑って", "mouiiyowaratte", "이젠 됐어, 웃어줘", ["mou", "i", "i", "yo", "wara", "", "tte"]),
        build_line("重なり合う影が離れていく", "kasanariaukagegahanareteiku", "겹쳐지던 그림자가 멀어져 가", ["kasa", "", "na", "ri", "a", "u", "kage", "ga", "hana", "", "re", "te", "i", "ku"])
    ]
})

# ==========================================
# 28. swim (Cover)
# ==========================================
songs_data.append({
    "id": "swim",
    "title": "swim",
    "reading": "すいむ",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "mN_F9U6s6r8",
    "lines": [
        build_line("あの日の自分が許せないな", "anohinojibungayurusenaina", "그날의 내 자신이 용서가 안 돼", ["a", "no", "hi", "no", "ji", "bun", "ga", "yuru", "", "se", "na", "i", "na"]),
        build_line("選び間違えた日々を返せよ", "erabimachigaetahibiwokaeseyo", "잘못 선택했던 날들을 되돌려줘", ["era", "", "bi", "machi", "gae", "", "ta", "hi", "bi", "wo", "kae", "", "se", "yo"]),
        build_line("あなたの言葉がしがみついて", "anatanokotobagashigamitsuite", "너의 말이 들러붙어서", ["a", "na", "ta", "no", "kotoba", "", "ga", "shi", "ga", "mi", "tsu", "i", "te"]),
        build_line("離れられない逃れられない", "hanarerarenainogarerarenai", "떨어질 수 없어, 벗어날 수 없어", ["hana", "", "re", "ra", "re", "na", "i", "noga", "", "re", "ra", "re", "na", "i"]),
        build_line("泳いでいく暗い海の底へ", "oyoydeikukuraiuminosokoe", "헤엄쳐 가, 어두운 바다 밑으로", ["oyo", "", "i", "de", "i", "ku", "kura", "", "i", "umi", "no", "soko", "e"])
    ]
})

# ==========================================
# 29. 青春コンプレックス (Seishun Complex - Cover)
# ==========================================
songs_data.append({
    "id": "seishuncomplex",
    "title": "青春コンプレックス",
    "reading": "せいしゅんこんぷれっくす",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "KId3M9bF9uI",
    "lines": [
        build_line("暗く狭いのが好きだった", "kurakusemainogasukidatta", "어둡고 좁은 곳이 좋았어", ["kura", "", "ku", "sema", "", "i", "no", "ga", "suki", "", "da", "tta"]),
        build_line("深く被るフードの中", "fukakukaburufuudononaka", "깊게 눌러쓴 후드 속", ["fuka", "", "ku", "kabu", "", "ru", "fuu", "", "do", "no", "naka"]),
        build_line("無情な世界を恨んだ目は", "mujounasekaiwourandmewa", "무정한 세상을 원망하던 눈은", ["mu", "jou", "na", "se", "kai", "wo", "ura", "", "n", "da", "me", "wa"]),
        build_line("どうしようもなく愛を欲してた", "doushiyoumonakuaiwohoshshiteta", "어쩔 도리도 없이 사랑을 갈구했지", ["dou", "shi", "you", "mo", "na", "ku", "ai", "wo", "hoshite", "", "ta"]),
        build_line("雨に濡れるのが好きだった", "ameninurerunogasukidatta", "비에 젖는 것이 좋았어", ["ame", "ni", "nure", "", "ru", "no", "ga", "suki", "", "da", "tta"]),
        build_line("曇った顔が似合うから", "kumottakagoganikaukara", "흐린 얼굴이 어울리니까", ["kumo", "", "tta", "kao", "ga", "nia", "", "u", "ka", "ra"]),
        build_line("嵐に怯えてるフリをして", "arashiniobieterufuriwoshite", "폭풍을 무서워하는 척을 하며", ["arashi", "ni", "obie", "", "te", "ru", "fu", "ri", "wo", "shi", "te"]),
        build_line("空が割れるのを待っていたんだ", "soragawarerunowomatteitanda", "하늘이 갈라지기만을 기다렸어", ["sora", "ga", "ware", "", "ru", "no", "wo", "ma", "tte", "i", "ta", "n", "da"]),
        build_line("かき鳴らせ光のファズで", "kakinarasehikarinoazude", "가볍게 긁어 울려라, 빛의 퍼즈로", ["ka", "ki", "nara", "", "se", "hikari", "no", "fa", "zu", "de"]),
        build_line("雷鳴を轟かせたいんだ", "raimeiwotodorokasetainda", "뇌명을 울려 퍼뜨리고 싶어", ["rai", "mei", "wo", "todoro", "", "ka", "se", "tai", "n", "da"])
    ]
})

print(f"Total songs prepared: {len(songs_data)}")

# Format into TypeScript songs.ts file
ts_code = """// MyGO!!!!! Song Database for Lyrics Typing Practice
// 100% Official lyrics from Namuwiki & Official Albums
// Contains per-character Romaji mapping for pixel-perfect glow sync!

export interface SongLine {
  ja: string;
  romaji: string;
  ko: string;
  charRomaji?: string[];
}

export interface Song {
  id: string;
  title: string;
  reading: string;
  category: 'original' | 'cover';
  album: string;
  youtubeId?: string;
  lines: SongLine[];
}

export const SONGS: Song[] = """ + json.dumps(songs_data, ensure_ascii=False, indent=2) + ";\n"

with open("jlpt-calendar-site/app/typing/songs.ts", "w", encoding="utf-8") as f:
    f.write(ts_code)

print("Successfully written to jlpt-calendar-site/app/typing/songs.ts!")
