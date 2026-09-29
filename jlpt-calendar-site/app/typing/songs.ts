// MyGO!!!!! Song Database for Lyrics Typing Practice
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

export const SONGS: Song[] = [
  {
    "id": "mayoiuta",
    "title": "迷星叫",
    "reading": "まよいうた",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "LvVat3Y17lc",
    "lines": [
      {
        "ja": "交差点の真ん中",
        "romaji": "kousatennomannaka",
        "ko": "교차로 한가운데",
        "charRomaji": [
          "kou",
          "sa",
          "ten",
          "no",
          "man",
          "n",
          "naka"
        ]
      },
      {
        "ja": "急ぐ人に紛れて",
        "romaji": "isoguhitonimagirete",
        "ko": "서두르는 사람들에 뒤섞여",
        "charRomaji": [
          "isogu",
          "",
          "hito",
          "ni",
          "magire",
          "",
          "te"
        ]
      },
      {
        "ja": "僕だけがあてもなく",
        "romaji": "bokudakegaatemonaku",
        "ko": "나만이 정처도 없이",
        "charRomaji": [
          "boku",
          "da",
          "ke",
          "ga",
          "a",
          "te",
          "mo",
          "na",
          "ku"
        ]
      },
      {
        "ja": "漂うみたいだ",
        "romaji": "tadayoumaitada",
        "ko": "떠도는 것만 같아",
        "charRomaji": [
          "tadayou",
          "",
          "mi",
          "tai",
          "",
          "da"
        ]
      },
      {
        "ja": "流行りの歌はいつも",
        "romaji": "hayarinoutawaitsumo",
        "ko": "유행하는 노래는 언제나",
        "charRomaji": [
          "hayari",
          "",
          "",
          "no",
          "uta",
          "wa",
          "i",
          "tsu",
          "mo"
        ]
      },
      {
        "ja": "僕のことは歌ってない",
        "romaji": "bokunokotowautattenai",
        "ko": "내 이야기는 노래하지 않아",
        "charRomaji": [
          "boku",
          "no",
          "ko",
          "to",
          "wa",
          "utatte",
          "",
          "",
          "na",
          "i"
        ]
      },
      {
        "ja": "ねえビジョンの中から",
        "romaji": "neebijonnonakanakara",
        "ko": "저기, 전광판 속에서",
        "charRomaji": [
          "ne",
          "e",
          "bi",
          "jo",
          "",
          "n",
          "no",
          "naka",
          "ka",
          "ra"
        ]
      },
      {
        "ja": "笑いかけないで",
        "romaji": "waraikakenaide",
        "ko": "웃는 얼굴로 바라보지 마",
        "charRomaji": [
          "warai",
          "",
          "ka",
          "ke",
          "na",
          "i",
          "de"
        ]
      },
      {
        "ja": "また今日も声にならずに",
        "romaji": "matakyoumokoeninarazuni",
        "ko": "또 오늘도 목소리가 되지 못한 채",
        "charRomaji": [
          "ma",
          "ta",
          "kyou",
          "",
          "mo",
          "koe",
          "ni",
          "na",
          "ra",
          "zu",
          "ni"
        ]
      },
      {
        "ja": "飲み込んだ感情",
        "romaji": "nomikondakanjou",
        "ko": "삼켜버린 감정",
        "charRomaji": [
          "nomi",
          "",
          "konda",
          "",
          "",
          "kan",
          "jou"
        ]
      },
      {
        "ja": "下書き埋め尽くして",
        "romaji": "shitagakiumetsukushite",
        "ko": "임시 저장을 가득 채우고",
        "charRomaji": [
          "shita",
          "gaki",
          "",
          "ume",
          "",
          "tsuku",
          "",
          "shi",
          "te"
        ]
      },
      {
        "ja": "迷子でもいい迷子でも進め",
        "romaji": "maigodemoiimaigodemosusume",
        "ko": "미아라도 좋아, 미아라도 나아가라",
        "charRomaji": [
          "mai",
          "go",
          "de",
          "mo",
          "i",
          "i",
          "mai",
          "go",
          "de",
          "mo",
          "susu",
          "me"
        ]
      }
    ]
  },
  {
    "id": "nanashigoe",
    "title": "名無声",
    "reading": "なもなき",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "2mM64qcBYg8",
    "lines": [
      {
        "ja": "何が僕にできるか",
        "romaji": "nanigabokunidekiruka",
        "ko": "무엇을 내가 할 수 있을까",
        "charRomaji": [
          "nani",
          "ga",
          "boku",
          "ni",
          "de",
          "ki",
          "ru",
          "ka"
        ]
      },
      {
        "ja": "わからないけれど",
        "romaji": "wakawanaikeredo",
        "ko": "알 수는 없지만",
        "charRomaji": [
          "wa",
          "ka",
          "ra",
          "na",
          "i",
          "ke",
          "re",
          "do"
        ]
      },
      {
        "ja": "言葉にすれば零れ落ちる",
        "romaji": "kotobanisurebakoboreochiru",
        "ko": "말을 하면 흘러넘쳐 떨어지는",
        "charRomaji": [
          "kotoba",
          "",
          "ni",
          "su",
          "re",
          "ba",
          "kobore",
          "",
          "ochi",
          "",
          "ru"
        ]
      },
      {
        "ja": "名前のない痛みを",
        "romaji": "namaenonaiitamiwo",
        "ko": "이름 없는 아픔을",
        "charRomaji": [
          "namae",
          "",
          "no",
          "na",
          "i",
          "ita",
          "",
          "mi",
          "wo"
        ]
      },
      {
        "ja": "抱きしめて歌うよ",
        "romaji": "dakishimeteutauyo",
        "ko": "끌어안고 노래할게",
        "charRomaji": [
          "daki",
          "",
          "shi",
          "me",
          "te",
          "uta",
          "u",
          "yo"
        ]
      },
      {
        "ja": "誰かの正解じゃなくて",
        "romaji": "daredanoseikaijanakute",
        "ko": "누군가의 정답이 아니라",
        "charRomaji": [
          "dare",
          "ka",
          "no",
          "sei",
          "kai",
          "ja",
          "na",
          "ku",
          "te"
        ]
      },
      {
        "ja": "僕だけの声で叫ぶ",
        "romaji": "bokudakenokoedesakebu",
        "ko": "나만의 목소리로 외칠 거야",
        "charRomaji": [
          "boku",
          "da",
          "ke",
          "no",
          "koe",
          "de",
          "sake",
          "bu"
        ]
      },
      {
        "ja": "夜の静寂を切り裂いて",
        "romaji": "yorunoshijimawokirisaite",
        "ko": "밤의 적막을 갈라버리고",
        "charRomaji": [
          "yoru",
          "no",
          "shijima",
          "",
          "wo",
          "kiri",
          "",
          "sai",
          "",
          "te"
        ]
      },
      {
        "ja": "此処にいると伝えるんだ",
        "romaji": "kokoniirutotsutaerunda",
        "ko": "여기에 있다고 전할 거야",
        "charRomaji": [
          "koko",
          "",
          "ni",
          "i",
          "ru",
          "to",
          "tsutae",
          "",
          "ru",
          "n",
          "da"
        ]
      }
    ]
  },
  {
    "id": "otoichie",
    "title": "音一会",
    "reading": "おといちえ",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "F-h-M4p2v6E",
    "lines": [
      {
        "ja": "僕の居場所はB5",
        "romaji": "bokunoibashowabiigo",
        "ko": "나의 있을 곳은 B5 노트",
        "charRomaji": [
          "boku",
          "no",
          "iba",
          "",
          "sho",
          "wa",
          "bii",
          "go"
        ]
      },
      {
        "ja": "ペンからこぼれる言葉を落として",
        "romaji": "penkarakoborerukotobawootoshite",
        "ko": "펜에서 흘러나오는 말을 떨어뜨리며",
        "charRomaji": [
          "pen",
          "ka",
          "ra",
          "ko",
          "bo",
          "re",
          "ru",
          "kotoba",
          "",
          "wo",
          "oto",
          "",
          "shi",
          "te"
        ]
      },
      {
        "ja": "白紙を埋めた僕の歌",
        "romaji": "hakushiwoumetabokunouta",
        "ko": "백지를 채운 나의 노래",
        "charRomaji": [
          "haku",
          "shi",
          "wo",
          "ume",
          "",
          "ta",
          "boku",
          "no",
          "uta"
        ]
      },
      {
        "ja": "届くはずのない叫びが",
        "romaji": "todokuhazunonaisakebiga",
        "ko": "닿을 리 없던 외침이",
        "charRomaji": [
          "todo",
          "",
          "ku",
          "ha",
          "zu",
          "no",
          "na",
          "i",
          "sake",
          "",
          "bi",
          "ga"
        ]
      },
      {
        "ja": "君の音と重なっていく",
        "romaji": "kiminoototokasanatteiku",
        "ko": "너의 소리와 겹쳐져 가",
        "charRomaji": [
          "kimi",
          "no",
          "oto",
          "to",
          "kasa",
          "",
          "na",
          "tte",
          "i",
          "ku"
        ]
      },
      {
        "ja": "ありがとう出会ってくれて",
        "romaji": "arigatoudeattekurete",
        "ko": "고마워, 만나주어서",
        "charRomaji": [
          "a",
          "ri",
          "ga",
          "tou",
          "dea",
          "",
          "tte",
          "ku",
          "re",
          "te"
        ]
      },
      {
        "ja": "一期一会のこの音で",
        "romaji": "ichigoichienokonootode",
        "ko": "일기일회의 이 소리로",
        "charRomaji": [
          "ichi",
          "go",
          "ichi",
          "e",
          "no",
          "ko",
          "no",
          "oto",
          "de"
        ]
      },
      {
        "ja": "僕らは繋がっている",
        "romaji": "bokurawatsunagatteiru",
        "ko": "우리들은 이어져 있어",
        "charRomaji": [
          "boku",
          "ra",
          "wa",
          "tsuna",
          "",
          "ga",
          "tte",
          "i",
          "ru"
        ]
      }
    ]
  },
  {
    "id": "senzaihyoumei",
    "title": "潜在表明",
    "reading": "せんざいひょうめい",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "zF0k41kI868",
    "lines": [
      {
        "ja": "地下鉄の窓に急に映る顔が",
        "romaji": "chikatetsunomadonikyuuniutsurukaoga",
        "ko": "지하철 창문에 갑자기 비치는 얼굴이",
        "charRomaji": [
          "chika",
          "",
          "tetsu",
          "no",
          "mado",
          "ni",
          "kyuu",
          "ni",
          "utsu",
          "",
          "ru",
          "kao",
          "ga"
        ]
      },
      {
        "ja": "じっとこっちを見る",
        "romaji": "jittokocchiwomiru",
        "ko": "가만히 이쪽을 바라봐",
        "charRomaji": [
          "ji",
          "tto",
          "ko",
          "cchi",
          "wo",
          "mi",
          "ru"
        ]
      },
      {
        "ja": "そのひどく不安気な目を",
        "romaji": "sonohidokufuanginamezwo",
        "ko": "그 몹시 불안한 눈을",
        "charRomaji": [
          "so",
          "no",
          "hi",
          "do",
          "ku",
          "fu",
          "an",
          "ge",
          "na",
          "me",
          "wo"
        ]
      },
      {
        "ja": "逸らすことも出来ず立ち尽くしていた",
        "romaji": "sorasukotomodekizutachitsukushiteita",
        "ko": "돌리지도 못하고 우두커니 서 있었어",
        "charRomaji": [
          "sora",
          "",
          "su",
          "ko",
          "to",
          "mo",
          "deki",
          "",
          "zu",
          "tachi",
          "",
          "tsuku",
          "",
          "shi",
          "te",
          "i",
          "ta"
        ]
      },
      {
        "ja": "耳の奥で後ろ指さす声がこだまする",
        "romaji": "miminookudeushirotubisasukoegakodamasuru",
        "ko": "귀 깊은 곳에서 손가락질하는 소리가 메아리쳐",
        "charRomaji": [
          "mimi",
          "no",
          "oku",
          "de",
          "ushiro",
          "",
          "yubi",
          "sa",
          "su",
          "koe",
          "ga",
          "kodama",
          "",
          "su",
          "ru"
        ]
      },
      {
        "ja": "深く深く潜ったままの",
        "romaji": "fukakufukakumuguttamamano",
        "ko": "깊고 깊게 숨죽여 잠든 채의",
        "charRomaji": [
          "fuka",
          "",
          "ku",
          "fuka",
          "",
          "ku",
          "mugu",
          "",
          "tta",
          "ma",
          "ma",
          "no"
        ]
      },
      {
        "ja": "僕の声を抱えて歩いた",
        "romaji": "bokunokoewokakaetearuita",
        "ko": "내 목소리를 끌어안고 걸었어",
        "charRomaji": [
          "boku",
          "no",
          "koe",
          "wo",
          "kaka",
          "",
          "e",
          "te",
          "aru",
          "",
          "i",
          "ta"
        ]
      }
    ]
  },
  {
    "id": "kageiromai",
    "title": "影色舞",
    "reading": "しるえっと だんす",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "zW8bS2Z8d7g",
    "lines": [
      {
        "ja": "あと一匙の憂鬱で",
        "romaji": "atohitosajinoyuuutsude",
        "ko": "앞으로 한 숟가락의 우울로",
        "charRomaji": [
          "a",
          "to",
          "hito",
          "saji",
          "",
          "no",
          "yuu",
          "utsu",
          "de"
        ]
      },
      {
        "ja": "壊れそうなんてのたまえど",
        "romaji": "kowaresounantenotamaedo",
        "ko": "부서질 것 같다고 말하지만",
        "charRomaji": [
          "kowa",
          "",
          "re",
          "sou",
          "na",
          "n",
          "te",
          "no",
          "ta",
          "ma",
          "e",
          "do"
        ]
      },
      {
        "ja": "記憶域圧されてしまう",
        "romaji": "kiokuikiosareteshimau",
        "ko": "기억 영역이 짓눌려 버려",
        "charRomaji": [
          "ki",
          "oku",
          "iki",
          "osa",
          "",
          "re",
          "te",
          "shi",
          "ma",
          "u"
        ]
      },
      {
        "ja": "もうなにもかも忘れて",
        "romaji": "mounanimokamowasurete",
        "ko": "이제 모든 걸 잊어버리고",
        "charRomaji": [
          "mou",
          "na",
          "ni",
          "mo",
          "ka",
          "mo",
          "wasu",
          "",
          "re",
          "te"
        ]
      },
      {
        "ja": "今宵はシルエットダンス",
        "romaji": "koyoiwashiruettodansu",
        "ko": "오늘 밤은 실루엣 댄스",
        "charRomaji": [
          "koyoi",
          "",
          "wa",
          "shi",
          "ru",
          "e",
          "tto",
          "da",
          "n",
          "su"
        ]
      },
      {
        "ja": "知らない要らない全然",
        "romaji": "shiranaiiranaizenzen",
        "ko": "몰라 필요 없어 전혀",
        "charRomaji": [
          "shira",
          "",
          "na",
          "i",
          "ira",
          "",
          "na",
          "i",
          "zen",
          "zen"
        ]
      },
      {
        "ja": "なんの法則もなくただ舞って舞う",
        "romaji": "nannohousokumonakutadamattemau",
        "ko": "어떤 법칙도 없이 그저 춤추고 춤춰",
        "charRomaji": [
          "na",
          "n",
          "no",
          "hou",
          "soku",
          "mo",
          "na",
          "ku",
          "ta",
          "da",
          "ma",
          "tte",
          "ma",
          "u"
        ]
      },
      {
        "ja": "超然的シルエットダンス",
        "romaji": "chouzentekishiruettodansu",
        "ko": "초연한 실루엣 댄스",
        "charRomaji": [
          "chou",
          "zen",
          "teki",
          "shi",
          "ru",
          "e",
          "tto",
          "da",
          "n",
          "su"
        ]
      }
    ]
  },
  {
    "id": "hitoshizuku",
    "title": "壱雫空",
    "reading": "ひとしずく",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "s_A_n9yU64s",
    "lines": [
      {
        "ja": "もしこの雨が上がっても",
        "romaji": "moshikonoamegaagattemo",
        "ko": "만약 이 비가 그치더라도",
        "charRomaji": [
          "mo",
          "shi",
          "ko",
          "no",
          "ame",
          "ga",
          "aga",
          "",
          "tte",
          "mo"
        ]
      },
      {
        "ja": "忘れずに歩いてくよ",
        "romaji": "wasurezuniaruitekuyo",
        "ko": "잊지 않고 걸어갈 거야",
        "charRomaji": [
          "wasu",
          "",
          "re",
          "zu",
          "ni",
          "aru",
          "",
          "i",
          "te",
          "ku",
          "yo"
        ]
      },
      {
        "ja": "最初のひとしずくに",
        "romaji": "saishonohitoshizukuni",
        "ko": "첫 번째 한 방울에",
        "charRomaji": [
          "sai",
          "sho",
          "no",
          "hi",
          "to",
          "shi",
          "zu",
          "ku",
          "ni"
        ]
      },
      {
        "ja": "顔上げた今日の僕を",
        "romaji": "kaoagetakyouanobokuwo",
        "ko": "얼굴을 든 오늘의 나를",
        "charRomaji": [
          "kao",
          "age",
          "",
          "ta",
          "kyou",
          "",
          "no",
          "boku",
          "wo"
        ]
      },
      {
        "ja": "透明な傘で作る",
        "romaji": "toumeinakasadetsukuru",
        "ko": "투명한 우산으로 만드는",
        "charRomaji": [
          "tou",
          "mei",
          "na",
          "kasa",
          "de",
          "tsuku",
          "ru"
        ]
      },
      {
        "ja": "ひとり分だけの世界",
        "romaji": "hitoribundakenosekai",
        "ko": "한 사람 몫만의 세계",
        "charRomaji": [
          "hito",
          "ri",
          "bun",
          "da",
          "ke",
          "no",
          "se",
          "kai"
        ]
      },
      {
        "ja": "この雨が上がってく時",
        "romaji": "konoamegaagattegutoki",
        "ko": "이 비가 그쳐갈 때",
        "charRomaji": [
          "ko",
          "no",
          "ame",
          "ga",
          "aga",
          "",
          "tte",
          "ku",
          "toki"
        ]
      },
      {
        "ja": "過ぎ去ってしまう瞬間を",
        "romaji": "sugisatteshimauimawwo",
        "ko": "지나가 버리는 순간을",
        "charRomaji": [
          "sugi",
          "",
          "sa",
          "tte",
          "shi",
          "ma",
          "u",
          "shun",
          "kan",
          "wo"
        ]
      },
      {
        "ja": "僕はあつめたいよひとしずくを",
        "romaji": "bokuwaatsumetaiyohitoshizukuwo",
        "ko": "나는 모으고 싶어, 한 방울을",
        "charRomaji": [
          "boku",
          "wa",
          "atsu",
          "me",
          "tai",
          "yo",
          "hi",
          "to",
          "shi",
          "zu",
          "ku",
          "wo"
        ]
      }
    ]
  },
  {
    "id": "shiori",
    "title": "栞",
    "reading": "しおり",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "KId3M9bF9uI",
    "lines": [
      {
        "ja": "普通とかあたりまえってなんだろう",
        "romaji": "futsuutokaatarimaettenandarou",
        "ko": "'보통'이라든가 '당연한 것'이란 뭘까",
        "charRomaji": [
          "fu",
          "tsuu",
          "to",
          "ka",
          "a",
          "ta",
          "ri",
          "ma",
          "e",
          "tte",
          "na",
          "n",
          "da",
          "rou"
        ]
      },
      {
        "ja": "今手にある物差しでは",
        "romaji": "imateaniarumonosashidewa",
        "ko": "지금 손에 쥔 잣대로는",
        "charRomaji": [
          "ima",
          "te",
          "ni",
          "a",
          "ru",
          "mono",
          "sashi",
          "",
          "de",
          "wa"
        ]
      },
      {
        "ja": "全然上手く測れなくって",
        "romaji": "zenzenumakuhakarenakutte",
        "ko": "전혀 제대로 잴 수가 없어서",
        "charRomaji": [
          "zen",
          "zen",
          "uma",
          "",
          "ku",
          "haka",
          "",
          "re",
          "na",
          "ku",
          "tte"
        ]
      },
      {
        "ja": "ページの間に挟んだ栞",
        "romaji": "peejinoaidenihasandashiori",
        "ko": "페이지 사이에 끼워둔 책갈피",
        "charRomaji": [
          "pee",
          "",
          "ji",
          "no",
          "aida",
          "",
          "ni",
          "hasa",
          "",
          "n",
          "da",
          "shiori"
        ]
      },
      {
        "ja": "君と過ごした日々の印",
        "romaji": "kimitosugoshitahibinoshirushi",
        "ko": "너와 함께 보낸 날들의 표시",
        "charRomaji": [
          "kimi",
          "to",
          "sugo",
          "",
          "shi",
          "ta",
          "hi",
          "bi",
          "no",
          "shirushi"
        ]
      },
      {
        "ja": "めくるたび甦る記憶",
        "romaji": "mekurutabiyomigaerukioku",
        "ko": "넘길 때마다 되살아나는 기억",
        "charRomaji": [
          "me",
          "ku",
          "ru",
          "ta",
          "bi",
          "yomi",
          "gae",
          "",
          "ru",
          "ki",
          "oku"
        ]
      },
      {
        "ja": "迷いながら歩いた道も",
        "romaji": "mayoinagaraaruitamichimo",
        "ko": "헤매며 걸었던 길도",
        "charRomaji": [
          "mayo",
          "",
          "i",
          "na",
          "ga",
          "ra",
          "aru",
          "",
          "i",
          "ta",
          "michi",
          "mo"
        ]
      },
      {
        "ja": "いつか宝物になるから",
        "romaji": "itsukatakaramononinarukara",
        "ko": "언젠가 보물이 될 테니까",
        "charRomaji": [
          "i",
          "tsu",
          "ka",
          "takara",
          "mono",
          "",
          "ni",
          "na",
          "ru",
          "ka",
          "ra"
        ]
      }
    ]
  },
  {
    "id": "tanebi",
    "title": "焚音打",
    "reading": "たねび",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "zX11UeP3h4Q",
    "lines": [
      {
        "ja": "きっと理由はバラバラだった",
        "romaji": "kittoriyuuwabarabaradatta",
        "ko": "분명 이유는 제각각이었어",
        "charRomaji": [
          "ki",
          "tto",
          "ri",
          "yuu",
          "wa",
          "ba",
          "ra",
          "ba",
          "ra",
          "da",
          "tta"
        ]
      },
      {
        "ja": "寄る辺のないあの日の僕たち",
        "romaji": "yorubenonaianohinobokutachi",
        "ko": "의지할 곳 없던 그날의 우리들",
        "charRomaji": [
          "yo",
          "ru",
          "be",
          "no",
          "na",
          "i",
          "a",
          "no",
          "hi",
          "no",
          "boku",
          "tachi",
          ""
        ]
      },
      {
        "ja": "もう二度と傷つきたくないって",
        "romaji": "mounidotokizutsukitakunaitte",
        "ko": "더는 상처받고 싶지 않다고",
        "charRomaji": [
          "mou",
          "ni",
          "do",
          "to",
          "kizu",
          "tsu",
          "ki",
          "ta",
          "ku",
          "na",
          "i",
          "tte"
        ]
      },
      {
        "ja": "そう思ってうつむいたのに",
        "romaji": "souomotteutsumuitanoni",
        "ko": "그렇게 생각하며 고개 숙였는데",
        "charRomaji": [
          "sou",
          "omo",
          "",
          "tte",
          "u",
          "tsu",
          "mu",
          "i",
          "ta",
          "no",
          "ni"
        ]
      },
      {
        "ja": "迷ってたから出会えて",
        "romaji": "mayottetakaratdeatte",
        "ko": "헤매고 있었기에 만날 수 있어서",
        "charRomaji": [
          "mayo",
          "",
          "tte",
          "ta",
          "ka",
          "ra",
          "dea",
          "",
          "e",
          "te"
        ]
      },
      {
        "ja": "やっと繋いだ手を",
        "romaji": "yattotsunaidatewo",
        "ko": "겨우 맞잡은 손을",
        "charRomaji": [
          "ya",
          "tto",
          "tsuna",
          "",
          "i",
          "da",
          "te",
          "wo"
        ]
      },
      {
        "ja": "もう僕は離さない",
        "romaji": "moubokuwahanasanai",
        "ko": "이제 난 놓지 않을 거야",
        "charRomaji": [
          "mou",
          "boku",
          "wa",
          "hana",
          "",
          "sa",
          "na",
          "i"
        ]
      },
      {
        "ja": "何があっても握りしめていく",
        "romaji": "nanigaattomonigirishimeteiku",
        "ko": "무슨 일이 있어도 꽉 쥐고 갈 거야",
        "charRomaji": [
          "nani",
          "ga",
          "a",
          "tte",
          "mo",
          "nigiri",
          "",
          "shi",
          "me",
          "te",
          "i",
          "ku"
        ]
      }
    ]
  },
  {
    "id": "hekitenbansou",
    "title": "碧天伴走",
    "reading": "へきてんばんそう",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "y_QO3Y_d-o4",
    "lines": [
      {
        "ja": "人知れず肩落としてる君がいるのに",
        "romaji": "hitoshirezukataotoshiterukimigairunoni",
        "ko": "남몰래 어깨를 떨구는 네가 있는데",
        "charRomaji": [
          "hito",
          "shire",
          "",
          "zu",
          "kata",
          "oto",
          "",
          "shi",
          "te",
          "ru",
          "kimi",
          "ga",
          "i",
          "ru",
          "no",
          "ni"
        ]
      },
      {
        "ja": "碧すぎてる空ばかりが眩しい",
        "romaji": "aokusugiterusorabakarigamabushii",
        "ko": "너무도 푸른 하늘만이 눈부셔",
        "charRomaji": [
          "aoku",
          "",
          "sugi",
          "",
          "te",
          "ru",
          "sora",
          "ba",
          "ka",
          "ri",
          "ga",
          "mabu",
          "shii",
          ""
        ]
      },
      {
        "ja": "僕はどんな言葉を君に言えばいいのか",
        "romaji": "bokuwadonnakotobawokiminiiebaiinoka",
        "ko": "나는 어떤 말을 네게 건네야 좋을까",
        "charRomaji": [
          "boku",
          "wa",
          "do",
          "n",
          "na",
          "kotoba",
          "",
          "wo",
          "kimi",
          "ni",
          "ie",
          "",
          "ba",
          "i",
          "i",
          "no",
          "ka"
        ]
      },
      {
        "ja": "君に何を伝えられるだろう",
        "romaji": "kimininaniwotsutaerarerudarou",
        "ko": "너에게 무엇을 전할 수 있을까",
        "charRomaji": [
          "kimi",
          "ni",
          "nani",
          "wo",
          "tsutae",
          "",
          "ra",
          "re",
          "ru",
          "da",
          "rou"
        ]
      },
      {
        "ja": "躓いて転んだって",
        "romaji": "tsumazuitekorondatte",
        "ko": "걸려 넘어진다 해도",
        "charRomaji": [
          "tsumazui",
          "",
          "",
          "te",
          "koron",
          "",
          "da",
          "tte"
        ]
      },
      {
        "ja": "立ち上がり来たんだ",
        "romaji": "tachiagarikitanda",
        "ko": "다시 일어서서 여기까지 왔잖아",
        "charRomaji": [
          "tachi",
          "aga",
          "",
          "ri",
          "ki",
          "ta",
          "n",
          "da"
        ]
      },
      {
        "ja": "頑張ってるいつでも",
        "romaji": "ganbatteruitsudemo",
        "ko": "언제나 힘내고 있어",
        "charRomaji": [
          "ganba",
          "",
          "tte",
          "ru",
          "i",
          "tsu",
          "de",
          "mo"
        ]
      },
      {
        "ja": "ここに立ってるだけで",
        "romaji": "kokonitatterudakede",
        "ko": "여기에 서 있는 것만으로도",
        "charRomaji": [
          "ko",
          "ko",
          "ni",
          "ta",
          "tte",
          "ru",
          "da",
          "ke",
          "de"
        ]
      },
      {
        "ja": "迷っても君と走っていきたいんだよ",
        "romaji": "mayottemokimitohashitteikitaindayo",
        "ko": "헤매더라도 너와 함께 달려가고 싶어",
        "charRomaji": [
          "mayo",
          "",
          "tte",
          "mo",
          "kimi",
          "to",
          "hashi",
          "",
          "tte",
          "i",
          "ki",
          "ta",
          "i",
          "n",
          "da",
          "yo"
        ]
      }
    ]
  },
  {
    "id": "utaimashou",
    "title": "歌いましょう鳴らしましょう",
    "reading": "うたいましょうならしましょう",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "zF0k41kI868",
    "lines": [
      {
        "ja": "鑑賞用の花のように遠くで",
        "romaji": "kanshouyounohananoyounitookude",
        "ko": "관상용 꽃처럼 먼 곳에서",
        "charRomaji": [
          "kan",
          "shou",
          "you",
          "no",
          "hana",
          "no",
          "you",
          "ni",
          "too",
          "ku",
          "de"
        ]
      },
      {
        "ja": "私見てるだけでいいのかい",
        "romaji": "watashimiterudakedeiinokai",
        "ko": "나를 그저 바라보기만 하면 되는 거니",
        "charRomaji": [
          "watashi",
          "mi",
          "te",
          "ru",
          "da",
          "ke",
          "de",
          "i",
          "i",
          "no",
          "kai"
        ]
      },
      {
        "ja": "歌いましょう鳴らしましょう",
        "romaji": "utaimashounarashimashou",
        "ko": "노래합시다 울려 퍼트립시다",
        "charRomaji": [
          "uta",
          "i",
          "ma",
          "shou",
          "nara",
          "",
          "shi",
          "ma",
          "shou"
        ]
      },
      {
        "ja": "この胸の衝動を解き放て",
        "romaji": "konomunenosyoudouwotokihanate",
        "ko": "이 가슴의 충동을 해방해",
        "charRomaji": [
          "ko",
          "no",
          "mune",
          "no",
          "shou",
          "dou",
          "wo",
          "toki",
          "hana",
          "",
          "te"
        ]
      },
      {
        "ja": "泥だらけの靴で踏み鳴らせ",
        "romaji": "dorodarakenokutsudefuminarase",
        "ko": "흙투성이 신발로 힘차게 굴러봐",
        "charRomaji": [
          "doro",
          "da",
          "ra",
          "ke",
          "no",
          "kutsu",
          "de",
          "fumi",
          "nara",
          "",
          "se"
        ]
      },
      {
        "ja": "僕らの音を響かせていこう",
        "romaji": "bokuranootowohibikaseteikou",
        "ko": "우리들의 소리를 울려 퍼트려 가자",
        "charRomaji": [
          "boku",
          "ra",
          "no",
          "oto",
          "wo",
          "hibi",
          "",
          "ka",
          "se",
          "te",
          "i",
          "kou"
        ]
      }
    ]
  },
  {
    "id": "haruhikage",
    "title": "春日影 (MyGO!!!!! ver.)",
    "reading": "はるひかげ",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "a9t98mP179E",
    "lines": [
      {
        "ja": "かじかんだ心震えるまなざし",
        "romaji": "kajikandakokorofuruerumanazashi",
        "ko": "얼어붙은 마음, 떨리는 눈빛",
        "charRomaji": [
          "ka",
          "ji",
          "ka",
          "n",
          "da",
          "kokoro",
          "furu",
          "",
          "e",
          "ru",
          "ma",
          "na",
          "za",
          "shi"
        ]
      },
      {
        "ja": "世界で僕はひとりぼっちだった",
        "romaji": "sekaidebokuwahitoribocchidatta",
        "ko": "세상에서 나는 외톨이였어",
        "charRomaji": [
          "se",
          "kai",
          "de",
          "boku",
          "wa",
          "hi",
          "to",
          "ri",
          "bo",
          "cchi",
          "da",
          "tta"
        ]
      },
      {
        "ja": "散ることしか知らない春は",
        "romaji": "chirukotoshikashiranaiharuwa",
        "ko": "지는 것밖에 모르는 봄은",
        "charRomaji": [
          "chi",
          "ru",
          "ko",
          "to",
          "shi",
          "ka",
          "shira",
          "",
          "na",
          "i",
          "haru",
          "wa"
        ]
      },
      {
        "ja": "毎年冷たくあしらう",
        "romaji": "maitoshitsumetakuaishirau",
        "ko": "매년 매정하게 대하네",
        "charRomaji": [
          "mai",
          "toshi",
          "tsume",
          "",
          "ta",
          "ku",
          "a",
          "shi",
          "ra",
          "u"
        ]
      },
      {
        "ja": "暗がりの中一方通行に",
        "romaji": "kuragarinonakaippoutsuukouni",
        "ko": "어둠 속 일방통행으로",
        "charRomaji": [
          "kura",
          "ga",
          "ri",
          "no",
          "naka",
          "i",
          "ppou",
          "tsuu",
          "kou",
          "ni"
        ]
      },
      {
        "ja": "ただただ言葉を書き殴って",
        "romaji": "tadatadakotobawokakinagutte",
        "ko": "그저 말을 휘갈겨 쓰며",
        "charRomaji": [
          "ta",
          "da",
          "ta",
          "da",
          "kotoba",
          "",
          "wo",
          "kaki",
          "nagu",
          "",
          "tte"
        ]
      },
      {
        "ja": "雲間を縫ってきらりきらり",
        "romaji": "kumomawonuuttekirarikirari",
        "ko": "구름 사이를 뚫고 반짝반짝",
        "charRomaji": [
          "kumo",
          "ma",
          "wo",
          "nu",
          "tte",
          "ki",
          "ra",
          "ri",
          "ki",
          "ra",
          "ri"
        ]
      },
      {
        "ja": "心満たしてはあふれ",
        "romaji": "kokoromitashitehaafure",
        "ko": "마음을 채우고는 넘쳐흘러",
        "charRomaji": [
          "kokoro",
          "mita",
          "",
          "shi",
          "te",
          "wa",
          "a",
          "fu",
          "re"
        ]
      },
      {
        "ja": "君の手はどうしてこんなにも温かいの",
        "romaji": "kiminotewadoushitekonnanimonatakaino",
        "ko": "네 손은 어째서 이렇게나 따스한 걸까",
        "charRomaji": [
          "kimi",
          "no",
          "te",
          "wa",
          "dou",
          "shi",
          "te",
          "ko",
          "n",
          "na",
          "ni",
          "mo",
          "atataka",
          "",
          "i",
          "no"
        ]
      },
      {
        "ja": "どうかこのまま離さないでいて",
        "romaji": "doukakonomamahanasanaideite",
        "ko": "부디 이대로 손을 놓지 말아줘",
        "charRomaji": [
          "dou",
          "ka",
          "ko",
          "no",
          "ma",
          "ma",
          "hana",
          "",
          "sa",
          "na",
          "i",
          "de",
          "i",
          "te"
        ]
      }
    ]
  },
  {
    "id": "utakotoba",
    "title": "詩超絆",
    "reading": "うたことば",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "QkX594yX8jE",
    "lines": [
      {
        "ja": "僕にはわからないんだいつも",
        "romaji": "bokuniwawakaranaindaitsumo",
        "ko": "내게는 알 수 없는 거야 언제나",
        "charRomaji": [
          "boku",
          "ni",
          "wa",
          "wa",
          "ka",
          "ra",
          "na",
          "i",
          "n",
          "da",
          "i",
          "tsu",
          "mo"
        ]
      },
      {
        "ja": "みつけられない正解も普通も",
        "romaji": "mitsukerarenaiseikaimofutsuumo",
        "ko": "찾을 수 없어 정답도 보통도",
        "charRomaji": [
          "mi",
          "tsu",
          "ke",
          "ra",
          "re",
          "na",
          "i",
          "sei",
          "kai",
          "mo",
          "fu",
          "tsuu",
          "mo"
        ]
      },
      {
        "ja": "世界はずっとずっと遠く",
        "romaji": "sekaiwazuttozuttotooku",
        "ko": "세상은 줄곧 아득히 먼",
        "charRomaji": [
          "se",
          "kai",
          "wa",
          "zu",
          "tto",
          "zu",
          "tto",
          "too",
          "ku"
        ]
      },
      {
        "ja": "僕には届かない場所にあるんだ",
        "romaji": "bokuniwatodokanaibashonianrunda",
        "ko": "내겐 닿지 않는 곳에 있는 거야",
        "charRomaji": [
          "boku",
          "ni",
          "wa",
          "todo",
          "",
          "ka",
          "na",
          "i",
          "ba",
          "sho",
          "ni",
          "a",
          "ru",
          "n",
          "da"
        ]
      },
      {
        "ja": "戻りたい伝えたい",
        "romaji": "modoritaitutaetai",
        "ko": "돌아가고 싶어 전하고 싶어",
        "charRomaji": [
          "modo",
          "",
          "ri",
          "tai",
          "tsuta",
          "",
          "e",
          "tai"
        ]
      },
      {
        "ja": "許されるなら僕は諦めたくない",
        "romaji": "yurusarerunarabokuwaakirametakunai",
        "ko": "용서받을 수 있다면 난 포기하고 싶지 않아",
        "charRomaji": [
          "yuru",
          "",
          "sa",
          "re",
          "ru",
          "na",
          "ra",
          "boku",
          "wa",
          "akira",
          "",
          "me",
          "ta",
          "ku",
          "na",
          "i"
        ]
      },
      {
        "ja": "うたういまああ届いて",
        "romaji": "utauimaaatodoite",
        "ko": "노래해 지금, 아아 닿기를",
        "charRomaji": [
          "u",
          "ta",
          "u",
          "ima",
          "a",
          "a",
          "todo",
          "",
          "i",
          "te"
        ]
      },
      {
        "ja": "君の胸にまだ間に合うかい",
        "romaji": "kiminomunenimadamaniaukai",
        "ko": "너의 가슴에 아직 늦지 않았을까",
        "charRomaji": [
          "kimi",
          "no",
          "mune",
          "ni",
          "ma",
          "da",
          "ma",
          "ni",
          "a",
          "u",
          "kai"
        ]
      },
      {
        "ja": "言葉を超えるため心を叫ぶ",
        "romaji": "kotobawokoerutamekokorowosakebu",
        "ko": "말을 뛰어넘기 위해 마음을 외쳐",
        "charRomaji": [
          "kotoba",
          "",
          "wo",
          "koe",
          "",
          "ru",
          "ta",
          "me",
          "kokoro",
          "wo",
          "sake",
          "bu"
        ]
      }
    ]
  },
  {
    "id": "meirohibi",
    "title": "迷路日々",
    "reading": "めいろひび",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "W2R2G9w2N-Q",
    "lines": [
      {
        "ja": "迷いながら戸惑いながら歩く",
        "romaji": "mayoinagaratomadoinagaraaruku",
        "ko": "헤매면서 망설이면서 걸어",
        "charRomaji": [
          "mayo",
          "",
          "i",
          "na",
          "ga",
          "ra",
          "tomado",
          "",
          "i",
          "na",
          "ga",
          "ra",
          "aru",
          "",
          "ku"
        ]
      },
      {
        "ja": "めいろの中で僕らは居合わせてた",
        "romaji": "meirononakadebokurawaimawasateta",
        "ko": "미로 속에서 우리들은 우연히 함께 있었어",
        "charRomaji": [
          "me",
          "i",
          "ro",
          "no",
          "naka",
          "de",
          "boku",
          "ra",
          "wa",
          "i",
          "a",
          "wa",
          "se",
          "te",
          "ta"
        ]
      },
      {
        "ja": "名前のない感情ああ抱きしめてる",
        "romaji": "namaenonaikanjouaadakishimeteru",
        "ko": "이름 없는 감정 아아 끌어안고 있어",
        "charRomaji": [
          "namae",
          "",
          "no",
          "na",
          "i",
          "kan",
          "jou",
          "a",
          "a",
          "daki",
          "",
          "shi",
          "me",
          "te",
          "ru"
        ]
      },
      {
        "ja": "ちいさな一瞬あつめたい",
        "romaji": "chiisananaisshunatsumetai",
        "ko": "작은 한순간을 모으고 싶어",
        "charRomaji": [
          "chi",
          "i",
          "sa",
          "na",
          "i",
          "sshun",
          "atsu",
          "me",
          "tai"
        ]
      },
      {
        "ja": "出口なんてどこにも見えなくても",
        "romaji": "deguchinantedokonimomienakutemo",
        "ko": "출구 따윈 어디에도 보이지 않는다 해도",
        "charRomaji": [
          "de",
          "guchi",
          "na",
          "n",
          "te",
          "do",
          "ko",
          "ni",
          "mo",
          "mie",
          "",
          "na",
          "ku",
          "te",
          "mo"
        ]
      },
      {
        "ja": "君と手をつないで進む日々",
        "romaji": "kimitotewotsunaidesusumuhibi",
        "ko": "너와 손을 잡고 나아가는 나날",
        "charRomaji": [
          "kimi",
          "to",
          "te",
          "wo",
          "tsuna",
          "",
          "i",
          "de",
          "susu",
          "",
          "mu",
          "hi",
          "bi"
        ]
      }
    ]
  },
  {
    "id": "noroshi",
    "title": "無路矢",
    "reading": "のろし",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "v8K8a0Q81rA",
    "lines": [
      {
        "ja": "無軌道を描く足跡でも",
        "romaji": "mukidouwokakuashiattodemo",
        "ko": "갈피 없는 궤도를 그리는 발자국이라도",
        "charRomaji": [
          "mu",
          "ki",
          "dou",
          "wo",
          "eka",
          "",
          "ku",
          "ashi",
          "ato",
          "de",
          "mo"
        ]
      },
      {
        "ja": "進み続けた",
        "romaji": "susumitsuzuketa",
        "ko": "계속해서 나아갔어",
        "charRomaji": [
          "susu",
          "",
          "mi",
          "tsuzu",
          "",
          "ke",
          "ta"
        ]
      },
      {
        "ja": "ほつれそうな心で",
        "romaji": "hotsuresounakokorode",
        "ko": "풀려버릴 것 같은 마음으로",
        "charRomaji": [
          "ho",
          "tsu",
          "re",
          "sou",
          "na",
          "kokoro",
          "de"
        ]
      },
      {
        "ja": "どこから来てどこに向かう",
        "romaji": "dokokarakitedokonimukau",
        "ko": "어디에서 와서 어디로 향하는가",
        "charRomaji": [
          "do",
          "ko",
          "ka",
          "ra",
          "ki",
          "te",
          "do",
          "ko",
          "ni",
          "muka",
          "u"
        ]
      },
      {
        "ja": "何を信じて生きていくの",
        "romaji": "naniwoshinjiteikiteikuno",
        "ko": "무엇을 믿고 살아가는 걸까",
        "charRomaji": [
          "nani",
          "wo",
          "shin",
          "ji",
          "te",
          "iki",
          "",
          "te",
          "i",
          "ku",
          "no"
        ]
      },
      {
        "ja": "道標も地図もなくて",
        "romaji": "douhyoumouchizumonakute",
        "ko": "이정표도 지도도 없이",
        "charRomaji": [
          "michi",
          "shirube",
          "mo",
          "chi",
          "zu",
          "mo",
          "na",
          "ku",
          "te"
        ]
      },
      {
        "ja": "フラつく足で掲げた狼煙",
        "romaji": "furatsukuashidekakagetanoroshi",
        "ko": "비틀거리는 걸음으로 피워 올린 봉화",
        "charRomaji": [
          "fu",
          "ra",
          "tsu",
          "ku",
          "ashi",
          "de",
          "kaka",
          "",
          "ge",
          "ta",
          "no",
          "ro",
          "shi"
        ]
      }
    ]
  },
  {
    "id": "sasunso",
    "title": "砂寸奏",
    "reading": "さすらい",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "Y5V-92Pq8Xw",
    "lines": [
      {
        "ja": "同じ音符を追いかけるのに",
        "romaji": "onajionpuwooikakerunoni",
        "ko": "같은 음표를 쫓아가는데도",
        "charRomaji": [
          "ona",
          "",
          "ji",
          "on",
          "pu",
          "wo",
          "oi",
          "",
          "ka",
          "ke",
          "ru",
          "no",
          "ni"
        ]
      },
      {
        "ja": "ズレていくのはどうしてだろう",
        "romaji": "zureteikuwadowshitedarou",
        "ko": "어긋나 버리는 건 어째서일까",
        "charRomaji": [
          "zu",
          "re",
          "te",
          "i",
          "ku",
          "no",
          "wa",
          "dou",
          "shi",
          "te",
          "da",
          "rou"
        ]
      },
      {
        "ja": "砂の粒のようにこぼれ落ちて",
        "romaji": "sunanotsubunoyounikoboreochite",
        "ko": "모래알처럼 손에서 흘러넘쳐 떨어져",
        "charRomaji": [
          "suna",
          "no",
          "tsubu",
          "no",
          "you",
          "ni",
          "kobo",
          "",
          "re",
          "ochi",
          "",
          "te"
        ]
      },
      {
        "ja": "足跡さえも消えてしまう",
        "romaji": "ashiattosaemokieteshimau",
        "ko": "발자국마저 지워져 버려",
        "charRomaji": [
          "ashi",
          "ato",
          "sa",
          "e",
          "mo",
          "kie",
          "",
          "te",
          "shi",
          "ma",
          "u"
        ]
      },
      {
        "ja": "それでも鳴らす僕らのリズム",
        "romaji": "soredemonarasubokuranorizumu",
        "ko": "그럼에도 울리는 우리들의 리듬",
        "charRomaji": [
          "so",
          "re",
          "de",
          "mo",
          "nara",
          "",
          "su",
          "boku",
          "ra",
          "no",
          "ri",
          "zu",
          "mu"
        ]
      },
      {
        "ja": "さすらいながら明日を探そう",
        "romaji": "sasurainagaraashitawosagasou",
        "ko": "방랑하면서 내일을 찾아가자",
        "charRomaji": [
          "sa",
          "su",
          "ra",
          "i",
          "na",
          "ga",
          "ra",
          "ashita",
          "",
          "wo",
          "saga",
          "",
          "sou"
        ]
      }
    ]
  },
  {
    "id": "kaisoufu",
    "title": "回層浮",
    "reading": "かいそうふ",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "gQO9mZq_T0A",
    "lines": [
      {
        "ja": "真夜中の入り口",
        "romaji": "mayonakanoniriguchi",
        "ko": "한밤중의 입구",
        "charRomaji": [
          "ma",
          "yo",
          "naka",
          "no",
          "iri",
          "guchi",
          ""
        ]
      },
      {
        "ja": "不意にぶり返した孤独",
        "romaji": "fuiniburihaeshitakodoku",
        "ko": "불현듯 되살아난 고독",
        "charRomaji": [
          "fu",
          "i",
          "ni",
          "buri",
          "kae",
          "",
          "shi",
          "ta",
          "ko",
          "doku"
        ]
      },
      {
        "ja": "水底に沈む光を見つめて",
        "romaji": "minasokonisizumuhikariwomitsumete",
        "ko": "물밑으로 가라앉는 빛을 바라보며",
        "charRomaji": [
          "mina",
          "soko",
          "ni",
          "shizu",
          "",
          "mu",
          "hikari",
          "wo",
          "mitsu",
          "",
          "me",
          "te"
        ]
      },
      {
        "ja": "浮かんでは消える記憶の層",
        "romaji": "ukandewakierukiokunosou",
        "ko": "떠올랐다 사라지는 기억의 층",
        "charRomaji": [
          "uka",
          "",
          "n",
          "de",
          "wa",
          "kie",
          "",
          "ru",
          "ki",
          "oku",
          "no",
          "sou"
        ]
      },
      {
        "ja": "息を吸い込んで泳ぎ出す",
        "romaji": "ikiwosuiikondeoyogidasu",
        "ko": "숨을 들이마시고 헤엄쳐 나가",
        "charRomaji": [
          "iki",
          "wo",
          "sui",
          "",
          "ko",
          "n",
          "de",
          "oyo",
          "",
          "gi",
          "da",
          "su"
        ]
      }
    ]
  },
  {
    "id": "shokyuusei",
    "title": "処救生",
    "reading": "こきゅう",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "H4K4aP8w09U",
    "lines": [
      {
        "ja": "こたえあわせ",
        "romaji": "kotaeawase",
        "ko": "답 맞춰보기",
        "charRomaji": [
          "ko",
          "ta",
          "e",
          "a",
          "wa",
          "se"
        ]
      },
      {
        "ja": "丸と罰に埋もれ",
        "romaji": "marutobatsuniumore",
        "ko": "동그라미와 가위표에 파묻혀",
        "charRomaji": [
          "maru",
          "to",
          "batsu",
          "ni",
          "umo",
          "",
          "re"
        ]
      },
      {
        "ja": "息苦しい部屋の中で",
        "romaji": "ikigurushiibeyanonakade",
        "ko": "숨 막히는 방 안에서",
        "charRomaji": [
          "iki",
          "guru",
          "",
          "shii",
          "he",
          "ya",
          "no",
          "naka",
          "de"
        ]
      },
      {
        "ja": "命の音を確かめていた",
        "romaji": "inochinootowotashikameteita",
        "ko": "생명의 소리를 확인하고 있었어",
        "charRomaji": [
          "inochi",
          "no",
          "oto",
          "wo",
          "tashika",
          "",
          "me",
          "te",
          "i",
          "ta"
        ]
      },
      {
        "ja": "救いを求めて叫ぶ呼吸",
        "romaji": "sukuiwomotometesakebukokyuu",
        "ko": "구원을 바라며 외치는 호흡",
        "charRomaji": [
          "suku",
          "",
          "i",
          "wo",
          "moto",
          "",
          "me",
          "te",
          "sake",
          "",
          "bu",
          "ko",
          "kyuu"
        ]
      }
    ]
  },
  {
    "id": "hashidoyama",
    "title": "端程山",
    "reading": "ぱのらま",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "6mJm078vGZQ",
    "lines": [
      {
        "ja": "どこまで歩けばいいのかなんて",
        "romaji": "dokomadearukebaiinokanante",
        "ko": "어디까지 걸어야 하는지 따윈",
        "charRomaji": [
          "do",
          "ko",
          "ma",
          "de",
          "aru",
          "",
          "ke",
          "ba",
          "i",
          "i",
          "no",
          "ka",
          "na",
          "n",
          "te"
        ]
      },
      {
        "ja": "知らないまま踏みしめてた",
        "romaji": "shiranaimamafumishimeteta",
        "ko": "모른 채 꾹꾹 내딛고 있었어",
        "charRomaji": [
          "shira",
          "",
          "na",
          "i",
          "ma",
          "ma",
          "fumi",
          "shime",
          "",
          "te",
          "ta"
        ]
      },
      {
        "ja": "見上げた空の広さに息をのむ",
        "romaji": "miagetasoranohirosaniikiwonomu",
        "ko": "올려다본 하늘의 넓음에 숨을 삼켜",
        "charRomaji": [
          "mi",
          "age",
          "",
          "ta",
          "sora",
          "no",
          "hiro",
          "",
          "sa",
          "ni",
          "iki",
          "wo",
          "no",
          "mu"
        ]
      },
      {
        "ja": "広がるパノラマの向こうへ",
        "romaji": "hirogarupanoramanomukouhe",
        "ko": "펼쳐지는 파노라마의 저편으로",
        "charRomaji": [
          "hiro",
          "",
          "ga",
          "ru",
          "pa",
          "no",
          "ra",
          "ma",
          "no",
          "mukou",
          "",
          "e"
        ]
      }
    ]
  },
  {
    "id": "rinpuu",
    "title": "輪符雨",
    "reading": "りふれいん",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "L-Z8B8X8Y-k",
    "lines": [
      {
        "ja": "硝子窓はすぐに雲に覆われて",
        "romaji": "garasumadowasugunikumonioowarete",
        "ko": "유리창은 곧바로 구름에 뒤덮이고",
        "charRomaji": [
          "garasu",
          "",
          "",
          "mado",
          "wa",
          "su",
          "gu",
          "ni",
          "kumo",
          "ni",
          "oowa",
          "",
          "re",
          "te"
        ]
      },
      {
        "ja": "冷たい雨が降り続く",
        "romaji": "tsumetaiamegafuritsuzuku",
        "ko": "차가운 비가 끝없이 내려",
        "charRomaji": [
          "tsume",
          "",
          "ta",
          "i",
          "ame",
          "ga",
          "furi",
          "tsuzu",
          "",
          "ku"
        ]
      },
      {
        "ja": "繰り返すメロディのように",
        "romaji": "kurikaesumerodinoyouni",
        "ko": "반복되는 멜로디처럼",
        "charRomaji": [
          "kuri",
          "kae",
          "",
          "su",
          "me",
          "ro",
          "di",
          "no",
          "you",
          "ni"
        ]
      },
      {
        "ja": "僕らの涙を洗い流して",
        "romaji": "bokuranonamidawowarainagashite",
        "ko": "우리들의 눈물을 씻어내 줘",
        "charRomaji": [
          "boku",
          "ra",
          "no",
          "namida",
          "wo",
          "arai",
          "naga",
          "",
          "shi",
          "te"
        ]
      }
    ]
  },
  {
    "id": "kokairou",
    "title": "孤壊牢",
    "reading": "こころ",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "v8K8a0Q81rA",
    "lines": [
      {
        "ja": "まるで違う生き物なのに",
        "romaji": "marudechigauikimononanoni",
        "ko": "마치 다른 생물인데도",
        "charRomaji": [
          "ma",
          "ru",
          "de",
          "chiga",
          "",
          "u",
          "iki",
          "mono",
          "",
          "na",
          "no",
          "ni"
        ]
      },
      {
        "ja": "何故か僕ら一括りで",
        "romaji": "nazekabokurahitokukuride",
        "ko": "어째서인지 우릴 하나로 묶어버리고",
        "charRomaji": [
          "naze",
          "ka",
          "boku",
          "ra",
          "hito",
          "kukuri",
          "",
          "de"
        ]
      },
      {
        "ja": "檻の中で叫び続けている",
        "romaji": "orinonakadesakebitsuzuketeiru",
        "ko": "우리 안에서 계속 외치고 있어",
        "charRomaji": [
          "ori",
          "no",
          "naka",
          "de",
          "sake",
          "",
          "bi",
          "tsuzu",
          "",
          "ke",
          "te",
          "i",
          "ru"
        ]
      },
      {
        "ja": "壊れそうな心を抱いて",
        "romaji": "kowaresounakokorowodaite",
        "ko": "부서질 것 같은 마음을 품고",
        "charRomaji": [
          "kowa",
          "",
          "re",
          "sou",
          "na",
          "kokoro",
          "wo",
          "da",
          "i",
          "te"
        ]
      }
    ]
  },
  {
    "id": "hoshuudou",
    "title": "歩拾道",
    "reading": "ほしゅうどう",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "Y5V-92Pq8Xw",
    "lines": [
      {
        "ja": "ツギハギのコンクリートを歩いていく",
        "romaji": "tsugihaginokonkuriitowoaruiteiku",
        "ko": "기워 맞춘 콘크리트 위를 걸어가",
        "charRomaji": [
          "tsu",
          "gi",
          "ha",
          "gi",
          "no",
          "ko",
          "n",
          "ku",
          "rii",
          "to",
          "wo",
          "aru",
          "",
          "i",
          "te",
          "i",
          "ku"
        ]
      },
      {
        "ja": "落としたものを一つずつ拾い集めて",
        "romaji": "otoshitamonowohitotsuzutsuhiroiatsumete",
        "ko": "떨어뜨린 것들을 하나씩 주워 모으며",
        "charRomaji": [
          "oto",
          "",
          "shi",
          "ta",
          "mono",
          "wo",
          "hito",
          "tsu",
          "zu",
          "tsu",
          "hiro",
          "",
          "i",
          "atsu",
          "",
          "me",
          "te"
        ]
      },
      {
        "ja": "スピードを上げて進む道",
        "romaji": "supiidowoaagetesusumumichi",
        "ko": "속도를 올려 나아가는 길",
        "charRomaji": [
          "su",
          "pii",
          "do",
          "wo",
          "age",
          "",
          "te",
          "susu",
          "",
          "mu",
          "michi"
        ]
      }
    ]
  },
  {
    "id": "yaonzen",
    "title": "夜隠染",
    "reading": "よかぜ",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "6mJm078vGZQ",
    "lines": [
      {
        "ja": "あきらめれば楽だった",
        "romaji": "akiramerebarakudatta",
        "ko": "포기하면 편했을 텐데",
        "charRomaji": [
          "a",
          "ki",
          "ra",
          "me",
          "re",
          "ba",
          "raku",
          "da",
          "tta"
        ]
      },
      {
        "ja": "夜風が吹き抜ける街で",
        "romaji": "yokazegafukinukerumachide",
        "ko": "밤바람이 불어 지나가는 거리에서",
        "charRomaji": [
          "yo",
          "kaze",
          "ga",
          "fuki",
          "nuke",
          "",
          "ru",
          "machi",
          "de"
        ]
      },
      {
        "ja": "染まっていく暗闇に抗うように",
        "romaji": "somatteikukurayaminiaragauyouni",
        "ko": "물들어가는 어둠에 맞서듯이",
        "charRomaji": [
          "soma",
          "",
          "tte",
          "i",
          "ku",
          "kura",
          "yami",
          "ni",
          "araga",
          "",
          "u",
          "you",
          "ni"
        ]
      },
      {
        "ja": "僕らは小さな火を灯す",
        "romaji": "bokurawachiisanahiwotomosu",
        "ko": "우리는 작은 불을 지펴",
        "charRomaji": [
          "boku",
          "ra",
          "wa",
          "chii",
          "sa",
          "na",
          "hi",
          "wo",
          "tomo",
          "su"
        ]
      }
    ]
  },
  {
    "id": "mushuutou",
    "title": "霧周途",
    "reading": "みすと",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "L-Z8B8X8Y-k",
    "lines": [
      {
        "ja": "立ち籠める霧から",
        "romaji": "tachikomerukirikara",
        "ko": "자욱하게 피어오르는 안개 속에서",
        "charRomaji": [
          "tachi",
          "kome",
          "",
          "ru",
          "kiri",
          "ka",
          "ra"
        ]
      },
      {
        "ja": "先が見えなくなっても",
        "romaji": "sakigamienakunattemo",
        "ko": "앞이 보이지 않게 된다 해도",
        "charRomaji": [
          "saki",
          "ga",
          "mie",
          "",
          "na",
          "ku",
          "na",
          "tte",
          "mo"
        ]
      },
      {
        "ja": "手探りで進む旅路",
        "romaji": "tesaguridesusumutabiji",
        "ko": "더듬거리며 나아가는 여로",
        "charRomaji": [
          "te",
          "saguri",
          "",
          "de",
          "susu",
          "",
          "mu",
          "tabi",
          "ji"
        ]
      },
      {
        "ja": "霧を切り拓いて僕らは行く",
        "romaji": "kiriwokirihiraitiebokurawayuku",
        "ko": "안개를 헤치며 우리는 가네",
        "charRomaji": [
          "kiri",
          "wo",
          "kiri",
          "hira",
          "",
          "i",
          "te",
          "boku",
          "ra",
          "wa",
          "yu",
          "ku"
        ]
      }
    ]
  },
  {
    "id": "shoumeisanka",
    "title": "証命讃歌",
    "reading": "しょうめいさんか",
    "category": "original",
    "album": "2nd Album 《跡導尋》",
    "youtubeId": "QkX594yX8jE",
    "lines": [
      {
        "ja": "くだらない前例は絶って",
        "romaji": "kudaranazenreiwatatte",
        "ko": "하찮은 전례는 끊어버리고",
        "charRomaji": [
          "ku",
          "da",
          "ra",
          "na",
          "i",
          "zen",
          "rei",
          "wa",
          "ta",
          "tte"
        ]
      },
      {
        "ja": "止まんない衝動に沿って",
        "romaji": "tomannaishoudounisotte",
        "ko": "멈추지 않는 충동을 따라서",
        "charRomaji": [
          "toma",
          "",
          "n",
          "na",
          "i",
          "shou",
          "dou",
          "ni",
          "so",
          "tte"
        ]
      },
      {
        "ja": "生きてる証を刻み込め",
        "romaji": "ikiteruakashiwokizamikome",
        "ko": "살아있다는 증거를 아로새겨라",
        "charRomaji": [
          "iki",
          "",
          "te",
          "ru",
          "akashi",
          "wo",
          "kizami",
          "kome",
          ""
        ]
      },
      {
        "ja": "命の讃歌を鳴り響かせろ",
        "romaji": "inochinosankawonarihibikasero",
        "ko": "생명의 찬가를 소리 높여 울려라",
        "charRomaji": [
          "inochi",
          "no",
          "san",
          "ka",
          "wo",
          "nari",
          "hibika",
          "",
          "se",
          "ro"
        ]
      }
    ]
  },
  {
    "id": "nonbreath",
    "title": "ノンブレス・オブリージュ",
    "reading": "のんぶれす おぶりーじゅ",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "QG3fM0qK9qg",
    "lines": [
      {
        "ja": "世界中のすべての人間に好かれるなんて気持ち悪いよ",
        "romaji": "sekaijuunosubetenoningennsukarerunantekimochowaruiyo",
        "ko": "온 세상 모든 사람에게 사랑받는다는 건 징그러운 일이야",
        "charRomaji": [
          "se",
          "kai",
          "juu",
          "no",
          "su",
          "be",
          "te",
          "no",
          "nin",
          "gen",
          "ni",
          "suka",
          "",
          "re",
          "ru",
          "na",
          "n",
          "te",
          "ki",
          "mo",
          "chi",
          "wa",
          "ru",
          "i",
          "yo"
        ]
      },
      {
        "ja": "だけど一つになれない教室で",
        "romaji": "dakedohitotsuninarenaikyoushitsude",
        "ko": "하지만 하나가 될 수 없는 교실에서",
        "charRomaji": [
          "da",
          "ke",
          "do",
          "hito",
          "tsu",
          "ni",
          "na",
          "re",
          "na",
          "i",
          "kyou",
          "shitsu",
          "de"
        ]
      },
      {
        "ja": "息を止めて息を止めて",
        "romaji": "ikiwotometeikiwotomete",
        "ko": "숨을 참고, 숨을 참고",
        "charRomaji": [
          "iki",
          "wo",
          "tome",
          "",
          "te",
          "iki",
          "wo",
          "tome",
          "",
          "te"
        ]
      },
      {
        "ja": "誰も傷つけないように潜って",
        "romaji": "daremokizutsukenaiyounikugutte",
        "ko": "누구도 상처입히지 않도록 숨죽이며",
        "charRomaji": [
          "dare",
          "mo",
          "kizu",
          "tsu",
          "ke",
          "na",
          "i",
          "you",
          "ni",
          "kugu",
          "",
          "tte"
        ]
      },
      {
        "ja": "苦しくても笑ってみせるんだ",
        "romaji": "kurushikutemowarattemiserunda",
        "ko": "괴로워도 웃어 보이는 거야",
        "charRomaji": [
          "kuru",
          "",
          "shi",
          "ku",
          "te",
          "mo",
          "wara",
          "",
          "tte",
          "mi",
          "se",
          "ru",
          "n",
          "da"
        ]
      }
    ]
  },
  {
    "id": "kiminokamisama",
    "title": "君の神様になりたい。",
    "reading": "きみのかみさまになりたい",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "V_S-v8m0k0A",
    "lines": [
      {
        "ja": "僕の命の歌で君が命を大事にすればいいのに",
        "romaji": "bokunoinochinoutadekimigainochiwodaijinisurebaiinoni",
        "ko": "내 생명의 노래로 네가 목숨을 소중히 여겼으면 좋을 텐데",
        "charRomaji": [
          "boku",
          "no",
          "inochi",
          "no",
          "uta",
          "de",
          "kimi",
          "ga",
          "inochi",
          "wo",
          "dai",
          "ji",
          "ni",
          "su",
          "re",
          "ba",
          "i",
          "i",
          "no",
          "ni"
        ]
      },
      {
        "ja": "僕の家族の歌で君が愛を大事にすればいいのに",
        "romaji": "bokunokazokunoutadekimigaaiwodaijinisurebaiinoni",
        "ko": "내 가족의 노래로 네가 사랑을 소중히 여겼으면 좋을 텐데",
        "charRomaji": [
          "boku",
          "no",
          "ka",
          "zoku",
          "no",
          "uta",
          "de",
          "kimi",
          "ga",
          "ai",
          "wo",
          "dai",
          "ji",
          "ni",
          "su",
          "re",
          "ba",
          "i",
          "i",
          "no",
          "ni"
        ]
      },
      {
        "ja": "そんなくだらない幻想を歌っている",
        "romaji": "sonnakudaranagensouwooutatteiru",
        "ko": "그런 시시한 환상을 노래하고 있어",
        "charRomaji": [
          "so",
          "n",
          "na",
          "ku",
          "da",
          "ra",
          "na",
          "i",
          "gen",
          "sou",
          "wo",
          "uta",
          "",
          "tte",
          "i",
          "ru"
        ]
      },
      {
        "ja": "君を救えない歌など",
        "romaji": "kimiwosukuenaiutanado",
        "ko": "너를 구할 수 없는 노래 따위",
        "charRomaji": [
          "kimi",
          "wo",
          "suku",
          "",
          "e",
          "na",
          "i",
          "uta",
          "na",
          "do"
        ]
      },
      {
        "ja": "僕にとっては意味がないんだ",
        "romaji": "bokunitottewaimiganainda",
        "ko": "나에게는 아무런 의미가 없어",
        "charRomaji": [
          "boku",
          "ni",
          "to",
          "tte",
          "wa",
          "i",
          "mi",
          "ga",
          "na",
          "i",
          "n",
          "da"
        ]
      }
    ]
  },
  {
    "id": "charles",
    "title": "シャルル",
    "reading": "しゃるる",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "gB_yD6zU_oQ",
    "lines": [
      {
        "ja": "さよならはあなたから言った",
        "romaji": "sayonarahaanatakarayitta",
        "ko": "작별은 당신이 먼저 말했지",
        "charRomaji": [
          "sa",
          "yo",
          "na",
          "ra",
          "wa",
          "a",
          "na",
          "ta",
          "ka",
          "ra",
          "i",
          "tta"
        ]
      },
      {
        "ja": "それなのに頬を濡らしてしまうの",
        "romaji": "sorenanonihohowonurashiteshimawuno",
        "ko": "그런데도 뺨을 적시고 마는 거야?",
        "charRomaji": [
          "so",
          "re",
          "na",
          "no",
          "ni",
          "hoho",
          "wo",
          "nura",
          "",
          "shi",
          "te",
          "shi",
          "ma",
          "u",
          "no"
        ]
      },
      {
        "ja": "そうやって昨日の事も消してしまうなら",
        "romaji": "souyattekinoubokotomokeshiteshimaunara",
        "ko": "그렇게 어제의 일도 지워버릴 거라면",
        "charRomaji": [
          "sou",
          "ya",
          "tte",
          "kinou",
          "",
          "no",
          "koto",
          "mo",
          "keshi",
          "",
          "te",
          "shi",
          "ma",
          "u",
          "na",
          "ra"
        ]
      },
      {
        "ja": "もういいよ笑って",
        "romaji": "mouiiyowaratte",
        "ko": "이젠 됐어, 웃어줘",
        "charRomaji": [
          "mou",
          "i",
          "i",
          "yo",
          "wara",
          "",
          "tte"
        ]
      },
      {
        "ja": "重なり合う影が離れていく",
        "romaji": "kasanariaukagegahanareteiku",
        "ko": "겹쳐지던 그림자가 멀어져 가",
        "charRomaji": [
          "kasa",
          "",
          "na",
          "ri",
          "a",
          "u",
          "kage",
          "ga",
          "hana",
          "",
          "re",
          "te",
          "i",
          "ku"
        ]
      }
    ]
  },
  {
    "id": "swim",
    "title": "swim",
    "reading": "すいむ",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "mN_F9U6s6r8",
    "lines": [
      {
        "ja": "あの日の自分が許せないな",
        "romaji": "anohinojibungayurusenaina",
        "ko": "그날의 내 자신이 용서가 안 돼",
        "charRomaji": [
          "a",
          "no",
          "hi",
          "no",
          "ji",
          "bun",
          "ga",
          "yuru",
          "",
          "se",
          "na",
          "i",
          "na"
        ]
      },
      {
        "ja": "選び間違えた日々を返せよ",
        "romaji": "erabimachigaetahibiwokaeseyo",
        "ko": "잘못 선택했던 날들을 되돌려줘",
        "charRomaji": [
          "era",
          "",
          "bi",
          "machi",
          "gae",
          "",
          "ta",
          "hi",
          "bi",
          "wo",
          "kae",
          "",
          "se",
          "yo"
        ]
      },
      {
        "ja": "あなたの言葉がしがみついて",
        "romaji": "anatanokotobagashigamitsuite",
        "ko": "너의 말이 들러붙어서",
        "charRomaji": [
          "a",
          "na",
          "ta",
          "no",
          "kotoba",
          "",
          "ga",
          "shi",
          "ga",
          "mi",
          "tsu",
          "i",
          "te"
        ]
      },
      {
        "ja": "離れられない逃れられない",
        "romaji": "hanarerarenainogarerarenai",
        "ko": "떨어질 수 없어, 벗어날 수 없어",
        "charRomaji": [
          "hana",
          "",
          "re",
          "ra",
          "re",
          "na",
          "i",
          "noga",
          "",
          "re",
          "ra",
          "re",
          "na",
          "i"
        ]
      },
      {
        "ja": "泳いでいく暗い海の底へ",
        "romaji": "oyoydeikukuraiuminosokoe",
        "ko": "헤엄쳐 가, 어두운 바다 밑으로",
        "charRomaji": [
          "oyo",
          "",
          "i",
          "de",
          "i",
          "ku",
          "kura",
          "",
          "i",
          "umi",
          "no",
          "soko",
          "e"
        ]
      }
    ]
  },
  {
    "id": "seishuncomplex",
    "title": "青春コンプレックス",
    "reading": "せいしゅんこんぷれっくす",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "KId3M9bF9uI",
    "lines": [
      {
        "ja": "暗く狭いのが好きだった",
        "romaji": "kurakusemainogasukidatta",
        "ko": "어둡고 좁은 곳이 좋았어",
        "charRomaji": [
          "kura",
          "",
          "ku",
          "sema",
          "",
          "i",
          "no",
          "ga",
          "suki",
          "",
          "da",
          "tta"
        ]
      },
      {
        "ja": "深く被るフードの中",
        "romaji": "fukakukaburufuudononaka",
        "ko": "깊게 눌러쓴 후드 속",
        "charRomaji": [
          "fuka",
          "",
          "ku",
          "kabu",
          "",
          "ru",
          "fuu",
          "",
          "do",
          "no",
          "naka"
        ]
      },
      {
        "ja": "無情な世界を恨んだ目は",
        "romaji": "mujounasekaiwourandmewa",
        "ko": "무정한 세상을 원망하던 눈은",
        "charRomaji": [
          "mu",
          "jou",
          "na",
          "se",
          "kai",
          "wo",
          "ura",
          "",
          "n",
          "da",
          "me",
          "wa"
        ]
      },
      {
        "ja": "どうしようもなく愛を欲してた",
        "romaji": "doushiyoumonakuaiwohoshshiteta",
        "ko": "어쩔 도리도 없이 사랑을 갈구했지",
        "charRomaji": [
          "dou",
          "shi",
          "you",
          "mo",
          "na",
          "ku",
          "ai",
          "wo",
          "hoshite",
          "",
          "ta"
        ]
      },
      {
        "ja": "雨に濡れるのが好きだった",
        "romaji": "ameninurerunogasukidatta",
        "ko": "비에 젖는 것이 좋았어",
        "charRomaji": [
          "ame",
          "ni",
          "nure",
          "",
          "ru",
          "no",
          "ga",
          "suki",
          "",
          "da",
          "tta"
        ]
      },
      {
        "ja": "曇った顔が似合うから",
        "romaji": "kumottakagoganikaukara",
        "ko": "흐린 얼굴이 어울리니까",
        "charRomaji": [
          "kumo",
          "",
          "tta",
          "kao",
          "ga",
          "nia",
          "",
          "u",
          "ka",
          "ra"
        ]
      },
      {
        "ja": "嵐に怯えてるフリをして",
        "romaji": "arashiniobieterufuriwoshite",
        "ko": "폭풍을 무서워하는 척을 하며",
        "charRomaji": [
          "arashi",
          "ni",
          "obie",
          "",
          "te",
          "ru",
          "fu",
          "ri",
          "wo",
          "shi",
          "te"
        ]
      },
      {
        "ja": "空が割れるのを待っていたんだ",
        "romaji": "soragawarerunowomatteitanda",
        "ko": "하늘이 갈라지기만을 기다렸어",
        "charRomaji": [
          "sora",
          "ga",
          "ware",
          "",
          "ru",
          "no",
          "wo",
          "ma",
          "tte",
          "i",
          "ta",
          "n",
          "da"
        ]
      },
      {
        "ja": "かき鳴らせ光のファズで",
        "romaji": "kakinarasehikarinoazude",
        "ko": "가볍게 긁어 울려라, 빛의 퍼즈로",
        "charRomaji": [
          "ka",
          "ki",
          "nara",
          "",
          "se",
          "hikari",
          "no",
          "fa",
          "zu",
          "de"
        ]
      },
      {
        "ja": "雷鳴を轟かせたいんだ",
        "romaji": "raimeiwotodorokasetainda",
        "ko": "뇌명을 울려 퍼뜨리고 싶어",
        "charRomaji": [
          "rai",
          "mei",
          "wo",
          "todoro",
          "",
          "ka",
          "se",
          "tai",
          "n",
          "da"
        ]
      }
    ]
  }
];
