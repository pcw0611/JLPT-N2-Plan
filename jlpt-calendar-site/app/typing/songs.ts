// MyGO!!!!! Song Database for Lyrics Typing Practice
// Fully verified discography with singles and albums indicated:
//   1st Album『迷跡波』 (13 tracks)
//   2nd Album『跡暖空』 (12 tracks)
//   3rd Album『致並跡』 (10 tracks)
//   Cover Collections (22 tracks)
// Total 57 songs completely verified with rich Part 1 & Part 2 lyrics!

export interface SongLine {
  ja: string;
  romaji: string;
  ko: string;
  charRomaji?: string[];
}

export interface SongPart {
  id: string;
  name: string;
  lines: SongLine[];
}

export interface Song {
  id: string;
  title: string;
  reading: string;
  category: 'original' | 'cover';
  album: string;
  youtubeId?: string;
  parts: SongPart[];
}

export const SONGS: Song[] = [
  {
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
        "lines": [
          {
            "ja": "交差点の真ん中 急ぐ人に紛れて",
            "romaji": "kousatennomannakaisoguhitonimagirete",
            "ko": "교차로 한가운데 바쁘게 스쳐 가는 사람들 속에",
            "charRomaji": [
              "kou",
              "sat",
              "en",
              "nom",
              "an",
              "nak",
              "ai",
              "",
              "sog",
              "uh",
              "ito",
              "ni",
              "mag",
              "ir",
              "ete"
            ]
          },
          {
            "ja": "僕だけがあてもなく 漂うみたいだ",
            "romaji": "bokudakegaatemonakutadayoumitaida",
            "ko": "나만 혼자 갈 곳 없이 떠도는 것 같아",
            "charRomaji": [
              "bo",
              "ku",
              "da",
              "ke",
              "ga",
              "at",
              "em",
              "on",
              "ak",
              "",
              "ut",
              "ada",
              "yo",
              "umi",
              "ta",
              "ida"
            ]
          },
          {
            "ja": "流行りの歌はいつも 僕のことは歌ってない",
            "romaji": "hayarinoutahaitsumobokunokotohautattenai",
            "ko": "유행하는 노래들은 늘 나와는 상관 없는 이야기 같아",
            "charRomaji": [
              "ha",
              "ya",
              "ri",
              "no",
              "ut",
              "ah",
              "ai",
              "ts",
              "um",
              "",
              "ob",
              "ok",
              "un",
              "ok",
              "ot",
              "oh",
              "au",
              "tat",
              "te",
              "nai"
            ]
          },
          {
            "ja": "ねえビジョンの中から 笑いかけないで",
            "romaji": "neebijonnonakakarawaraikakenaide",
            "ko": "저기, 화면 속에서 웃지 말아줘",
            "charRomaji": [
              "ne",
              "eb",
              "ij",
              "on",
              "no",
              "na",
              "ka",
              "ka",
              "ra",
              "wa",
              "",
              "ra",
              "ik",
              "ak",
              "en",
              "a",
              "id",
              "e"
            ]
          },
          {
            "ja": "また今日も声にならずに 飲み込んだ感情",
            "romaji": "matakyoumokoeninarazuninomikondakanjou",
            "ko": "오늘도 또 입 밖으로 꺼내지 못하고 삼켜버린 감정들",
            "charRomaji": [
              "ma",
              "ta",
              "ky",
              "ou",
              "mo",
              "ko",
              "en",
              "in",
              "ar",
              "az",
              "un",
              "",
              "in",
              "om",
              "ik",
              "on",
              "dak",
              "an",
              "jou"
            ]
          },
          {
            "ja": "下書き埋め尽くして",
            "romaji": "shitagakiumetsukushite",
            "ko": "글로만 적어내려가며",
            "charRomaji": [
              "sh",
              "it",
              "aga",
              "ki",
              "ume",
              "ts",
              "uku",
              "sh",
              "ite"
            ]
          },
          {
            "ja": "ああ そうやって何千回夜を越える",
            "romaji": "aasouyattenanzenkaiyoruwokoeru",
            "ko": "아아, 그렇게 몇 천 번의 밤을 보냈어",
            "charRomaji": [
              "aa",
              "so",
              "",
              "uy",
              "at",
              "te",
              "na",
              "nz",
              "en",
              "ka",
              "iy",
              "or",
              "uw",
              "ok",
              "oe",
              "ru"
            ]
          },
          {
            "ja": "僕のため それだけ それだけだったんだよ",
            "romaji": "bokunotamesoredakesoredakedattandayo",
            "ko": "나를 위해, 그것뿐, 그것뿐이었어",
            "charRomaji": [
              "bo",
              "ku",
              "no",
              "ta",
              "",
              "me",
              "so",
              "re",
              "da",
              "",
              "ke",
              "so",
              "re",
              "da",
              "ke",
              "da",
              "tt",
              "an",
              "da",
              "yo"
            ]
          },
          {
            "ja": "出口探し 溢れただけの言葉",
            "romaji": "deguchisagashikoboretadakenokotoba",
            "ko": "출구를 찾아 헤매다 쏟아져 넘쳐버린 말들",
            "charRomaji": [
              "deg",
              "uch",
              "isa",
              "gas",
              "",
              "hik",
              "obo",
              "ret",
              "ada",
              "ke",
              "nok",
              "ot",
              "oba"
            ]
          },
          {
            "ja": "君の心へ届いて 隙間をちょっと埋めるなら",
            "romaji": "kiminokokorohetodoitesukimawochottoumerunara",
            "ko": "만약 너의 마음에 닿아서 텅 빈 틈을 조금이라도 채울 수 있다면",
            "charRomaji": [
              "ki",
              "mi",
              "no",
              "ko",
              "ko",
              "ro",
              "he",
              "",
              "to",
              "doi",
              "te",
              "suk",
              "im",
              "awo",
              "ch",
              "ott",
              "ou",
              "mer",
              "un",
              "ara"
            ]
          },
          {
            "ja": "こんな僕でも ここにいる 叫ぶよ",
            "romaji": "konnabokudemokokoniirusakebuyo",
            "ko": "이런 나라도 여기에 있다고 외칠게",
            "charRomaji": [
              "ko",
              "nn",
              "ab",
              "ok",
              "ud",
              "em",
              "",
              "ok",
              "ok",
              "on",
              "ii",
              "ru",
              "",
              "sak",
              "eb",
              "uyo"
            ]
          },
          {
            "ja": "迷い星のうた",
            "romaji": "mayoihoshinouta",
            "ko": "길잃은 별의 노래",
            "charRomaji": [
              "ma",
              "yoi",
              "ho",
              "shi",
              "no",
              "uta"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番)",
        "lines": [
          {
            "ja": "問われることは何故か 将来のことばかり",
            "romaji": "towarerukotohanazekashourainokotobakari",
            "ko": "왜인지 사람들은 늘 내 장래에 대해서만 묻곤 해",
            "charRomaji": [
              "to",
              "wa",
              "re",
              "ru",
              "ko",
              "to",
              "ha",
              "na",
              "ze",
              "ka",
              "",
              "sh",
              "ou",
              "ra",
              "ino",
              "ko",
              "tob",
              "ak",
              "ari"
            ]
          },
          {
            "ja": "目の前にいる僕の 今はおざなりで",
            "romaji": "menomaeniirubokunoimawaozanaride",
            "ko": "눈앞에 있는 지금의 나는 뒷전인 채로",
            "charRomaji": [
              "me",
              "no",
              "ma",
              "en",
              "ii",
              "ru",
              "bo",
              "ku",
              "",
              "no",
              "im",
              "aw",
              "ao",
              "zan",
              "ar",
              "ide"
            ]
          },
          {
            "ja": "華やぎに馴染めない この心を無視して",
            "romaji": "hanayagininajimenaikonokokorowomushishite",
            "ko": "화려함에 어울리지 못하는 이 마음을 외면하면서",
            "charRomaji": [
              "ha",
              "na",
              "ya",
              "gi",
              "nin",
              "aj",
              "ime",
              "na",
              "iko",
              "",
              "no",
              "kok",
              "or",
              "owo",
              "mu",
              "shi",
              "sh",
              "ite"
            ]
          },
          {
            "ja": "輝かしい明日を 推奨しないでくれ",
            "romaji": "kagayakashiiashitawosuishoushinaidekure",
            "ko": "찬란한 내일만 강요하지 말아줘",
            "charRomaji": [
              "kag",
              "aya",
              "kas",
              "hi",
              "ias",
              "hi",
              "taw",
              "",
              "os",
              "uis",
              "ho",
              "ush",
              "in",
              "aid",
              "ek",
              "ure"
            ]
          },
          {
            "ja": "夜空にチカチカ光る 頼りない星屑",
            "romaji": "yozoranichikachikahikarutayorinaihoshikuzu",
            "ko": "밤하늘에 반짝반짝 빛나는 의지할 수 없는 작은 별들",
            "charRomaji": [
              "yoz",
              "ora",
              "nic",
              "hik",
              "ach",
              "ika",
              "hik",
              "aru",
              "tay",
              "",
              "or",
              "ina",
              "ih",
              "osh",
              "ik",
              "uzu"
            ]
          },
          {
            "ja": "躊躇いながらはぐれて",
            "romaji": "tamerainagarahagurete",
            "ko": "망설이다가 길을 잃고",
            "charRomaji": [
              "ta",
              "me",
              "ra",
              "in",
              "ag",
              "ar",
              "ah",
              "ag",
              "ur",
              "ete"
            ]
          },
          {
            "ja": "ああ 彷徨っているそれが僕",
            "romaji": "aasamayotteirusoregaboku",
            "ko": "아아, 그렇게 헤매는 게 바로 나야",
            "charRomaji": [
              "aa",
              "sa",
              "",
              "ma",
              "yo",
              "tt",
              "ei",
              "ru",
              "so",
              "re",
              "ga",
              "bo",
              "ku"
            ]
          },
          {
            "ja": "僕になる それしか それしかできないだろう",
            "romaji": "bokuninarusoreshikasoreshikadekinaidarou",
            "ko": "나 자신이 될 거야, 그것밖에, 그것밖에 할 수 없잖아",
            "charRomaji": [
              "bo",
              "ku",
              "ni",
              "na",
              "",
              "ru",
              "so",
              "re",
              "sh",
              "",
              "ik",
              "as",
              "or",
              "es",
              "hi",
              "ka",
              "de",
              "ki",
              "nai",
              "da",
              "rou"
            ]
          },
          {
            "ja": "誰の真似も 上手くやれないんだ",
            "romaji": "darenomanemoumakuyarenainda",
            "ko": "누구처럼 되는 것도 제대로 할 수 없어",
            "charRomaji": [
              "da",
              "re",
              "no",
              "ma",
              "ne",
              "",
              "mo",
              "um",
              "ak",
              "uy",
              "ar",
              "en",
              "ai",
              "nd",
              "a"
            ]
          },
          {
            "ja": "こんな痛い日々をなんで 退屈だって片付ける？",
            "romaji": "konnaitaihibiwonandetaikutsudattekatazukeru",
            "ko": "이 고통스러운 날들을 어떻게 지루하다고 넘길 수 있겠어?",
            "charRomaji": [
              "ko",
              "nn",
              "ai",
              "ta",
              "ih",
              "ib",
              "iw",
              "on",
              "an",
              "de",
              "ta",
              "",
              "ik",
              "ut",
              "su",
              "da",
              "tte",
              "ka",
              "taz",
              "uk",
              "eru",
              ""
            ]
          },
          {
            "ja": "よろめきながらでも もがいているんだよ",
            "romaji": "yoromekinagarademomogaiteirundayo",
            "ko": "비틀거리면서도 발버둥치고 있는 거야",
            "charRomaji": [
              "yo",
              "ro",
              "me",
              "ki",
              "na",
              "ga",
              "ra",
              "de",
              "mo",
              "",
              "mo",
              "ga",
              "it",
              "ei",
              "r",
              "un",
              "d",
              "ay",
              "o"
            ]
          },
          {
            "ja": "迷い星のうた",
            "romaji": "mayoihoshinouta",
            "ko": "길잃은 별의 노래",
            "charRomaji": [
              "ma",
              "yoi",
              "ho",
              "shi",
              "no",
              "uta"
            ]
          }
        ]
      },
      {
        "id": "part3",
        "name": "Part 3 (ラスト・Cメロ~完走)",
        "lines": [
          {
            "ja": "僕のため それだけ それだけだったんだよ",
            "romaji": "bokunotamesoredakesoredakedattandayo",
            "ko": "나를 위해, 그것뿐, 그것뿐이었어",
            "charRomaji": [
              "bo",
              "ku",
              "no",
              "ta",
              "",
              "me",
              "so",
              "re",
              "da",
              "",
              "ke",
              "so",
              "re",
              "da",
              "ke",
              "da",
              "tt",
              "an",
              "da",
              "yo"
            ]
          },
          {
            "ja": "涙流し やっと生まれた言葉",
            "romaji": "namidanagashiyattoumaretakotoba",
            "ko": "눈물을 흘려 간신히 태어난 말들",
            "charRomaji": [
              "nam",
              "ida",
              "na",
              "",
              "gas",
              "hi",
              "yat",
              "to",
              "uma",
              "re",
              "tak",
              "ot",
              "oba"
            ]
          },
          {
            "ja": "どこかで同じように ヒリヒリする胸抱えて",
            "romaji": "dokokadeonajiyounihirihirisurumunekakaete",
            "ko": "어디선가 나처럼 아픈 마음을 안고",
            "charRomaji": [
              "do",
              "ko",
              "ka",
              "de",
              "on",
              "aj",
              "iy",
              "ou",
              "ni",
              "",
              "hi",
              "ri",
              "hi",
              "ri",
              "su",
              "rum",
              "un",
              "eka",
              "ka",
              "ete"
            ]
          },
          {
            "ja": "震える君に 僕もいる 叫ぶよ",
            "romaji": "furuerukiminibokumoirusakebuyo",
            "ko": "떨고 있을 너에게 나도 여기 있다고 외칠게",
            "charRomaji": [
              "fu",
              "rue",
              "ru",
              "kim",
              "in",
              "",
              "ibo",
              "ku",
              "moi",
              "ru",
              "",
              "sak",
              "eb",
              "uyo"
            ]
          },
          {
            "ja": "迷い星のうた",
            "romaji": "mayoihoshinouta",
            "ko": "길잃은 별의 노래",
            "charRomaji": [
              "ma",
              "yoi",
              "ho",
              "shi",
              "no",
              "uta"
            ]
          }
        ]
      },
      {
        "id": "full",
        "name": "Part 4 (★全曲フル完走★)",
        "lines": [
          {
            "ja": "交差点の真ん中 急ぐ人に紛れて",
            "romaji": "kousatennomannakaisoguhitonimagirete",
            "ko": "교차로 한가운데 바쁘게 스쳐 가는 사람들 속에",
            "charRomaji": [
              "kou",
              "sat",
              "en",
              "nom",
              "an",
              "nak",
              "ai",
              "",
              "sog",
              "uh",
              "ito",
              "ni",
              "mag",
              "ir",
              "ete"
            ]
          },
          {
            "ja": "僕だけがあてもなく 漂うみたいだ",
            "romaji": "bokudakegaatemonakutadayoumitaida",
            "ko": "나만 혼자 갈 곳 없이 떠도는 것 같아",
            "charRomaji": [
              "bo",
              "ku",
              "da",
              "ke",
              "ga",
              "at",
              "em",
              "on",
              "ak",
              "",
              "ut",
              "ada",
              "yo",
              "umi",
              "ta",
              "ida"
            ]
          },
          {
            "ja": "流行りの歌はいつも 僕のことは歌ってない",
            "romaji": "hayarinoutahaitsumobokunokotohautattenai",
            "ko": "유행하는 노래들은 늘 나와는 상관 없는 이야기 같아",
            "charRomaji": [
              "ha",
              "ya",
              "ri",
              "no",
              "ut",
              "ah",
              "ai",
              "ts",
              "um",
              "",
              "ob",
              "ok",
              "un",
              "ok",
              "ot",
              "oh",
              "au",
              "tat",
              "te",
              "nai"
            ]
          },
          {
            "ja": "ねえビジョンの中から 笑いかけないで",
            "romaji": "neebijonnonakakarawaraikakenaide",
            "ko": "저기, 화면 속에서 웃지 말아줘",
            "charRomaji": [
              "ne",
              "eb",
              "ij",
              "on",
              "no",
              "na",
              "ka",
              "ka",
              "ra",
              "wa",
              "",
              "ra",
              "ik",
              "ak",
              "en",
              "a",
              "id",
              "e"
            ]
          },
          {
            "ja": "また今日も声にならずに 飲み込んだ感情",
            "romaji": "matakyoumokoeninarazuninomikondakanjou",
            "ko": "오늘도 또 입 밖으로 꺼내지 못하고 삼켜버린 감정들",
            "charRomaji": [
              "ma",
              "ta",
              "ky",
              "ou",
              "mo",
              "ko",
              "en",
              "in",
              "ar",
              "az",
              "un",
              "",
              "in",
              "om",
              "ik",
              "on",
              "dak",
              "an",
              "jou"
            ]
          },
          {
            "ja": "下書き埋め尽くして",
            "romaji": "shitagakiumetsukushite",
            "ko": "글로만 적어내려가며",
            "charRomaji": [
              "sh",
              "it",
              "aga",
              "ki",
              "ume",
              "ts",
              "uku",
              "sh",
              "ite"
            ]
          },
          {
            "ja": "ああ そうやって何千回夜を越える",
            "romaji": "aasouyattenanzenkaiyoruwokoeru",
            "ko": "아아, 그렇게 몇 천 번의 밤을 보냈어",
            "charRomaji": [
              "aa",
              "so",
              "",
              "uy",
              "at",
              "te",
              "na",
              "nz",
              "en",
              "ka",
              "iy",
              "or",
              "uw",
              "ok",
              "oe",
              "ru"
            ]
          },
          {
            "ja": "僕のため それだけ それだけだったんだよ",
            "romaji": "bokunotamesoredakesoredakedattandayo",
            "ko": "나를 위해, 그것뿐, 그것뿐이었어",
            "charRomaji": [
              "bo",
              "ku",
              "no",
              "ta",
              "",
              "me",
              "so",
              "re",
              "da",
              "",
              "ke",
              "so",
              "re",
              "da",
              "ke",
              "da",
              "tt",
              "an",
              "da",
              "yo"
            ]
          },
          {
            "ja": "出口探し 溢れただけの言葉",
            "romaji": "deguchisagashikoboretadakenokotoba",
            "ko": "출구를 찾아 헤매다 쏟아져 넘쳐버린 말들",
            "charRomaji": [
              "deg",
              "uch",
              "isa",
              "gas",
              "",
              "hik",
              "obo",
              "ret",
              "ada",
              "ke",
              "nok",
              "ot",
              "oba"
            ]
          },
          {
            "ja": "君の心へ届いて 隙間をちょっと埋めるなら",
            "romaji": "kiminokokorohetodoitesukimawochottoumerunara",
            "ko": "만약 너의 마음에 닿아서 텅 빈 틈을 조금이라도 채울 수 있다면",
            "charRomaji": [
              "ki",
              "mi",
              "no",
              "ko",
              "ko",
              "ro",
              "he",
              "",
              "to",
              "doi",
              "te",
              "suk",
              "im",
              "awo",
              "ch",
              "ott",
              "ou",
              "mer",
              "un",
              "ara"
            ]
          },
          {
            "ja": "こんな僕でも ここにいる 叫ぶよ",
            "romaji": "konnabokudemokokoniirusakebuyo",
            "ko": "이런 나라도 여기에 있다고 외칠게",
            "charRomaji": [
              "ko",
              "nn",
              "ab",
              "ok",
              "ud",
              "em",
              "",
              "ok",
              "ok",
              "on",
              "ii",
              "ru",
              "",
              "sak",
              "eb",
              "uyo"
            ]
          },
          {
            "ja": "迷い星のうた",
            "romaji": "mayoihoshinouta",
            "ko": "길잃은 별의 노래",
            "charRomaji": [
              "ma",
              "yoi",
              "ho",
              "shi",
              "no",
              "uta"
            ]
          },
          {
            "ja": "問われることは何故か 将来のことばかり",
            "romaji": "towarerukotohanazekashourainokotobakari",
            "ko": "왜인지 사람들은 늘 내 장래에 대해서만 묻곤 해",
            "charRomaji": [
              "to",
              "wa",
              "re",
              "ru",
              "ko",
              "to",
              "ha",
              "na",
              "ze",
              "ka",
              "",
              "sh",
              "ou",
              "ra",
              "ino",
              "ko",
              "tob",
              "ak",
              "ari"
            ]
          },
          {
            "ja": "目の前にいる僕の 今はおざなりで",
            "romaji": "menomaeniirubokunoimawaozanaride",
            "ko": "눈앞에 있는 지금의 나는 뒷전인 채로",
            "charRomaji": [
              "me",
              "no",
              "ma",
              "en",
              "ii",
              "ru",
              "bo",
              "ku",
              "",
              "no",
              "im",
              "aw",
              "ao",
              "zan",
              "ar",
              "ide"
            ]
          },
          {
            "ja": "華やぎに馴染めない この心を無視して",
            "romaji": "hanayagininajimenaikonokokorowomushishite",
            "ko": "화려함에 어울리지 못하는 이 마음을 외면하면서",
            "charRomaji": [
              "ha",
              "na",
              "ya",
              "gi",
              "nin",
              "aj",
              "ime",
              "na",
              "iko",
              "",
              "no",
              "kok",
              "or",
              "owo",
              "mu",
              "shi",
              "sh",
              "ite"
            ]
          },
          {
            "ja": "輝かしい明日を 推奨しないでくれ",
            "romaji": "kagayakashiiashitawosuishoushinaidekure",
            "ko": "찬란한 내일만 강요하지 말아줘",
            "charRomaji": [
              "kag",
              "aya",
              "kas",
              "hi",
              "ias",
              "hi",
              "taw",
              "",
              "os",
              "uis",
              "ho",
              "ush",
              "in",
              "aid",
              "ek",
              "ure"
            ]
          },
          {
            "ja": "夜空にチカチカ光る 頼りない星屑",
            "romaji": "yozoranichikachikahikarutayorinaihoshikuzu",
            "ko": "밤하늘에 반짝반짝 빛나는 의지할 수 없는 작은 별들",
            "charRomaji": [
              "yoz",
              "ora",
              "nic",
              "hik",
              "ach",
              "ika",
              "hik",
              "aru",
              "tay",
              "",
              "or",
              "ina",
              "ih",
              "osh",
              "ik",
              "uzu"
            ]
          },
          {
            "ja": "躊躇いながらはぐれて",
            "romaji": "tamerainagarahagurete",
            "ko": "망설이다가 길을 잃고",
            "charRomaji": [
              "ta",
              "me",
              "ra",
              "in",
              "ag",
              "ar",
              "ah",
              "ag",
              "ur",
              "ete"
            ]
          },
          {
            "ja": "ああ 彷徨っているそれが僕",
            "romaji": "aasamayotteirusoregaboku",
            "ko": "아아, 그렇게 헤매는 게 바로 나야",
            "charRomaji": [
              "aa",
              "sa",
              "",
              "ma",
              "yo",
              "tt",
              "ei",
              "ru",
              "so",
              "re",
              "ga",
              "bo",
              "ku"
            ]
          },
          {
            "ja": "僕になる それしか それしかできないだろう",
            "romaji": "bokuninarusoreshikasoreshikadekinaidarou",
            "ko": "나 자신이 될 거야, 그것밖에, 그것밖에 할 수 없잖아",
            "charRomaji": [
              "bo",
              "ku",
              "ni",
              "na",
              "",
              "ru",
              "so",
              "re",
              "sh",
              "",
              "ik",
              "as",
              "or",
              "es",
              "hi",
              "ka",
              "de",
              "ki",
              "nai",
              "da",
              "rou"
            ]
          },
          {
            "ja": "誰の真似も 上手くやれないんだ",
            "romaji": "darenomanemoumakuyarenainda",
            "ko": "누구처럼 되는 것도 제대로 할 수 없어",
            "charRomaji": [
              "da",
              "re",
              "no",
              "ma",
              "ne",
              "",
              "mo",
              "um",
              "ak",
              "uy",
              "ar",
              "en",
              "ai",
              "nd",
              "a"
            ]
          },
          {
            "ja": "こんな痛い日々をなんで 退屈だって片付ける？",
            "romaji": "konnaitaihibiwonandetaikutsudattekatazukeru",
            "ko": "이 고통스러운 날들을 어떻게 지루하다고 넘길 수 있겠어?",
            "charRomaji": [
              "ko",
              "nn",
              "ai",
              "ta",
              "ih",
              "ib",
              "iw",
              "on",
              "an",
              "de",
              "ta",
              "",
              "ik",
              "ut",
              "su",
              "da",
              "tte",
              "ka",
              "taz",
              "uk",
              "eru",
              ""
            ]
          },
          {
            "ja": "よろめきながらでも もがいているんだよ",
            "romaji": "yoromekinagarademomogaiteirundayo",
            "ko": "비틀거리면서도 발버둥치고 있는 거야",
            "charRomaji": [
              "yo",
              "ro",
              "me",
              "ki",
              "na",
              "ga",
              "ra",
              "de",
              "mo",
              "",
              "mo",
              "ga",
              "it",
              "ei",
              "r",
              "un",
              "d",
              "ay",
              "o"
            ]
          },
          {
            "ja": "迷い星のうた",
            "romaji": "mayoihoshinouta",
            "ko": "길잃은 별의 노래",
            "charRomaji": [
              "ma",
              "yoi",
              "ho",
              "shi",
              "no",
              "uta"
            ]
          },
          {
            "ja": "僕のため それだけ それだけだったんだよ",
            "romaji": "bokunotamesoredakesoredakedattandayo",
            "ko": "나를 위해, 그것뿐, 그것뿐이었어",
            "charRomaji": [
              "bo",
              "ku",
              "no",
              "ta",
              "",
              "me",
              "so",
              "re",
              "da",
              "",
              "ke",
              "so",
              "re",
              "da",
              "ke",
              "da",
              "tt",
              "an",
              "da",
              "yo"
            ]
          },
          {
            "ja": "涙流し やっと生まれた言葉",
            "romaji": "namidanagashiyattoumaretakotoba",
            "ko": "눈물을 흘려 간신히 태어난 말들",
            "charRomaji": [
              "nam",
              "ida",
              "na",
              "",
              "gas",
              "hi",
              "yat",
              "to",
              "uma",
              "re",
              "tak",
              "ot",
              "oba"
            ]
          },
          {
            "ja": "どこかで同じように ヒリヒリする胸抱えて",
            "romaji": "dokokadeonajiyounihirihirisurumunekakaete",
            "ko": "어디선가 나처럼 아픈 마음을 안고",
            "charRomaji": [
              "do",
              "ko",
              "ka",
              "de",
              "on",
              "aj",
              "iy",
              "ou",
              "ni",
              "",
              "hi",
              "ri",
              "hi",
              "ri",
              "su",
              "rum",
              "un",
              "eka",
              "ka",
              "ete"
            ]
          },
          {
            "ja": "震える君に 僕もいる 叫ぶよ",
            "romaji": "furuerukiminibokumoirusakebuyo",
            "ko": "떨고 있을 너에게 나도 여기 있다고 외칠게",
            "charRomaji": [
              "fu",
              "rue",
              "ru",
              "kim",
              "in",
              "",
              "ibo",
              "ku",
              "moi",
              "ru",
              "",
              "sak",
              "eb",
              "uyo"
            ]
          },
          {
            "ja": "迷い星のうた",
            "romaji": "mayoihoshinouta",
            "ko": "길잃은 별의 노래",
            "charRomaji": [
              "ma",
              "yoi",
              "ho",
              "shi",
              "no",
              "uta"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "nanashigoe",
    "title": "名無声",
    "reading": "なもなき",
    "category": "original",
    "album": "1st Single『迷星叫』c/w, 1st Album『迷跡波』",
    "youtubeId": "2mM64qcBYg8",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "何が僕にできるかわからないけれど",
            "romaji": "nanigabokunidekirukawakaranaikeredo",
            "ko": "내가 무엇을 할 수 있는지 알지 못하지만",
            "charRomaji": [
              "nani",
              "ga",
              "boku",
              "ni",
              "de",
              "ki",
              "ru",
              "ka",
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
            "ja": "違うよどこかに向かう途中じゃない",
            "romaji": "chigauyodokokanimukautochuujanai",
            "ko": "아니야 어딘가로 향하는 도중이 아니야",
            "charRomaji": [
              "chiga",
              "u",
              "yo",
              "do",
              "ko",
              "ka",
              "ni",
              "mu",
              "ka",
              "u",
              "to",
              "chuu",
              "j",
              "a",
              "na",
              "i"
            ]
          },
          {
            "ja": "今日の僕は前日譚じゃない",
            "romaji": "kyounobokuhazenjittanjanai",
            "ko": "오늘의 나는 전일담 따위가 아니야",
            "charRomaji": [
              "k",
              "you",
              "no",
              "boku",
              "ha",
              "ze",
              "njit",
              "tan",
              "j",
              "a",
              "na",
              "i"
            ]
          },
          {
            "ja": "足りない何かを求めてくより",
            "romaji": "tarinainanikawomotometekuyori",
            "ko": "부족한 무언가를 찾아 헤매기보다",
            "charRomaji": [
              "ta",
              "ri",
              "na",
              "i",
              "nani",
              "ka",
              "wo",
              "moto",
              "me",
              "te",
              "ku",
              "yo",
              "ri"
            ]
          },
          {
            "ja": "僕のままで生きてみたい",
            "romaji": "bokunomamadeikitemitai",
            "ko": "나의 모습 그대로 살아보고 싶어",
            "charRomaji": [
              "boku",
              "no",
              "ma",
              "ma",
              "de",
              "i",
              "ki",
              "te",
              "mi",
              "ta",
              "i"
            ]
          },
          {
            "ja": "遠くにある理想よりもたった今に敏感に",
            "romaji": "tookuniarurisouyorimotattaimanibinkanni",
            "ko": "멀리 있는 이상보다 바로 지금에 민감하게",
            "charRomaji": [
              "too",
              "ku",
              "ni",
              "a",
              "ru",
              "ri",
              "sou",
              "yo",
              "ri",
              "mo",
              "ta",
              "t",
              "ta",
              "ima",
              "ni",
              "bin",
              "kan",
              "ni"
            ]
          },
          {
            "ja": "ほんの数秒でアーカイブされて",
            "romaji": "honnosuubyoudeaakaibusarete",
            "ko": "불과 몇 초 만에 아카이브되어",
            "charRomaji": [
              "ho",
              "n",
              "no",
              "suu",
              "byou",
              "dea",
              "a",
              "",
              "ka",
              "i",
              "bu",
              "sa",
              "re",
              "te"
            ]
          },
          {
            "ja": "過去になってくその前に",
            "romaji": "kakoninattekusonomaeni",
            "ko": "과거가 되어버리기 그 전에",
            "charRomaji": [
              "ka",
              "ko",
              "ni",
              "na",
              "t",
              "te",
              "ku",
              "so",
              "no",
              "mae",
              "ni"
            ]
          },
          {
            "ja": "僕が見つけた今日の煌めく空",
            "romaji": "bokugamitsuketakyounokiramekusora",
            "ko": "내가 찾아낸 오늘의 눈부신 하늘을",
            "charRomaji": [
              "boku",
              "ga",
              "mi",
              "tsu",
              "ke",
              "ta",
              "k",
              "you",
              "no",
              "kira",
              "me",
              "ku",
              "sora"
            ]
          },
          {
            "ja": "誰かにちょっと伝えたい",
            "romaji": "darekanichottotsutaetai",
            "ko": "누군가에게 조금은 전하고 싶어",
            "charRomaji": [
              "dare",
              "ka",
              "ni",
              "ch",
              "o",
              "t",
              "to",
              "tsuta",
              "e",
              "ta",
              "i"
            ]
          },
          {
            "ja": "綺麗すぎる色は疲れるから",
            "romaji": "kireisugiruirowatsukarerukara",
            "ko": "너무나 화려한 색은 지치니까",
            "charRomaji": [
              "ki",
              "rei",
              "su",
              "gi",
              "ru",
              "iro",
              "wa",
              "tsuka",
              "re",
              "ru",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "そのままを映していたい何者でもない僕で",
            "romaji": "sonomamawoutsushiteitainanimonodemonaibokude",
            "ko": "있는 그대로를 비추고 싶어, 그 누구도 아닌 나로서",
            "charRomaji": [
              "so",
              "no",
              "ma",
              "ma",
              "wo",
              "utsu",
              "shi",
              "te",
              "i",
              "ta",
              "i",
              "nani",
              "mono",
              "de",
              "mo",
              "na",
              "i",
              "boku",
              "de"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "ちょうどよく笑ってそれわかるだとか",
            "romaji": "choudoyokuwarattesorewakarudatoka",
            "ko": "적당히 웃으며 '그거 뭔지 알지' 따위를",
            "charRomaji": [
              "ch",
              "o",
              "u",
              "do",
              "yo",
              "ku",
              "wara",
              "t",
              "te",
              "so",
              "re",
              "wa",
              "ka",
              "ru",
              "da",
              "to",
              "ka"
            ]
          },
          {
            "ja": "なぜ上手く言えないんだろう",
            "romaji": "nazeumakuienaindarou",
            "ko": "어째서 자연스럽게 말하지 못하는 걸까",
            "charRomaji": [
              "na",
              "ze",
              "u",
              "ma",
              "ku",
              "i",
              "e",
              "na",
              "i",
              "n",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "本当の気持ちを加工しなくちゃ",
            "romaji": "hontounokimochiwokakoushinakucha",
            "ko": "진심을 가공하지 않으면",
            "charRomaji": [
              "hon",
              "tou",
              "no",
              "ki",
              "mo",
              "chi",
              "wo",
              "ka",
              "kou",
              "shi",
              "na",
              "ku",
              "ch",
              "a"
            ]
          },
          {
            "ja": "みんなにはなれないみたい",
            "romaji": "minnanihanarenaimitai",
            "ko": "'모두'가 될 수는 없는 모양이야",
            "charRomaji": [
              "mi",
              "n",
              "na",
              "ni",
              "ha",
              "na",
              "re",
              "na",
              "i",
              "mi",
              "ta",
              "i"
            ]
          },
          {
            "ja": "たった一つのアカウントじゃ表せないように",
            "romaji": "tattahitotsunoakauntojaarawasenaiyouni",
            "ko": "단 하나의 계정으로는 다 담아낼 수 없듯이",
            "charRomaji": [
              "ta",
              "t",
              "ta",
              "hito",
              "tsu",
              "no",
              "a",
              "ka",
              "u",
              "n",
              "to",
              "j",
              "a",
              "arawa",
              "se",
              "na",
              "i",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "幾つもの僕をもっているけど",
            "romaji": "ikutsumonobokuwomotteirukedo",
            "ko": "수많은 나를 품고 있지만",
            "charRomaji": [
              "iku",
              "tsu",
              "mo",
              "no",
              "boku",
              "wo",
              "mo",
              "t",
              "te",
              "i",
              "ru",
              "ke",
              "do"
            ]
          },
          {
            "ja": "どこにもいないそんな気持ち",
            "romaji": "dokonimoinaisonnakimochi",
            "ko": "어디에도 존재하지 않는 그런 기분",
            "charRomaji": [
              "do",
              "ko",
              "ni",
              "mo",
              "i",
              "na",
              "i",
              "so",
              "n",
              "na",
              "ki",
              "mo",
              "chi"
            ]
          },
          {
            "ja": "僕が口ずさんだ歌は誰も知らないけど",
            "romaji": "bokugakuchizusandautawadaremoshiranaikedo",
            "ko": "내가 흥얼거린 노래는 아무도 모르지만",
            "charRomaji": [
              "boku",
              "ga",
              "kuchi",
              "zu",
              "sa",
              "n",
              "da",
              "uta",
              "wa",
              "dare",
              "mo",
              "shi",
              "ra",
              "na",
              "i",
              "ke",
              "do"
            ]
          },
          {
            "ja": "ゼロじゃない一つを主張するため",
            "romaji": "zerojanaihitotsuwoshuchousurutame",
            "ko": "0이 아닌 1을 증명하기 위해",
            "charRomaji": [
              "ze",
              "ro",
              "j",
              "a",
              "na",
              "i",
              "hito",
              "tsu",
              "wo",
              "shu",
              "chou",
              "su",
              "ru",
              "ta",
              "me"
            ]
          },
          {
            "ja": "僕はここに立っていたい何者でもないままで",
            "romaji": "bokuhakokonitatteitainanimonodemonaimamade",
            "ko": "나는 여기에 서 있고 싶어, 그 누구도 아닌 채로",
            "charRomaji": [
              "boku",
              "ha",
              "ko",
              "ko",
              "ni",
              "ta",
              "t",
              "te",
              "i",
              "ta",
              "i",
              "nani",
              "mono",
              "de",
              "mo",
              "na",
              "i",
              "ma",
              "ma",
              "de"
            ]
          },
          {
            "ja": "心がぎゅっと動いたそれを声にしたい",
            "romaji": "kokorogagyuttougoitasorewokoenishitai",
            "ko": "마음이 쿵 하고 움직인 그것을 소리로 내고 싶어",
            "charRomaji": [
              "kokoro",
              "ga",
              "gy",
              "u",
              "t",
              "to",
              "ugo",
              "i",
              "ta",
              "so",
              "re",
              "wo",
              "koe",
              "ni",
              "shi",
              "ta",
              "i"
            ]
          },
          {
            "ja": "そのままを抱きしめていたい何者でもない僕で",
            "romaji": "sonomamawodakishimeteitainanimonodemonaibokude",
            "ko": "있는 그대로를 끌어안고 싶어, 그 누구도 아닌 나로서",
            "charRomaji": [
              "so",
              "no",
              "ma",
              "ma",
              "wo",
              "da",
              "ki",
              "shi",
              "me",
              "te",
              "i",
              "ta",
              "i",
              "nani",
              "mono",
              "de",
              "mo",
              "na",
              "i",
              "boku",
              "de"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "otoichie",
    "title": "音一会",
    "reading": "おといちえ",
    "category": "original",
    "album": "2nd Single『音一会』, 1st Album『迷跡波』",
    "youtubeId": "FlDoO0F4p44",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "僕の居場所はB5ペンからこぼれる言葉を落として",
            "romaji": "bokunoibashowabiigopenkarakoborerukotobawootoshite",
            "ko": "내가 머물 곳은 B5 노트, 펜에서 흘러넘친 말들을 떨어뜨리며",
            "charRomaji": [
              "boku",
              "no",
              "i",
              "ba",
              "sho",
              "wa",
              "b",
              "iigo",
              "pe",
              "n",
              "ka",
              "ra",
              "ko",
              "bo",
              "re",
              "ru",
              "ko",
              "toba",
              "wo",
              "o",
              "to",
              "shi",
              "te"
            ]
          },
          {
            "ja": "誰にも届くはずなんかなかった",
            "romaji": "darenimotodokuhazunankanakatta",
            "ko": "누구에게도 닿을 리가 없었어",
            "charRomaji": [
              "dare",
              "ni",
              "mo",
              "todo",
              "ku",
              "ha",
              "zu",
              "na",
              "n",
              "ka",
              "na",
              "ka",
              "t",
              "ta"
            ]
          },
          {
            "ja": "視線を落とした小さな世界で僕だけの感情だった",
            "romaji": "shisenwootoshitachiisanasekaidebokudakenokanjoudatta",
            "ko": "시선을 떨군 작은 세계에서 오직 나만의 감정이었어",
            "charRomaji": [
              "shi",
              "sen",
              "wo",
              "o",
              "to",
              "shi",
              "ta",
              "chii",
              "sa",
              "na",
              "se",
              "kai",
              "de",
              "boku",
              "da",
              "ke",
              "no",
              "kan",
              "jou",
              "da",
              "t",
              "ta"
            ]
          },
          {
            "ja": "誰も傷つけないように自分の声も消して",
            "romaji": "daremokizutsukenaiyounijibunnokoemokeshite",
            "ko": "아무도 상처 주지 않도록 자신의 목소리마저 지우고",
            "charRomaji": [
              "dare",
              "mo",
              "kizu",
              "tsu",
              "ke",
              "na",
              "i",
              "yo",
              "u",
              "ni",
              "ji",
              "bun",
              "no",
              "koe",
              "mo",
              "ke",
              "shi",
              "te"
            ]
          },
          {
            "ja": "息を殺して過ごしていた毎日に",
            "romaji": "ikiwokoroshitesugoshiteitamainichini",
            "ko": "숨을 죽이며 버텨내던 하루하루에",
            "charRomaji": [
              "iki",
              "wo",
              "koro",
              "shi",
              "te",
              "su",
              "go",
              "shi",
              "te",
              "i",
              "ta",
              "mai",
              "nichi",
              "ni"
            ]
          },
          {
            "ja": "君が鳴らした音が風穴を開けたんだ",
            "romaji": "kimiganarashitaotogakazaanawohiraketanda",
            "ko": "네가 울린 소리가 거센 바람구멍을 뚫어주었어",
            "charRomaji": [
              "kimi",
              "ga",
              "na",
              "ra",
              "shi",
              "ta",
              "oto",
              "ga",
              "kaza",
              "ana",
              "wo",
              "hira",
              "ke",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "届くはずのない叫びが君の手を引き寄せて",
            "romaji": "todokuhazunonaisakebigakiminotewohikiyosete",
            "ko": "닿을 리 없던 외침이 너의 손을 끌어당겨서",
            "charRomaji": [
              "todo",
              "ku",
              "ha",
              "zu",
              "no",
              "na",
              "i",
              "sake",
              "bi",
              "ga",
              "kimi",
              "no",
              "te",
              "wo",
              "hi",
              "ki",
              "yo",
              "se",
              "te"
            ]
          },
          {
            "ja": "不器用なままの僕らが出会えた奇跡",
            "romaji": "bukiyounamamanobokuragadeaetakiseki",
            "ko": "서투른 그대로의 우리들이 마주칠 수 있었던 기적",
            "charRomaji": [
              "bu",
              "ki",
              "you",
              "na",
              "ma",
              "ma",
              "no",
              "boku",
              "ra",
              "ga",
              "de",
              "a",
              "e",
              "ta",
              "ki",
              "seki"
            ]
          },
          {
            "ja": "ありがとう出会ってくれて",
            "romaji": "arigatoudeattekurete",
            "ko": "고마워, 나를 만나주어서",
            "charRomaji": [
              "a",
              "ri",
              "ga",
              "to",
              "u",
              "de",
              "a",
              "t",
              "te",
              "ku",
              "re",
              "te"
            ]
          },
          {
            "ja": "この音でひとつになれるなら",
            "romaji": "konootodehitotsuninarerunara",
            "ko": "이 소리로 하나가 될 수 있다면",
            "charRomaji": [
              "ko",
              "no",
              "oto",
              "de",
              "hi",
              "to",
              "tsu",
              "ni",
              "na",
              "re",
              "ru",
              "na",
              "ra"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "ノートの余白に書きなぐった迷い",
            "romaji": "nootonoyohakunikakinaguttamayoi",
            "ko": "노트 여백에 휘갈겨 쓴 방황",
            "charRomaji": [
              "noo",
              "",
              "to",
              "no",
              "yo",
              "haku",
              "ni",
              "ka",
              "ki",
              "na",
              "gu",
              "t",
              "ta",
              "mayo",
              "i"
            ]
          },
          {
            "ja": "誰にも見せられない恥ずかしい自分も",
            "romaji": "darenimomiserarenaihazukashiijibunmo",
            "ko": "누구에게도 보여줄 수 없는 부끄러운 내 모습도",
            "charRomaji": [
              "dare",
              "ni",
              "mo",
              "mi",
              "se",
              "ra",
              "re",
              "na",
              "i",
              "ha",
              "zu",
              "ka",
              "shi",
              "i",
              "ji",
              "bun",
              "mo"
            ]
          },
          {
            "ja": "君が肯定してくれたから",
            "romaji": "kimigakouteishitekuretakara",
            "ko": "네가 긍정해 주었으니까",
            "charRomaji": [
              "kimi",
              "ga",
              "kou",
              "tei",
              "shi",
              "te",
              "ku",
              "re",
              "ta",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "僕は僕を好きになれそうだよ",
            "romaji": "bokuhabokuwosukininaresoudayo",
            "ko": "나는 나 자신을 좋아할 수 있을 것 같아",
            "charRomaji": [
              "boku",
              "ha",
              "boku",
              "wo",
              "su",
              "ki",
              "ni",
              "na",
              "re",
              "so",
              "u",
              "da",
              "yo"
            ]
          },
          {
            "ja": "一生なんて大げさな言葉",
            "romaji": "isshounanteoogesanakotoba",
            "ko": "평생이라는 거창한 말",
            "charRomaji": [
              "i",
              "sshou",
              "na",
              "n",
              "te",
              "oo",
              "ge",
              "sa",
              "na",
              "ko",
              "toba"
            ]
          },
          {
            "ja": "信じられなかったはずなのに",
            "romaji": "shinjirarenakattahazunanoni",
            "ko": "믿지 못했을 텐데도",
            "charRomaji": [
              "shin",
              "ji",
              "ra",
              "re",
              "na",
              "ka",
              "t",
              "ta",
              "ha",
              "zu",
              "na",
              "no",
              "ni"
            ]
          },
          {
            "ja": "君となら信じてみたいと思えたんだ",
            "romaji": "kimitonarashinjitemitaitoomoetanda",
            "ko": "너와 함께라면 믿어보고 싶다고 생각했어",
            "charRomaji": [
              "kimi",
              "to",
              "na",
              "ra",
              "shin",
              "ji",
              "te",
              "mi",
              "ta",
              "i",
              "to",
              "omo",
              "e",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "一期一会じゃ終わらせない",
            "romaji": "ichigoichiejaowarasenai",
            "ko": "일기일회로 끝나게 두지 않아",
            "charRomaji": [
              "ichi",
              "go",
              "ichi",
              "e",
              "j",
              "a",
              "o",
              "wa",
              "ra",
              "se",
              "na",
              "i"
            ]
          },
          {
            "ja": "僕らの音一会はずっと続いていく",
            "romaji": "bokuranootoichiehazuttotsuzuiteiku",
            "ko": "우리의 소리와 만남은 언제까지나 계속될 거야",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "oto",
              "ichi",
              "e",
              "ha",
              "zu",
              "t",
              "to",
              "tsuzu",
              "i",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "迷いながら叫びながら未来へ鳴り響け",
            "romaji": "mayoinagarasakebinagaramiraihenarihibike",
            "ko": "방황하면서도, 소리치면서도 미래를 향해 울려 퍼져라",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ga",
              "ra",
              "sake",
              "bi",
              "na",
              "ga",
              "ra",
              "mi",
              "rai",
              "he",
              "na",
              "ri",
              "hibi",
              "ke"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "senzaihyoumei",
    "title": "潜在表明",
    "reading": "せんざいひょうめい",
    "category": "original",
    "album": "2nd Single『音一会』c/w, 1st Album『迷跡波』",
    "youtubeId": "bkUqxpb_vYY",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "地下鉄の窓に急に映る顔がじっとこっちを見る",
            "romaji": "chikatetsunomadonikyuuniutsurukaogajittokocchiwomiru",
            "ko": "지하철 창문에 문득 비친 얼굴이 가만히 이쪽을 바라봐",
            "charRomaji": [
              "chi",
              "ka",
              "tetsu",
              "no",
              "mado",
              "ni",
              "kyuu",
              "ni",
              "utsu",
              "ru",
              "kao",
              "ga",
              "ji",
              "t",
              "to",
              "ko",
              "c",
              "chi",
              "wo",
              "mi",
              "ru"
            ]
          },
          {
            "ja": "そのひどく不安気な目を逸らすことも出来ず立ち尽くしていた",
            "romaji": "sonohidokufuankinamewosorasukotomodekizutachitsukushiteita",
            "ko": "그 몹시 불안한 눈길을 돌리지도 못한 채 우두커니 서 있었지",
            "charRomaji": [
              "so",
              "no",
              "hi",
              "do",
              "ku",
              "fu",
              "an",
              "ki",
              "na",
              "me",
              "wo",
              "so",
              "ra",
              "su",
              "ko",
              "to",
              "mo",
              "de",
              "ki",
              "zu",
              "ta",
              "chi",
              "tsu",
              "ku",
              "shi",
              "te",
              "i",
              "ta"
            ]
          },
          {
            "ja": "耳の奥で後ろ指さす声がこだまする",
            "romaji": "miminookudeushiroyubisasukoegakodamasuru",
            "ko": "귓속 깊은 곳에서 손가락질하는 목소리가 메아리쳐",
            "charRomaji": [
              "mimi",
              "no",
              "oku",
              "de",
              "ushi",
              "ro",
              "yubi",
              "sa",
              "su",
              "koe",
              "ga",
              "ko",
              "da",
              "ma",
              "su",
              "ru"
            ]
          },
          {
            "ja": "僕が僕であろうとすればするほど厭う声は大きくなるみたいだ",
            "romaji": "bokugabokudearoutosurebasuruhodoitoukoewaookikunarumitaida",
            "ko": "내가 나로서 있으려 할수록 싫어하는 목소리는 더 커지는 것 같아",
            "charRomaji": [
              "boku",
              "ga",
              "boku",
              "de",
              "a",
              "ro",
              "u",
              "to",
              "su",
              "re",
              "ba",
              "su",
              "ru",
              "ho",
              "do",
              "ito",
              "u",
              "koe",
              "wa",
              "oo",
              "ki",
              "ku",
              "na",
              "ru",
              "mi",
              "ta",
              "i",
              "da"
            ]
          },
          {
            "ja": "ねえ僕はあのときどうすればよかった",
            "romaji": "neebokuhaanotokidousurebayokatta",
            "ko": "저기, 나는 그때 어떻게 했어야 했던 걸까",
            "charRomaji": [
              "ne",
              "e",
              "boku",
              "ha",
              "a",
              "no",
              "to",
              "ki",
              "do",
              "u",
              "su",
              "re",
              "ba",
              "yo",
              "ka",
              "t",
              "ta"
            ]
          },
          {
            "ja": "わからないわからないままチクチクと時間だけがただ過ぎていく",
            "romaji": "wakaranaiwakaranaimamachikuchikutojikandakegatadasugiteiku",
            "ko": "모르겠어, 알지 못한 채로 따끔따끔 시간만이 그저 흘러가",
            "charRomaji": [
              "wa",
              "ka",
              "ra",
              "na",
              "i",
              "wa",
              "ka",
              "ra",
              "na",
              "i",
              "ma",
              "ma",
              "chi",
              "ku",
              "chi",
              "ku",
              "to",
              "ji",
              "kan",
              "da",
              "ke",
              "ga",
              "ta",
              "da",
              "su",
              "gi",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "ため息のようにドアが開くゆらゆらと進む地下通路",
            "romaji": "tameikinoyounidoagahirakuyurayuratosusumuchikatsuuro",
            "ko": "한숨처럼 문이 열리고 흔들흔들 나아가는 지하 통로",
            "charRomaji": [
              "ta",
              "me",
              "iki",
              "no",
              "yo",
              "u",
              "ni",
              "do",
              "a",
              "ga",
              "hira",
              "ku",
              "yu",
              "ra",
              "yu",
              "ra",
              "to",
              "susu",
              "mu",
              "chi",
              "ka",
              "tsu",
              "uro"
            ]
          },
          {
            "ja": "歩いても歩いても答えなんか出ない",
            "romaji": "aruitemoaruitemokotaenankadenai",
            "ko": "걷고 또 걸어도 해답 따윈 나오지 않아",
            "charRomaji": [
              "aru",
              "i",
              "te",
              "mo",
              "aru",
              "i",
              "te",
              "mo",
              "kota",
              "e",
              "na",
              "n",
              "ka",
              "de",
              "na",
              "i"
            ]
          },
          {
            "ja": "地上へ出ると煩いくらいの散光が僕を責めた",
            "romaji": "chijouhederutourusaikurainosankougabokuwosemeta",
            "ko": "지상으로 나오자 시끄러울 정도의 산란광이 나를 꾸짖었어",
            "charRomaji": [
              "chi",
              "jou",
              "he",
              "de",
              "ru",
              "to",
              "urusa",
              "i",
              "ku",
              "ra",
              "i",
              "no",
              "san",
              "kou",
              "ga",
              "boku",
              "wo",
              "se",
              "me",
              "ta"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "深く深く潜ったままの僕の声を抱えて歩いた",
            "romaji": "fukakufukakumoguttamamanobokunokoewokakaetearuita",
            "ko": "깊고 깊게 가라앉은 채인 나의 목소리를 끌어안고 걸었어",
            "charRomaji": [
              "fuka",
              "ku",
              "fuka",
              "ku",
              "mogu",
              "t",
              "ta",
              "ma",
              "ma",
              "no",
              "boku",
              "no",
              "koe",
              "wo",
              "kaka",
              "e",
              "te",
              "aru",
              "i",
              "ta"
            ]
          },
          {
            "ja": "太陽にあぶり出される僕の孤独のカタチが",
            "romaji": "taiyouniaburidasarerubokunokodokunokatachiga",
            "ko": "태양 아래 적나라하게 드러나는 내 고독의 모양이",
            "charRomaji": [
              "tai",
              "you",
              "ni",
              "a",
              "bu",
              "ri",
              "da",
              "sa",
              "re",
              "ru",
              "boku",
              "no",
              "ko",
              "doku",
              "no",
              "ka",
              "ta",
              "chi",
              "ga"
            ]
          },
          {
            "ja": "後ずさりするように影になった",
            "romaji": "atozusarisuruyounikageninatta",
            "ko": "뒷걸음질 치듯이 그림자가 되었지",
            "charRomaji": [
              "ato",
              "zu",
              "sa",
              "ri",
              "su",
              "ru",
              "yo",
              "u",
              "ni",
              "kage",
              "ni",
              "na",
              "t",
              "ta"
            ]
          },
          {
            "ja": "眩しすぎる正しさで僕へと照りつけないで",
            "romaji": "mabushisugirutadashisadebokuhetoteritsukenaide",
            "ko": "눈부신 올바름으로 나를 내리쬐지 말아줘",
            "charRomaji": [
              "mabu",
              "shi",
              "su",
              "gi",
              "ru",
              "tada",
              "shi",
              "sa",
              "de",
              "boku",
              "he",
              "to",
              "te",
              "ri",
              "tsu",
              "ke",
              "na",
              "i",
              "de"
            ]
          },
          {
            "ja": "遮ったこの腕だけが僕を庇う",
            "romaji": "saegittakonoudedakegabokuwokabau",
            "ko": "가로막은 이 두 팔만이 나를 감싸네",
            "charRomaji": [
              "saegi",
              "t",
              "ta",
              "ko",
              "no",
              "ude",
              "da",
              "ke",
              "ga",
              "boku",
              "wo",
              "kaba",
              "u"
            ]
          },
          {
            "ja": "逃げるように駆け込んだゲームセンター",
            "romaji": "nigeruyounikakekondageemusentaa",
            "ko": "도망치듯 뛰어 들어간 오락실",
            "charRomaji": [
              "ni",
              "ge",
              "ru",
              "yo",
              "u",
              "ni",
              "ka",
              "ke",
              "ko",
              "n",
              "da",
              "gee",
              "",
              "mu",
              "se",
              "n",
              "taa",
              ""
            ]
          },
          {
            "ja": "ドクンドクンモグラを叩く音が響いていた",
            "romaji": "dokundokunmogurawotatakuotogahibiiteita",
            "ko": "두근두근 두더지를 두드리는 소리가 울려 퍼졌어",
            "charRomaji": [
              "do",
              "ku",
              "n",
              "do",
              "ku",
              "n",
              "mo",
              "gu",
              "ra",
              "wo",
              "tata",
              "ku",
              "oto",
              "ga",
              "hibi",
              "i",
              "te",
              "i",
              "ta"
            ]
          },
          {
            "ja": "叩かれては沈んでいくその姿はまるで僕だ",
            "romaji": "tatakaretehashizundeikusonosugatahamarudebokuda",
            "ko": "두들겨 맞으며 가라앉아 가는 그 모습은 꼭 나 같았어",
            "charRomaji": [
              "tata",
              "ka",
              "re",
              "te",
              "ha",
              "shizu",
              "n",
              "de",
              "i",
              "ku",
              "so",
              "no",
              "sugata",
              "ha",
              "ma",
              "ru",
              "de",
              "boku",
              "da"
            ]
          },
          {
            "ja": "ため息に曇って見えなくなっていた場所",
            "romaji": "tameikinikumottemienakunatteitabasho",
            "ko": "한숨에 흐려져 보이지 않게 되어버린 장소",
            "charRomaji": [
              "ta",
              "me",
              "iki",
              "ni",
              "kumo",
              "t",
              "te",
              "mi",
              "e",
              "na",
              "ku",
              "na",
              "t",
              "te",
              "i",
              "ta",
              "ba",
              "sho"
            ]
          },
          {
            "ja": "そこにうずくまっていたんだずっと気づけずにいたんだ",
            "romaji": "sokoniuzukumatteitandazuttokizukezuniitanda",
            "ko": "거기에 웅크리고 있었던 거야, 계속 깨닫지 못하고 있었던 거야",
            "charRomaji": [
              "so",
              "ko",
              "ni",
              "u",
              "zu",
              "ku",
              "ma",
              "t",
              "te",
              "i",
              "ta",
              "n",
              "da",
              "zu",
              "t",
              "to",
              "ki",
              "zu",
              "ke",
              "zu",
              "ni",
              "i",
              "ta",
              "n",
              "da"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "kageiromai",
    "title": "影色舞",
    "reading": "しるえっと だんす",
    "category": "original",
    "album": "2nd Single『音一会』c/w, 1st Album『迷跡波』",
    "youtubeId": "iFIXi6zzCls",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "あと一匙の憂鬱で壊れそうなんて",
            "romaji": "atoichisajinoyuuutsudekowaresounante",
            "ko": "앞으로 한 스푼의 우울로 무너져버릴 것 같다고",
            "charRomaji": [
              "a",
              "to",
              "ichi",
              "saji",
              "no",
              "yuu",
              "utsu",
              "de",
              "kowa",
              "re",
              "so",
              "u",
              "na",
              "n",
              "te"
            ]
          },
          {
            "ja": "のたまえどおかまいなく記憶域圧されてしまう",
            "romaji": "notamaedookamainakukiokuikiosareteshimau",
            "ko": "지껄여대도 아랑곳없이 기억 영역은 짓눌려버려",
            "charRomaji": [
              "no",
              "ta",
              "ma",
              "e",
              "do",
              "o",
              "ka",
              "ma",
              "i",
              "na",
              "ku",
              "ki",
              "oku",
              "iki",
              "o",
              "sa",
              "re",
              "te",
              "shi",
              "ma",
              "u"
            ]
          },
          {
            "ja": "躓いては縋っていた未検証フィロソフィー",
            "romaji": "chiitehatsuitteitahitsujikenshoufirosofii",
            "ko": "넘어질 때마다 매달렸던 미검증 철학",
            "charRomaji": [
              "chi",
              "i",
              "te",
              "ha",
              "tsui",
              "t",
              "te",
              "i",
              "ta",
              "hitsuji",
              "ken",
              "shou",
              "f",
              "i",
              "ro",
              "so",
              "f",
              "ii",
              ""
            ]
          },
          {
            "ja": "己さえごまかせないチープな理論武装",
            "romaji": "onoresaegomakasenaichiipunarironbusou",
            "ko": "자신조차 속이지 못하는 값싼 이론 무장",
            "charRomaji": [
              "onore",
              "sa",
              "e",
              "go",
              "ma",
              "ka",
              "se",
              "na",
              "i",
              "chii",
              "",
              "pu",
              "na",
              "ri",
              "ron",
              "bu",
              "sou"
            ]
          },
          {
            "ja": "答えが出るまでとか未来永劫",
            "romaji": "kotaegaderumadetokamiraieigou",
            "ko": "답이 나올 때까지라니 영원무궁한 소리",
            "charRomaji": [
              "kota",
              "e",
              "ga",
              "de",
              "ru",
              "ma",
              "de",
              "to",
              "ka",
              "mi",
              "rai",
              "ei",
              "gou"
            ]
          },
          {
            "ja": "とめどない思考回路を誰かねえ止めて",
            "romaji": "tomedonaishikoukairowodarekaneetomete",
            "ko": "끝없는 사고 회로를 누군가 제발 멈춰줘",
            "charRomaji": [
              "to",
              "me",
              "do",
              "na",
              "i",
              "shi",
              "kou",
              "ka",
              "iro",
              "wo",
              "dare",
              "ka",
              "ne",
              "e",
              "to",
              "me",
              "te"
            ]
          },
          {
            "ja": "もうなにもかも忘れて今宵はシルエットダンス",
            "romaji": "mounanimokamowasuretekoyoiwashiruettodansu",
            "ko": "이젠 모든 것을 다 잊어버리고 오늘 밤은 실루엣 댄스",
            "charRomaji": [
              "mo",
              "u",
              "na",
              "ni",
              "mo",
              "ka",
              "mo",
              "wasu",
              "re",
              "te",
              "ko",
              "yoi",
              "wa",
              "shi",
              "ru",
              "e",
              "t",
              "to",
              "da",
              "n",
              "su"
            ]
          },
          {
            "ja": "知らない要らない全然なんの法則もなくただ舞って舞う",
            "romaji": "shiranaiiranaizenzennannohousokumonakutadamattemau",
            "ko": "몰라, 필요 없어, 전혀 아무 법칙도 없이 그저 춤추고 춤춰",
            "charRomaji": [
              "shi",
              "ra",
              "na",
              "i",
              "i",
              "ra",
              "na",
              "i",
              "zen",
              "zen",
              "na",
              "n",
              "no",
              "ho",
              "usoku",
              "mo",
              "na",
              "ku",
              "ta",
              "da",
              "ma",
              "t",
              "te",
              "ma",
              "u"
            ]
          },
          {
            "ja": "照明一切を消しちゃってさあ宇宙へとリンク",
            "romaji": "shoumeiissaiwokeshichattesaauchuuhetorinku",
            "ko": "조명을 모조리 다 꺼버리고 자 우주로 링크해",
            "charRomaji": [
              "shou",
              "mei",
              "i",
              "ssai",
              "wo",
              "ke",
              "shi",
              "ch",
              "a",
              "t",
              "te",
              "sa",
              "a",
              "u",
              "chuu",
              "he",
              "to",
              "ri",
              "n",
              "ku"
            ]
          },
          {
            "ja": "ビートに呼応して浮かび上がる超然的シルエットダンス",
            "romaji": "biitonikooushiteukabiagaruchouzentekishiruettodansu",
            "ko": "비트에 호응하며 떠오르는 초연한 실루엣 댄스",
            "charRomaji": [
              "bii",
              "",
              "to",
              "ni",
              "ko",
              "ou",
              "shi",
              "te",
              "u",
              "ka",
              "bi",
              "a",
              "ga",
              "ru",
              "chou",
              "zen",
              "teki",
              "shi",
              "ru",
              "e",
              "t",
              "to",
              "da",
              "n",
              "su"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "音の中に溶けていく僕のリアリティー",
            "romaji": "otononakanitoketeikubokunoriariteii",
            "ko": "소리 속에 녹아들어 가는 나의 리얼리티",
            "charRomaji": [
              "oto",
              "no",
              "naka",
              "ni",
              "to",
              "ke",
              "te",
              "i",
              "ku",
              "boku",
              "no",
              "ri",
              "a",
              "ri",
              "t",
              "eii",
              ""
            ]
          },
          {
            "ja": "感傷も焦燥も粉々にちりぬる模様",
            "romaji": "kanshoumoshousoumokonagonanichirinurumoyou",
            "ko": "감상도 초조함도 산산조각 흩날리는 무늬",
            "charRomaji": [
              "kan",
              "shou",
              "mo",
              "shou",
              "sou",
              "mo",
              "konago",
              "na",
              "ni",
              "chi",
              "ri",
              "nu",
              "ru",
              "mo",
              "you"
            ]
          },
          {
            "ja": "五臓六腑に響いちゃって脈打つメロディライン",
            "romaji": "gozouroppunihibiichattemyakuutsumerodirain",
            "ko": "오장육부에 울려 퍼지며 요동치는 멜로디 라인",
            "charRomaji": [
              "go",
              "zou",
              "ro",
              "ppu",
              "ni",
              "hibi",
              "i",
              "ch",
              "a",
              "t",
              "te",
              "myaku",
              "u",
              "tsu",
              "me",
              "ro",
              "d",
              "i",
              "ra",
              "i",
              "n"
            ]
          },
          {
            "ja": "この僕を駆け巡る流星が跳ねる",
            "romaji": "konobokuwokakemegururyuuseigahaneru",
            "ko": "이 나를 내달리는 유성이 튀어 올라",
            "charRomaji": [
              "ko",
              "no",
              "boku",
              "wo",
              "ka",
              "ke",
              "megu",
              "ru",
              "ryu",
              "usei",
              "ga",
              "ha",
              "ne",
              "ru"
            ]
          },
          {
            "ja": "飛び込んだならそこはもう無重力浮遊してダンス",
            "romaji": "tobikondanarasokohamoumujuuryokufuyuushitedansu",
            "ko": "뛰어들었다면 그곳은 이미 무중력, 부유하며 댄스",
            "charRomaji": [
              "to",
              "bi",
              "ko",
              "n",
              "da",
              "na",
              "ra",
              "so",
              "ko",
              "ha",
              "mo",
              "u",
              "mu",
              "ju",
              "uryoku",
              "fu",
              "yuu",
              "shi",
              "te",
              "da",
              "n",
              "su"
            ]
          },
          {
            "ja": "意味ない間違い全然気にもとめないで舞って舞う",
            "romaji": "iminaimachigaizenzenkinimotomenaidemattemau",
            "ko": "의미 없어, 실수해도 전혀 신경 쓰지 말고 춤추고 춤춰",
            "charRomaji": [
              "i",
              "mi",
              "na",
              "i",
              "ma",
              "chiga",
              "i",
              "zen",
              "zen",
              "ki",
              "ni",
              "mo",
              "to",
              "me",
              "na",
              "i",
              "de",
              "ma",
              "t",
              "te",
              "ma",
              "u"
            ]
          },
          {
            "ja": "何一つ生み出さないああ透明な自由",
            "romaji": "nanihitotsuumidasanaiaatoumeinajiyuu",
            "ko": "단 하나도 만들어내지 않는 아아 투명한 자유",
            "charRomaji": [
              "nani",
              "hito",
              "tsu",
              "u",
              "mi",
              "da",
              "sa",
              "na",
              "i",
              "a",
              "a",
              "tou",
              "mei",
              "na",
              "ji",
              "yuu"
            ]
          },
          {
            "ja": "全部リセットで空っぽになれたら",
            "romaji": "zenburisettodekarapponinaretara",
            "ko": "전부 리셋해서 텅 비어버릴 수 있다면",
            "charRomaji": [
              "zen",
              "bu",
              "ri",
              "se",
              "t",
              "to",
              "de",
              "kara",
              "p",
              "po",
              "ni",
              "na",
              "re",
              "ta",
              "ra"
            ]
          },
          {
            "ja": "宇宙をクラウドにして預けてしまえすべて",
            "romaji": "uchuuwokuraudonishiteazuketeshimaesubete",
            "ko": "우주를 클라우드로 삼아 맡겨버려라 모든 것을",
            "charRomaji": [
              "u",
              "chuu",
              "wo",
              "ku",
              "ra",
              "u",
              "do",
              "ni",
              "shi",
              "te",
              "azu",
              "ke",
              "te",
              "shi",
              "ma",
              "e",
              "su",
              "be",
              "te"
            ]
          },
          {
            "ja": "金輪際誰も知らない夜僕の夜前衛的シルエットダンス",
            "romaji": "konrinzaidaremoshiranaiyorubokunoyazeneitekishiruettodansu",
            "ko": "결코 그 누구도 알지 못하는 밤, 나의 밤, 전위적 실루엣 댄스",
            "charRomaji": [
              "ko",
              "n",
              "rinzai",
              "dare",
              "mo",
              "shi",
              "ra",
              "na",
              "i",
              "yoru",
              "boku",
              "no",
              "ya",
              "z",
              "enei",
              "teki",
              "shi",
              "ru",
              "e",
              "t",
              "to",
              "da",
              "n",
              "su"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "hitoshizuku",
    "title": "壱雫空",
    "reading": "ひとしずく",
    "category": "original",
    "album": "3rd Single『壱雫空』, 1st Album『迷跡波』",
    "youtubeId": "_CraJ8654Bg",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "もしこの雨が上がっても忘れずに歩いてくよ",
            "romaji": "moshikonoamegaagattemowasurezuniaruitekuyo",
            "ko": "만약 이 비가 그치더라도 잊지 않고 걸어갈게",
            "charRomaji": [
              "mo",
              "shi",
              "ko",
              "no",
              "ame",
              "ga",
              "a",
              "ga",
              "t",
              "te",
              "mo",
              "wasu",
              "re",
              "zu",
              "ni",
              "aru",
              "i",
              "te",
              "ku",
              "yo"
            ]
          },
          {
            "ja": "最初のひとしずくに顔上げた今日の僕を",
            "romaji": "saishonohitoshizukunikaoagetakyounobokuwo",
            "ko": "첫 한 방울에 고개를 들었던 오늘의 나를",
            "charRomaji": [
              "sa",
              "isho",
              "no",
              "hi",
              "to",
              "shi",
              "zu",
              "ku",
              "ni",
              "kao",
              "a",
              "ge",
              "ta",
              "k",
              "you",
              "no",
              "boku",
              "wo"
            ]
          },
          {
            "ja": "透明な傘で作るひとり分だけの世界",
            "romaji": "toumeinakasadetsukuruhitorifundakenosekai",
            "ko": "투명한 우산으로 만든 나 한 사람만의 세계",
            "charRomaji": [
              "tou",
              "mei",
              "na",
              "kasa",
              "de",
              "tsuku",
              "ru",
              "hi",
              "to",
              "ri",
              "fun",
              "da",
              "ke",
              "no",
              "se",
              "kai"
            ]
          },
          {
            "ja": "そっと逃げ込んでいた",
            "romaji": "sottonigekondeita",
            "ko": "가만히 도망쳐 숨어 있었지",
            "charRomaji": [
              "so",
              "t",
              "to",
              "ni",
              "ge",
              "ko",
              "n",
              "de",
              "i",
              "ta"
            ]
          },
          {
            "ja": "ビニール越しの空からこぼれ落ちる音響いて",
            "romaji": "biniirukoshinosorakarakoboreochiruotohibiite",
            "ko": "비닐 너머의 하늘에서 흘러떨어지는 소리가 울려 퍼져",
            "charRomaji": [
              "bi",
              "nii",
              "",
              "ru",
              "ko",
              "shi",
              "nosor",
              "a",
              "ka",
              "ra",
              "ko",
              "bo",
              "re",
              "o",
              "chi",
              "ru",
              "ot",
              "ohibi",
              "i",
              "te"
            ]
          },
          {
            "ja": "滲む心へと溶けた",
            "romaji": "nijimukokorohetotoketa",
            "ko": "번져가는 마음으로 녹아들었어",
            "charRomaji": [
              "niji",
              "mu",
              "kokoroh",
              "e",
              "to",
              "to",
              "ke",
              "ta"
            ]
          },
          {
            "ja": "泣きじゃくっているこの空といこう",
            "romaji": "nakijakutteirukonosoratoikou",
            "ko": "흐느껴 울고 있는 이 하늘과 함께 가자",
            "charRomaji": [
              "na",
              "ki",
              "j",
              "a",
              "ku",
              "t",
              "te",
              "i",
              "ru",
              "ko",
              "no",
              "sora",
              "to",
              "i",
              "ko",
              "u"
            ]
          },
          {
            "ja": "通り過ぎる時を待つだけじゃなくて",
            "romaji": "tourisugirutokiwomatsudakejanakute",
            "ko": "지나가는 시간을 그저 기다리기만 하는 게 아니라",
            "charRomaji": [
              "tou",
              "ri",
              "su",
              "gi",
              "ru",
              "toki",
              "wo",
              "ma",
              "tsu",
              "da",
              "ke",
              "j",
              "a",
              "na",
              "ku",
              "te"
            ]
          },
          {
            "ja": "僕は見つめていたいんだよ",
            "romaji": "bokuhamitsumeteitaindayo",
            "ko": "나는 똑바로 바라보고 싶어",
            "charRomaji": [
              "boku",
              "ha",
              "mi",
              "tsu",
              "me",
              "te",
              "i",
              "ta",
              "i",
              "n",
              "da",
              "yo"
            ]
          },
          {
            "ja": "無色でもそこにあるもの",
            "romaji": "mushokudemosokoniarumono",
            "ko": "색이 없어도 분명 거기에 존재하는 것을",
            "charRomaji": [
              "mu",
              "shoku",
              "de",
              "mo",
              "so",
              "ko",
              "ni",
              "a",
              "ru",
              "mo",
              "no"
            ]
          },
          {
            "ja": "この雨が上がってく時なにもなかったように",
            "romaji": "konoamegaagattekutokinanimonakattayouni",
            "ko": "이 비가 그쳐갈 때 아무 일도 없었던 것처럼",
            "charRomaji": [
              "ko",
              "no",
              "ame",
              "ga",
              "a",
              "ga",
              "t",
              "te",
              "ku",
              "toki",
              "na",
              "ni",
              "mo",
              "na",
              "ka",
              "t",
              "ta",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "消えてく傘花みたいに心は上手に折り畳めないから",
            "romaji": "kietekukasahanamitainikokorohajouzunioritatamenaikara",
            "ko": "접히는 우산꽃처럼 마음은 깔끔하게 접히지 않으니까",
            "charRomaji": [
              "ki",
              "e",
              "te",
              "ku",
              "kasa",
              "hana",
              "mi",
              "ta",
              "i",
              "ni",
              "kokoro",
              "ha",
              "",
              "jouzu",
              "ni",
              "o",
              "ri",
              "tata",
              "me",
              "na",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "過ぎ去ってしまう瞬間を僕は集めたいよ",
            "romaji": "sugisatteshimaushunkanwobokuhaatsumetaiyo",
            "ko": "지나가버리는 순간들을 나는 모으고 싶어",
            "charRomaji": [
              "su",
              "gi",
              "sa",
              "t",
              "te",
              "shi",
              "ma",
              "u",
              "shun",
              "kan",
              "wo",
              "boku",
              "ha",
              "atsu",
              "me",
              "ta",
              "i",
              "yo"
            ]
          },
          {
            "ja": "ああひとしずくを",
            "romaji": "aahitoshizukuwo",
            "ko": "아아, 이 한 방울의 눈물을",
            "charRomaji": [
              "a",
              "a",
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
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "とめどなく傘にすべり落ちる雫が揺れて描いてく",
            "romaji": "tomedonakukasanisuberiochirushizukugayureteegaiteku",
            "ko": "끝없이 우산을 타고 미끄러지는 물방울이 흔들리며 그려가",
            "charRomaji": [
              "to",
              "me",
              "do",
              "na",
              "ku",
              "kasa",
              "ni",
              "su",
              "be",
              "ri",
              "o",
              "chi",
              "ru",
              "shizuku",
              "ga",
              "yu",
              "re",
              "te",
              "ega",
              "i",
              "te",
              "ku"
            ]
          },
          {
            "ja": "風に震えてはぐずついてる僕みたいな",
            "romaji": "kazenifuruetehaguzutsuiterubokumitaina",
            "ko": "바람에 떨며 칭얼거리는 나 같은",
            "charRomaji": [
              "kaze",
              "ni",
              "furu",
              "e",
              "te",
              "ha",
              "gu",
              "zu",
              "tsu",
              "i",
              "te",
              "ru",
              "boku",
              "mi",
              "ta",
              "i",
              "na"
            ]
          },
          {
            "ja": "くすんでる今日を映した",
            "romaji": "kusunderukyouwoutsushita",
            "ko": "칙칙하게 흐린 오늘을 비추었어",
            "charRomaji": [
              "ku",
              "su",
              "n",
              "de",
              "ru",
              "k",
              "you",
              "wo",
              "utsu",
              "shi",
              "ta"
            ]
          },
          {
            "ja": "迷い続けるこの空といこう",
            "romaji": "mayoitsuzukerukonosoratoikou",
            "ko": "끝없이 방황하는 이 하늘과 함께 가자",
            "charRomaji": [
              "mayo",
              "i",
              "tsuzu",
              "ke",
              "ru",
              "ko",
              "no",
              "sora",
              "to",
              "i",
              "ko",
              "u"
            ]
          },
          {
            "ja": "ただよう雲だって一秒先なんて",
            "romaji": "tadayoukumodatteichibyousakinante",
            "ko": "떠도는 구름조차 1초 뒤의 앞일 따위",
            "charRomaji": [
              "ta",
              "da",
              "yo",
              "u",
              "kumo",
              "da",
              "t",
              "te",
              "ichi",
              "byou",
              "saki",
              "na",
              "n",
              "te"
            ]
          },
          {
            "ja": "わからないままいくんだろう",
            "romaji": "wakaranaimamaikundarou",
            "ko": "알지 못한 채 흘러가는 것이겠지",
            "charRomaji": [
              "wa",
              "ka",
              "ra",
              "na",
              "i",
              "ma",
              "ma",
              "i",
              "ku",
              "n",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "不安で鈍く霞んでく明日も",
            "romaji": "fuandenibukukasundekuashitamo",
            "ko": "불안으로 둔하게 흐려져 가는 내일도",
            "charRomaji": [
              "fu",
              "an",
              "de",
              "nibu",
              "ku",
              "kasu",
              "n",
              "de",
              "ku",
              "a",
              "shita",
              "mo"
            ]
          },
          {
            "ja": "もしこの雨が上がっても忘れたくないから",
            "romaji": "moshikonoamegaagattemowasuretakunaikara",
            "ko": "만약 이 비가 그치더라도 잊고 싶지 않으니까",
            "charRomaji": [
              "mo",
              "shi",
              "ko",
              "no",
              "ame",
              "ga",
              "a",
              "ga",
              "t",
              "te",
              "mo",
              "wasu",
              "re",
              "ta",
              "ku",
              "na",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "たった今を書きとめておきたいんだ",
            "romaji": "tattaimawokakitometeokitainda",
            "ko": "오직 지금 이 순간을 적어두고 싶어",
            "charRomaji": [
              "ta",
              "t",
              "ta",
              "ima",
              "wo",
              "ka",
              "ki",
              "to",
              "me",
              "te",
              "o",
              "ki",
              "ta",
              "i",
              "n",
              "da"
            ]
          },
          {
            "ja": "この手じゃ届かないあの空から点線の糸で",
            "romaji": "konotejatodokanaianoakaratensennoitode",
            "ko": "이 손으로는 닿지 않는 저 하늘에서 점선의 실로",
            "charRomaji": [
              "ko",
              "no",
              "te",
              "j",
              "a",
              "todo",
              "ka",
              "na",
              "i",
              "a",
              "no",
              "a",
              "ka",
              "ra",
              "ten",
              "sen",
              "no",
              "ito",
              "de"
            ]
          },
          {
            "ja": "つなぐように届いたひとしずく",
            "romaji": "tsunaguyounitodoitahitoshizuku",
            "ko": "이어주듯이 내게 와 닿은 한 방울",
            "charRomaji": [
              "tsu",
              "na",
              "gu",
              "yo",
              "u",
              "ni",
              "todo",
              "i",
              "ta",
              "hi",
              "to",
              "shi",
              "zu",
              "ku"
            ]
          },
          {
            "ja": "最後のひと粒が小さく光って僕を映した",
            "romaji": "saigonohitotsubugachiisakuhikattebokuwoutsushita",
            "ko": "마지막 한 방울이 작게 반짝이며 나를 비추었어",
            "charRomaji": [
              "sa",
              "igo",
              "no",
              "hi",
              "to",
              "tsubu",
              "ga",
              "chii",
              "sa",
              "ku",
              "hika",
              "t",
              "te",
              "boku",
              "wo",
              "utsu",
              "shi",
              "ta"
            ]
          },
          {
            "ja": "まだ道は乾かないだろう潤んだ風を吸い込んだ",
            "romaji": "madamichiwakawakanaidaroujunndakazewosuikonda",
            "ko": "아직 길은 마르지 않았겠지, 촉촉한 바람을 들이마셨어",
            "charRomaji": [
              "ma",
              "da",
              "michi",
              "wa",
              "kawa",
              "ka",
              "na",
              "i",
              "da",
              "ro",
              "u",
              "jun",
              "n",
              "da",
              "kaze",
              "wo",
              "su",
              "i",
              "ko",
              "n",
              "da"
            ]
          },
          {
            "ja": "僕は連れていこうああひとしずくを",
            "romaji": "bokuhatsureteikouaahitoshizukuwo",
            "ko": "나는 데리고 갈게, 아아 한 방울의 물방울을",
            "charRomaji": [
              "boku",
              "ha",
              "tsu",
              "re",
              "te",
              "i",
              "ko",
              "u",
              "a",
              "a",
              "hi",
              "to",
              "shi",
              "zu",
              "ku",
              "wo"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "shiori",
    "title": "栞",
    "reading": "しおり",
    "category": "original",
    "album": "3rd Single『壱雫空』c/w, 1st Album『迷跡波』",
    "youtubeId": "wuUZjdiUCj0",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "普通とかあたりまえってなんだろう",
            "romaji": "futsuutokaatarimaettenandarou",
            "ko": "평범하다거나 당연하다는 건 대체 뭘까",
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
              "t",
              "te",
              "na",
              "n",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "今手にある物差しでは全然上手く測れなくって",
            "romaji": "imateniarumonosashidehazenzenumakuhakarenakutte",
            "ko": "지금 손에 쥔 잣대로는 전혀 제대로 잴 수가 없어서",
            "charRomaji": [
              "ima",
              "te",
              "ni",
              "a",
              "ru",
              "mono",
              "sa",
              "shi",
              "de",
              "ha",
              "zen",
              "zen",
              "u",
              "ma",
              "ku",
              "haka",
              "re",
              "na",
              "ku",
              "t",
              "te"
            ]
          },
          {
            "ja": "吐いてはまた吸い込んだ不安に僕は為すがまま立ち尽くして",
            "romaji": "haitehamatasuikondafuannibokuhanasugamamatachitsukushite",
            "ko": "내뱉고는 다시 들이마신 불안에 나는 속수무책 우두커니 서서",
            "charRomaji": [
              "ha",
              "i",
              "te",
              "ha",
              "ma",
              "ta",
              "su",
              "i",
              "ko",
              "n",
              "da",
              "fu",
              "an",
              "ni",
              "boku",
              "ha",
              "na",
              "su",
              "ga",
              "ma",
              "ma",
              "ta",
              "chi",
              "tsu",
              "ku",
              "shi",
              "te"
            ]
          },
          {
            "ja": "不器用で空回って傷つくことから逃げている",
            "romaji": "bukiyoudekaramawatteikizutsukukotokaranigeteiru",
            "ko": "서툴고 헛돌기만 하며 상처받는 것으로부터 도망치고 있어",
            "charRomaji": [
              "bu",
              "ki",
              "you",
              "de",
              "kar",
              "amawa",
              "t",
              "tei",
              "kizu",
              "tsu",
              "ku",
              "ko",
              "to",
              "ka",
              "ra",
              "ni",
              "ge",
              "te",
              "i",
              "ru"
            ]
          },
          {
            "ja": "現実とノートで行ったり来たり慰めて",
            "romaji": "genjittonootodeittarikitarinagusamete",
            "ko": "현실과 노트 사이를 오가며 스스로를 위로하고",
            "charRomaji": [
              "gen",
              "jit",
              "to",
              "noo",
              "",
              "to",
              "de",
              "i",
              "t",
              "ta",
              "ri",
              "ki",
              "ta",
              "ri",
              "nagusa",
              "me",
              "te"
            ]
          },
          {
            "ja": "ああなんて生きづらい世界なんだろう",
            "romaji": "aananteikizuraisekainandarou",
            "ko": "아아, 이 얼마나 살아가기 버거운 세상인가",
            "charRomaji": [
              "a",
              "a",
              "na",
              "n",
              "te",
              "i",
              "ki",
              "zu",
              "ra",
              "i",
              "se",
              "kai",
              "na",
              "n",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "だけどだけど全部全部ぼくだから",
            "romaji": "dakedodakedozenbuzenbubokudakara",
            "ko": "그렇지만, 그렇지만 전부 다 나 자신이니까",
            "charRomaji": [
              "da",
              "ke",
              "do",
              "da",
              "ke",
              "do",
              "zen",
              "bu",
              "zen",
              "bu",
              "bo",
              "ku",
              "da",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "うじうじしくしくぼくだから",
            "romaji": "ujiujishikushikubokudakara",
            "ko": "우물쭈물 훌쩍훌쩍 우는 나 자신이니까",
            "charRomaji": [
              "u",
              "ji",
              "u",
              "ji",
              "shi",
              "ku",
              "shi",
              "ku",
              "bo",
              "ku",
              "da",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "全部全部抱きしめて少し眠ろう",
            "romaji": "zenbuzenbudakishimetesukoshinemurou",
            "ko": "전부 다 끌어안고서 잠시 잠에 들자",
            "charRomaji": [
              "zen",
              "bu",
              "zen",
              "bu",
              "da",
              "ki",
              "shi",
              "me",
              "te",
              "suko",
              "shi",
              "nemu",
              "ro",
              "u"
            ]
          },
          {
            "ja": "いたいのいたいのとんでゆけ",
            "romaji": "itainoitainotondeyuke",
            "ko": "아픈 것아, 아픈 것아 저 멀리 날아가라",
            "charRomaji": [
              "i",
              "ta",
              "i",
              "no",
              "i",
              "ta",
              "i",
              "no",
              "to",
              "n",
              "de",
              "yu",
              "ke"
            ]
          },
          {
            "ja": "悲しみにすべてを奪われないように",
            "romaji": "kanashiminisubetewoubawarenaiyouni",
            "ko": "슬픔에 모든 것을 빼앗기지 않도록",
            "charRomaji": [
              "kana",
              "shi",
              "mi",
              "ni",
              "su",
              "be",
              "te",
              "wo",
              "uba",
              "wa",
              "re",
              "na",
              "i",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "僕は僕の味方でいようよ",
            "romaji": "bokuhabokunomikatadeiyouyo",
            "ko": "나는 언제나 나의 편이 되어줄 거야",
            "charRomaji": [
              "boku",
              "ha",
              "boku",
              "no",
              "mi",
              "kata",
              "de",
              "i",
              "yo",
              "u",
              "yo"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "人の顔色を窺いながら流されるままに衣食住",
            "romaji": "hitonokaoirowoukagainagaranagasarerumamaniishokujuu",
            "ko": "사람들의 눈치를 보며 휩쓸리는 대로 이어가는 의식주",
            "charRomaji": [
              "hito",
              "no",
              "kao",
              "iro",
              "wo",
              "ukaga",
              "i",
              "na",
              "ga",
              "ra",
              "naga",
              "sa",
              "re",
              "ru",
              "ma",
              "ma",
              "ni",
              "i",
              "shoku",
              "juu"
            ]
          },
          {
            "ja": "僕はなにがしたいんだろう",
            "romaji": "bokuhananigashitaindarou",
            "ko": "나는 대체 무엇을 하고 싶은 걸까",
            "charRomaji": [
              "boku",
              "ha",
              "na",
              "ni",
              "ga",
              "shi",
              "ta",
              "i",
              "n",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "こんなにも惨めで情けなくても",
            "romaji": "konnanimosanmedenasakenakutemo",
            "ko": "이토록 비참하고 한심할지라도",
            "charRomaji": [
              "ko",
              "n",
              "na",
              "ni",
              "mo",
              "san",
              "me",
              "de",
              "nasa",
              "ke",
              "na",
              "ku",
              "te",
              "mo"
            ]
          },
          {
            "ja": "僕はまだ自分を変えられそうにない",
            "romaji": "bokuhamadajibunwokaeraresouninai",
            "ko": "나는 아직 스스로를 바꿀 수 있을 것 같지 않아",
            "charRomaji": [
              "boku",
              "ha",
              "ma",
              "da",
              "ji",
              "bun",
              "wo",
              "ka",
              "e",
              "ra",
              "re",
              "so",
              "u",
              "ni",
              "na",
              "i"
            ]
          },
          {
            "ja": "気弱で八方美人嫌われることを恐れている",
            "romaji": "kiyowadehappoubijinkirawarerukotowoosoreteiru",
            "ko": "마음이 여려 팔방미인마냥 미움받는 것을 두려워하고 있어",
            "charRomaji": [
              "ki",
              "yowa",
              "de",
              "ha",
              "ppou",
              "bi",
              "jin",
              "kira",
              "wa",
              "re",
              "ru",
              "ko",
              "to",
              "wo",
              "oso",
              "re",
              "te",
              "i",
              "ru"
            ]
          },
          {
            "ja": "現実とノートで行ったり来たり励まして",
            "romaji": "genjittonootodeittarikitarihagemashite",
            "ko": "현실과 노트 사이를 오가며 스스로를 북돋우고",
            "charRomaji": [
              "gen",
              "jit",
              "to",
              "noo",
              "",
              "to",
              "de",
              "i",
              "t",
              "ta",
              "ri",
              "ki",
              "ta",
              "ri",
              "hage",
              "ma",
              "shi",
              "te"
            ]
          },
          {
            "ja": "物事に何でもかんでも意味を見出さなくたっていいからさ",
            "romaji": "monogotoninandemokandemoimiwomidasanakutatteiikarasa",
            "ko": "매사에 사사건건 의미를 억지로 찾아내지 않아도 괜찮으니까",
            "charRomaji": [
              "mono",
              "goto",
              "ni",
              "nan",
              "de",
              "mo",
              "ka",
              "n",
              "de",
              "mo",
              "i",
              "mi",
              "wo",
              "mi",
              "da",
              "sa",
              "na",
              "ku",
              "ta",
              "t",
              "te",
              "i",
              "i",
              "ka",
              "ra",
              "sa"
            ]
          },
          {
            "ja": "信じてもいいのかなここにいてもいいのかな",
            "romaji": "shinjitemoiinokanakokoniitemoiinokana",
            "ko": "믿어도 되는 걸까, 여기에 있어도 되는 걸까",
            "charRomaji": [
              "shin",
              "ji",
              "te",
              "mo",
              "i",
              "i",
              "no",
              "ka",
              "na",
              "ko",
              "ko",
              "ni",
              "i",
              "te",
              "mo",
              "i",
              "i",
              "no",
              "ka",
              "na"
            ]
          },
          {
            "ja": "自分自身を優しく受け止めて",
            "romaji": "jibunjishinwoyasashikuuketomete",
            "ko": "자기 자신을 다정하게 받아들여줘",
            "charRomaji": [
              "ji",
              "bun",
              "ji",
              "shin",
              "wo",
              "yasa",
              "shi",
              "ku",
              "u",
              "ke",
              "to",
              "me",
              "te"
            ]
          },
          {
            "ja": "たった一度の僕の人生愛するかどうかは僕次第",
            "romaji": "tattaichidonobokunojinseiaisurukadoukahabokushidai",
            "ko": "단 한 번뿐인 나의 인생, 사랑할지 어떨지는 나에게 달렸어",
            "charRomaji": [
              "ta",
              "t",
              "ta",
              "ichi",
              "do",
              "no",
              "boku",
              "no",
              "ji",
              "nsei",
              "ai",
              "su",
              "ru",
              "ka",
              "do",
              "u",
              "ka",
              "ha",
              "boku",
              "shi",
              "dai"
            ]
          },
          {
            "ja": "言葉は瑞々しく光るよだからだから",
            "romaji": "kotobawamizumizushikuhikaruyodakaradakara",
            "ko": "말들은 파릇파릇하게 빛날 거야, 그러니까",
            "charRomaji": [
              "ko",
              "toba",
              "wa",
              "mizumi",
              "zu",
              "shi",
              "ku",
              "hika",
              "ru",
              "yo",
              "da",
              "ka",
              "ra",
              "da",
              "ka",
              "ra"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "tanebi",
    "title": "焚音打",
    "reading": "たねび",
    "category": "original",
    "album": "Digital Single (2023), 2nd Album『跡暖空』",
    "youtubeId": "mNEbrOEoAHg",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "きっと理由はバラバラだった寄る辺のないあの日の僕たち",
            "romaji": "kittoriyuuwabarabaradattayoruhennonaianonichinobokutachi",
            "ko": "분명 이유는 제각각이었어, 의지할 곳 없던 그날의 우리들",
            "charRomaji": [
              "ki",
              "t",
              "to",
              "ri",
              "yuu",
              "wa",
              "ba",
              "ra",
              "ba",
              "ra",
              "da",
              "t",
              "ta",
              "yo",
              "ru",
              "hen",
              "no",
              "na",
              "i",
              "a",
              "no",
              "nichi",
              "no",
              "boku",
              "ta",
              "chi"
            ]
          },
          {
            "ja": "もう二度と傷つきたくないってそう思ってうつむいたのに",
            "romaji": "mounidotokizutsukitakunaittesouomotteutsumuitanoni",
            "ko": "이제 두 번 다시 상처 입고 싶지 않다고, 그리 생각하며 고개 숙였는데",
            "charRomaji": [
              "mo",
              "u",
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
              "t",
              "te",
              "so",
              "u",
              "omo",
              "t",
              "te",
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
            "ja": "迷ってたから出会えてやっとつないだ手を",
            "romaji": "mayottetakaradeaeteyattotsunaidatewo",
            "ko": "헤매고 있었기에 만날 수 있어서, 겨우 맞잡은 손을",
            "charRomaji": [
              "mayo",
              "t",
              "te",
              "ta",
              "ka",
              "ra",
              "de",
              "a",
              "e",
              "te",
              "ya",
              "t",
              "to",
              "tsu",
              "na",
              "i",
              "da",
              "te",
              "wo"
            ]
          },
          {
            "ja": "もう僕は離さない何があっても握りしめていく",
            "romaji": "moubokuhahanasanainanigaattemonigirishimeteiku",
            "ko": "이제 나는 놓지 않아, 무슨 일이 있어도 꼭 쥐고 나아갈 거야",
            "charRomaji": [
              "mo",
              "u",
              "boku",
              "ha",
              "hana",
              "sa",
              "na",
              "i",
              "nani",
              "ga",
              "a",
              "t",
              "te",
              "mo",
              "nigi",
              "ri",
              "shi",
              "me",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "正解なんてわからなくて転んでまた痛みを知った",
            "romaji": "seikainantewakaranakutekorondemataitamiwoshitta",
            "ko": "정답 따윈 알지 못해서 넘어지고 또다시 아픔을 배웠어",
            "charRomaji": [
              "sei",
              "kai",
              "na",
              "n",
              "te",
              "wa",
              "ka",
              "ra",
              "na",
              "ku",
              "te",
              "koro",
              "n",
              "de",
              "ma",
              "ta",
              "ita",
              "mi",
              "wo",
              "shi",
              "t",
              "ta"
            ]
          },
          {
            "ja": "それでも立ち上がった君を笑うはずなんてない",
            "romaji": "soredemotachiagattakimiwowarauhazunantenai",
            "ko": "그런데도 다시 일어선 너를 비웃을 리가 없잖아",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "ta",
              "chi",
              "a",
              "ga",
              "t",
              "ta",
              "kimi",
              "wo",
              "wara",
              "u",
              "ha",
              "zu",
              "na",
              "n",
              "te",
              "na",
              "i"
            ]
          },
          {
            "ja": "行き止まりばかりでもまた道を探す",
            "romaji": "ikidomaribakaridemomatamichiwosagasu",
            "ko": "막다른 길뿐이라도 다시금 길을 찾아내",
            "charRomaji": [
              "i",
              "ki",
              "do",
              "ma",
              "ri",
              "ba",
              "ka",
              "ri",
              "de",
              "mo",
              "ma",
              "ta",
              "michi",
              "wo",
              "saga",
              "su"
            ]
          },
          {
            "ja": "この音で響き合うためここに立つため",
            "romaji": "konootodehibikiautamekokonitatsutame",
            "ko": "이 소리로 서로 공명하기 위해, 여기에 서기 위해",
            "charRomaji": [
              "ko",
              "no",
              "oto",
              "de",
              "hibi",
              "ki",
              "a",
              "u",
              "ta",
              "me",
              "ko",
              "ko",
              "ni",
              "ta",
              "tsu",
              "ta",
              "me"
            ]
          },
          {
            "ja": "心の中に瞬間灯った小さな火消さないでいて",
            "romaji": "kokorononakanishunkantomottachiisanahikeshisanaideite",
            "ko": "마음속에 순간 타오른 작은 불씨를 꺼트리지 말아줘",
            "charRomaji": [
              "kokoro",
              "no",
              "naka",
              "ni",
              "shun",
              "kan",
              "tomo",
              "t",
              "ta",
              "chii",
              "sa",
              "na",
              "hi",
              "keshi",
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
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "完璧なんてほど遠い僕たちだけど",
            "romaji": "kanpekinantehodotooibokutachidakedo",
            "ko": "완벽 따위와는 거리가 먼 우리들이지만",
            "charRomaji": [
              "kan",
              "peki",
              "na",
              "n",
              "te",
              "ho",
              "do",
              "too",
              "i",
              "boku",
              "ta",
              "chi",
              "da",
              "ke",
              "do"
            ]
          },
          {
            "ja": "この音色でしかたきつけられない胸が今騒ぎ出して",
            "romaji": "kononeirodeshikatakitsukerarenaimunegaimasawagidashite",
            "ko": "이 음색으로밖에 불붙일 수 없는 가슴이 지금 요동치기 시작해",
            "charRomaji": [
              "ko",
              "no",
              "ne",
              "iro",
              "de",
              "shi",
              "ka",
              "ta",
              "ki",
              "tsu",
              "ke",
              "ra",
              "re",
              "na",
              "i",
              "mune",
              "ga",
              "ima",
              "sawa",
              "gi",
              "da",
              "shi",
              "te"
            ]
          },
          {
            "ja": "心の真ん中に宿す歌を灯りに",
            "romaji": "kokoronomannakaniyadosuutawoakarini",
            "ko": "마음 한가운데 품은 노래를 등불 삼아",
            "charRomaji": [
              "kokoro",
              "no",
              "ma",
              "n",
              "naka",
              "ni",
              "yado",
              "su",
              "uta",
              "wo",
              "aka",
              "ri",
              "ni"
            ]
          },
          {
            "ja": "僕たちの音鳴らしていたいよ",
            "romaji": "bokutachinootonarashiteitaiyo",
            "ko": "우리들의 소리를 울려 퍼지게 하고 싶어",
            "charRomaji": [
              "boku",
              "ta",
              "chi",
              "no",
              "oto",
              "na",
              "ra",
              "shi",
              "te",
              "i",
              "ta",
              "i",
              "yo"
            ]
          },
          {
            "ja": "たった今ここに立つ僕たちを照らそう",
            "romaji": "tattaimakokonitatsubokutachiwoterasou",
            "ko": "바로 지금 여기에 서 있는 우리들을 비추자",
            "charRomaji": [
              "ta",
              "t",
              "ta",
              "ima",
              "ko",
              "ko",
              "ni",
              "ta",
              "tsu",
              "boku",
              "ta",
              "chi",
              "wo",
              "te",
              "ra",
              "so",
              "u"
            ]
          },
          {
            "ja": "迷うことに迷わないでいいよ",
            "romaji": "mayoukotonimayowanaideiiyo",
            "ko": "망설이는 것에 망설이지 않아도 괜찮아",
            "charRomaji": [
              "mayo",
              "u",
              "ko",
              "to",
              "ni",
              "mayo",
              "wa",
              "na",
              "i",
              "de",
              "i",
              "i",
              "yo"
            ]
          },
          {
            "ja": "言葉になんてしたところで戸惑う人の目が怖かった",
            "romaji": "kotobaninanteshitatokorodetomadouhitonomegakowakatta",
            "ko": "말로 해봤자 당혹스러워하는 사람들의 시선이 두려웠어",
            "charRomaji": [
              "ko",
              "toba",
              "ni",
              "na",
              "n",
              "te",
              "shi",
              "ta",
              "to",
              "ko",
              "ro",
              "de",
              "to",
              "mado",
              "u",
              "hito",
              "no",
              "me",
              "ga",
              "kowa",
              "ka",
              "t",
              "ta"
            ]
          },
          {
            "ja": "それでも抱えた声を決めてくれた音楽",
            "romaji": "soredemokakaetakoewokimetekuretaongaku",
            "ko": "그럼에도 끌어안은 목소리를 믿어주었던 음악",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "kaka",
              "e",
              "ta",
              "koe",
              "wo",
              "ki",
              "me",
              "te",
              "ku",
              "re",
              "ta",
              "o",
              "ngaku"
            ]
          },
          {
            "ja": "こぼれた涙さえここじゃ暖かく",
            "romaji": "koboretanamidasaekokojaatatakaku",
            "ko": "흘러내린 눈물조차 여기선 따뜻하게",
            "charRomaji": [
              "ko",
              "bo",
              "re",
              "ta",
              "namida",
              "sa",
              "e",
              "ko",
              "ko",
              "j",
              "a",
              "atata",
              "ka",
              "ku"
            ]
          },
          {
            "ja": "ほら穴のライブハウスに咲いた熱は分け合う種火",
            "romaji": "horaananoraibuhausunisaitanetsuwawakeautanebi",
            "ko": "동굴 같은 라이브하우스에 피어난 열기는 함께 나누는 불씨",
            "charRomaji": [
              "ho",
              "ra",
              "ana",
              "no",
              "ra",
              "i",
              "bu",
              "ha",
              "u",
              "su",
              "ni",
              "sa",
              "i",
              "ta",
              "netsu",
              "wa",
              "wa",
              "ke",
              "a",
              "u",
              "tane",
              "bi"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "hekitenbansou",
    "title": "碧天伴走",
    "reading": "へきてんばんそう",
    "category": "original",
    "album": "3rd Single『壱雫空』c/w, 1st Album『迷跡波』",
    "youtubeId": "zsO9_fZP2Uc",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "人知れず肩落としてる君がいるのに",
            "romaji": "hitoshirezukataotoshiterukimigairunoni",
            "ko": "아무도 모르게 어깨를 떨구고 있는 네가 있는데",
            "charRomaji": [
              "hi",
              "toshi",
              "re",
              "zu",
              "kata",
              "o",
              "to",
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
            "romaji": "hekisugiterusorabakarigamabushii",
            "ko": "너무나 푸르른 하늘만이 눈이 부셔",
            "charRomaji": [
              "heki",
              "su",
              "gi",
              "te",
              "ru",
              "sora",
              "ba",
              "ka",
              "ri",
              "ga",
              "mabu",
              "shi",
              "i"
            ]
          },
          {
            "ja": "僕はどんな言葉を君に言えばいいのか",
            "romaji": "bokuhadonnakotobawokiminiiebaiinoka",
            "ko": "나는 어떤 말을 너에게 해주면 좋을까",
            "charRomaji": [
              "boku",
              "ha",
              "do",
              "n",
              "na",
              "ko",
              "toba",
              "wo",
              "kimi",
              "ni",
              "i",
              "e",
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
              "tsuta",
              "e",
              "ra",
              "re",
              "ru",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "脆くやわいこころで生きる",
            "romaji": "zeikuyawaikokorodeikiru",
            "ko": "연약하고 무른 마음으로 살아가는",
            "charRomaji": [
              "zei",
              "ku",
              "ya",
              "wa",
              "i",
              "ko",
              "ko",
              "ro",
              "de",
              "i",
              "ki",
              "ru"
            ]
          },
          {
            "ja": "僕らは傷つく生き物で",
            "romaji": "bokurawakizutsukuikimonode",
            "ko": "우리는 쉽게 상처 입는 생물이라서",
            "charRomaji": [
              "boku",
              "ra",
              "wa",
              "kizu",
              "tsu",
              "ku",
              "i",
              "ki",
              "mono",
              "de"
            ]
          },
          {
            "ja": "なのに今日だって頑張ってる",
            "romaji": "nanonikyoudatteganbatteru",
            "ko": "그런데도 오늘조차도 너는 힘내고 있어",
            "charRomaji": [
              "na",
              "no",
              "ni",
              "k",
              "you",
              "da",
              "t",
              "te",
              "gan",
              "ba",
              "t",
              "te",
              "ru"
            ]
          },
          {
            "ja": "十分君はもう頑張ってる",
            "romaji": "juubunkimihamouganbatteru",
            "ko": "충분히 너는 이미 열심히 하고 있어",
            "charRomaji": [
              "ju",
              "ubun",
              "kimi",
              "ha",
              "mo",
              "u",
              "gan",
              "ba",
              "t",
              "te",
              "ru"
            ]
          },
          {
            "ja": "躓いて転んだって立ち上がり来たんだ",
            "romaji": "chiitekorondattetachiagarikitanda",
            "ko": "발이 걸려 넘어졌어도 다시 일어나 여기까지 왔잖아",
            "charRomaji": [
              "chi",
              "i",
              "te",
              "koro",
              "n",
              "da",
              "t",
              "te",
              "ta",
              "chi",
              "a",
              "ga",
              "ri",
              "ki",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "いつでもここに立ってるだけで必死なんだから",
            "romaji": "itsudemokokonitatterudakedehisshinandakara",
            "ko": "언제라도 그저 여기에 서 있는 것만으로도 필사적인 거니까",
            "charRomaji": [
              "i",
              "tsu",
              "de",
              "mo",
              "ko",
              "ko",
              "ni",
              "ta",
              "t",
              "te",
              "ru",
              "da",
              "ke",
              "de",
              "his",
              "shi",
              "na",
              "n",
              "da",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "ジタバタでラクじゃないけれど",
            "romaji": "jitabataderakujanaikeredo",
            "ko": "허둥대며 편하지는 않겠지만",
            "charRomaji": [
              "ji",
              "ta",
              "ba",
              "ta",
              "de",
              "ra",
              "ku",
              "j",
              "a",
              "na",
              "i",
              "ke",
              "re",
              "do"
            ]
          },
          {
            "ja": "迷っても君と進んでみたいよいいかな",
            "romaji": "mayottemokimitosusundemitaiyoiikana",
            "ko": "방황하더라도 너와 함께 나아가보고 싶어, 괜찮을까?",
            "charRomaji": [
              "mayo",
              "t",
              "te",
              "mo",
              "kimi",
              "to",
              "susu",
              "n",
              "de",
              "mi",
              "ta",
              "i",
              "yo",
              "i",
              "i",
              "ka",
              "na"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "誰かにはちっぽけなものだったとしても",
            "romaji": "darekanihachippokenamonodattatoshitemo",
            "ko": "누군가에게는 보잘것없는 하찮은 것일지라도",
            "charRomaji": [
              "dare",
              "ka",
              "ni",
              "ha",
              "chi",
              "p",
              "po",
              "ke",
              "na",
              "mo",
              "no",
              "da",
              "t",
              "ta",
              "to",
              "shi",
              "te",
              "mo"
            ]
          },
          {
            "ja": "君にとってはなにより大事なこと",
            "romaji": "kiminitottehananiyoridaijinakoto",
            "ko": "너에게 있어서는 무엇보다도 소중한 것",
            "charRomaji": [
              "kimi",
              "ni",
              "to",
              "t",
              "te",
              "ha",
              "na",
              "ni",
              "yo",
              "ri",
              "da",
              "iji",
              "na",
              "ko",
              "to"
            ]
          },
          {
            "ja": "壊さないで失わないで守りたいからとなりにいる",
            "romaji": "kowasanaideushinawanaidemamoritaikaratonariniiru",
            "ko": "망가뜨리지 마, 잃어버리지 마, 지켜주고 싶어서 곁에 있어",
            "charRomaji": [
              "kowa",
              "sa",
              "na",
              "i",
              "de",
              "ushina",
              "wa",
              "na",
              "i",
              "de",
              "mamo",
              "ri",
              "ta",
              "i",
              "ka",
              "ra",
              "to",
              "na",
              "ri",
              "ni",
              "i",
              "ru"
            ]
          },
          {
            "ja": "僕なんか言うのはやめるよ",
            "romaji": "bokunankaiunohayameruyo",
            "ko": "'나 따위가'라고 말하는 건 이제 그만둘게",
            "charRomaji": [
              "boku",
              "na",
              "n",
              "ka",
              "i",
              "u",
              "no",
              "ha",
              "ya",
              "me",
              "ru",
              "yo"
            ]
          },
          {
            "ja": "君にも言ってほしくないから",
            "romaji": "kiminimoittehoshikunaikara",
            "ko": "너도 그런 말은 하지 않았으면 좋겠으니까",
            "charRomaji": [
              "kimi",
              "ni",
              "mo",
              "i",
              "t",
              "te",
              "ho",
              "shi",
              "ku",
              "na",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "だから顔上げて伝えるよ",
            "romaji": "dakarakaoagetetsutaeruyo",
            "ko": "그러니까 고개를 들고 마음을 전해줘",
            "charRomaji": [
              "da",
              "ka",
              "ra",
              "kao",
              "a",
              "ge",
              "te",
              "tsuta",
              "e",
              "ru",
              "yo"
            ]
          },
          {
            "ja": "頑張ったよ昨日の君だって",
            "romaji": "ganbattayokinounokimidatte",
            "ko": "정말 수고 많았어, 어제의 너도",
            "charRomaji": [
              "gan",
              "ba",
              "t",
              "ta",
              "yo",
              "ki",
              "nou",
              "no",
              "kimi",
              "da",
              "t",
              "te"
            ]
          },
          {
            "ja": "思うようにいかないそんな毎日だって",
            "romaji": "omouyouniikanaisonnamainichidatte",
            "ko": "마음먹은 대로 되지 않는 그런 매일매일이라도",
            "charRomaji": [
              "omo",
              "u",
              "yo",
              "u",
              "ni",
              "i",
              "ka",
              "na",
              "i",
              "so",
              "n",
              "na",
              "mai",
              "nichi",
              "da",
              "t",
              "te"
            ]
          },
          {
            "ja": "頑張ったと知ってる僕は知ってるだから",
            "romaji": "ganbattatoshitterubokuhashitterudakara",
            "ko": "열심히 했다는 걸 알아, 나는 다 알고 있으니까",
            "charRomaji": [
              "gan",
              "ba",
              "t",
              "ta",
              "to",
              "shi",
              "t",
              "te",
              "ru",
              "boku",
              "ha",
              "shi",
              "t",
              "te",
              "ru",
              "da",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "こころを隠さないでほしい",
            "romaji": "kokorowokakusanaidehoshii",
            "ko": "마음을 숨기지 말아줬으면 해",
            "charRomaji": [
              "ko",
              "ko",
              "ro",
              "wo",
              "kaku",
              "sa",
              "na",
              "i",
              "de",
              "ho",
              "shi",
              "i"
            ]
          },
          {
            "ja": "逃げてもいい道が見えなくても",
            "romaji": "nigetemoiimichigamienakutemo",
            "ko": "도망쳐도 괜찮아, 길이 보이지 않더라도",
            "charRomaji": [
              "ni",
              "ge",
              "te",
              "mo",
              "i",
              "i",
              "michi",
              "ga",
              "mi",
              "e",
              "na",
              "ku",
              "te",
              "mo"
            ]
          },
          {
            "ja": "迷っても君と走っていたいんだよ一緒に",
            "romaji": "mayottemokimitohashitteitaindayoisshoni",
            "ko": "헤매더라도 너와 함께 달리고 싶은 거야, 함께",
            "charRomaji": [
              "mayo",
              "t",
              "te",
              "mo",
              "kimi",
              "to",
              "hashi",
              "t",
              "te",
              "i",
              "ta",
              "i",
              "n",
              "da",
              "yo",
              "i",
              "ssho",
              "ni"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "utaimashou",
    "title": "歌いましょう鳴らしましょう",
    "reading": "うたいましょうならしましょう",
    "category": "original",
    "album": "1st Album『迷跡波』",
    "youtubeId": "_0FI8xSgI1s",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "歌いましょう鳴らしましょう",
            "romaji": "utaimashounarashimashou",
            "ko": "노래합시다 울려 퍼뜨립시다",
            "charRomaji": [
              "uta",
              "i",
              "ma",
              "sh",
              "o",
              "u",
              "na",
              "ra",
              "shi",
              "ma",
              "sh",
              "o",
              "u"
            ]
          },
          {
            "ja": "声が枯れてしまうほどに",
            "romaji": "koegakareteshimauhodoni",
            "ko": "목이 쉬어버릴 정도로",
            "charRomaji": [
              "koe",
              "ga",
              "ka",
              "re",
              "te",
              "shi",
              "ma",
              "u",
              "ho",
              "do",
              "ni"
            ]
          },
          {
            "ja": "心臓の音響かせて",
            "romaji": "shinzounootohibikasete",
            "ko": "심장의 고동 소리를 울리며",
            "charRomaji": [
              "shin",
              "zou",
              "no",
              "ot",
              "ohibi",
              "ka",
              "se",
              "te"
            ]
          },
          {
            "ja": "何度でも此処で出逢おう",
            "romaji": "nandodemokokodeshutsuhouou",
            "ko": "몇 번이고 이곳에서 만나자",
            "charRomaji": [
              "nan",
              "do",
              "de",
              "mo",
              "ko",
              "ko",
              "de",
              "shutsu",
              "hou",
              "o",
              "u"
            ]
          },
          {
            "ja": "迷子のままでもいいから",
            "romaji": "maigonomamademoiikara",
            "ko": "미아인 채라도 괜찮으니까",
            "charRomaji": [
              "ma",
              "igo",
              "no",
              "ma",
              "ma",
              "de",
              "mo",
              "i",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "手探りで掴み取るんだ",
            "romaji": "tesaguridetsukamitorunda",
            "ko": "더듬어가며 움켜쥐는 거야",
            "charRomaji": [
              "te",
              "sagu",
              "ri",
              "de",
              "tsuka",
              "mi",
              "to",
              "ru",
              "n",
              "da"
            ]
          },
          {
            "ja": "孤独の影を切り裂いて",
            "romaji": "kodokunokagewokirisaite",
            "ko": "고독의 그림자를 베어 가르고",
            "charRomaji": [
              "ko",
              "doku",
              "no",
              "kage",
              "wo",
              "ki",
              "ri",
              "sa",
              "i",
              "te"
            ]
          },
          {
            "ja": "新しい風を呼び込もう",
            "romaji": "atarashiikazewoyobikomou",
            "ko": "새로운 바람을 불러들이자",
            "charRomaji": [
              "atara",
              "shi",
              "i",
              "kaze",
              "wo",
              "yo",
              "bi",
              "ko",
              "mo",
              "u"
            ]
          },
          {
            "ja": "胸の奥底で燻る情熱",
            "romaji": "munenookusokodeiburujounetsu",
            "ko": "가슴속 깊은 곳에서 그을리는 열정",
            "charRomaji": [
              "mune",
              "no",
              "oku",
              "soko",
              "de",
              "ibu",
              "ru",
              "jou",
              "netsu"
            ]
          },
          {
            "ja": "解き放て今この場所で",
            "romaji": "tokihoutteimakonobashode",
            "ko": "해방해라, 지금 이 자리에서",
            "charRomaji": [
              "to",
              "ki",
              "hout",
              "te",
              "ima",
              "ko",
              "no",
              "ba",
              "sho",
              "de"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "泣いた夜を忘れずに",
            "romaji": "naitayoruwowasurezuni",
            "ko": "울었던 밤을 잊지 않은 채",
            "charRomaji": [
              "na",
              "i",
              "ta",
              "yoru",
              "wo",
              "wasu",
              "re",
              "zu",
              "ni"
            ]
          },
          {
            "ja": "歩き出せば道になる",
            "romaji": "arukidasebamichininaru",
            "ko": "걸어나가면 그것이 길이 돼",
            "charRomaji": [
              "aru",
              "ki",
              "da",
              "se",
              "ba",
              "michi",
              "ni",
              "na",
              "ru"
            ]
          },
          {
            "ja": "掠れた声で紡いだメロディ",
            "romaji": "ryakuretakoedebouidamerodi",
            "ko": "쉰 목소리로 자아낸 멜로디",
            "charRomaji": [
              "ryaku",
              "re",
              "ta",
              "koe",
              "de",
              "bou",
              "i",
              "da",
              "me",
              "ro",
              "d",
              "i"
            ]
          },
          {
            "ja": "君に届くその日まで",
            "romaji": "kiminitodokusononichimade",
            "ko": "너에게 가닿을 그날까지",
            "charRomaji": [
              "kimi",
              "ni",
              "todo",
              "ku",
              "so",
              "no",
              "nichi",
              "ma",
              "de"
            ]
          },
          {
            "ja": "鳴らし続けろ僕らの衝動",
            "romaji": "narashitsuzukerobokuranoshoudou",
            "ko": "계속 울려 퍼뜨려라 우리들의 충동",
            "charRomaji": [
              "na",
              "ra",
              "shi",
              "tsuzu",
              "ke",
              "ro",
              "boku",
              "ra",
              "no",
              "shou",
              "dou"
            ]
          },
          {
            "ja": "決して消えない火を灯して",
            "romaji": "kesshitekienaihiwotomoshite",
            "ko": "결코 꺼지지 않는 불을 밝히며",
            "charRomaji": [
              "kes",
              "shi",
              "te",
              "ki",
              "e",
              "na",
              "i",
              "hi",
              "wo",
              "tomo",
              "shi",
              "te"
            ]
          },
          {
            "ja": "どんな明日が待っていても",
            "romaji": "donnaashitagamatteitemo",
            "ko": "어떤 내일이 기다리고 있더라도",
            "charRomaji": [
              "do",
              "n",
              "na",
              "a",
              "shita",
              "ga",
              "ma",
              "t",
              "te",
              "i",
              "te",
              "mo"
            ]
          },
          {
            "ja": "迷いながら共に行こう",
            "romaji": "mayoinagaratomoniikou",
            "ko": "방황하면서도 함께 나아가자",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ga",
              "ra",
              "tomo",
              "ni",
              "i",
              "ko",
              "u"
            ]
          },
          {
            "ja": "僕らの歌声響き渡る空へ",
            "romaji": "bokuranoutagoehibikiwatarusorahe",
            "ko": "우리들의 노랫소리 울려 퍼지는 하늘로",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "uta",
              "goe",
              "hibi",
              "ki",
              "wata",
              "ru",
              "sora",
              "he"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "haruhikage",
    "title": "春日影 (MyGO!!!!! ver.)",
    "reading": "はるひかげ",
    "category": "original",
    "album": "配信 Single (2023), 1st Album『迷跡波』",
    "youtubeId": "ZsvJUh03MwI",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "悴んだ心ふるえる眼差し",
            "romaji": "kajikandakokorofuruerumanazashi",
            "ko": "얼어붙은 마음, 떨리는 눈빛",
            "charRomaji": [
              "kajika",
              "n",
              "da",
              "kokoro",
              "fu",
              "ru",
              "e",
              "ru",
              "ma",
              "naza",
              "shi"
            ]
          },
          {
            "ja": "世界の中で僕はひとりぼっちだった",
            "romaji": "sekainonakadebokuhahitoribotchidatta",
            "ko": "세계 속에서 나는 외톨이였어",
            "charRomaji": [
              "se",
              "kai",
              "no",
              "naka",
              "de",
              "boku",
              "ha",
              "hi",
              "to",
              "ri",
              "bo",
              "t",
              "chi",
              "da",
              "t",
              "ta"
            ]
          },
          {
            "ja": "知っているのは春が枯れゆく季節だということ",
            "romaji": "shitteirunohaharugakareyukukisetsudatoiukoto",
            "ko": "알고 있는 건 봄이 저물어가는 계절이라는 것",
            "charRomaji": [
              "shi",
              "t",
              "te",
              "i",
              "ru",
              "no",
              "ha",
              "haru",
              "ga",
              "ka",
              "re",
              "yu",
              "ku",
              "ki",
              "setsu",
              "da",
              "to",
              "i",
              "u",
              "ko",
              "to"
            ]
          },
          {
            "ja": "私は毎年枯らしていった",
            "romaji": "watashiwamaitoshikarashiteitta",
            "ko": "나는 매년 시들게 해버렸지",
            "charRomaji": [
              "watashi",
              "wa",
              "ma",
              "itoshi",
              "ka",
              "ra",
              "shi",
              "te",
              "i",
              "t",
              "ta"
            ]
          },
          {
            "ja": "光が射す方へ一方通行の場所",
            "romaji": "hikarigasasuhouheippoutsuukounobasho",
            "ko": "빛이 비치는 곳을 향한 일방통행의 장소",
            "charRomaji": [
              "hikari",
              "ga",
              "sa",
              "su",
              "hou",
              "he",
              "i",
              "p",
              "po",
              "utsuukou",
              "no",
              "ba",
              "sho"
            ]
          },
          {
            "ja": "ただ言葉を紙に綴るだけ",
            "romaji": "tadakotobawokaminitsuzurudake",
            "ko": "그저 말을 종이에 엮어갈 뿐",
            "charRomaji": [
              "ta",
              "da",
              "ko",
              "toba",
              "wo",
              "kami",
              "ni",
              "tsuzu",
              "ru",
              "da",
              "ke"
            ]
          },
          {
            "ja": "虚しいと分かっていても",
            "romaji": "munashiitowakatteitemo",
            "ko": "허무하다는 것을 알면서도",
            "charRomaji": [
              "muna",
              "shi",
              "i",
              "to",
              "wa",
              "ka",
              "t",
              "te",
              "i",
              "te",
              "mo"
            ]
          },
          {
            "ja": "救いを探し続けていた",
            "romaji": "sukuiwosagashitsuzuketeita",
            "ko": "구원을 계속 찾아 헤매었어",
            "charRomaji": [
              "suku",
              "i",
              "wo",
              "saga",
              "shi",
              "tsuzu",
              "ke",
              "te",
              "i",
              "ta"
            ]
          },
          {
            "ja": "いまなら分かる気がする",
            "romaji": "imanarawakarukigasuru",
            "ko": "지금이라면 알 것만 같아",
            "charRomaji": [
              "i",
              "ma",
              "na",
              "ra",
              "wa",
              "ka",
              "ru",
              "ki",
              "ga",
              "su",
              "ru"
            ]
          },
          {
            "ja": "あの日泣けなかったのは私",
            "romaji": "anonichinakenakattanohawatashi",
            "ko": "그날 울지 못했던 건 바로 나였어",
            "charRomaji": [
              "a",
              "no",
              "nichi",
              "na",
              "ke",
              "na",
              "ka",
              "t",
              "ta",
              "no",
              "ha",
              "watashi"
            ]
          },
          {
            "ja": "光は優しく連れてゆく",
            "romaji": "hikariwayasashikutsureteyuku",
            "ko": "빛은 다정하게 나를 이끌어가",
            "charRomaji": [
              "hikari",
              "wa",
              "yasa",
              "shi",
              "ku",
              "tsu",
              "re",
              "te",
              "yu",
              "ku"
            ]
          },
          {
            "ja": "雲間にチラリチラリ",
            "romaji": "kumomanichirarichirari",
            "ko": "구름 사이로 얼핏얼핏",
            "charRomaji": [
              "kumo",
              "ma",
              "ni",
              "chi",
              "ra",
              "ri",
              "chi",
              "ra",
              "ri"
            ]
          },
          {
            "ja": "心満たされて溢れる",
            "romaji": "kokoromitasareteafureru",
            "ko": "마음이 가득 차서 흘러넘치네",
            "charRomaji": [
              "kokoro",
              "mi",
              "ta",
              "sa",
              "re",
              "te",
              "afu",
              "re",
              "ru"
            ]
          },
          {
            "ja": "いつしかホロリホロリ",
            "romaji": "itsushikahororihorori",
            "ko": "어느덧 눈물이 주르륵",
            "charRomaji": [
              "i",
              "tsu",
              "shi",
              "ka",
              "ho",
              "ro",
              "ri",
              "ho",
              "ro",
              "ri"
            ]
          },
          {
            "ja": "熱く熱く濡らしてゆく",
            "romaji": "atsukuatsukunurashiteyuku",
            "ko": "뜨겁게 뜨겁게 적셔가네",
            "charRomaji": [
              "atsu",
              "ku",
              "atsu",
              "ku",
              "nu",
              "ra",
              "shi",
              "te",
              "yu",
              "ku"
            ]
          },
          {
            "ja": "君の手はどうしてこんなにあたたかいの",
            "romaji": "kiminotehadoushitekonnaniatatakaino",
            "ko": "너의 손은 어째서 이렇게 따뜻한 걸까",
            "charRomaji": [
              "kimi",
              "no",
              "te",
              "ha",
              "do",
              "u",
              "shi",
              "te",
              "ko",
              "n",
              "na",
              "ni",
              "a",
              "ta",
              "ta",
              "ka",
              "i",
              "no"
            ]
          },
          {
            "ja": "ねえお願いこのまま離さないでいて",
            "romaji": "neeonegaikonomamahanasanaideite",
            "ko": "있잖아 부탁이야 이대로 놓지 말아줘",
            "charRomaji": [
              "ne",
              "e",
              "o",
              "nega",
              "i",
              "ko",
              "no",
              "ma",
              "ma",
              "hana",
              "sa",
              "na",
              "i",
              "de",
              "i",
              "te"
            ]
          },
          {
            "ja": "ずっとずっと離さないでいて",
            "romaji": "zuttozuttohanasanaideite",
            "ko": "영원히 영원히 놓지 말아줘",
            "charRomaji": [
              "zu",
              "t",
              "to",
              "zu",
              "t",
              "to",
              "hana",
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
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "解いては結んでほどけたり",
            "romaji": "toitehamusundehodoketari",
            "ko": "풀었다간 다시 묶고 풀어지며",
            "charRomaji": [
              "to",
              "i",
              "te",
              "ha",
              "musu",
              "n",
              "de",
              "ho",
              "do",
              "ke",
              "ta",
              "ri"
            ]
          },
          {
            "ja": "誰もがそれを喜び悲しみながら",
            "romaji": "daremogasorewoyorokobikanashiminagara",
            "ko": "누구나 그것을 기뻐하고 슬퍼하면서",
            "charRomaji": [
              "dare",
              "mo",
              "ga",
              "so",
              "re",
              "wo",
              "yoroko",
              "bi",
              "kana",
              "shi",
              "mi",
              "na",
              "ga",
              "ra"
            ]
          },
          {
            "ja": "愛を数えてゆく",
            "romaji": "aiwokazoeteyuku",
            "ko": "사랑을 헤아려 가네",
            "charRomaji": [
              "ai",
              "wo",
              "kazo",
              "e",
              "te",
              "yu",
              "ku"
            ]
          },
          {
            "ja": "鼓動を確かめるように",
            "romaji": "kodouwotashikameruyouni",
            "ko": "고동을 확인하듯이",
            "charRomaji": [
              "ko",
              "dou",
              "wo",
              "tashi",
              "ka",
              "me",
              "ru",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "いまなら分かる気がする",
            "romaji": "imanarawakarukigasuru",
            "ko": "지금이라면 알 것만 같아",
            "charRomaji": [
              "i",
              "ma",
              "na",
              "ra",
              "wa",
              "ka",
              "ru",
              "ki",
              "ga",
              "su",
              "ru"
            ]
          },
          {
            "ja": "あの日泣けなかったのは私",
            "romaji": "anonichinakenakattanohawatashi",
            "ko": "그날 울지 못했던 건 바로 나였어",
            "charRomaji": [
              "a",
              "no",
              "nichi",
              "na",
              "ke",
              "na",
              "ka",
              "t",
              "ta",
              "no",
              "ha",
              "watashi"
            ]
          },
          {
            "ja": "光は優しく抱きしめた",
            "romaji": "hikariwayasashikudakishimeta",
            "ko": "빛은 다정하게 나를 끌어안았지",
            "charRomaji": [
              "hikari",
              "wa",
              "yasa",
              "shi",
              "ku",
              "da",
              "ki",
              "shi",
              "me",
              "ta"
            ]
          },
          {
            "ja": "照らされた世界咲き誇る誰か",
            "romaji": "terasaretasekaisakihokorudareka",
            "ko": "빛이 비친 세상, 활짝 피어난 누군가",
            "charRomaji": [
              "te",
              "ra",
              "sa",
              "re",
              "ta",
              "se",
              "kai",
              "sa",
              "ki",
              "hoko",
              "ru",
              "dare",
              "ka"
            ]
          },
          {
            "ja": "あたたかさを知った春は私の為",
            "romaji": "atatakasawoshittaharuwawatashinotame",
            "ko": "따스함을 알게 된 봄은 나를 위한 것",
            "charRomaji": [
              "a",
              "ta",
              "ta",
              "ka",
              "sa",
              "wo",
              "shi",
              "t",
              "ta",
              "haru",
              "wa",
              "watashi",
              "no",
              "tame"
            ]
          },
          {
            "ja": "君の為涙を流すよ",
            "romaji": "kiminotamenamidawonagasuyo",
            "ko": "너를 위해 눈물을 흘릴게",
            "charRomaji": [
              "kimi",
              "no",
              "tame",
              "namidaw",
              "o",
              "naga",
              "su",
              "yo"
            ]
          },
          {
            "ja": "ああ眩しいのにな",
            "romaji": "aamabushiinonina",
            "ko": "아아 눈이 부신데도",
            "charRomaji": [
              "a",
              "a",
              "mabu",
              "shi",
              "i",
              "no",
              "ni",
              "na"
            ]
          },
          {
            "ja": "ああ苦しいのにな",
            "romaji": "aakurushiinonina",
            "ko": "아아 가슴이 아픈데도",
            "charRomaji": [
              "a",
              "a",
              "kuru",
              "shi",
              "i",
              "no",
              "ni",
              "na"
            ]
          },
          {
            "ja": "雲間にチラリチラリ",
            "romaji": "kumomanichirarichirari",
            "ko": "구름 사이로 얼핏얼핏",
            "charRomaji": [
              "kumo",
              "ma",
              "ni",
              "chi",
              "ra",
              "ri",
              "chi",
              "ra",
              "ri"
            ]
          },
          {
            "ja": "心満たされて溢れる",
            "romaji": "kokoromitasareteafureru",
            "ko": "마음이 가득 차서 흘러넘치네",
            "charRomaji": [
              "kokoro",
              "mi",
              "ta",
              "sa",
              "re",
              "te",
              "afu",
              "re",
              "ru"
            ]
          },
          {
            "ja": "いつしかホロリホロリ",
            "romaji": "itsushikahororihorori",
            "ko": "어느덧 눈물이 주르륵",
            "charRomaji": [
              "i",
              "tsu",
              "shi",
              "ka",
              "ho",
              "ro",
              "ri",
              "ho",
              "ro",
              "ri"
            ]
          },
          {
            "ja": "熱く熱く濡らしてゆく",
            "romaji": "atsukuatsukunurashiteyuku",
            "ko": "뜨겁게 뜨겁게 적셔가네",
            "charRomaji": [
              "atsu",
              "ku",
              "atsu",
              "ku",
              "nu",
              "ra",
              "shi",
              "te",
              "yu",
              "ku"
            ]
          },
          {
            "ja": "君の手はどうしてこんなにあたたかいの",
            "romaji": "kiminotehadoushitekonnaniatatakaino",
            "ko": "너의 손은 어째서 이렇게 따뜻한 걸까",
            "charRomaji": [
              "kimi",
              "no",
              "te",
              "ha",
              "do",
              "u",
              "shi",
              "te",
              "ko",
              "n",
              "na",
              "ni",
              "a",
              "ta",
              "ta",
              "ka",
              "i",
              "no"
            ]
          },
          {
            "ja": "ずっとずっと離さないでいて",
            "romaji": "zuttozuttohanasanaideite",
            "ko": "영원히 영원히 놓지 말아줘",
            "charRomaji": [
              "zu",
              "t",
              "to",
              "zu",
              "t",
              "to",
              "hana",
              "sa",
              "na",
              "i",
              "de",
              "i",
              "te"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "utakotoba",
    "title": "詩超絆",
    "reading": "うたことば",
    "category": "original",
    "album": "1st Album『迷跡波』",
    "youtubeId": "wJ-OebTVyvk",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "僕にはわからないんだいつもみつけられない",
            "romaji": "bokunihawakaranaindaitsumomitsukerarenai",
            "ko": "나에게는 알 수가 없어, 언제나 찾아낼 수 없어",
            "charRomaji": [
              "boku",
              "ni",
              "ha",
              "wa",
              "ka",
              "ra",
              "na",
              "i",
              "n",
              "da",
              "i",
              "tsu",
              "mo",
              "mi",
              "tsu",
              "ke",
              "ra",
              "re",
              "na",
              "i"
            ]
          },
          {
            "ja": "正解も普通も世界はずっとずっとずっと遠く",
            "romaji": "seikaimofutsuumosekaihazuttozuttozuttotooku",
            "ko": "정답도, 평범함도, 세상은 언제나 아득히 먼",
            "charRomaji": [
              "sei",
              "kai",
              "mo",
              "fu",
              "tsuu",
              "mo",
              "se",
              "kai",
              "ha",
              "zu",
              "t",
              "to",
              "zu",
              "t",
              "to",
              "zu",
              "t",
              "to",
              "too",
              "ku"
            ]
          },
          {
            "ja": "僕には届かない場所にあるんだ",
            "romaji": "bokunihatodokanaibashoniarunda",
            "ko": "나에게는 닿지 않는 곳에 있는 거야",
            "charRomaji": [
              "boku",
              "ni",
              "ha",
              "todo",
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
            "ja": "ひだまりを抱きしめていた春も",
            "romaji": "hidamariwodakishimeteitaharumo",
            "ko": "양지를 끌어안고 있었던 봄도",
            "charRomaji": [
              "hi",
              "da",
              "ma",
              "ri",
              "wo",
              "da",
              "ki",
              "shi",
              "me",
              "te",
              "i",
              "ta",
              "haru",
              "mo"
            ]
          },
          {
            "ja": "夏が照らしすぎて消えてしまいそうで",
            "romaji": "natsugaterashisugitekieteshimaisoude",
            "ko": "여름이 너무 뜨겁게 비춰서 사라져버릴 것만 같아서",
            "charRomaji": [
              "natsu",
              "ga",
              "te",
              "ra",
              "shi",
              "su",
              "gi",
              "te",
              "ki",
              "e",
              "te",
              "shi",
              "ma",
              "i",
              "so",
              "u",
              "de"
            ]
          },
          {
            "ja": "アスファルトで干からびてしまうなら",
            "romaji": "asufarutodekankarabiteshimaunara",
            "ko": "아스팔트 위에서 바싹 말라버릴 바에야",
            "charRomaji": [
              "a",
              "su",
              "f",
              "a",
              "ru",
              "to",
              "de",
              "kan",
              "ka",
              "ra",
              "bi",
              "te",
              "shi",
              "ma",
              "u",
              "na",
              "ra"
            ]
          },
          {
            "ja": "僕はずっと石の下に隠れていたかった",
            "romaji": "bokuhazuttoishinoshitanikakureteitakatta",
            "ko": "나는 차라리 돌멩이 밑에 숨어있고 싶었어",
            "charRomaji": [
              "boku",
              "ha",
              "zu",
              "t",
              "to",
              "ishi",
              "no",
              "shita",
              "ni",
              "kaku",
              "re",
              "te",
              "i",
              "ta",
              "ka",
              "t",
              "ta"
            ]
          },
          {
            "ja": "再び僕が壊してしまったんだ",
            "romaji": "futatabibokugakowashiteshimattanda",
            "ko": "다시 또 내가 부숴버리고 말았어",
            "charRomaji": [
              "futata",
              "bi",
              "boku",
              "ga",
              "kowa",
              "shi",
              "te",
              "shi",
              "ma",
              "t",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "失いたくなくて忘れたくなくて",
            "romaji": "ushinaitakunakutewasuretakunakute",
            "ko": "잃고 싶지 않아서, 잊어버리고 싶지 않아서",
            "charRomaji": [
              "ushina",
              "i",
              "ta",
              "ku",
              "na",
              "ku",
              "te",
              "wasu",
              "re",
              "ta",
              "ku",
              "na",
              "ku",
              "te"
            ]
          },
          {
            "ja": "なのに力なく手を離してしまった",
            "romaji": "nanonichikaranakutewohanashiteshimatta",
            "ko": "그런데도 힘없이 손을 놓아버리고 말았지",
            "charRomaji": [
              "na",
              "no",
              "ni",
              "chikara",
              "na",
              "ku",
              "te",
              "wo",
              "hana",
              "shi",
              "te",
              "shi",
              "ma",
              "t",
              "ta"
            ]
          },
          {
            "ja": "戻りたい伝えたい許されるなら僕はあきらめたくない",
            "romaji": "modoritaitsutaetaiyurusarerunarabokuhaakirametakunai",
            "ko": "돌아가고 싶어, 전하고 싶어, 용서받을 수 있다면 포기하고 싶지 않아",
            "charRomaji": [
              "modo",
              "ri",
              "ta",
              "i",
              "tsuta",
              "e",
              "ta",
              "i",
              "yuru",
              "sa",
              "re",
              "ru",
              "na",
              "ra",
              "boku",
              "ha",
              "a",
              "ki",
              "ra",
              "me",
              "ta",
              "ku",
              "na",
              "i"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "誰にも見つけてほしくなかった",
            "romaji": "darenimomitsuketehoshikunakatta",
            "ko": "누구에게도 들키고 싶지 않았어",
            "charRomaji": [
              "dare",
              "ni",
              "mo",
              "mi",
              "tsu",
              "ke",
              "te",
              "ho",
              "shi",
              "ku",
              "na",
              "ka",
              "t",
              "ta"
            ]
          },
          {
            "ja": "なのに君といることがどんなに嬉しかったかも",
            "romaji": "nanonikimitoirukotogadonnaniureshikattakamo",
            "ko": "그런데도 너와 함께 있는 것이 얼마나 기뻤는지도",
            "charRomaji": [
              "na",
              "no",
              "ni",
              "kimi",
              "to",
              "i",
              "ru",
              "ko",
              "to",
              "ga",
              "do",
              "n",
              "na",
              "ni",
              "ure",
              "shi",
              "ka",
              "t",
              "ta",
              "ka",
              "mo"
            ]
          },
          {
            "ja": "まだちゃんと言えてないから",
            "romaji": "madachantoietenaikara",
            "ko": "아직 제대로 전하지 못했으니까",
            "charRomaji": [
              "ma",
              "da",
              "ch",
              "a",
              "n",
              "to",
              "i",
              "e",
              "te",
              "na",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "だから傷つけたくなんかなかった",
            "romaji": "dakarakizutsuketakunankanakatta",
            "ko": "그러니까 상처 주고 싶지는 않았어",
            "charRomaji": [
              "da",
              "ka",
              "ra",
              "kizu",
              "tsu",
              "ke",
              "ta",
              "ku",
              "na",
              "n",
              "ka",
              "na",
              "ka",
              "t",
              "ta"
            ]
          },
          {
            "ja": "こんなふうに離れたくなかった",
            "romaji": "konnafuunihanaretakunakatta",
            "ko": "이런 식으로 헤어지고 싶지는 않았단 말이야",
            "charRomaji": [
              "ko",
              "n",
              "na",
              "fu",
              "u",
              "ni",
              "hana",
              "re",
              "ta",
              "ku",
              "na",
              "ka",
              "t",
              "ta"
            ]
          },
          {
            "ja": "上手く言えなかった言葉それでも届けたい言葉",
            "romaji": "umakuienakattakotobasoredemotodoketaikotoba",
            "ko": "서툴러서 말하지 못했던 말, 그래도 전하고 싶은 말",
            "charRomaji": [
              "u",
              "ma",
              "ku",
              "i",
              "e",
              "na",
              "ka",
              "t",
              "ta",
              "ko",
              "toba",
              "so",
              "re",
              "de",
              "mo",
              "todo",
              "ke",
              "ta",
              "i",
              "ko",
              "toba"
            ]
          },
          {
            "ja": "うたううたうたう今ああ届いて君の胸に",
            "romaji": "utauutautauimaaatodoitekiminomuneni",
            "ko": "노래를 불러, 지금 아아 닿기를 너의 가슴에",
            "charRomaji": [
              "u",
              "ta",
              "u",
              "u",
              "ta",
              "u",
              "ta",
              "u",
              "ima",
              "a",
              "a",
              "todo",
              "i",
              "te",
              "kimi",
              "no",
              "mune",
              "ni"
            ]
          },
          {
            "ja": "まだ間に合うかいこころを叫ぶ言葉を超えるため",
            "romaji": "madamaniaukaikokorowosakebukotobawokoerutame",
            "ko": "아직 늦지 않았을까, 마음을 외치는 말을 뛰어넘기 위해",
            "charRomaji": [
              "ma",
              "da",
              "ma",
              "ni",
              "a",
              "u",
              "ka",
              "i",
              "ko",
              "ko",
              "ro",
              "wo",
              "sake",
              "bu",
              "ko",
              "toba",
              "wo",
              "ko",
              "e",
              "ru",
              "ta",
              "me"
            ]
          },
          {
            "ja": "君に届くまでうたう",
            "romaji": "kiminitodokumadeutau",
            "ko": "너에게 닿을 때까지 노래할게",
            "charRomaji": [
              "kimi",
              "ni",
              "todo",
              "ku",
              "ma",
              "de",
              "u",
              "ta",
              "u"
            ]
          },
          {
            "ja": "一緒に泣きたいよ一緒に笑いたいよ",
            "romaji": "isshoninakitaiyoisshoniwaraitaiyo",
            "ko": "함께 울고 싶어, 함께 웃고 싶어",
            "charRomaji": [
              "i",
              "ssho",
              "ni",
              "na",
              "ki",
              "ta",
              "i",
              "yo",
              "i",
              "ssho",
              "ni",
              "wara",
              "i",
              "ta",
              "i",
              "yo"
            ]
          },
          {
            "ja": "僕らの道が平行線だとしても痛いほど伝わるから",
            "romaji": "bokuranomichigaheikousendatoshitemoitaihodotsutawarukara",
            "ko": "우리의 길이 영원히 평행선일지라도 아플 만큼 전해지니까",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "michi",
              "ga",
              "he",
              "ikou",
              "sen",
              "da",
              "to",
              "shi",
              "te",
              "mo",
              "ita",
              "i",
              "ho",
              "do",
              "tsuta",
              "wa",
              "ru",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "うたう手と手をつなぐうたずっと一緒にいよう",
            "romaji": "utautetotewotsunaguutazuttoisshoniiyou",
            "ko": "노래해, 손과 손을 마주 잡는 노래, 언제까지나 함께 있자",
            "charRomaji": [
              "u",
              "ta",
              "u",
              "te",
              "to",
              "te",
              "wo",
              "tsu",
              "na",
              "gu",
              "u",
              "ta",
              "zu",
              "t",
              "to",
              "i",
              "ssho",
              "ni",
              "i",
              "yo",
              "u"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "meirohibi",
    "title": "迷路日々",
    "reading": "めいろひび",
    "category": "original",
    "album": "1st Album『迷跡波』",
    "youtubeId": "STgVa-reZkM",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "迷いながら戸惑いながら歩く",
            "romaji": "mayoinagaratomadoinagaraaruku",
            "ko": "헤매면서도, 당황하면서도 걸어가",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ga",
              "ra",
              "to",
              "mado",
              "i",
              "na",
              "ga",
              "ra",
              "aru",
              "ku"
            ]
          },
          {
            "ja": "めいろの中で僕らは居合わせてた",
            "romaji": "meirononakadebokurawaiawaseteta",
            "ko": "미로 속에서 우리들은 우연히 마주쳤어",
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
            "ko": "이름 없는 감정을 아아 끌어안고 있어",
            "charRomaji": [
              "na",
              "mae",
              "no",
              "na",
              "i",
              "kan",
              "jou",
              "a",
              "a",
              "da",
              "ki",
              "shi",
              "me",
              "te",
              "ru"
            ]
          },
          {
            "ja": "ちいさな一瞬集めたい",
            "romaji": "chiisanaisshunatsumetai",
            "ko": "작은 한순간들을 모으고 싶어",
            "charRomaji": [
              "chi",
              "i",
              "sa",
              "na",
              "is",
              "shun",
              "atsu",
              "me",
              "ta",
              "i"
            ]
          },
          {
            "ja": "こぼれ落ちた街の隅で震えていた昨日も",
            "romaji": "koboreochitamachinosumidefurueteitakinoumo",
            "ko": "흘러떨어진 거리 한구석에서 떨고 있던 어제도",
            "charRomaji": [
              "ko",
              "bo",
              "re",
              "o",
              "chi",
              "ta",
              "machi",
              "no",
              "sumi",
              "de",
              "furu",
              "e",
              "te",
              "i",
              "ta",
              "ki",
              "nou",
              "mo"
            ]
          },
          {
            "ja": "ちっぽけだって隠さないでいたいよ",
            "romaji": "chippokedattekakusanaideitaiyo",
            "ko": "하찮다고 해서 숨기지 않고 있고 싶어",
            "charRomaji": [
              "chi",
              "p",
              "po",
              "ke",
              "da",
              "t",
              "te",
              "kaku",
              "sa",
              "na",
              "i",
              "de",
              "i",
              "ta",
              "i",
              "yo"
            ]
          },
          {
            "ja": "はみ出したまま不揃いな僕らでも",
            "romaji": "hamidashitamamafuzoroinabokurademo",
            "ko": "삐져나온 채 제각각인 우리들이라도",
            "charRomaji": [
              "ha",
              "mi",
              "da",
              "shi",
              "ta",
              "ma",
              "ma",
              "fu",
              "zoro",
              "i",
              "na",
              "boku",
              "ra",
              "de",
              "mo"
            ]
          },
          {
            "ja": "いびつな言葉でずれてはすれ違ってさ",
            "romaji": "ibitsunakotobadezuretehasurechigattesa",
            "ko": "일그러진 말로 어긋나고 엇갈리면서",
            "charRomaji": [
              "i",
              "bi",
              "tsu",
              "na",
              "ko",
              "toba",
              "de",
              "zu",
              "re",
              "te",
              "ha",
              "su",
              "re",
              "chiga",
              "t",
              "te",
              "sa"
            ]
          },
          {
            "ja": "傷つけたことに傷ついてる",
            "romaji": "kizutsuketakotonikizutsuiteru",
            "ko": "상처 준 사실에 스스로 상처 입고 있어",
            "charRomaji": [
              "kizu",
              "tsu",
              "ke",
              "ta",
              "ko",
              "to",
              "ni",
              "kizu",
              "tsu",
              "i",
              "te",
              "ru"
            ]
          },
          {
            "ja": "それでもこの手をほどかない",
            "romaji": "soredemokonotewohodokanai",
            "ko": "그럼에도 이 손을 놓지 않아",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "ko",
              "no",
              "te",
              "wo",
              "ho",
              "do",
              "ka",
              "na",
              "i"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "ひとりよがりあてもなくて机の中しまい込んでいた",
            "romaji": "hitoriyogariatemonakutetsukuenonakashimaikondeita",
            "ko": "독선적이고 정처 없이 책상 속에 처박아 두었던",
            "charRomaji": [
              "hi",
              "to",
              "ri",
              "yo",
              "ga",
              "ri",
              "a",
              "te",
              "mo",
              "na",
              "ku",
              "te",
              "tsukue",
              "no",
              "naka",
              "shi",
              "ma",
              "i",
              "ko",
              "n",
              "de",
              "i",
              "ta"
            ]
          },
          {
            "ja": "ぐるぐる止まらないくよくよとめどない",
            "romaji": "gurugurutomaranaikuyokuyotomedonai",
            "ko": "빙글빙글 멈추지 않아, 끙끙대며 끝이 없어",
            "charRomaji": [
              "gu",
              "ru",
              "gu",
              "ru",
              "to",
              "ma",
              "ra",
              "na",
              "i",
              "ku",
              "yo",
              "ku",
              "yo",
              "to",
              "me",
              "do",
              "na",
              "i"
            ]
          },
          {
            "ja": "隠れて怯える欠片と僕はここで歌うよ",
            "romaji": "kakureteobierukakeratobokuhakokodeutauyo",
            "ko": "숨어서 겁먹은 조각들과 나는 여기서 노래할게",
            "charRomaji": [
              "kaku",
              "re",
              "te",
              "obi",
              "e",
              "ru",
              "ka",
              "kera",
              "to",
              "boku",
              "ha",
              "ko",
              "ko",
              "de",
              "uta",
              "u",
              "yo"
            ]
          },
          {
            "ja": "僕の中で蠢いていた熱が音に放たれ",
            "romaji": "bokunonakadeshuniteitanetsugaotonihouttare",
            "ko": "내 안에서 꿈틀거리던 열기가 소리로 해방되어",
            "charRomaji": [
              "boku",
              "no",
              "naka",
              "de",
              "shun",
              "i",
              "te",
              "i",
              "ta",
              "netsu",
              "ga",
              "oto",
              "ni",
              "hout",
              "ta",
              "re"
            ]
          },
          {
            "ja": "おぼつかない小声で叫びだした",
            "romaji": "obotsukanaikogoedesakebidashita",
            "ko": "불안한 작은 목소리로 외치기 시작했어",
            "charRomaji": [
              "o",
              "bo",
              "tsu",
              "ka",
              "na",
              "i",
              "ko",
              "goe",
              "de",
              "sake",
              "bi",
              "da",
              "shi",
              "ta"
            ]
          },
          {
            "ja": "迷子のまま曲がりくねった道でも",
            "romaji": "maigonomamamagarikunettamichidemo",
            "ko": "미아인 채로 구불구불 굽어진 길이라도",
            "charRomaji": [
              "ma",
              "igo",
              "no",
              "ma",
              "ma",
              "ma",
              "ga",
              "ri",
              "ku",
              "ne",
              "t",
              "ta",
              "michi",
              "de",
              "mo"
            ]
          },
          {
            "ja": "諦めなかった僕らのしるしだから",
            "romaji": "akiramenakattabokuranoshirushidakara",
            "ko": "포기하지 않았던 우리들의 증표이니까",
            "charRomaji": [
              "akira",
              "me",
              "na",
              "ka",
              "t",
              "ta",
              "boku",
              "ra",
              "no",
              "shi",
              "ru",
              "shi",
              "da",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "胸の中ああ羽ばたく時を待ってる",
            "romaji": "munenonakaaahanebatakutokiwomatteru",
            "ko": "가슴속에서 아아 날갯짓할 때를 기다리고 있어",
            "charRomaji": [
              "mune",
              "no",
              "naka",
              "a",
              "a",
              "hane",
              "ba",
              "ta",
              "ku",
              "toki",
              "wo",
              "ma",
              "t",
              "te",
              "ru"
            ]
          },
          {
            "ja": "隣で一緒に奏でたいよ迷っても一生離れない",
            "romaji": "tonarideisshonikanadetaiyomayottemoisshouhanarenai",
            "ko": "곁에서 함께 연주하고 싶어, 헤맨대도 평생 떨어지지 않아",
            "charRomaji": [
              "tonari",
              "de",
              "i",
              "ssho",
              "ni",
              "kana",
              "de",
              "ta",
              "i",
              "yo",
              "mayo",
              "t",
              "te",
              "mo",
              "i",
              "sshou",
              "hana",
              "re",
              "na",
              "i"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "noroshi",
    "title": "無路矢",
    "reading": "のろし",
    "category": "original",
    "album": "Digital Single (2023), 1st Album『迷跡波』",
    "youtubeId": "s3BTDeNKufQ",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "無軌道を描く足跡でも進み続けた",
            "romaji": "mukidouwoegakusokusekidemosusumitsuzuketa",
            "ko": "궤도 없는 발자국일지라도 계속 나아갔어",
            "charRomaji": [
              "mu",
              "ki",
              "dou",
              "wo",
              "ega",
              "ku",
              "so",
              "kuseki",
              "de",
              "mo",
              "susu",
              "mi",
              "tsuzu",
              "ke",
              "ta"
            ]
          },
          {
            "ja": "ほつれそうな心でどこから来てどこに向かう",
            "romaji": "hotsuresounakokorodedokokarakitedokonimukau",
            "ko": "풀려버릴 것 같은 마음으로 어디서 와서 어디로 향하나",
            "charRomaji": [
              "ho",
              "tsu",
              "re",
              "so",
              "u",
              "na",
              "kokoro",
              "de",
              "do",
              "ko",
              "ka",
              "ra",
              "ki",
              "te",
              "do",
              "ko",
              "ni",
              "mu",
              "ka",
              "u"
            ]
          },
          {
            "ja": "何を信じて生きていくの道標も地図もなくて",
            "romaji": "naniwoshinjiteikiteikunodouhyoumochizumonakute",
            "ko": "무엇을 믿고 살아가는가, 이정표도 지도도 없이",
            "charRomaji": [
              "nani",
              "wo",
              "shin",
              "ji",
              "te",
              "i",
              "ki",
              "te",
              "i",
              "ku",
              "no",
              "do",
              "uhyou",
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
            "ja": "フラつく足で生まれた星にいるはずなのに何故か",
            "romaji": "furatsukuashideumaretahoshiniiruhazunanoninazeka",
            "ko": "휘청이는 발로, 태어난 별에 분명 있을 텐데 어째서인지",
            "charRomaji": [
              "fu",
              "ra",
              "tsu",
              "ku",
              "ashi",
              "de",
              "u",
              "ma",
              "re",
              "ta",
              "hoshi",
              "ni",
              "i",
              "ru",
              "ha",
              "zu",
              "na",
              "no",
              "ni",
              "na",
              "ze",
              "ka"
            ]
          },
          {
            "ja": "本当は僕だけが違う星から来たみたいなんだ",
            "romaji": "hontouwabokudakegachigauhoshikarakitamitainanda",
            "ko": "사실은 나만이 다른 별에서 온 것만 같아",
            "charRomaji": [
              "hon",
              "tou",
              "wa",
              "boku",
              "da",
              "ke",
              "ga",
              "chiga",
              "u",
              "hoshi",
              "ka",
              "ra",
              "ki",
              "ta",
              "mi",
              "ta",
              "i",
              "na",
              "n",
              "da"
            ]
          },
          {
            "ja": "途切れそうな言葉でも繋いでほしいその音で",
            "romaji": "togiresounakotobademotsunaidehoshiisonootode",
            "ko": "끊어질 것 같은 말이라도 이어주길 바라, 그 소리로",
            "charRomaji": [
              "to",
              "gi",
              "re",
              "so",
              "u",
              "na",
              "ko",
              "toba",
              "de",
              "mo",
              "tsuna",
              "i",
              "de",
              "ho",
              "shi",
              "i",
              "so",
              "no",
              "oto",
              "de"
            ]
          },
          {
            "ja": "羅列を刻む言葉たちがジリジリ焦げる",
            "romaji": "raretsuwokizamukotobatachigajirijirikogeru",
            "ko": "나열을 새기는 말들이 바짝바짝 타들어가",
            "charRomaji": [
              "ra",
              "retsu",
              "wo",
              "kiza",
              "mu",
              "ko",
              "toba",
              "ta",
              "chi",
              "ga",
              "ji",
              "ri",
              "ji",
              "ri",
              "ko",
              "ge",
              "ru"
            ]
          },
          {
            "ja": "紙を擦る熱が狼煙になるここにいると",
            "romaji": "kamiwosurunetsuganoroshininarukokoniiruto",
            "ko": "종이를 문지르는 열기가 봉화가 된다, 여기에 있다고",
            "charRomaji": [
              "kami",
              "wo",
              "su",
              "ru",
              "netsu",
              "ga",
              "no",
              "roshi",
              "ni",
              "na",
              "ru",
              "ko",
              "ko",
              "ni",
              "i",
              "ru",
              "to"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "空へ高くのぼってく荒野に立つ雛のように",
            "romaji": "sorahetakakunobottekukouyanitatsuhinanoyouni",
            "ko": "하늘 높이 피어올라가, 황야에 선 새끼 새처럼",
            "charRomaji": [
              "sora",
              "he",
              "taka",
              "ku",
              "no",
              "bo",
              "t",
              "te",
              "ku",
              "ko",
              "uya",
              "ni",
              "ta",
              "tsu",
              "hina",
              "no",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "胸震わせて生まれた星だけ同じだった",
            "romaji": "muneshinwaseteumaretahoshidakeonajidatta",
            "ko": "가슴을 떨며, 태어난 별만이 같았을 뿐인",
            "charRomaji": [
              "mune",
              "shin",
              "wa",
              "se",
              "te",
              "u",
              "ma",
              "re",
              "ta",
              "hoshi",
              "da",
              "ke",
              "ona",
              "ji",
              "da",
              "t",
              "ta"
            ]
          },
          {
            "ja": "僕と君なのに叫びたい想いが重なる",
            "romaji": "bokutokiminanonisakebitaiomoigakasanaru",
            "ko": "나와 너인데도 외치고 싶은 마음이 겹쳐져",
            "charRomaji": [
              "boku",
              "to",
              "kimi",
              "na",
              "no",
              "ni",
              "sake",
              "bi",
              "ta",
              "i",
              "omo",
              "i",
              "ga",
              "kasa",
              "na",
              "ru"
            ]
          },
          {
            "ja": "世界が僕らを拒んだとしても",
            "romaji": "sekaigabokurawokyondatoshitemo",
            "ko": "세상이 우리를 거부한다 할지라도",
            "charRomaji": [
              "se",
              "kai",
              "ga",
              "boku",
              "ra",
              "wo",
              "kyo",
              "n",
              "da",
              "to",
              "shi",
              "te",
              "mo"
            ]
          },
          {
            "ja": "この音だけは嘘をつかない",
            "romaji": "konootodakehausowotsukanai",
            "ko": "이 소리만은 결코 거짓말을 하지 않아",
            "charRomaji": [
              "ko",
              "no",
              "oto",
              "da",
              "ke",
              "ha",
              "uso",
              "wo",
              "tsu",
              "ka",
              "na",
              "i"
            ]
          },
          {
            "ja": "狼煙を上げろ暗闇を切り裂くように",
            "romaji": "noroshiwoagerokurayamiwokirisakuyouni",
            "ko": "봉화를 올려라, 칠흑 같은 어둠을 가르듯이",
            "charRomaji": [
              "no",
              "roshi",
              "wo",
              "a",
              "ge",
              "ro",
              "kura",
              "yami",
              "wo",
              "ki",
              "ri",
              "sa",
              "ku",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "迷いながら僕らは此処に立っている",
            "romaji": "mayoinagarabokurawakokonitatteiru",
            "ko": "헤매면서도 우리들은 이곳에 서 있다",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ga",
              "ra",
              "boku",
              "ra",
              "wa",
              "ko",
              "ko",
              "ni",
              "ta",
              "t",
              "te",
              "i",
              "ru"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "sasunso",
    "title": "砂寸奏",
    "reading": "さすらい",
    "category": "original",
    "album": "4th Single『砂寸奏』, 2nd Album『跡暖空』",
    "youtubeId": "uiWLU577gYY",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "同じ音符を追いかけるのに昨日とは何かが違うみたいだ",
            "romaji": "onajionpuwooikakerunonikinoutohananikagachigaumitaida",
            "ko": "같은 음표를 쫓아가는데도 어제와는 무언가 다른 것만 같아",
            "charRomaji": [
              "ona",
              "ji",
              "o",
              "npu",
              "wo",
              "o",
              "i",
              "ka",
              "ke",
              "ru",
              "no",
              "ni",
              "ki",
              "nou",
              "to",
              "ha",
              "nani",
              "ka",
              "ga",
              "chiga",
              "u",
              "mi",
              "ta",
              "i",
              "da"
            ]
          },
          {
            "ja": "止まらないよね砂時計サラサラこぼれ落ちてく",
            "romaji": "tomaranaiyonesunadokeisarasarakoboreochiteku",
            "ko": "멈추지 않네 모래시계, 사르르 흘러떨어져 가",
            "charRomaji": [
              "to",
              "ma",
              "ra",
              "na",
              "i",
              "yo",
              "ne",
              "suna",
              "do",
              "kei",
              "sa",
              "ra",
              "sa",
              "ra",
              "ko",
              "bo",
              "re",
              "o",
              "chi",
              "te",
              "ku"
            ]
          },
          {
            "ja": "一秒前の僕はもういない彷徨する渇望",
            "romaji": "ichibyoumaenobokuhamouinaisamayosurukatsubou",
            "ko": "1초 전의 나는 이미 없어, 방황하는 갈망",
            "charRomaji": [
              "ichi",
              "byou",
              "mae",
              "no",
              "boku",
              "ha",
              "mo",
              "u",
              "i",
              "na",
              "i",
              "sama",
              "yo",
              "su",
              "ru",
              "katsu",
              "bou"
            ]
          },
          {
            "ja": "もう止めないでいいよねたった今今にしかさわれない",
            "romaji": "moutomenaideiiyonetattaimaimanishikasawarenai",
            "ko": "이제 멈추지 않아도 괜찮지, 오직 지금, 지금에만 손닿을 수 있어",
            "charRomaji": [
              "mo",
              "u",
              "to",
              "me",
              "na",
              "i",
              "de",
              "i",
              "i",
              "yo",
              "ne",
              "ta",
              "t",
              "ta",
              "ima",
              "ima",
              "ni",
              "shi",
              "ka",
              "sa",
              "wa",
              "re",
              "na",
              "i"
            ]
          },
          {
            "ja": "ぐるりの音君と持ち寄ったこの鼓動が現在地",
            "romaji": "gururinootokimitomochiyottakonokodougagenzaichi",
            "ko": "에워싼 소리, 너와 함께 가져온 이 고동이 바로 현재 위치",
            "charRomaji": [
              "gu",
              "ru",
              "ri",
              "no",
              "oto",
              "kimi",
              "to",
              "mo",
              "chi",
              "yo",
              "t",
              "ta",
              "ko",
              "no",
              "ko",
              "dou",
              "ga",
              "gen",
              "zai",
              "chi"
            ]
          },
          {
            "ja": "揺らせ旅人のようにうたからうたへ",
            "romaji": "yurasetabibitonoyouniutakarautahe",
            "ko": "흔들어라, 여행자처럼 노래에서 노래로",
            "charRomaji": [
              "yu",
              "ra",
              "se",
              "tabi",
              "bito",
              "no",
              "yo",
              "u",
              "ni",
              "u",
              "ta",
              "ka",
              "ra",
              "u",
              "ta",
              "he"
            ]
          },
          {
            "ja": "乾いた喉が掠れる声が絞り出してた咆哮",
            "romaji": "kawaitanodogakasurerukoegashiboridashitetahoukou",
            "ko": "메마른 목이, 쉰 목소리가 쥐어짜 내던 포효",
            "charRomaji": [
              "kawa",
              "i",
              "ta",
              "nodo",
              "ga",
              "kasu",
              "re",
              "ru",
              "koe",
              "ga",
              "shibo",
              "ri",
              "da",
              "shi",
              "te",
              "ta",
              "hou",
              "kou"
            ]
          },
          {
            "ja": "この身に刻む方向感覚見失う",
            "romaji": "konominikizamuhoukoukankakumiushinau",
            "ko": "이 몸에 깊이 새기며 방향 감각을 잃어버리네",
            "charRomaji": [
              "ko",
              "no",
              "mi",
              "ni",
              "kiza",
              "mu",
              "hou",
              "kou",
              "kan",
              "kaku",
              "mi",
              "ushina",
              "u"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "さかさま宇宙に転がって手を伸ばしたものはなんだった",
            "romaji": "sakasamauchuunikorogattetewonobashitamonohanandatta",
            "ko": "거꾸로 우주 위로 굴러떨어져 손을 뻗었던 것은 대체 무엇이었나",
            "charRomaji": [
              "sa",
              "ka",
              "sa",
              "ma",
              "u",
              "chuu",
              "ni",
              "koro",
              "ga",
              "t",
              "te",
              "te",
              "wo",
              "no",
              "ba",
              "shi",
              "ta",
              "mo",
              "no",
              "ha",
              "na",
              "n",
              "da",
              "t",
              "ta"
            ]
          },
          {
            "ja": "過去も未来も見えないくらいたった今今にしか叫べない",
            "romaji": "kakomomiraimomienaikuraitattaimaimanishikasakebenai",
            "ko": "과거도 미래도 보이지 않을 만큼, 오직 지금, 지금에만 외칠 수 있어",
            "charRomaji": [
              "ka",
              "ko",
              "mo",
              "mi",
              "rai",
              "mo",
              "mi",
              "e",
              "na",
              "i",
              "ku",
              "ra",
              "i",
              "ta",
              "t",
              "ta",
              "ima",
              "ima",
              "ni",
              "shi",
              "ka",
              "sake",
              "be",
              "na",
              "i"
            ]
          },
          {
            "ja": "砂埃舞うステージの上僕らの砂寸奏",
            "romaji": "sunabokorimausuteejinouebokuranosunasunsou",
            "ko": "모래 먼지 휘날리는 무대 위, 우리들의 사스라이",
            "charRomaji": [
              "suna",
              "bokori",
              "ma",
              "u",
              "su",
              "tee",
              "",
              "ji",
              "no",
              "ue",
              "boku",
              "ra",
              "no",
              "suna",
              "sun",
              "sou"
            ]
          },
          {
            "ja": "流されるまま消えていく時間の中で",
            "romaji": "nagasarerumamakieteikujikannonakade",
            "ko": "흘러가는 대로 사라져 가는 시간 속에서",
            "charRomaji": [
              "naga",
              "sa",
              "re",
              "ru",
              "ma",
              "ma",
              "ki",
              "e",
              "te",
              "i",
              "ku",
              "ji",
              "kan",
              "no",
              "naka",
              "de"
            ]
          },
          {
            "ja": "立ち止まることさえ許されないなら",
            "romaji": "tachitomarukotosaeyurusarenainara",
            "ko": "멈춰 서는 것조차 용납되지 않는다면",
            "charRomaji": [
              "ta",
              "chi",
              "to",
              "ma",
              "ru",
              "ko",
              "to",
              "sa",
              "e",
              "yuru",
              "sa",
              "re",
              "na",
              "i",
              "na",
              "ra"
            ]
          },
          {
            "ja": "この瞬間を焼き尽くすように歌うだけ",
            "romaji": "konoshunkanwoyakitsukusuyouniutaudake",
            "ko": "이 순간을 전부 불태워버리듯 노래할 뿐",
            "charRomaji": [
              "ko",
              "no",
              "shun",
              "kan",
              "wo",
              "ya",
              "ki",
              "tsu",
              "ku",
              "su",
              "yo",
              "u",
              "ni",
              "uta",
              "u",
              "da",
              "ke"
            ]
          },
          {
            "ja": "迷子の足跡が道になるまで",
            "romaji": "maigonosokusekigamichininarumade",
            "ko": "미아의 발자국이 하나의 길이 될 때까지",
            "charRomaji": [
              "ma",
              "igo",
              "no",
              "so",
              "kuseki",
              "ga",
              "michi",
              "ni",
              "na",
              "ru",
              "ma",
              "de"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "kaisoufu",
    "title": "回層浮",
    "reading": "かいそうふ",
    "category": "original",
    "album": "4th Single『砂寸奏』c/w, 2nd Album『跡暖空』",
    "youtubeId": "k5u1nueXES8",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "水の底に沈んでいくように",
            "romaji": "mizunosokonishizundeikuyouni",
            "ko": "물 밑바닥으로 가라앉아 가듯이",
            "charRomaji": [
              "mizu",
              "no",
              "soko",
              "ni",
              "shizu",
              "n",
              "de",
              "i",
              "ku",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "音のない世界で息を潜めてた",
            "romaji": "otononaisekaideikiwohisometeta",
            "ko": "소리 없는 세상에서 숨을 죽이고 있었어",
            "charRomaji": [
              "oto",
              "no",
              "na",
              "i",
              "se",
              "kai",
              "de",
              "iki",
              "wo",
              "hiso",
              "me",
              "te",
              "ta"
            ]
          },
          {
            "ja": "浮き沈み繰り返す感情の波",
            "romaji": "ukishizumikurikaesukanjounonami",
            "ko": "뜨고 가라앉음을 되풀이하는 감정의 파도",
            "charRomaji": [
              "u",
              "ki",
              "shizu",
              "mi",
              "ku",
              "ri",
              "kae",
              "su",
              "kan",
              "jou",
              "no",
              "nami"
            ]
          },
          {
            "ja": "どこへ流されてゆくのかも知らずに",
            "romaji": "dokohenagasareteyukunokamoshirazuni",
            "ko": "어디로 휩쓸려 가는지도 모른 채",
            "charRomaji": [
              "do",
              "ko",
              "he",
              "naga",
              "sa",
              "re",
              "te",
              "yu",
              "ku",
              "no",
              "ka",
              "mo",
              "shi",
              "ra",
              "zu",
              "ni"
            ]
          },
          {
            "ja": "光の届かない深い階層で",
            "romaji": "hikarinotodokanaifukaikaisoude",
            "ko": "빛이 닿지 않는 깊은 계층에서",
            "charRomaji": [
              "hikari",
              "no",
              "todo",
              "ka",
              "na",
              "i",
              "fuka",
              "i",
              "kai",
              "sou",
              "de"
            ]
          },
          {
            "ja": "ずっと自分の輪郭を探していた",
            "romaji": "zuttojibunnorinkakuwosagashiteita",
            "ko": "줄곧 나의 윤곽을 찾아 헤매고 있었어",
            "charRomaji": [
              "zu",
              "t",
              "to",
              "ji",
              "bun",
              "no",
              "rin",
              "kaku",
              "wo",
              "saga",
              "shi",
              "te",
              "i",
              "ta"
            ]
          },
          {
            "ja": "泡のように消えてしまいそうな声",
            "romaji": "awanoyounikieteshimaisounakoe",
            "ko": "거품처럼 사라져버릴 것만 같은 목소리",
            "charRomaji": [
              "awa",
              "no",
              "yo",
              "u",
              "ni",
              "ki",
              "e",
              "te",
              "shi",
              "ma",
              "i",
              "so",
              "u",
              "na",
              "koe"
            ]
          },
          {
            "ja": "それでも叫びたかったんだ",
            "romaji": "soredemosakebitakattanda",
            "ko": "그럼에도 외치고 싶었어",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "sake",
              "bi",
              "ta",
              "ka",
              "t",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "冷たい水圧に押し潰されそうでも",
            "romaji": "tsumetaisuiatsunioshitsubusaresoudemo",
            "ko": "차가운 수압에 짓눌릴 것만 같아도",
            "charRomaji": [
              "tsume",
              "ta",
              "i",
              "sui",
              "atsu",
              "ni",
              "o",
              "shi",
              "tsubu",
              "sa",
              "re",
              "so",
              "u",
              "de",
              "mo"
            ]
          },
          {
            "ja": "僕の心は此処にある",
            "romaji": "bokunokokorohakokoniaru",
            "ko": "나의 마음은 이곳에 있어",
            "charRomaji": [
              "boku",
              "no",
              "kokoro",
              "ha",
              "ko",
              "ko",
              "ni",
              "a",
              "ru"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "幾重にも重なる想いの層を突き破り",
            "romaji": "ikuenimokasanaruomoinosouwotsukiyaburi",
            "ko": "겹겹이 포개진 마음의 층을 뚫고서",
            "charRomaji": [
              "i",
              "kue",
              "ni",
              "mo",
              "kasa",
              "na",
              "ru",
              "omo",
              "i",
              "no",
              "sou",
              "wo",
              "tsu",
              "ki",
              "yabu",
              "ri"
            ]
          },
          {
            "ja": "浮かび上がっていく水面を目指して",
            "romaji": "ukabiagatteikusuimenwomezashite",
            "ko": "떠올라가는 수면을 향해",
            "charRomaji": [
              "u",
              "ka",
              "bi",
              "a",
              "ga",
              "t",
              "te",
              "i",
              "ku",
              "sui",
              "men",
              "wo",
              "me",
              "za",
              "shi",
              "te"
            ]
          },
          {
            "ja": "冷たい水圧を振りほどくように",
            "romaji": "tsumetaisuiatsuwofurihodokuyouni",
            "ko": "차가운 수압을 뿌리치듯이",
            "charRomaji": [
              "tsume",
              "ta",
              "i",
              "sui",
              "atsu",
              "wo",
              "fu",
              "ri",
              "ho",
              "do",
              "ku",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "この手で明日を手繰り寄せる",
            "romaji": "konotedeashitawotaguriyoseru",
            "ko": "이 손으로 내일을 끌어당긴다",
            "charRomaji": [
              "ko",
              "no",
              "te",
              "de",
              "a",
              "shita",
              "wo",
              "ta",
              "gu",
              "ri",
              "yo",
              "se",
              "ru"
            ]
          },
          {
            "ja": "息を吸い込む瞬間の痛みが",
            "romaji": "ikiwosuikomushunkannoitamiga",
            "ko": "숨을 들이마시는 순간의 아픔이",
            "charRomaji": [
              "iki",
              "wo",
              "su",
              "i",
              "ko",
              "mu",
              "shun",
              "kan",
              "no",
              "ita",
              "mi",
              "ga"
            ]
          },
          {
            "ja": "生きている証だと教えてくれる",
            "romaji": "ikiteirushoudatooshietekureru",
            "ko": "살아있다는 증표라고 가르쳐줘",
            "charRomaji": [
              "i",
              "ki",
              "te",
              "i",
              "ru",
              "shou",
              "da",
              "to",
              "oshi",
              "e",
              "te",
              "ku",
              "re",
              "ru"
            ]
          },
          {
            "ja": "回層の果てに見つけた光",
            "romaji": "kaisounohatenimitsuketahikari",
            "ko": "회층의 끝에서 발견한 한 줄기 빛",
            "charRomaji": [
              "kai",
              "sou",
              "no",
              "ha",
              "te",
              "ni",
              "mi",
              "tsu",
              "ke",
              "ta",
              "hikari"
            ]
          },
          {
            "ja": "もう二度と離さないから",
            "romaji": "mounidotohanasanaikara",
            "ko": "이제 두 번 다시 놓지 않을 테니까",
            "charRomaji": [
              "mo",
              "u",
              "ni",
              "do",
              "to",
              "hana",
              "sa",
              "na",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "水面を突き破り叫ぶ僕らの歌",
            "romaji": "suimenwotsukiyaburisakebubokuranouta",
            "ko": "수면을 뚫고 부르짖는 우리들의 노래",
            "charRomaji": [
              "sui",
              "men",
              "wo",
              "tsu",
              "ki",
              "yabu",
              "ri",
              "sake",
              "bu",
              "boku",
              "ra",
              "no",
              "uta"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "shokyuusei",
    "title": "処救生",
    "reading": "こきゅう",
    "category": "original",
    "album": "4th Single『砂寸奏』c/w, 2nd Album『跡暖空』",
    "youtubeId": "1_XZ0VJIpwI",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "こたえあわせ丸とバツに埋もれ",
            "romaji": "kotaeawasemarutobatsuniumore",
            "ko": "정답 맞추기, 동그라미와 가위표에 파묻혀",
            "charRomaji": [
              "ko",
              "ta",
              "e",
              "a",
              "wa",
              "se",
              "maru",
              "to",
              "ba",
              "tsu",
              "ni",
              "u",
              "mo",
              "re"
            ]
          },
          {
            "ja": "四方八方出口のない夜にまみれ僕は独り",
            "romaji": "shihouhappoudeguchinonaiyorunimamirebokuhahitori",
            "ko": "사방팔방 출구 없는 밤에 짓눌려 나는 홀로 남아",
            "charRomaji": [
              "shi",
              "hou",
              "ha",
              "ppou",
              "de",
              "guchi",
              "no",
              "na",
              "i",
              "yoru",
              "ni",
              "ma",
              "mi",
              "re",
              "boku",
              "ha",
              "hito",
              "ri"
            ]
          },
          {
            "ja": "止まってしまうのが怖くて瞼閉じたまま走るみたいに",
            "romaji": "tomatteshimaunogakowakutemabutatojitamamahashirumitaini",
            "ko": "멈춰 서는 것이 두려워서 눈을 감은 채 달리는 것처럼",
            "charRomaji": [
              "to",
              "ma",
              "t",
              "te",
              "shi",
              "ma",
              "u",
              "no",
              "ga",
              "kowa",
              "ku",
              "te",
              "mabuta",
              "to",
              "ji",
              "ta",
              "ma",
              "ma",
              "hashi",
              "ru",
              "mi",
              "ta",
              "i",
              "ni"
            ]
          },
          {
            "ja": "また痣焦ってばかりで溺れかけていた僕を呼んだ",
            "romaji": "matashiasettebakarideoborekaketeitabokuwoyonda",
            "ko": "또다시 멍이 들어, 조급해하기만 하며 빠져 죽어가던 나를 불렀어",
            "charRomaji": [
              "ma",
              "ta",
              "shi",
              "ase",
              "t",
              "te",
              "ba",
              "ka",
              "ri",
              "de",
              "obo",
              "re",
              "ka",
              "ke",
              "te",
              "i",
              "ta",
              "boku",
              "wo",
              "yo",
              "n",
              "da"
            ]
          },
          {
            "ja": "放たれる導かれる吸い寄せられる鼓動",
            "romaji": "houttarerumichibikarerusuiyoserarerukodou",
            "ko": "해방되어, 이끌려가며, 빨려 들어가는 고동",
            "charRomaji": [
              "hout",
              "ta",
              "re",
              "ru",
              "michibi",
              "ka",
              "re",
              "ru",
              "su",
              "i",
              "yo",
              "se",
              "ra",
              "re",
              "ru",
              "ko",
              "dou"
            ]
          },
          {
            "ja": "僕のまま吸って吐くだけそれだけが何故こんな難しくって嫌になる",
            "romaji": "bokunomamasuttehakudakesoredakeganazekonnamuzukashikutteiyaninaru",
            "ko": "나인 채로 들이쉬고 내쉴 뿐인 그것이 어째서 이리 어렵고 지겨운 걸까",
            "charRomaji": [
              "boku",
              "no",
              "ma",
              "ma",
              "su",
              "t",
              "te",
              "ha",
              "ku",
              "da",
              "ke",
              "so",
              "re",
              "da",
              "ke",
              "ga",
              "na",
              "ze",
              "ko",
              "n",
              "na",
              "muzuka",
              "shi",
              "ku",
              "t",
              "te",
              "iya",
              "ni",
              "na",
              "ru"
            ]
          },
          {
            "ja": "全てをぶつけても壊れないでいてくれた",
            "romaji": "subetewobutsuketemokowarenaideitekureta",
            "ko": "모든 것을 온 힘껏 부딪쳐도 부서지지 않고 버텨주었어",
            "charRomaji": [
              "sube",
              "te",
              "wo",
              "bu",
              "tsu",
              "ke",
              "te",
              "mo",
              "kowa",
              "re",
              "na",
              "i",
              "de",
              "i",
              "te",
              "ku",
              "re",
              "ta"
            ]
          },
          {
            "ja": "抱かれる身を委ねる音の波へと本能で",
            "romaji": "dakarerumiwoyudaneruotononamihetohonnoude",
            "ko": "안기어, 몸을 맡기어, 소리의 파도로 본능으로",
            "charRomaji": [
              "da",
              "ka",
              "re",
              "ru",
              "mi",
              "wo",
              "yuda",
              "ne",
              "ru",
              "oto",
              "no",
              "nami",
              "he",
              "to",
              "hon",
              "nou",
              "de"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "一心に大切があれば失うことに怯えてしまいそうで",
            "romaji": "isshinnitaisetsugaarebaushinaukotoniobieteshimaisoude",
            "ko": "한마음으로 소중한 것이 생기면 잃어버리는 게 두려워질 것만 같아서",
            "charRomaji": [
              "i",
              "sshin",
              "ni",
              "tai",
              "setsu",
              "ga",
              "a",
              "re",
              "ba",
              "ushina",
              "u",
              "ko",
              "to",
              "ni",
              "obi",
              "e",
              "te",
              "shi",
              "ma",
              "i",
              "so",
              "u",
              "de"
            ]
          },
          {
            "ja": "繋ぎ合うこと遠ざけていた",
            "romaji": "tsunagiaukototoozaketeita",
            "ko": "서로 이어지는 것을 멀리하고 있었지",
            "charRomaji": [
              "tsuna",
              "gi",
              "a",
              "u",
              "ko",
              "to",
              "too",
              "za",
              "ke",
              "te",
              "i",
              "ta"
            ]
          },
          {
            "ja": "やっぱりはみだしてしまう窮屈で漂ってる",
            "romaji": "yapparihamidashiteshimaukyuukutsudetadayotteru",
            "ko": "역시나 삐져나오고 마는, 비좁아서 표류하고 있어",
            "charRomaji": [
              "ya",
              "p",
              "pa",
              "ri",
              "ha",
              "mi",
              "da",
              "shi",
              "te",
              "shi",
              "ma",
              "u",
              "kyuu",
              "kutsu",
              "de",
              "tadayo",
              "t",
              "te",
              "ru"
            ]
          },
          {
            "ja": "だけど何度でも戻ってくる",
            "romaji": "dakedonandodemomodottekuru",
            "ko": "그렇지만 몇 번이고 다시 돌아오고 말아",
            "charRomaji": [
              "da",
              "ke",
              "do",
              "nan",
              "do",
              "de",
              "mo",
              "modo",
              "t",
              "te",
              "ku",
              "ru"
            ]
          },
          {
            "ja": "僕のまま吸って吐けたらそれだけで此処にいる理由になる",
            "romaji": "bokunomamasuttehaketarasoredakedekokoniiruriyuuninaru",
            "ko": "나인 채로 숨 쉬고 뱉을 수 있다면 그것만으로 여기에 있을 이유가 돼",
            "charRomaji": [
              "boku",
              "no",
              "ma",
              "ma",
              "su",
              "t",
              "te",
              "ha",
              "ke",
              "ta",
              "ra",
              "so",
              "re",
              "da",
              "ke",
              "de",
              "ko",
              "ko",
              "ni",
              "i",
              "ru",
              "ri",
              "yuu",
              "ni",
              "na",
              "ru"
            ]
          },
          {
            "ja": "言葉になれなくて旋律にこめた受けとってくれる",
            "romaji": "kotobaninarenakutesenritsunikometauketottekureru",
            "ko": "말로 되지 못해서 선율에 담아냈어, 받아주겠니?",
            "charRomaji": [
              "ko",
              "toba",
              "ni",
              "na",
              "re",
              "na",
              "ku",
              "te",
              "sen",
              "ritsu",
              "ni",
              "ko",
              "me",
              "ta",
              "u",
              "ke",
              "to",
              "t",
              "te",
              "ku",
              "re",
              "ru"
            ]
          },
          {
            "ja": "繰り返す日々よどうか僕らになってゆけ",
            "romaji": "kurikaesuhibiyodoukabokuraninatteyuke",
            "ko": "되풀이되는 나날이여, 제발 우리들이 되어가라",
            "charRomaji": [
              "ku",
              "ri",
              "kae",
              "su",
              "hi",
              "bi",
              "yo",
              "do",
              "u",
              "ka",
              "boku",
              "ra",
              "ni",
              "na",
              "t",
              "te",
              "yu",
              "ke"
            ]
          },
          {
            "ja": "生きている待ち合わせるいつでも音楽に帰ろう",
            "romaji": "ikiteirumachiawaseruitsudemoongakunikaerou",
            "ko": "살아가고 있어, 약속 장소에서 만나, 언제라도 음악으로 돌아가자",
            "charRomaji": [
              "i",
              "ki",
              "te",
              "i",
              "ru",
              "ma",
              "chi",
              "a",
              "wa",
              "se",
              "ru",
              "i",
              "tsu",
              "de",
              "mo",
              "o",
              "ngaku",
              "ni",
              "kae",
              "ro",
              "u"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "hashidoyama",
    "title": "端程山",
    "reading": "ぱのらま",
    "category": "original",
    "album": "5th Single『端程山』, 2nd Album『跡暖空』",
    "youtubeId": "1c2uSrAGF9Q",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "どこまで歩けばいいのかなんて",
            "romaji": "dokomadearukebaiinokanante",
            "ko": "어디까지 걸어가야 하는지 따위",
            "charRomaji": [
              "do",
              "ko",
              "ma",
              "de",
              "aru",
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
            "ko": "알지 못한 채 대지를 딛고 있었어",
            "charRomaji": [
              "shi",
              "ra",
              "na",
              "i",
              "ma",
              "ma",
              "fu",
              "mi",
              "shi",
              "me",
              "te",
              "ta"
            ]
          },
          {
            "ja": "重い足で沈みながら",
            "romaji": "omoiashideshizuminagara",
            "ko": "무거운 발걸음으로 깊이 빠져들며",
            "charRomaji": [
              "omo",
              "i",
              "ashi",
              "de",
              "shizu",
              "mi",
              "na",
              "ga",
              "ra"
            ]
          },
          {
            "ja": "僕らだけの轍作って",
            "romaji": "bokuradakenowadachitsukutte",
            "ko": "우리들만의 수레바퀴 자국을 새기며",
            "charRomaji": [
              "boku",
              "ra",
              "da",
              "ke",
              "no",
              "wadachi",
              "tsuku",
              "t",
              "te"
            ]
          },
          {
            "ja": "ねえ僕が見せたいと思った景色",
            "romaji": "neebokugamisetaitoomottakeshiki",
            "ko": "있잖아, 내가 보여주고 싶다 여겼던 경치가",
            "charRomaji": [
              "ne",
              "e",
              "boku",
              "ga",
              "mi",
              "se",
              "ta",
              "i",
              "to",
              "omo",
              "t",
              "ta",
              "ke",
              "shiki"
            ]
          },
          {
            "ja": "君が欲しいものとは少し違ってしまっても",
            "romaji": "kimigahoshiimonotohasukoshichigatteshimattemo",
            "ko": "네가 바랐던 것과는 조금 달라져 버린다 해도",
            "charRomaji": [
              "kimi",
              "ga",
              "ho",
              "shi",
              "i",
              "mo",
              "no",
              "to",
              "ha",
              "suko",
              "shi",
              "chiga",
              "t",
              "te",
              "shi",
              "ma",
              "t",
              "te",
              "mo"
            ]
          },
          {
            "ja": "夕空に抱かれる君と僕の",
            "romaji": "yuuzoranidakarerukimitobokuno",
            "ko": "저녁노을에 안긴 너와 나의",
            "charRomaji": [
              "yu",
              "uzora",
              "ni",
              "da",
              "ka",
              "re",
              "ru",
              "kimi",
              "to",
              "boku",
              "no"
            ]
          },
          {
            "ja": "まばらな歩幅で同じ色に染まる頬を",
            "romaji": "mabaranahohabadeonajiironisomaruhoowo",
            "ko": "제각각인 보폭 속에서 같은 색으로 물드는 뺨을",
            "charRomaji": [
              "ma",
              "ba",
              "ra",
              "na",
              "ho",
              "haba",
              "de",
              "ona",
              "ji",
              "iro",
              "ni",
              "so",
              "ma",
              "ru",
              "hoo",
              "wo"
            ]
          },
          {
            "ja": "見つけてこころが撫でられてくよ",
            "romaji": "mitsuketekokoroganaderaretekuyo",
            "ko": "발견하고서 마음이 부드럽게 어루만져져 가",
            "charRomaji": [
              "mi",
              "tsu",
              "ke",
              "te",
              "ko",
              "ko",
              "ro",
              "ga",
              "na",
              "de",
              "ra",
              "re",
              "te",
              "ku",
              "yo"
            ]
          },
          {
            "ja": "憂鬱が解けてく陽炎の空",
            "romaji": "yuuutsugatoketekukagerounosora",
            "ko": "우울함이 녹아내리는 아지랑이 낀 하늘",
            "charRomaji": [
              "yuu",
              "utsu",
              "ga",
              "to",
              "ke",
              "te",
              "ku",
              "ka",
              "gerou",
              "no",
              "sora"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "やさしさに満ちるひとやすみしよう",
            "romaji": "yasashisanimichiruhitoyasumishiyou",
            "ko": "다정함으로 가득 차, 잠시 쉬어가자",
            "charRomaji": [
              "ya",
              "sa",
              "shi",
              "sa",
              "ni",
              "mi",
              "chi",
              "ru",
              "hi",
              "to",
              "ya",
              "su",
              "mi",
              "shi",
              "yo",
              "u"
            ]
          },
          {
            "ja": "荷物をおろして今日までの僕らに",
            "romaji": "nimotsuwooroshitekyoumadenobokurani",
            "ko": "짐을 내려놓고 오늘까지의 우리들에게",
            "charRomaji": [
              "ni",
              "motsu",
              "wo",
              "o",
              "ro",
              "shi",
              "te",
              "k",
              "you",
              "ma",
              "de",
              "no",
              "boku",
              "ra",
              "ni"
            ]
          },
          {
            "ja": "息をついてまた歩き出そう",
            "romaji": "ikiwotsuitemataarukidasou",
            "ko": "숨을 고르고서 다시 걸어나가자",
            "charRomaji": [
              "iki",
              "wo",
              "tsu",
              "i",
              "te",
              "ma",
              "ta",
              "aru",
              "ki",
              "da",
              "so",
              "u"
            ]
          },
          {
            "ja": "果てのない山を越えていこう",
            "romaji": "hatenonaiyamawokoeteikou",
            "ko": "끝없는 산을 넘어가자",
            "charRomaji": [
              "ha",
              "te",
              "no",
              "na",
              "i",
              "yama",
              "wo",
              "ko",
              "e",
              "te",
              "i",
              "ko",
              "u"
            ]
          },
          {
            "ja": "転がり落ちても手を取り合って",
            "romaji": "korogariochitemotewotoriatte",
            "ko": "굴러떨어진대도 서로 손을 맞잡고",
            "charRomaji": [
              "koro",
              "ga",
              "ri",
              "o",
              "chi",
              "te",
              "mo",
              "te",
              "wo",
              "to",
              "ri",
              "a",
              "t",
              "te"
            ]
          },
          {
            "ja": "擦りむいた傷さえ誇らしく思える",
            "romaji": "surimuitakizusaehokorashikuomoeru",
            "ko": "까진 상처조차 자랑스럽게 여겨질 거야",
            "charRomaji": [
              "su",
              "ri",
              "mu",
              "i",
              "ta",
              "kizu",
              "sa",
              "e",
              "hoko",
              "ra",
              "shi",
              "ku",
              "omo",
              "e",
              "ru"
            ]
          },
          {
            "ja": "明日へと続くこの端程山",
            "romaji": "ashitahetotsuzukukonohajihodoyama",
            "ko": "내일로 이어지는 이 하테야마",
            "charRomaji": [
              "a",
              "shita",
              "he",
              "to",
              "tsuzu",
              "ku",
              "ko",
              "no",
              "haji",
              "hodo",
              "yama"
            ]
          },
          {
            "ja": "僕らの旅路は終わらない",
            "romaji": "bokuranotabijiwaowaranai",
            "ko": "우리들의 여정은 끝나지 않아",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "tabi",
              "ji",
              "wa",
              "o",
              "wa",
              "ra",
              "na",
              "i"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "rinpuu",
    "title": "輪符雨",
    "reading": "りふれいん",
    "category": "original",
    "album": "5th Single『端程山』c/w, 2nd Album『跡暖空』",
    "youtubeId": "xNF9semW-Ng",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "硝子窓はすぐに雲に覆われて",
            "romaji": "garasumadohasugunikumonioowarete",
            "ko": "유리창은 금세 구름에 뒤덮여",
            "charRomaji": [
              "ga",
              "rasu",
              "mado",
              "ha",
              "su",
              "gu",
              "ni",
              "kumo",
              "ni",
              "oo",
              "wa",
              "re",
              "te"
            ]
          },
          {
            "ja": "ちょっと先も見通せない",
            "romaji": "chottosakimomitoosenai",
            "ko": "조금 앞조차 내다볼 수가 없어",
            "charRomaji": [
              "ch",
              "o",
              "t",
              "to",
              "saki",
              "mo",
              "mi",
              "too",
              "se",
              "na",
              "i"
            ]
          },
          {
            "ja": "遠くなった記憶何度見返して",
            "romaji": "tookunattakiokunandomikaeshite",
            "ko": "아득해진 기억을 몇 번이고 되돌아보며",
            "charRomaji": [
              "too",
              "ku",
              "na",
              "t",
              "ta",
              "ki",
              "oku",
              "nan",
              "do",
              "mi",
              "kae",
              "shi",
              "te"
            ]
          },
          {
            "ja": "あふれそうなメモリすれすれでたゆたう",
            "romaji": "afuresounamemorisuresuredetayutau",
            "ko": "넘칠 것 같은 메모리 한계에서 위태롭게 흔들려",
            "charRomaji": [
              "a",
              "fu",
              "re",
              "so",
              "u",
              "na",
              "me",
              "mo",
              "ri",
              "su",
              "re",
              "su",
              "re",
              "de",
              "ta",
              "yu",
              "ta",
              "u"
            ]
          },
          {
            "ja": "しとしと続いてる不機嫌な空模様は",
            "romaji": "shitoshitotsuzuiterufukigennasoramoyouwa",
            "ko": "부슬부슬 이어지는 찌푸린 날씨는",
            "charRomaji": [
              "shi",
              "to",
              "shi",
              "to",
              "tsuzu",
              "i",
              "te",
              "ru",
              "fu",
              "ki",
              "gen",
              "na",
              "sora",
              "mo",
              "you",
              "wa"
            ]
          },
          {
            "ja": "あの日と地続きでまだやまない",
            "romaji": "anonichitochitsuzukidemadayamanai",
            "ko": "그날과 땅으로 이어져 아직 그치지 않아",
            "charRomaji": [
              "a",
              "no",
              "nichi",
              "to",
              "chi",
              "tsuzu",
              "ki",
              "de",
              "ma",
              "da",
              "ya",
              "ma",
              "na",
              "i"
            ]
          },
          {
            "ja": "振り切って降りきらないフリして",
            "romaji": "furikitteorikiranaifurishite",
            "ko": "뿌리치고서 다 내리지 않는 척하며",
            "charRomaji": [
              "fu",
              "ri",
              "ki",
              "t",
              "te",
              "o",
              "ri",
              "ki",
              "ra",
              "na",
              "i",
              "fu",
              "ri",
              "shi",
              "te"
            ]
          },
          {
            "ja": "誤魔化せない後悔を飲みこんでる",
            "romaji": "gomakasenaikoukaiwonomikonderu",
            "ko": "얼버무릴 수 없는 후회를 삼키고 있어",
            "charRomaji": [
              "go",
              "ma",
              "ka",
              "se",
              "na",
              "i",
              "kou",
              "kai",
              "wo",
              "no",
              "mi",
              "ko",
              "n",
              "de",
              "ru"
            ]
          },
          {
            "ja": "降りきって振り出しに戻っても",
            "romaji": "orikittefuridashinimodottemo",
            "ko": "다 내리고 원점으로 되돌아간대도",
            "charRomaji": [
              "o",
              "ri",
              "ki",
              "t",
              "te",
              "fu",
              "ri",
              "da",
              "shi",
              "ni",
              "modo",
              "t",
              "te",
              "mo"
            ]
          },
          {
            "ja": "きっと空は晴れない今はこのままでいい",
            "romaji": "kittosorawaharenaiimahakonomamadeii",
            "ko": "분명 하늘은 개지 않아, 지금은 이대로 좋아",
            "charRomaji": [
              "ki",
              "t",
              "to",
              "sora",
              "wa",
              "ha",
              "re",
              "na",
              "i",
              "ima",
              "ha",
              "ko",
              "no",
              "ma",
              "ma",
              "de",
              "i",
              "i"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "やり過ごした気持ち雲が連れてきて",
            "romaji": "yarisugoshitakimochikumogatsuretekite",
            "ko": "그저 넘겨버렸던 감정을 구름이 데려와",
            "charRomaji": [
              "ya",
              "ri",
              "su",
              "go",
              "shi",
              "ta",
              "ki",
              "mo",
              "chi",
              "kumo",
              "ga",
              "tsu",
              "re",
              "te",
              "ki",
              "te"
            ]
          },
          {
            "ja": "同じ場面を幾度となく上映させるの",
            "romaji": "onajibamenwoikudotonakujoueisaseruno",
            "ko": "똑같은 장면을 수없이 상영하게 만들어",
            "charRomaji": [
              "ona",
              "ji",
              "ba",
              "men",
              "wo",
              "iku",
              "do",
              "to",
              "na",
              "ku",
              "jou",
              "ei",
              "sa",
              "se",
              "ru",
              "no"
            ]
          },
          {
            "ja": "ざんざん打つならあきらめてしまえるのに",
            "romaji": "zanzanutsunaraakirameteshimaerunoni",
            "ko": "세차게 쏟아붓는다면 차라리 포기해버릴 텐데",
            "charRomaji": [
              "za",
              "n",
              "za",
              "n",
              "u",
              "tsu",
              "na",
              "ra",
              "a",
              "ki",
              "ra",
              "me",
              "te",
              "shi",
              "ma",
              "e",
              "ru",
              "no",
              "ni"
            ]
          },
          {
            "ja": "やわな青い期待がまだやまない",
            "romaji": "yawanaaoikitaigamadayamanai",
            "ko": "물렁하고 푸르른 기대가 아직 멎지 않아",
            "charRomaji": [
              "ya",
              "wa",
              "na",
              "ao",
              "i",
              "ki",
              "tai",
              "ga",
              "ma",
              "da",
              "ya",
              "ma",
              "na",
              "i"
            ]
          },
          {
            "ja": "引きずって必死になってひっきりなしに",
            "romaji": "hikizuttehisshininattehikkirinashini",
            "ko": "질질 끌며 필사적으로 끊임없이",
            "charRomaji": [
              "hi",
              "ki",
              "zu",
              "t",
              "te",
              "his",
              "shi",
              "ni",
              "na",
              "t",
              "te",
              "hi",
              "k",
              "ki",
              "ri",
              "na",
              "shi",
              "ni"
            ]
          },
          {
            "ja": "求め続けてしまう消えない残像",
            "romaji": "motometsuzuketeshimaukienaizanzou",
            "ko": "계속 갈구하고 마는 사라지지 않는 잔상",
            "charRomaji": [
              "moto",
              "me",
              "tsuzu",
              "ke",
              "te",
              "shi",
              "ma",
              "u",
              "ki",
              "e",
              "na",
              "i",
              "zan",
              "zou"
            ]
          },
          {
            "ja": "密かにひび割れてしまったものでも",
            "romaji": "hisokanihibiwareteshimattamonodemo",
            "ko": "남몰래 금이 가버린 것이라도",
            "charRomaji": [
              "hiso",
              "ka",
              "ni",
              "hi",
              "bi",
              "wa",
              "re",
              "te",
              "shi",
              "ma",
              "t",
              "ta",
              "mo",
              "no",
              "de",
              "mo"
            ]
          },
          {
            "ja": "捨てられずに今もこの手の中",
            "romaji": "suterarezuniimamokonotenonaka",
            "ko": "버리지 못한 채 지금도 이 손안에",
            "charRomaji": [
              "su",
              "te",
              "ra",
              "re",
              "zu",
              "ni",
              "ima",
              "mo",
              "ko",
              "no",
              "te",
              "no",
              "naka"
            ]
          },
          {
            "ja": "雫窓じゃ泣いていてもわからない",
            "romaji": "shizukumadojanaiteitemowakaranai",
            "ko": "물방울 맺힌 창문으로는 울고 있어도 알 수 없어",
            "charRomaji": [
              "shizuku",
              "mado",
              "j",
              "a",
              "na",
              "i",
              "te",
              "i",
              "te",
              "mo",
              "wa",
              "ka",
              "ra",
              "na",
              "i"
            ]
          },
          {
            "ja": "置き去りの僕でもやまないでいいこのまま",
            "romaji": "okizarinobokudemoyamanaideiikonomama",
            "ko": "남겨진 나일지라도 멈추지 않아도 돼, 이대로",
            "charRomaji": [
              "o",
              "ki",
              "za",
              "ri",
              "no",
              "boku",
              "de",
              "mo",
              "ya",
              "ma",
              "na",
              "i",
              "de",
              "i",
              "i",
              "ko",
              "no",
              "ma",
              "ma"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "kokairou",
    "title": "孤壊牢",
    "reading": "こころ",
    "category": "original",
    "album": "5th Single『端程山』c/w, 2nd Album『跡暖空』",
    "youtubeId": "MQkr0cVfyjQ",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "まるで違う生き物なのに何故か僕ら一括りで",
            "romaji": "marudechigauikimononanoninazekabokuraikkatsuride",
            "ko": "전혀 다른 생물인데도 어째서인지 우리를 하나로 묶어",
            "charRomaji": [
              "ma",
              "ru",
              "de",
              "chiga",
              "u",
              "i",
              "ki",
              "mono",
              "na",
              "no",
              "ni",
              "na",
              "ze",
              "ka",
              "boku",
              "ra",
              "ik",
              "katsu",
              "ri",
              "de"
            ]
          },
          {
            "ja": "語られる度に虚しい上辺だけを飛ばし読みして",
            "romaji": "katararerudonimunashiiuwabedakewotobashiyomishite",
            "ko": "언급될 때마다 공허해, 겉모습만을 훑어 읽고서",
            "charRomaji": [
              "kata",
              "ra",
              "re",
              "ru",
              "do",
              "ni",
              "muna",
              "shi",
              "i",
              "u",
              "wabe",
              "da",
              "ke",
              "wo",
              "to",
              "ba",
              "shi",
              "yo",
              "mi",
              "shi",
              "te"
            ]
          },
          {
            "ja": "計り知れるそんな物が僕だというなら",
            "romaji": "hakarishirerusonnamonogabokudatoiunara",
            "ko": "헤아려 알 수 있는 그런 것이 나라면",
            "charRomaji": [
              "haka",
              "ri",
              "shi",
              "re",
              "ru",
              "so",
              "n",
              "na",
              "mono",
              "ga",
              "boku",
              "da",
              "to",
              "i",
              "u",
              "na",
              "ra"
            ]
          },
          {
            "ja": "分からなくていいよ分かろうとするな",
            "romaji": "wakaranakuteiiyowakaroutosuruna",
            "ko": "이해하지 않아도 돼, 억지로 이해하려 들지 마",
            "charRomaji": [
              "wa",
              "ka",
              "ra",
              "na",
              "ku",
              "te",
              "i",
              "i",
              "yo",
              "wa",
              "ka",
              "ro",
              "u",
              "to",
              "su",
              "ru",
              "na"
            ]
          },
          {
            "ja": "修復が間に合わないこころこころ",
            "romaji": "shuufukugamaniawanaikokorokokoro",
            "ko": "수복이 미처 따라가지 못해, 마음이, 마음이",
            "charRomaji": [
              "shuu",
              "fuku",
              "ga",
              "ma",
              "ni",
              "a",
              "wa",
              "na",
              "i",
              "ko",
              "ko",
              "ro",
              "ko",
              "ko",
              "ro"
            ]
          },
          {
            "ja": "壊れない消えない物は何処にもない",
            "romaji": "kowarenaikienaimonowadokonimonai",
            "ko": "부서지지 않고 사라지지 않는 것은 어디에도 없어",
            "charRomaji": [
              "kowa",
              "re",
              "na",
              "i",
              "ki",
              "e",
              "na",
              "i",
              "mono",
              "wa",
              "do",
              "ko",
              "ni",
              "mo",
              "na",
              "i"
            ]
          },
          {
            "ja": "誰も教えてくれない投げ出されていた僕ら",
            "romaji": "daremooshietekurenainagedasareteitabokura",
            "ko": "아무도 가르쳐주지 않아, 내던져져 있던 우리들",
            "charRomaji": [
              "dare",
              "mo",
              "oshi",
              "e",
              "te",
              "ku",
              "re",
              "na",
              "i",
              "na",
              "ge",
              "da",
              "sa",
              "re",
              "te",
              "i",
              "ta",
              "boku",
              "ra"
            ]
          },
          {
            "ja": "明日もない描けないどんなに鮮やかな景色も",
            "romaji": "ashitamonaiegakenaidonnanisenyakanakeshikimo",
            "ko": "내일도 없어, 그릴 수 없어, 아무리 선명한 경치도",
            "charRomaji": [
              "a",
              "shita",
              "mo",
              "na",
              "i",
              "ega",
              "ke",
              "na",
              "i",
              "do",
              "n",
              "na",
              "ni",
              "sen",
              "ya",
              "ka",
              "na",
              "ke",
              "shiki",
              "mo"
            ]
          },
          {
            "ja": "僕の目には鈍色に映る仕様",
            "romaji": "bokunomeniwanibiironiutsurushiyou",
            "ko": "내 눈에는 잿빛으로 비치는 운명",
            "charRomaji": [
              "boku",
              "no",
              "me",
              "ni",
              "wa",
              "nibi",
              "iro",
              "ni",
              "utsu",
              "ru",
              "shi",
              "you"
            ]
          },
          {
            "ja": "それでもこころは僕の物だ",
            "romaji": "soredemokokorohabokunomonoda",
            "ko": "그럼에도 마음은 온전히 나의 것이다",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "ko",
              "ko",
              "ro",
              "ha",
              "boku",
              "no",
              "mono",
              "da"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "迷い込んだ方程式も解があると知ってるなら",
            "romaji": "mayoikondahouteishikimokaigaarutoshitterunara",
            "ko": "헤매 들어간 방정식도 해답이 있다는 걸 안다면",
            "charRomaji": [
              "mayo",
              "i",
              "ko",
              "n",
              "da",
              "ho",
              "utei",
              "shiki",
              "mo",
              "kai",
              "ga",
              "a",
              "ru",
              "to",
              "shi",
              "t",
              "te",
              "ru",
              "na",
              "ra"
            ]
          },
          {
            "ja": "不可解な今日より幾分ましに見えたんだ",
            "romaji": "fukakainakyouyoriikubunmashinimietanda",
            "ko": "이해할 수 없는 오늘보다 훨씬 나아 보였어",
            "charRomaji": [
              "fu",
              "ka",
              "kai",
              "na",
              "k",
              "you",
              "yo",
              "ri",
              "i",
              "kubun",
              "ma",
              "shi",
              "ni",
              "mi",
              "e",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "大枠に填まれないこころこころ",
            "romaji": "oowakunitenmarenaikokorokokoro",
            "ko": "커다란 틀에 끼워 맞춰지지 않는 마음이",
            "charRomaji": [
              "oo",
              "waku",
              "ni",
              "ten",
              "ma",
              "re",
              "na",
              "i",
              "ko",
              "ko",
              "ro",
              "ko",
              "ko",
              "ro"
            ]
          },
          {
            "ja": "鰾膠無い世界だと僕に差し出すその手",
            "romaji": "ukibukuronikawanaisekaidatobokunisashidasusonote",
            "ko": "붙임성 없는 세상이라며 내게 내미는 그 손",
            "charRomaji": [
              "ukibukuro",
              "nikawa",
              "na",
              "i",
              "se",
              "kai",
              "da",
              "to",
              "boku",
              "ni",
              "sa",
              "shi",
              "da",
              "su",
              "so",
              "no",
              "te"
            ]
          },
          {
            "ja": "正しいらしい道筋へ招く誘う",
            "romaji": "tadashiirashiimichisujihemanekusasou",
            "ko": "올바른 듯한 길로 손짓하며 유혹하네",
            "charRomaji": [
              "tada",
              "shi",
              "i",
              "ra",
              "shi",
              "i",
              "michi",
              "suji",
              "he",
              "mane",
              "ku",
              "saso",
              "u"
            ]
          },
          {
            "ja": "手負いの僕らは信じるすべさえ持たなくて",
            "romaji": "teoiinobokurawashinjirusubesaemotanakute",
            "ko": "상처 입은 우리는 믿을 방법조차 갖추지 못해서",
            "charRomaji": [
              "te",
              "oi",
              "i",
              "no",
              "boku",
              "ra",
              "wa",
              "shin",
              "ji",
              "ru",
              "su",
              "be",
              "sa",
              "e",
              "mo",
              "ta",
              "na",
              "ku",
              "te"
            ]
          },
          {
            "ja": "胸を劈く音だけが何よりも確かで",
            "romaji": "munewotsunzakuotodakegananiyorimotashikade",
            "ko": "가슴을 찢는 소리만이 그 무엇보다도 확실해서",
            "charRomaji": [
              "mune",
              "wo",
              "tsunza",
              "ku",
              "oto",
              "da",
              "ke",
              "ga",
              "nani",
              "yo",
              "ri",
              "mo",
              "tashi",
              "ka",
              "de"
            ]
          },
          {
            "ja": "こころは僕の物だと喚く",
            "romaji": "kokorohabokunomonodatowameku",
            "ko": "마음은 나의 것이라고 울부짖는다",
            "charRomaji": [
              "ko",
              "ko",
              "ro",
              "ha",
              "boku",
              "no",
              "mono",
              "da",
              "to",
              "wame",
              "ku"
            ]
          },
          {
            "ja": "撒いたはずの目印はもう啄まれて",
            "romaji": "sanitahazunomejirushihamoutakumarete",
            "ko": "뿌려두었을 표식은 이미 쪼아 먹혀버려",
            "charRomaji": [
              "san",
              "i",
              "ta",
              "ha",
              "zu",
              "no",
              "me",
              "jirushi",
              "ha",
              "mo",
              "u",
              "taku",
              "ma",
              "re",
              "te"
            ]
          },
          {
            "ja": "帰り道を忘れてしまった放浪",
            "romaji": "kaerimichiwowasureteshimattahourou",
            "ko": "돌아갈 길을 잊어버리고 만 방랑",
            "charRomaji": [
              "kae",
              "ri",
              "michi",
              "wo",
              "wasu",
              "re",
              "te",
              "shi",
              "ma",
              "t",
              "ta",
              "ho",
              "urou"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "hoshuudou",
    "title": "歩拾道",
    "reading": "ほしゅうどう",
    "category": "original",
    "album": "Digital Single (2024), 2nd Album『跡暖空』",
    "youtubeId": "EEeYU4-dhZk",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "急ぎ足で通り過ぎる街の影",
            "romaji": "isogiashidetourisugirumachinokage",
            "ko": "빠른 걸음으로 스쳐 지나가는 거리의 그림자",
            "charRomaji": [
              "iso",
              "gi",
              "ashi",
              "de",
              "tou",
              "ri",
              "su",
              "gi",
              "ru",
              "machi",
              "no",
              "kage"
            ]
          },
          {
            "ja": "自分のペースさえ見失いそうで",
            "romaji": "jibunnopeesusaemiushinaisoude",
            "ko": "나만의 보폭조차 잃어버릴 것만 같아서",
            "charRomaji": [
              "ji",
              "bun",
              "no",
              "pee",
              "",
              "su",
              "sa",
              "e",
              "mi",
              "ushina",
              "i",
              "so",
              "u",
              "de"
            ]
          },
          {
            "ja": "落ちていた欠片を拾い集めながら",
            "romaji": "ochiteitakakerawohiroiatsumenagara",
            "ko": "떨어져 있던 조각들을 하나씩 주워 모으며",
            "charRomaji": [
              "o",
              "chi",
              "te",
              "i",
              "ta",
              "ka",
              "kera",
              "wo",
              "hiro",
              "i",
              "atsu",
              "me",
              "na",
              "ga",
              "ra"
            ]
          },
          {
            "ja": "一歩ずつ確かめるように踏みしめる",
            "romaji": "ippozuttashikameruyounifumishimeru",
            "ko": "한 걸음씩 확인하듯 대지를 딛는다",
            "charRomaji": [
              "i",
              "ppo",
              "zu",
              "t",
              "tashi",
              "ka",
              "me",
              "ru",
              "yo",
              "u",
              "ni",
              "fu",
              "mi",
              "shi",
              "me",
              "ru"
            ]
          },
          {
            "ja": "スピードを競う世界の中で",
            "romaji": "supiidowokisousekainonakade",
            "ko": "속도를 겨루는 세상 속에서",
            "charRomaji": [
              "su",
              "pii",
              "",
              "do",
              "wo",
              "kiso",
              "u",
              "se",
              "kai",
              "no",
              "naka",
              "de"
            ]
          },
          {
            "ja": "立ち止まることの怖さに怯えてた",
            "romaji": "tachitomarukotonokowasaniobieteta",
            "ko": "멈춰 서는 것에 대한 두려움에 떨고 있었어",
            "charRomaji": [
              "ta",
              "chi",
              "to",
              "ma",
              "ru",
              "ko",
              "to",
              "no",
              "kowa",
              "sa",
              "ni",
              "obi",
              "e",
              "te",
              "ta"
            ]
          },
          {
            "ja": "だけど拾い集めた小さな石ころが",
            "romaji": "dakedohiroiatsumetachiisanaishikoroga",
            "ko": "하지만 주워 모은 작은 조약돌들이",
            "charRomaji": [
              "da",
              "ke",
              "do",
              "hiro",
              "i",
              "atsu",
              "me",
              "ta",
              "chii",
              "sa",
              "na",
              "ishi",
              "ko",
              "ro",
              "ga"
            ]
          },
          {
            "ja": "いつか僕らの道になるんだ",
            "romaji": "itsukabokuranomichininarunda",
            "ko": "언젠가 우리들의 길이 되는 거야",
            "charRomaji": [
              "i",
              "tsu",
              "ka",
              "boku",
              "ra",
              "no",
              "michi",
              "ni",
              "na",
              "ru",
              "n",
              "da"
            ]
          },
          {
            "ja": "誰かと比べることなんてない",
            "romaji": "darekatokuraberukotonantenai",
            "ko": "누군가와 비교할 것 따윈 전혀 없어",
            "charRomaji": [
              "dare",
              "ka",
              "to",
              "kura",
              "be",
              "ru",
              "ko",
              "to",
              "na",
              "n",
              "te",
              "na",
              "i"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "拾い集めた傷跡こそが宝物",
            "romaji": "hiroiatsumetakizuatokosogatakaramono",
            "ko": "주워 모은 상처야말로 소중한 보물",
            "charRomaji": [
              "hiro",
              "i",
              "atsu",
              "me",
              "ta",
              "kizu",
              "ato",
              "ko",
              "so",
              "ga",
              "takara",
              "mono"
            ]
          },
          {
            "ja": "息を切らしながら歩き続ける道",
            "romaji": "ikiwokirashinagaraarukitsuzukerumichi",
            "ko": "숨을 헐떡이며 계속 걸어가는 이 길",
            "charRomaji": [
              "iki",
              "wo",
              "ki",
              "ra",
              "shi",
              "na",
              "ga",
              "ra",
              "aru",
              "ki",
              "tsuzu",
              "ke",
              "ru",
              "michi"
            ]
          },
          {
            "ja": "遠回りでもいい僕らの足跡",
            "romaji": "toomawaridemoiibokuranosokuseki",
            "ko": "멀리 돌아가도 좋아 우리들의 발자국",
            "charRomaji": [
              "to",
              "omawa",
              "ri",
              "de",
              "mo",
              "i",
              "i",
              "boku",
              "ra",
              "no",
              "so",
              "kuseki"
            ]
          },
          {
            "ja": "拾い集めた言葉を紡ぎ合わせて",
            "romaji": "hiroiatsumetakotobawotsumugiawasete",
            "ko": "주워 모은 말들을 함께 엮어서",
            "charRomaji": [
              "hiro",
              "i",
              "atsu",
              "me",
              "ta",
              "ko",
              "toba",
              "wo",
              "tsumu",
              "gi",
              "a",
              "wa",
              "se",
              "te"
            ]
          },
          {
            "ja": "世界でたったひとつの歌を歌おう",
            "romaji": "sekaidetattahitotsunoutawoutaou",
            "ko": "세상에서 단 하나뿐인 노래를 부르자",
            "charRomaji": [
              "se",
              "kai",
              "de",
              "ta",
              "t",
              "ta",
              "hi",
              "to",
              "tsu",
              "no",
              "uta",
              "wo",
              "uta",
              "o",
              "u"
            ]
          },
          {
            "ja": "前を向いてまた一歩踏み出そう",
            "romaji": "maewomuitemataippofumidasou",
            "ko": "앞을 향해 다시 한 걸음 내딛자",
            "charRomaji": [
              "mae",
              "wo",
              "mu",
              "i",
              "te",
              "ma",
              "ta",
              "i",
              "ppo",
              "fu",
              "mi",
              "da",
              "so",
              "u"
            ]
          },
          {
            "ja": "どこまでも続くこの歩拾道を",
            "romaji": "dokomademotsuzukukonohoshuumichiwo",
            "ko": "어디까지고 이어지는 이 보습도를",
            "charRomaji": [
              "do",
              "ko",
              "ma",
              "de",
              "mo",
              "tsuzu",
              "ku",
              "ko",
              "no",
              "ho",
              "shuu",
              "michi",
              "wo"
            ]
          },
          {
            "ja": "僕らだけのスピードで走破しよう",
            "romaji": "bokuradakenosupiidodesouhashiyou",
            "ko": "우리들만의 스피드로 완주하자",
            "charRomaji": [
              "boku",
              "ra",
              "da",
              "ke",
              "no",
              "su",
              "pii",
              "",
              "do",
              "de",
              "sou",
              "ha",
              "shi",
              "yo",
              "u"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "yaonzen",
    "title": "夜隠染",
    "reading": "よかぜ",
    "category": "original",
    "album": "2nd Album『跡暖空』",
    "youtubeId": "7kPyHJ2SA9g",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "夜の帳が降りて街を覆い隠す",
            "romaji": "yorunochougaoritemachiwoooikakusu",
            "ko": "밤의 장막이 내려 거리를 덮어 가리고",
            "charRomaji": [
              "yoru",
              "no",
              "chou",
              "ga",
              "o",
              "ri",
              "te",
              "machi",
              "wo",
              "oo",
              "i",
              "kaku",
              "su"
            ]
          },
          {
            "ja": "誰にも見せたくない涙を染み込ませて",
            "romaji": "darenimomisetakunainamidawosomikomasete",
            "ko": "누구에게도 보이고 싶지 않은 눈물을 스며들게 해",
            "charRomaji": [
              "dare",
              "ni",
              "mo",
              "mi",
              "se",
              "ta",
              "ku",
              "na",
              "i",
              "namidaw",
              "o",
              "so",
              "mi",
              "ko",
              "ma",
              "se",
              "te"
            ]
          },
          {
            "ja": "静まり返る部屋の片隅で",
            "romaji": "shizumarikaeruheyanokatasumide",
            "ko": "쥐죽은 듯 조용한 방 한구석에서",
            "charRomaji": [
              "shizu",
              "ma",
              "ri",
              "kae",
              "ru",
              "he",
              "ya",
              "no",
              "kata",
              "sumi",
              "de"
            ]
          },
          {
            "ja": "蠢く感情をそっと解き放つ",
            "romaji": "ugomekukanjouwosottotokihouttsu",
            "ko": "꿈틀대는 감정을 가만히 해방시켜",
            "charRomaji": [
              "ugome",
              "ku",
              "kan",
              "jou",
              "wo",
              "so",
              "t",
              "to",
              "to",
              "ki",
              "hout",
              "tsu"
            ]
          },
          {
            "ja": "闇に紛れて吐き出す溜息も",
            "romaji": "yaminimagiretehakidasutameikimo",
            "ko": "어둠에 묻혀 뱉어내는 한숨도",
            "charRomaji": [
              "yami",
              "ni",
              "magi",
              "re",
              "te",
              "ha",
              "ki",
              "da",
              "su",
              "tame",
              "iki",
              "mo"
            ]
          },
          {
            "ja": "朝が来れば消えてしまう幻",
            "romaji": "asagakorebakieteshimaumaboroshi",
            "ko": "아침이 오면 사라져버릴 환상",
            "charRomaji": [
              "asa",
              "ga",
              "ko",
              "re",
              "ba",
              "ki",
              "e",
              "te",
              "shi",
              "ma",
              "u",
              "maboroshi"
            ]
          },
          {
            "ja": "それでも僕の中で濃く染まり続ける",
            "romaji": "soredemobokunonakadekokusomaritsuzukeru",
            "ko": "그럼에도 내 안에서 짙게 물들어가는",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "boku",
              "no",
              "naka",
              "de",
              "ko",
              "ku",
              "so",
              "ma",
              "ri",
              "tsuzu",
              "ke",
              "ru"
            ]
          },
          {
            "ja": "決して拭えない真実の色",
            "romaji": "kesshiteshokuenaishinjitsunoiro",
            "ko": "결코 닦아낼 수 없는 진실의 색채",
            "charRomaji": [
              "kes",
              "shi",
              "te",
              "shoku",
              "e",
              "na",
              "i",
              "shi",
              "njitsu",
              "no",
              "iro"
            ]
          },
          {
            "ja": "暗闇に潜む本音を抱きしめて",
            "romaji": "kurayaminihisomuhonnewodakishimete",
            "ko": "어둠 속에 깃든 진심을 끌어안고",
            "charRomaji": [
              "kura",
              "yami",
              "ni",
              "hiso",
              "mu",
              "hon",
              "ne",
              "wo",
              "da",
              "ki",
              "shi",
              "me",
              "te"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "夜に隠れたままじゃ終われないから",
            "romaji": "yorunikakuretamamajaowarenaikara",
            "ko": "밤에 숨은 채로는 끝낼 수 없으니까",
            "charRomaji": [
              "yoru",
              "ni",
              "kaku",
              "re",
              "ta",
              "ma",
              "ma",
              "j",
              "a",
              "o",
              "wa",
              "re",
              "na",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "染まった痛みを力に変えて立ち上がる",
            "romaji": "somattaitamiwochikaranikaetetachiagaru",
            "ko": "물든 아픔을 힘으로 바꾸어 일어선다",
            "charRomaji": [
              "so",
              "ma",
              "t",
              "ta",
              "ita",
              "mi",
              "wo",
              "chikara",
              "ni",
              "ka",
              "e",
              "te",
              "ta",
              "chi",
              "a",
              "ga",
              "ru"
            ]
          },
          {
            "ja": "滲んでいく夜空の星を睨みつけて",
            "romaji": "shinndeikuyozoranohoshiwoniramitsukete",
            "ko": "번져가는 밤하늘의 별을 노려보며",
            "charRomaji": [
              "shin",
              "n",
              "de",
              "i",
              "ku",
              "yo",
              "zora",
              "no",
              "hoshi",
              "wo",
              "nira",
              "mi",
              "tsu",
              "ke",
              "te"
            ]
          },
          {
            "ja": "誰も知らない夜明けを探しに行こう",
            "romaji": "daremoshiranaiyoakewosagashiniikou",
            "ko": "아무도 모르는 새벽을 찾으러 가자",
            "charRomaji": [
              "dare",
              "mo",
              "shi",
              "ra",
              "na",
              "i",
              "yo",
              "a",
              "ke",
              "wo",
              "saga",
              "shi",
              "ni",
              "i",
              "ko",
              "u"
            ]
          },
          {
            "ja": "染められた孤独の影を振り払い",
            "romaji": "someraretakodokunokagewofuriharai",
            "ko": "물들여진 고독의 그림자를 뿌리치고",
            "charRomaji": [
              "so",
              "me",
              "ra",
              "re",
              "ta",
              "ko",
              "doku",
              "no",
              "kage",
              "wo",
              "fu",
              "ri",
              "hara",
              "i"
            ]
          },
          {
            "ja": "自分の色で世界を塗り替えるんだ",
            "romaji": "jibunnoirodesekaiwonurikaerunda",
            "ko": "나만의 색으로 세상을 덧칠하는 거야",
            "charRomaji": [
              "ji",
              "bun",
              "no",
              "iro",
              "de",
              "se",
              "kai",
              "wo",
              "nu",
              "ri",
              "ka",
              "e",
              "ru",
              "n",
              "da"
            ]
          },
          {
            "ja": "暗闇を切り裂いて響く歌声",
            "romaji": "kurayamiwokirisaitehibikuutagoe",
            "ko": "칠흑의 어둠을 가르고 울려 퍼지는 노랫소리",
            "charRomaji": [
              "kura",
              "yami",
              "wo",
              "ki",
              "ri",
              "sa",
              "i",
              "te",
              "hibi",
              "ku",
              "uta",
              "goe"
            ]
          },
          {
            "ja": "朝焼けへと続く僕らの叫び",
            "romaji": "asayakehetotsuzukubokuranosakebi",
            "ko": "아침 노을로 이어지는 우리들의 외침",
            "charRomaji": [
              "asa",
              "ya",
              "ke",
              "he",
              "to",
              "tsuzu",
              "ku",
              "boku",
              "ra",
              "no",
              "sake",
              "bi"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "mushuutou",
    "title": "霧周途",
    "reading": "みすと",
    "category": "original",
    "album": "2nd Album『跡暖空』",
    "youtubeId": "qJPXncScNA4",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "立ち込める深い霧が視界を奪う",
            "romaji": "tachikomerufukaikirigashikaiwoubau",
            "ko": "자욱한 짙은 안개가 시야를 앗아가",
            "charRomaji": [
              "ta",
              "chi",
              "ko",
              "me",
              "ru",
              "fuka",
              "i",
              "kiri",
              "ga",
              "shi",
              "kai",
              "wo",
              "uba",
              "u"
            ]
          },
          {
            "ja": "どちらへ進めばいいのかもわからず",
            "romaji": "dochirahesusumebaiinokamowakarazu",
            "ko": "어느 쪽으로 나아가야 할지도 모른 채",
            "charRomaji": [
              "do",
              "chi",
              "ra",
              "he",
              "susu",
              "me",
              "ba",
              "i",
              "i",
              "no",
              "ka",
              "mo",
              "wa",
              "ka",
              "ra",
              "zu"
            ]
          },
          {
            "ja": "足元さえおぼつかないまま",
            "romaji": "ashimotosaeobotsukanaimama",
            "ko": "발밑조차 불안하게 비틀거리며",
            "charRomaji": [
              "ashi",
              "moto",
              "sa",
              "e",
              "o",
              "bo",
              "tsu",
              "ka",
              "na",
              "i",
              "ma",
              "ma"
            ]
          },
          {
            "ja": "彷徨う迷路の中で立ち尽くしていた",
            "romaji": "samayoumeirononakadetachitsukushiteita",
            "ko": "방황하는 미로 속에서 망연히 서 있었어",
            "charRomaji": [
              "sama",
              "yo",
              "u",
              "me",
              "iro",
              "no",
              "naka",
              "de",
              "ta",
              "chi",
              "tsu",
              "ku",
              "shi",
              "te",
              "i",
              "ta"
            ]
          },
          {
            "ja": "霧の向こうから微かに聞こえる音",
            "romaji": "kirinomukoukarakasukanikikoeruoto",
            "ko": "안개 저편에서 희미하게 들려오는 소리",
            "charRomaji": [
              "kiri",
              "no",
              "mu",
              "ko",
              "u",
              "ka",
              "ra",
              "kasu",
              "ka",
              "ni",
              "ki",
              "ko",
              "e",
              "ru",
              "oto"
            ]
          },
          {
            "ja": "それを頼りに手探りで歩き出す",
            "romaji": "sorewotayorinitesaguridearukidasu",
            "ko": "그것을 의지 삼아 더듬으며 걸어나가",
            "charRomaji": [
              "so",
              "re",
              "wo",
              "tayo",
              "ri",
              "ni",
              "te",
              "sagu",
              "ri",
              "de",
              "aru",
              "ki",
              "da",
              "su"
            ]
          },
          {
            "ja": "不安で震える指先を握りしめて",
            "romaji": "fuandefurueruyubisakiwonigirishimete",
            "ko": "불안으로 떨리는 손가락 끝을 꼭 쥐고서",
            "charRomaji": [
              "fu",
              "an",
              "de",
              "furu",
              "e",
              "ru",
              "yubi",
              "saki",
              "wo",
              "nigi",
              "ri",
              "shi",
              "me",
              "te"
            ]
          },
          {
            "ja": "一歩ずつ前へと進んでいく",
            "romaji": "ippozutsumaehetosusundeiku",
            "ko": "한 걸음씩 앞을 향해 나아간다",
            "charRomaji": [
              "i",
              "ppo",
              "zu",
              "tsu",
              "mae",
              "he",
              "to",
              "susu",
              "n",
              "de",
              "i",
              "ku"
            ]
          },
          {
            "ja": "霧深き道を行く旅人のように",
            "romaji": "kiribukakimichiwoikutabibitonoyouni",
            "ko": "짙은 안갯속을 걷는 나그네처럼",
            "charRomaji": [
              "kiri",
              "buka",
              "ki",
              "michi",
              "wo",
              "i",
              "ku",
              "tabi",
              "bito",
              "no",
              "yo",
              "u",
              "ni"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "霧の周りを回り続ける道でも",
            "romaji": "kirinomawariwomawaritsuzukerumichidemo",
            "ko": "안개 주위를 맴돌기만 하는 길일지라도",
            "charRomaji": [
              "kiri",
              "no",
              "mawa",
              "ri",
              "wo",
              "mawa",
              "ri",
              "tsuzu",
              "ke",
              "ru",
              "michi",
              "de",
              "mo"
            ]
          },
          {
            "ja": "迷いながら見つけた仲間がいる",
            "romaji": "mayoinagaramitsuketanakamagairu",
            "ko": "헤매면서 찾아낸 동료들이 있어",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ga",
              "ra",
              "mi",
              "tsu",
              "ke",
              "ta",
              "naka",
              "ma",
              "ga",
              "i",
              "ru"
            ]
          },
          {
            "ja": "晴れない空を呪うよりも",
            "romaji": "harenaisorawonorouyorimo",
            "ko": "개지 않는 하늘을 저주하기보다",
            "charRomaji": [
              "ha",
              "re",
              "na",
              "i",
              "sora",
              "wo",
              "noro",
              "u",
              "yo",
              "ri",
              "mo"
            ]
          },
          {
            "ja": "今この手を取り合って進もう",
            "romaji": "imakonotewotoriattesusumou",
            "ko": "지금 이 손을 맞잡고 나아가자",
            "charRomaji": [
              "ima",
              "ko",
              "no",
              "te",
              "wo",
              "to",
              "ri",
              "a",
              "t",
              "te",
              "susu",
              "mo",
              "u"
            ]
          },
          {
            "ja": "やがて霧が晴れるその時まで",
            "romaji": "yagatekirigaharerusonotokimade",
            "ko": "이윽고 안개가 걷힐 그 순간까지",
            "charRomaji": [
              "ya",
              "ga",
              "te",
              "kiri",
              "ga",
              "ha",
              "re",
              "ru",
              "so",
              "no",
              "toki",
              "ma",
              "de"
            ]
          },
          {
            "ja": "僕らの歌は途切れることはない",
            "romaji": "bokuranoutawatogirerukotohanai",
            "ko": "우리들의 노래는 끊어지지 않아",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "uta",
              "wa",
              "to",
              "gi",
              "re",
              "ru",
              "ko",
              "to",
              "ha",
              "na",
              "i"
            ]
          },
          {
            "ja": "霧周途を抜けた先にある光",
            "romaji": "kirishuutowonuketasakiniaruhikari",
            "ko": "안개 길을 빠져나간 끝에 있는 빛",
            "charRomaji": [
              "kiri",
              "shuu",
              "to",
              "wo",
              "nu",
              "ke",
              "ta",
              "saki",
              "ni",
              "a",
              "ru",
              "hikari"
            ]
          },
          {
            "ja": "信じて歩み続ける僕らの旅路",
            "romaji": "shinjiteayumitsuzukerubokuranotabiji",
            "ko": "믿고 계속 걸어가는 우리들의 여정",
            "charRomaji": [
              "shin",
              "ji",
              "te",
              "ayu",
              "mi",
              "tsuzu",
              "ke",
              "ru",
              "boku",
              "ra",
              "no",
              "tabi",
              "ji"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "shoumeisanka",
    "title": "証命讃歌",
    "reading": "しょうめいさんか",
    "category": "original",
    "album": "Digital Single (2026), 3rd Album『致並跡』",
    "youtubeId": "C_OJtQMU52Y",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "くだらない前例は絶って",
            "romaji": "kudaranaizenreiwazetsutte",
            "ko": "시시껄렁한 전례 따윈 시원하게 끊어버리고",
            "charRomaji": [
              "ku",
              "da",
              "ra",
              "na",
              "i",
              "zen",
              "rei",
              "wa",
              "zetsu",
              "t",
              "te"
            ]
          },
          {
            "ja": "止まんない衝動に沿って",
            "romaji": "tomannaishoudounisotte",
            "ko": "멈추지 않는 끓어오르는 충동을 따라서",
            "charRomaji": [
              "to",
              "ma",
              "n",
              "na",
              "i",
              "shou",
              "dou",
              "ni",
              "so",
              "t",
              "te"
            ]
          },
          {
            "ja": "好きに紡げ運命",
            "romaji": "sukinitsumugeunmei",
            "ko": "원하는 대로 자아내라 너만의 운명을",
            "charRomaji": [
              "su",
              "ki",
              "ni",
              "tsumu",
              "ge",
              "un",
              "mei"
            ]
          },
          {
            "ja": "無理に言葉にする必要はない",
            "romaji": "murinikotobanisuruhitsuyouhanai",
            "ko": "억지로 말로 만들어낼 필요는 전혀 없어",
            "charRomaji": [
              "mu",
              "ri",
              "ni",
              "ko",
              "toba",
              "ni",
              "su",
              "ru",
              "hitsu",
              "you",
              "ha",
              "na",
              "i"
            ]
          },
          {
            "ja": "心で命を放つよ",
            "romaji": "kokorodeinochiwohouttsuyo",
            "ko": "온 마음으로 살아있다는 증표를 뿜어낼게",
            "charRomaji": [
              "kokoro",
              "de",
              "inochiw",
              "o",
              "hout",
              "tsu",
              "yo"
            ]
          },
          {
            "ja": "迷いを恐れず突き進め",
            "romaji": "mayoiwoosorezutsukisusume",
            "ko": "방황 따위 두려워 말고 거침없이 돌진해라",
            "charRomaji": [
              "mayo",
              "i",
              "wo",
              "oso",
              "re",
              "zu",
              "tsu",
              "ki",
              "susu",
              "me"
            ]
          },
          {
            "ja": "歪んだ現実をぶち破れ",
            "romaji": "hizundagenjitsuwobuchiyabure",
            "ko": "뒤틀린 현실의 벽을 통쾌하게 부숴버려라",
            "charRomaji": [
              "hizu",
              "n",
              "da",
              "gen",
              "jitsu",
              "wo",
              "bu",
              "chi",
              "yabu",
              "re"
            ]
          },
          {
            "ja": "僕らが僕らであるために",
            "romaji": "bokuragabokuradearutameni",
            "ko": "우리들이 우리 자신으로 살아가기 위해서",
            "charRomaji": [
              "boku",
              "ra",
              "ga",
              "boku",
              "ra",
              "de",
              "a",
              "ru",
              "ta",
              "me",
              "ni"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "誰かの引いた境界線越えて",
            "romaji": "darekanohiitakyoukaisenkoete",
            "ko": "누군가가 그어둔 경계선을 뛰어넘어서",
            "charRomaji": [
              "dare",
              "ka",
              "no",
              "hi",
              "i",
              "ta",
              "kyou",
              "kai",
              "sen",
              "ko",
              "e",
              "te"
            ]
          },
          {
            "ja": "鳴らし続けろ魂の叫び",
            "romaji": "narashitsuzukerotamashiinosakebi",
            "ko": "계속해서 울려라 가슴 깊은 영혼의 절규를",
            "charRomaji": [
              "na",
              "ra",
              "shi",
              "tsuzu",
              "ke",
              "ro",
              "tamashii",
              "no",
              "sake",
              "bi"
            ]
          },
          {
            "ja": "命の讃歌を高らかに歌え",
            "romaji": "inochinosankawotakarakaniutae",
            "ko": "생명의 찬가를 드높이 목청껏 노래해라",
            "charRomaji": [
              "inochi",
              "no",
              "san",
              "ka",
              "wo",
              "taka",
              "ra",
              "ka",
              "ni",
              "uta",
              "e"
            ]
          },
          {
            "ja": "決して消せない僕らの鼓動",
            "romaji": "kesshitekesenaibokuranokodou",
            "ko": "결코 꺼뜨릴 수 없는 우리들의 뜨거운 고동",
            "charRomaji": [
              "kes",
              "shi",
              "te",
              "ke",
              "se",
              "na",
              "i",
              "boku",
              "ra",
              "no",
              "ko",
              "dou"
            ]
          },
          {
            "ja": "燃え盛る情熱を胸に抱いて",
            "romaji": "moemorujounetsuwomunenidaite",
            "ko": "활활 타오르는 정열을 가슴에 품어 안고",
            "charRomaji": [
              "mo",
              "e",
              "mo",
              "ru",
              "jou",
              "netsu",
              "wo",
              "mune",
              "ni",
              "da",
              "i",
              "te"
            ]
          },
          {
            "ja": "暗闇を切り裂く光になれ",
            "romaji": "kurayamiwokirisakuhikarininare",
            "ko": "칠흑 같은 어둠을 베어 가르는 빛이 되어라",
            "charRomaji": [
              "kura",
              "yami",
              "wo",
              "ki",
              "ri",
              "sa",
              "ku",
              "hikari",
              "ni",
              "na",
              "re"
            ]
          },
          {
            "ja": "響け永遠に証命讃歌",
            "romaji": "hibikeeiennishouinochisanka",
            "ko": "영원토록 울려 퍼져라 우리들의 증명찬가여",
            "charRomaji": [
              "hibi",
              "ke",
              "ei",
              "en",
              "ni",
              "shou",
              "inochi",
              "san",
              "ka"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "nonbreath",
    "title": "ノンブレス・オブリージュ",
    "reading": "のんぶれす おぶりーじゅ",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "cdVOlppDwFo",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "ノンブレスノンブレスノンブレスオブリージュ",
            "romaji": "nonburesunonburesunonburesuoburiiju",
            "ko": "논브레스 논브레스 논브레스 오블리주",
            "charRomaji": [
              "no",
              "n",
              "bu",
              "re",
              "su",
              "no",
              "n",
              "bu",
              "re",
              "su",
              "no",
              "n",
              "bu",
              "re",
              "su",
              "o",
              "bu",
              "rii",
              "",
              "j",
              "u"
            ]
          },
          {
            "ja": "息が詰まる息が詰まる息が詰まる街だ",
            "romaji": "ikigatsumaruikigatsumaruikigatsumarumachida",
            "ko": "숨이 턱 막히는, 숨이 막히는, 숨이 꽉 막히는 거리야",
            "charRomaji": [
              "iki",
              "ga",
              "tsu",
              "ma",
              "ru",
              "iki",
              "ga",
              "tsu",
              "ma",
              "ru",
              "iki",
              "ga",
              "tsu",
              "ma",
              "ru",
              "machi",
              "da"
            ]
          },
          {
            "ja": "誰も彼も正しさを振りかざして",
            "romaji": "daremokaremotadashisawofurikazashite",
            "ko": "너나 할 것 없이 올바름을 칼처럼 휘두르며",
            "charRomaji": [
              "dare",
              "mo",
              "kare",
              "mo",
              "tada",
              "shi",
              "sa",
              "wo",
              "fu",
              "ri",
              "ka",
              "za",
              "shi",
              "te"
            ]
          },
          {
            "ja": "誰かを裁くことばかりに夢中だ",
            "romaji": "darekawosabakukotobakarinimuchuuda",
            "ko": "누군가를 심판하는 데에만 푹 빠져 있지",
            "charRomaji": [
              "dare",
              "ka",
              "wo",
              "saba",
              "ku",
              "ko",
              "to",
              "ba",
              "ka",
              "ri",
              "ni",
              "mu",
              "chuu",
              "da"
            ]
          },
          {
            "ja": "酸素を吸って二酸化炭素を吐き出すように",
            "romaji": "sansowosuttenisankatansowohakidasuyouni",
            "ko": "산소를 들이마시고 이산화탄소를 뱉어내듯이",
            "charRomaji": [
              "san",
              "so",
              "wo",
              "su",
              "t",
              "te",
              "ni",
              "san",
              "ka",
              "ta",
              "nso",
              "wo",
              "ha",
              "ki",
              "da",
              "su",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "当たり前のことを当たり前にやりたいだけなのに",
            "romaji": "atarimaenokotowoatarimaeniyaritaidakenanoni",
            "ko": "당연한 것을 당연하게 하고 싶을 뿐인데",
            "charRomaji": [
              "a",
              "ta",
              "ri",
              "mae",
              "no",
              "ko",
              "to",
              "wo",
              "a",
              "ta",
              "ri",
              "mae",
              "ni",
              "ya",
              "ri",
              "ta",
              "i",
              "da",
              "ke",
              "na",
              "no",
              "ni"
            ]
          },
          {
            "ja": "どうしてこんなに苦しいんだろう",
            "romaji": "doushitekonnanikurushiindarou",
            "ko": "어째서 이렇게나 괴롭고 숨 막히는 걸까",
            "charRomaji": [
              "do",
              "u",
              "shi",
              "te",
              "ko",
              "n",
              "na",
              "ni",
              "kuru",
              "shi",
              "i",
              "n",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "僕たちの声は届かないまま",
            "romaji": "bokutachinokoewatodokanaimama",
            "ko": "우리들의 목소리는 닿지 못한 채로",
            "charRomaji": [
              "boku",
              "ta",
              "chi",
              "no",
              "koe",
              "wa",
              "todo",
              "ka",
              "na",
              "i",
              "ma",
              "ma"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "綺麗事ばかり並べたタイムラインをスクロールして",
            "romaji": "kireigotobakarinarabetataimurainwosukuroorushite",
            "ko": "허울 좋은 말만 잔뜩 늘어놓은 타임라인을 스크롤하며",
            "charRomaji": [
              "ki",
              "re",
              "igoto",
              "ba",
              "ka",
              "ri",
              "nara",
              "be",
              "ta",
              "ta",
              "i",
              "mu",
              "ra",
              "i",
              "n",
              "wo",
              "su",
              "ku",
              "roo",
              "",
              "ru",
              "shi",
              "te"
            ]
          },
          {
            "ja": "自分の居場所を探してみてもどこにもない",
            "romaji": "jibunnoibashowosagashitemitemodokonimonai",
            "ko": "내가 있을 자리를 찾아보아도 어디에도 없어",
            "charRomaji": [
              "ji",
              "bun",
              "no",
              "i",
              "ba",
              "sho",
              "wo",
              "saga",
              "shi",
              "te",
              "mi",
              "te",
              "mo",
              "do",
              "ko",
              "ni",
              "mo",
              "na",
              "i"
            ]
          },
          {
            "ja": "それでも僕らは息を止めてはいけないんだ",
            "romaji": "soredemobokurawaikiwotometehaikenainda",
            "ko": "그럼에도 우리들은 숨을 멈춰서는 안 되는 거야",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "boku",
              "ra",
              "wa",
              "iki",
              "wo",
              "to",
              "me",
              "te",
              "ha",
              "i",
              "ke",
              "na",
              "i",
              "n",
              "da"
            ]
          },
          {
            "ja": "苦しくてもみっともなくても",
            "romaji": "kurushikutemomittomonakutemo",
            "ko": "괴로울지라도 꼴사나울지라도",
            "charRomaji": [
              "kuru",
              "shi",
              "ku",
              "te",
              "mo",
              "mi",
              "t",
              "to",
              "mo",
              "na",
              "ku",
              "te",
              "mo"
            ]
          },
          {
            "ja": "息を吸って吐いて生き延びてやる",
            "romaji": "ikiwosuttehaiteikinobiteyaru",
            "ko": "숨을 들이마시고 뱉으며 기필코 살아남아 주겠어",
            "charRomaji": [
              "iki",
              "wo",
              "su",
              "t",
              "te",
              "ha",
              "i",
              "te",
              "i",
              "ki",
              "no",
              "bi",
              "te",
              "ya",
              "ru"
            ]
          },
          {
            "ja": "この歪な世界で僕だけの歌を歌いながら",
            "romaji": "konohizunasekaidebokudakenoutawoutainagara",
            "ko": "이 뒤틀린 세상 속에서 나만의 노래를 부르며",
            "charRomaji": [
              "ko",
              "no",
              "hizu",
              "na",
              "se",
              "kai",
              "de",
              "boku",
              "da",
              "ke",
              "no",
              "uta",
              "wo",
              "uta",
              "i",
              "na",
              "ga",
              "ra"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "kiminokamisama",
    "title": "君の神様になりたい。",
    "reading": "きみのかみさまになりたい",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "W8bWP-E7IJE",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "君の神様になりたかった僕の偽善で",
            "romaji": "kiminokamisamaninaritakattabokunogizende",
            "ko": "너의 신이 되고 싶었어, 나의 위선으로",
            "charRomaji": [
              "kimi",
              "no",
              "kami",
              "sama",
              "ni",
              "na",
              "ri",
              "ta",
              "ka",
              "t",
              "ta",
              "boku",
              "no",
              "gi",
              "zen",
              "de"
            ]
          },
          {
            "ja": "誰かを救えるような人間になりたかった",
            "romaji": "darekawosukueruyounaningenninaritakatta",
            "ko": "누군가를 구할 수 있는 그런 인간이 되고 싶었어",
            "charRomaji": [
              "dare",
              "ka",
              "wo",
              "suku",
              "e",
              "ru",
              "yo",
              "u",
              "na",
              "nin",
              "gen",
              "ni",
              "na",
              "ri",
              "ta",
              "ka",
              "t",
              "ta"
            ]
          },
          {
            "ja": "自分のことすら愛せないくせに",
            "romaji": "jibunnokotosuraaisenaikuseni",
            "ko": "자기 자신조차 사랑하지 못하는 주제에",
            "charRomaji": [
              "ji",
              "bun",
              "no",
              "ko",
              "to",
              "su",
              "ra",
              "ai",
              "se",
              "na",
              "i",
              "ku",
              "se",
              "ni"
            ]
          },
          {
            "ja": "誰かの痛みを背負おうとしていた",
            "romaji": "darekanoitamiwoseoioutoshiteita",
            "ko": "누군가의 아픔을 짊어지려 하고 있었지",
            "charRomaji": [
              "dare",
              "ka",
              "no",
              "ita",
              "mi",
              "wo",
              "se",
              "oi",
              "o",
              "u",
              "to",
              "shi",
              "te",
              "i",
              "ta"
            ]
          },
          {
            "ja": "無情な世界を恨んだ目は",
            "romaji": "mujounasekaiwourandamewa",
            "ko": "무정한 세상을 원망하던 눈은",
            "charRomaji": [
              "mu",
              "jou",
              "na",
              "se",
              "kai",
              "wo",
              "ura",
              "n",
              "da",
              "me",
              "wa"
            ]
          },
          {
            "ja": "どうしようもなく愛を欲してた",
            "romaji": "doushiyoumonakuaiwohosshiteta",
            "ko": "어쩔 도리도 없이 사랑을 갈구했지",
            "charRomaji": [
              "do",
              "u",
              "shi",
              "yo",
              "u",
              "mo",
              "na",
              "ku",
              "ai",
              "wo",
              "hos",
              "shi",
              "te",
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
              "nu",
              "re",
              "ru",
              "no",
              "ga",
              "su",
              "ki",
              "da",
              "t",
              "ta"
            ]
          },
          {
            "ja": "曇った顔が似合うから",
            "romaji": "kumottakaoganiaukara",
            "ko": "흐린 얼굴이 어울리니까",
            "charRomaji": [
              "kumo",
              "t",
              "ta",
              "kao",
              "ga",
              "ni",
              "a",
              "u",
              "ka",
              "ra"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "僕の歌で君が救われるなら",
            "romaji": "bokunoutadekimigasukuwarerunara",
            "ko": "나의 노래로 네가 구원받을 수 있다면",
            "charRomaji": [
              "boku",
              "no",
              "uta",
              "de",
              "kimi",
              "ga",
              "suku",
              "wa",
              "re",
              "ru",
              "na",
              "ra"
            ]
          },
          {
            "ja": "この命なんていくらでも削ってやるよ",
            "romaji": "konoinochinanteikurademokezutteyaruyo",
            "ko": "이 목숨 따위 얼마든지 깎아내 주겠어",
            "charRomaji": [
              "ko",
              "no",
              "inochi",
              "na",
              "n",
              "te",
              "i",
              "ku",
              "ra",
              "de",
              "mo",
              "kezu",
              "t",
              "te",
              "ya",
              "ru",
              "yo"
            ]
          },
          {
            "ja": "だけど現実はそんなに甘くなくて",
            "romaji": "dakedogenjitsuhasonnaniamakunakute",
            "ko": "그렇지만 현실은 그렇게 호락호락하지 않아서",
            "charRomaji": [
              "da",
              "ke",
              "do",
              "gen",
              "jitsu",
              "ha",
              "so",
              "n",
              "na",
              "ni",
              "ama",
              "ku",
              "na",
              "ku",
              "te"
            ]
          },
          {
            "ja": "君の涙ひとつ拭えやしないんだ",
            "romaji": "kiminonamidahitotsushokueyashinainda",
            "ko": "너의 눈물 한 방울조차 닦아주지 못하잖아",
            "charRomaji": [
              "kimi",
              "no",
              "namida",
              "hi",
              "to",
              "tsu",
              "shoku",
              "e",
              "ya",
              "shi",
              "na",
              "i",
              "n",
              "da"
            ]
          },
          {
            "ja": "それでも僕は歌うよ君の神様にはなれなくても",
            "romaji": "soredemobokuhautauyokiminokamisamanihanarenakutemo",
            "ko": "그래도 나는 노래할 거야, 너의 신 따윈 될 수 없더라도",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "boku",
              "ha",
              "uta",
              "u",
              "yo",
              "kimi",
              "no",
              "kami",
              "sama",
              "ni",
              "ha",
              "na",
              "re",
              "na",
              "ku",
              "te",
              "mo"
            ]
          },
          {
            "ja": "隣で一緒に迷うことくらいはできるから",
            "romaji": "tonarideisshonimayoukotokuraihadekirukara",
            "ko": "곁에서 함께 헤매어주는 것만큼은 할 수 있으니까",
            "charRomaji": [
              "tonari",
              "de",
              "i",
              "ssho",
              "ni",
              "mayo",
              "u",
              "ko",
              "to",
              "ku",
              "ra",
              "i",
              "ha",
              "de",
              "ki",
              "ru",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "生きろ生きろと叫び続けるよ",
            "romaji": "ikiroikirotosakebitsuzukeruyo",
            "ko": "살아라, 살아라 하고 계속 외쳐줄게",
            "charRomaji": [
              "i",
              "ki",
              "ro",
              "i",
              "ki",
              "ro",
              "to",
              "sake",
              "bi",
              "tsuzu",
              "ke",
              "ru",
              "yo"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "charles",
    "title": "シャルル",
    "reading": "しゃるる",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "IKtjzy0uDkQ",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "さよならはあなたから言った",
            "romaji": "sayonarahaanatakaraitta",
            "ko": "작별은 당신이 먼저 말했지",
            "charRomaji": [
              "sa",
              "yo",
              "na",
              "ra",
              "ha",
              "a",
              "na",
              "ta",
              "ka",
              "ra",
              "i",
              "t",
              "ta"
            ]
          },
          {
            "ja": "それなのに頬を濡らしてしまうの",
            "romaji": "sorenanonihoowonurashiteshimauno",
            "ko": "그런데도 뺨을 적셔버리고 마는 거야",
            "charRomaji": [
              "so",
              "re",
              "na",
              "no",
              "ni",
              "hoo",
              "wo",
              "nu",
              "ra",
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
            "romaji": "souyattekinounokotomokeshiteshimaunara",
            "ko": "그렇게 어제의 일조차 지워버릴 거라면",
            "charRomaji": [
              "so",
              "u",
              "ya",
              "t",
              "te",
              "ki",
              "nou",
              "no",
              "koto",
              "mo",
              "ke",
              "shi",
              "te",
              "shi",
              "ma",
              "u",
              "na",
              "ra"
            ]
          },
          {
            "ja": "もういいよ笑ってくれよ",
            "romaji": "mouiiyowarattekureyo",
            "ko": "이제 됐어, 차라리 비웃어줘",
            "charRomaji": [
              "mo",
              "u",
              "i",
              "i",
              "yo",
              "wara",
              "t",
              "te",
              "ku",
              "re",
              "yo"
            ]
          },
          {
            "ja": "絡みつく愛憎に息が詰まる夜を越えて",
            "romaji": "karamitsukuaizouniikigatsumaruyoruwokoete",
            "ko": "얽혀드는 애증에 숨이 턱 막히는 밤을 넘어서",
            "charRomaji": [
              "kara",
              "mi",
              "tsu",
              "ku",
              "ai",
              "zou",
              "ni",
              "iki",
              "ga",
              "tsu",
              "ma",
              "ru",
              "yoru",
              "wo",
              "ko",
              "e",
              "te"
            ]
          },
          {
            "ja": "僕らはどこへ向かうのだろう",
            "romaji": "bokurahadokohemukaunodarou",
            "ko": "우리들은 어디로 향하는 걸까",
            "charRomaji": [
              "boku",
              "ra",
              "ha",
              "do",
              "ko",
              "he",
              "mu",
              "ka",
              "u",
              "no",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "シャルル踊り明かそうぜこの夜を",
            "romaji": "sharuruodoriakasouzekonoyoruwo",
            "ko": "샤를, 밤새워 춤추자꾸나 이 밤을",
            "charRomaji": [
              "sh",
              "a",
              "ru",
              "ru",
              "odo",
              "ri",
              "a",
              "ka",
              "so",
              "u",
              "ze",
              "ko",
              "no",
              "yoru",
              "wo"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "曖昧な言葉で濁さないで",
            "romaji": "aimainakotobadenigosanaide",
            "ko": "애매한 말로 얼버무리지 말아줘",
            "charRomaji": [
              "ai",
              "mai",
              "na",
              "ko",
              "toba",
              "de",
              "nigo",
              "sa",
              "na",
              "i",
              "de"
            ]
          },
          {
            "ja": "傷つくならいっそ綺麗に引き裂いて",
            "romaji": "kizutsukunaraissokireinihikisaite",
            "ko": "상처받을 거라면 차라리 말끔하게 찢어발겨줘",
            "charRomaji": [
              "kizu",
              "tsu",
              "ku",
              "na",
              "ra",
              "i",
              "s",
              "so",
              "ki",
              "rei",
              "ni",
              "hi",
              "ki",
              "sa",
              "i",
              "te"
            ]
          },
          {
            "ja": "愛していたよなんて過去形で語らないで",
            "romaji": "itoshiteitayonantekakokeidekataranaide",
            "ko": "사랑했었다는 둥 과거형으로 지껄이지 마",
            "charRomaji": [
              "ito",
              "shi",
              "te",
              "i",
              "ta",
              "yo",
              "na",
              "n",
              "te",
              "ka",
              "ko",
              "kei",
              "de",
              "kata",
              "ra",
              "na",
              "i",
              "de"
            ]
          },
          {
            "ja": "今も胸が張り裂けそうなんだから",
            "romaji": "imamomunegaharisakesounandakara",
            "ko": "지금도 가슴이 찢어질 것만 같으니까",
            "charRomaji": [
              "ima",
              "mo",
              "mune",
              "ga",
              "ha",
              "ri",
              "sa",
              "ke",
              "so",
              "u",
              "na",
              "n",
              "da",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "歌い狂え夜が明けるその時まで",
            "romaji": "utaikyoueyorugaakerusonotokimade",
            "ko": "미친 듯이 노래해라, 날이 밝아오는 그 순간까지",
            "charRomaji": [
              "uta",
              "i",
              "kyou",
              "e",
              "yoru",
              "ga",
              "a",
              "ke",
              "ru",
              "so",
              "no",
              "toki",
              "ma",
              "de"
            ]
          },
          {
            "ja": "僕らの青春はまだ終わらない",
            "romaji": "bokuranoseishunhamadaowaranai",
            "ko": "우리들의 청춘은 아직 끝나지 않았어",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "se",
              "ishun",
              "ha",
              "ma",
              "da",
              "o",
              "wa",
              "ra",
              "na",
              "i"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "swim",
    "title": "swim",
    "reading": "すいむ",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "AEZ7suhPML0",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "泳いで泳いで波をかき分けて",
            "romaji": "oyoideoyoidenamiwokakiwakete",
            "ko": "헤엄치고 헤엄쳐서 거센 파도를 헤치며",
            "charRomaji": [
              "oyo",
              "i",
              "de",
              "oyo",
              "i",
              "de",
              "nami",
              "wo",
              "ka",
              "ki",
              "wa",
              "ke",
              "te"
            ]
          },
          {
            "ja": "息継ぎさえ忘れるくらい夢中で",
            "romaji": "ikitsugisaewasurerukuraimuchuude",
            "ko": "숨 쉬는 것조차 잊어버릴 만큼 정신없이",
            "charRomaji": [
              "iki",
              "tsu",
              "gi",
              "sa",
              "e",
              "wasu",
              "re",
              "ru",
              "ku",
              "ra",
              "i",
              "mu",
              "chuu",
              "de"
            ]
          },
          {
            "ja": "冷たい水が身体を包んでも",
            "romaji": "tsumetaimizugashintaiwotsutsundemo",
            "ko": "차가운 물이 온몸을 휘감아도",
            "charRomaji": [
              "tsume",
              "ta",
              "i",
              "mizu",
              "ga",
              "shi",
              "ntai",
              "wo",
              "tsutsu",
              "n",
              "de",
              "mo"
            ]
          },
          {
            "ja": "前に進むことだけをやめない",
            "romaji": "maenisusumukotodakewoyamenai",
            "ko": "앞으로 나아가는 것만을 멈추지 않아",
            "charRomaji": [
              "mae",
              "ni",
              "susu",
              "mu",
              "ko",
              "to",
              "da",
              "ke",
              "wo",
              "ya",
              "me",
              "na",
              "i"
            ]
          },
          {
            "ja": "沈んでいきそうな孤独の海で",
            "romaji": "shizundeikisounakodokunoumide",
            "ko": "가라앉아 버릴 것만 같은 고독의 바다에서",
            "charRomaji": [
              "shizu",
              "n",
              "de",
              "i",
              "ki",
              "so",
              "u",
              "na",
              "ko",
              "doku",
              "no",
              "umi",
              "de"
            ]
          },
          {
            "ja": "君の手を探し続けているんだ",
            "romaji": "kiminotewosagashitsuzuketeirunda",
            "ko": "너의 손을 쉼 없이 찾아 헤매고 있어",
            "charRomaji": [
              "kimi",
              "no",
              "te",
              "wo",
              "saga",
              "shi",
              "tsuzu",
              "ke",
              "te",
              "i",
              "ru",
              "n",
              "da"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "光の射す水面を目指して蹴り上げる",
            "romaji": "hikarinosasusuimenwomezashitekeriageru",
            "ko": "빛이 내리쬐는 수면을 향해 힘껏 발장구를 쳐",
            "charRomaji": [
              "hikari",
              "no",
              "sa",
              "su",
              "sui",
              "men",
              "wo",
              "me",
              "za",
              "shi",
              "te",
              "ke",
              "ri",
              "a",
              "ge",
              "ru"
            ]
          },
          {
            "ja": "僕らの夏はまだ終わっちゃいない",
            "romaji": "bokuranonatsuhamadaowatchainai",
            "ko": "우리들의 눈부신 여름은 아직 끝나지 않았어",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "natsu",
              "ha",
              "ma",
              "da",
              "o",
              "wa",
              "t",
              "ch",
              "a",
              "i",
              "na",
              "i"
            ]
          },
          {
            "ja": "息を切らして笑い合える日まで",
            "romaji": "ikiwokirashitewaraiaeruhimade",
            "ko": "숨을 헐떡이며 함께 마주 보고 웃을 날까지",
            "charRomaji": [
              "iki",
              "wo",
              "ki",
              "ra",
              "shi",
              "te",
              "wara",
              "i",
              "a",
              "e",
              "r",
              "uhi",
              "ma",
              "de"
            ]
          },
          {
            "ja": "この青い海をどこまでも泳ぎ抜く",
            "romaji": "konoaoiumiwodokomademooyoginuku",
            "ko": "이 푸르른 바다를 어디까지고 헤엄쳐 나가리라",
            "charRomaji": [
              "ko",
              "no",
              "ao",
              "i",
              "umi",
              "wo",
              "do",
              "ko",
              "ma",
              "de",
              "mo",
              "oyo",
              "gi",
              "nu",
              "ku"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "seishuncomplex",
    "title": "青春コンプレックス",
    "reading": "せいしゅんこんぷれっくす",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "V_PDo4_K8OI",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (1番・A/Bメロ)",
        "lines": [
          {
            "ja": "暗く狭いのが好きだった",
            "romaji": "kurakusemainogasukidatta",
            "ko": "어둡고 좁은 곳이 좋았어",
            "charRomaji": [
              "kura",
              "ku",
              "sema",
              "i",
              "no",
              "ga",
              "su",
              "ki",
              "da",
              "t",
              "ta"
            ]
          },
          {
            "ja": "深く被るフードの中",
            "romaji": "fukakukoumurufuudononaka",
            "ko": "깊게 눌러쓴 후드 속",
            "charRomaji": [
              "fuka",
              "ku",
              "koumu",
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
            "romaji": "mujounasekaiwourandamewa",
            "ko": "무정한 세상을 원망하던 눈은",
            "charRomaji": [
              "mu",
              "jou",
              "na",
              "se",
              "kai",
              "wo",
              "ura",
              "n",
              "da",
              "me",
              "wa"
            ]
          },
          {
            "ja": "どうしようもなく愛を欲してた",
            "romaji": "doushiyoumonakuaiwohosshiteta",
            "ko": "어쩔 도리도 없이 사랑을 갈구했지",
            "charRomaji": [
              "do",
              "u",
              "shi",
              "yo",
              "u",
              "mo",
              "na",
              "ku",
              "ai",
              "wo",
              "hos",
              "shi",
              "te",
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
              "nu",
              "re",
              "ru",
              "no",
              "ga",
              "su",
              "ki",
              "da",
              "t",
              "ta"
            ]
          },
          {
            "ja": "曇った顔が似合うから",
            "romaji": "kumottakaoganiaukara",
            "ko": "흐린 얼굴이 어울리니까",
            "charRomaji": [
              "kumo",
              "t",
              "ta",
              "kao",
              "ga",
              "ni",
              "a",
              "u",
              "ka",
              "ra"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (サビ・大暴走)",
        "lines": [
          {
            "ja": "嵐に怯えてるフリをして",
            "romaji": "arashiniobieterufuriwoshite",
            "ko": "폭풍을 무서워하는 척을 하며",
            "charRomaji": [
              "arashi",
              "ni",
              "obi",
              "e",
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
              "wa",
              "re",
              "ru",
              "no",
              "wo",
              "ma",
              "t",
              "te",
              "i",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "かき鳴らせ光のファズで",
            "romaji": "kakinarasehikarinofazude",
            "ko": "가볍게 긁어 울려라, 빛의 퍼즈로",
            "charRomaji": [
              "ka",
              "ki",
              "na",
              "ra",
              "se",
              "hikari",
              "no",
              "f",
              "a",
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
              "ka",
              "se",
              "ta",
              "i",
              "n",
              "da"
            ]
          },
          {
            "ja": "打ち鳴らせ痛みの先へ",
            "romaji": "uchinaraseitaminosakihe",
            "ko": "두드려 울려라, 아픔의 저편으로",
            "charRomaji": [
              "u",
              "chi",
              "na",
              "ra",
              "se",
              "ita",
              "mi",
              "no",
              "saki",
              "he"
            ]
          },
          {
            "ja": "どうしよう大暴走獰猛な鼓動を",
            "romaji": "doushiyoudaibousoudoumounakodouwo",
            "ko": "어떡하지 대폭주! 사나운 고동을",
            "charRomaji": [
              "do",
              "u",
              "shi",
              "yo",
              "u",
              "dai",
              "bou",
              "sou",
              "do",
              "umou",
              "na",
              "ko",
              "dou",
              "wo"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "naimononedari",
    "title": "ないものねだり",
    "reading": "ないものねだり",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "07Qzp6RlybE",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (1番・サビ)",
        "lines": [
          {
            "ja": "いつだってわがままばっかで",
            "ko": "언제나 제멋대로 굴기만 하고",
            "romaji": "itsudattewagamamabakkade",
            "charRomaji": [
              "i",
              "tsu",
              "da",
              "t",
              "te",
              "wa",
              "ga",
              "ma",
              "ma",
              "ba",
              "k",
              "ka",
              "de"
            ]
          },
          {
            "ja": "子供みたいねって笑われた",
            "ko": "아이 같다고 웃음거리가 되었지",
            "romaji": "kodomomitainettewarawareta",
            "charRomaji": [
              "ko",
              "domo",
              "mi",
              "ta",
              "i",
              "ne",
              "t",
              "te",
              "wara",
              "wa",
              "re",
              "ta"
            ]
          },
          {
            "ja": "ゆらゆら揺れる僕の心",
            "ko": "흔들흔들 흔들리는 내 마음",
            "romaji": "yurayurayurerubokunokokoro",
            "charRomaji": [
              "yu",
              "ra",
              "yu",
              "ra",
              "yu",
              "re",
              "ru",
              "boku",
              "no",
              "kokoro"
            ]
          },
          {
            "ja": "風に吹かれてどこへゆく",
            "ko": "바람에 날려 어디로 가나",
            "romaji": "kazenifukaretedokoheyuku",
            "charRomaji": [
              "kaze",
              "ni",
              "fu",
              "ka",
              "re",
              "te",
              "do",
              "ko",
              "he",
              "yu",
              "ku"
            ]
          },
          {
            "ja": "ないものねだりの僕らは",
            "ko": "없는 것만 탐내는 우리들은",
            "romaji": "naimononedarinobokurawa",
            "charRomaji": [
              "na",
              "i",
              "mo",
              "no",
              "ne",
              "da",
              "ri",
              "no",
              "boku",
              "ra",
              "wa"
            ]
          },
          {
            "ja": "いつまで経っても満たされない",
            "ko": "언제까지 지나도 채워지지 않아",
            "romaji": "itsumadehettemomitasarenai",
            "charRomaji": [
              "i",
              "tsu",
              "ma",
              "de",
              "he",
              "t",
              "te",
              "mo",
              "mi",
              "ta",
              "sa",
              "re",
              "na",
              "i"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (サビ・ラスト)",
        "lines": [
          {
            "ja": "ああ言えばこう言う君の",
            "ko": "이 말 하면 저 말 하는 너의",
            "romaji": "aaiebakouiukimino",
            "charRomaji": [
              "a",
              "a",
              "i",
              "e",
              "ba",
              "ko",
              "u",
              "i",
              "u",
              "kimi",
              "no"
            ]
          },
          {
            "ja": "屁理屈に嫌気がさした",
            "ko": "억지 부림에 싫증이 났어",
            "romaji": "herikutsuniiyakegasashita",
            "charRomaji": [
              "he",
              "ri",
              "kutsu",
              "ni",
              "iya",
              "ke",
              "ga",
              "sa",
              "shi",
              "ta"
            ]
          },
          {
            "ja": "波に身を任せて泳いでく",
            "ko": "파도에 몸을 맡기고 헤엄쳐 가",
            "romaji": "naminimiwomakaseteoyoideku",
            "charRomaji": [
              "nami",
              "ni",
              "mi",
              "wo",
              "maka",
              "se",
              "te",
              "oyo",
              "i",
              "de",
              "ku"
            ]
          },
          {
            "ja": "愛されたいと願うほど",
            "ko": "사랑받고 싶다고 바랄수록",
            "romaji": "aisaretaitonegauhodo",
            "charRomaji": [
              "ai",
              "sa",
              "re",
              "ta",
              "i",
              "to",
              "nega",
              "u",
              "ho",
              "do"
            ]
          },
          {
            "ja": "空回りして傷ついて",
            "ko": "겉돌기만 하고 상처 입고",
            "romaji": "karamawarishitekizutsuite",
            "charRomaji": [
              "ka",
              "ramawa",
              "ri",
              "shi",
              "te",
              "kizu",
              "tsu",
              "i",
              "te"
            ]
          },
          {
            "ja": "それでも手を伸ばし続けた",
            "ko": "그래도 손을 계속 뻗었지",
            "romaji": "soredemotewonobashitsuzuketa",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "te",
              "wo",
              "no",
              "ba",
              "shi",
              "tsuzu",
              "ke",
              "ta"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "moudoku",
    "title": "猛独が襲う",
    "reading": "もうどくがおそう",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "IrOg6rQx9wI",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (1番・サビ)",
        "lines": [
          {
            "ja": "春を告げる雨が降り止んだら",
            "ko": "봄을 알리는 비가 그치면",
            "romaji": "haruwotsugeruamegaoriyandara",
            "charRomaji": [
              "haru",
              "wo",
              "tsu",
              "ge",
              "ru",
              "ame",
              "ga",
              "o",
              "ri",
              "ya",
              "n",
              "da",
              "ra"
            ]
          },
          {
            "ja": "少しだけ前を向いて歩こう",
            "ko": "조금만 앞을 향해 걸어가자",
            "romaji": "sukoshidakemaewomuitearukou",
            "charRomaji": [
              "suko",
              "shi",
              "da",
              "ke",
              "mae",
              "wo",
              "mu",
              "i",
              "te",
              "aru",
              "ko",
              "u"
            ]
          },
          {
            "ja": "心に染み付いた冷たさを",
            "ko": "마음에 물든 차가움을",
            "romaji": "kokoronisomitsuitatsumetasawo",
            "charRomaji": [
              "kokoro",
              "ni",
              "so",
              "mi",
              "tsu",
              "i",
              "ta",
              "tsume",
              "ta",
              "sa",
              "wo"
            ]
          },
          {
            "ja": "忘れられたらいいのにな",
            "ko": "잊을 수 있다면 좋을 텐데",
            "romaji": "wasureraretaraiinonina",
            "charRomaji": [
              "wasu",
              "re",
              "ra",
              "re",
              "ta",
              "ra",
              "i",
              "i",
              "no",
              "ni",
              "na"
            ]
          },
          {
            "ja": "猛毒が身体を蝕んでいく",
            "ko": "맹독이 몸을 좀먹어 가",
            "romaji": "moudokugashintaiwoshokundeiku",
            "charRomaji": [
              "mou",
              "doku",
              "ga",
              "shi",
              "ntai",
              "wo",
              "shoku",
              "n",
              "de",
              "i",
              "ku"
            ]
          },
          {
            "ja": "息もできないほどの痛みを",
            "ko": "숨도 쉴 수 없을 만큼의 아픔을",
            "romaji": "ikimodekinaihodonoitamiwo",
            "charRomaji": [
              "iki",
              "mo",
              "de",
              "ki",
              "na",
              "i",
              "ho",
              "do",
              "no",
              "ita",
              "mi",
              "wo"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (サビ・ラスト)",
        "lines": [
          {
            "ja": "誰かのせいにしたって",
            "ko": "남 탓을 해 봤자",
            "romaji": "darekanoseinishitatte",
            "charRomaji": [
              "dare",
              "ka",
              "no",
              "se",
              "i",
              "ni",
              "shi",
              "ta",
              "t",
              "te"
            ]
          },
          {
            "ja": "何も変わりはしないから",
            "ko": "아무것도 변하지 않으니까",
            "romaji": "nanimokawarihashinaikara",
            "charRomaji": [
              "nani",
              "mo",
              "ka",
              "wa",
              "ri",
              "ha",
              "shi",
              "na",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "それでも僕らは叫んでる",
            "ko": "그래도 우리들은 외치고 있어",
            "romaji": "soredemobokurawasakenderu",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "boku",
              "ra",
              "wa",
              "sake",
              "n",
              "de",
              "ru"
            ]
          },
          {
            "ja": "声が枯れるその時まで",
            "ko": "목소리가 쉴 그 순간까지",
            "romaji": "koegakarerusonotokimade",
            "charRomaji": [
              "koe",
              "ga",
              "ka",
              "re",
              "ru",
              "so",
              "no",
              "toki",
              "ma",
              "de"
            ]
          },
          {
            "ja": "生きている理由を探して",
            "ko": "살아가는 이유를 찾아서",
            "romaji": "ikiteiruriyuuwosagashite",
            "charRomaji": [
              "i",
              "ki",
              "te",
              "i",
              "ru",
              "ri",
              "yuu",
              "wo",
              "saga",
              "shi",
              "te"
            ]
          },
          {
            "ja": "明日への一歩を踏み出す",
            "ko": "내일을 향한 한 걸음을 내딛네",
            "romaji": "ashitahenoippowofumidasu",
            "charRomaji": [
              "a",
              "shita",
              "he",
              "no",
              "i",
              "ppo",
              "wo",
              "fu",
              "mi",
              "da",
              "su"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "whitenoise",
    "title": "ホワイトノイズ",
    "reading": "ほわいとのいず",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "oea788qfTug",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (1番・サビ)",
        "lines": [
          {
            "ja": "街を切り裂くような排気音が",
            "ko": "거리를 가르는 듯한 배기음이",
            "romaji": "machiwokirisakuyounahaikionga",
            "charRomaji": [
              "machi",
              "wo",
              "ki",
              "ri",
              "sa",
              "ku",
              "yo",
              "u",
              "na",
              "hai",
              "ki",
              "on",
              "ga"
            ]
          },
          {
            "ja": "足元で唸っている",
            "ko": "발밑에서 울부짖고 있어",
            "romaji": "ashimotodeunatteiru",
            "charRomaji": [
              "ashi",
              "moto",
              "de",
              "una",
              "t",
              "te",
              "i",
              "ru"
            ]
          },
          {
            "ja": "猛スピードで進む世界で",
            "ko": "맹렬한 스피드로 나아가는 세계에서",
            "romaji": "takeshisupiidodesusumusekaide",
            "charRomaji": [
              "takeshi",
              "su",
              "pii",
              "",
              "do",
              "de",
              "susu",
              "mu",
              "se",
              "kai",
              "de"
            ]
          },
          {
            "ja": "取り残された僕の影",
            "ko": "뒤처져 남겨진 나의 그림자",
            "romaji": "torinokosaretabokunokage",
            "charRomaji": [
              "to",
              "ri",
              "noko",
              "sa",
              "re",
              "ta",
              "boku",
              "no",
              "kage"
            ]
          },
          {
            "ja": "ヒーローなんていなくても",
            "ko": "히어로 같은 건 없어도",
            "romaji": "hiiroonanteinakutemo",
            "charRomaji": [
              "hi",
              "",
              "iroo",
              "",
              "na",
              "n",
              "te",
              "i",
              "na",
              "ku",
              "te",
              "mo"
            ]
          },
          {
            "ja": "立ち上がらなきゃいけないんだ",
            "ko": "일어서야만 해",
            "romaji": "tachiagaranakyaikenainda",
            "charRomaji": [
              "ta",
              "chi",
              "a",
              "ga",
              "ra",
              "na",
              "ky",
              "a",
              "i",
              "ke",
              "na",
              "i",
              "n",
              "da"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (サビ・ラスト)",
        "lines": [
          {
            "ja": "瓦礫の下に埋もれた声を",
            "ko": "잔해 밑에 묻힌 목소리를",
            "romaji": "garekinoshitaniumoretakoewo",
            "charRomaji": [
              "ga",
              "reki",
              "no",
              "shita",
              "ni",
              "u",
              "mo",
              "re",
              "ta",
              "koe",
              "wo"
            ]
          },
          {
            "ja": "誰かが見つけてくれるはず",
            "ko": "누군가가 찾아내 줄 거야",
            "romaji": "darekagamitsuketekureruhazu",
            "charRomaji": [
              "dare",
              "ka",
              "ga",
              "mi",
              "tsu",
              "ke",
              "te",
              "ku",
              "re",
              "ru",
              "ha",
              "zu"
            ]
          },
          {
            "ja": "ホワイトノイズを掻き消して",
            "ko": "화이트 노이즈를 지워 없애며",
            "romaji": "howaitonoizuwokakikeshite",
            "charRomaji": [
              "ho",
              "wa",
              "i",
              "to",
              "no",
              "i",
              "zu",
              "wo",
              "ka",
              "ki",
              "ke",
              "shi",
              "te"
            ]
          },
          {
            "ja": "僕らの歌を響かせる",
            "ko": "우리의 노래를 울려 퍼지게 해",
            "romaji": "bokuranoutawohibikaseru",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "uta",
              "wo",
              "hibi",
              "ka",
              "se",
              "ru"
            ]
          },
          {
            "ja": "痛みを抱えて生きていく",
            "ko": "아픔을 끌어안고 살아가리라",
            "romaji": "itamiwokakaeteikiteiku",
            "charRomaji": [
              "ita",
              "mi",
              "wo",
              "kaka",
              "e",
              "te",
              "i",
              "ki",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "未来をこの手で掴むまで",
            "ko": "미래를 이 손으로 잡을 때까지",
            "romaji": "miraiwokonotedetsukamumade",
            "charRomaji": [
              "mi",
              "rai",
              "wo",
              "ko",
              "no",
              "te",
              "de",
              "tsuka",
              "mu",
              "ma",
              "de"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "soraniutaeba",
    "title": "空に歌えば",
    "reading": "そらにうたえば",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "GvWf3Lh9mvE",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (1番・サビ)",
        "lines": [
          {
            "ja": "虚しさとか悔しさとか",
            "ko": "허무함이나 분함 따위는",
            "romaji": "munashisatokakuyashisatoka",
            "charRomaji": [
              "muna",
              "shi",
              "sa",
              "to",
              "ka",
              "kuya",
              "shi",
              "sa",
              "to",
              "ka"
            ]
          },
          {
            "ja": "全部捨て去ってしまえたら",
            "ko": "전부 던져 버릴 수 있다면",
            "romaji": "zenbusutesatteshimaetara",
            "charRomaji": [
              "zen",
              "bu",
              "su",
              "te",
              "sa",
              "t",
              "te",
              "shi",
              "ma",
              "e",
              "ta",
              "ra"
            ]
          },
          {
            "ja": "どれだけ楽になれるだろう",
            "ko": "얼마나 편해질 수 있을까",
            "romaji": "doredakerakuninarerudarou",
            "charRomaji": [
              "do",
              "re",
              "da",
              "ke",
              "raku",
              "ni",
              "na",
              "re",
              "ru",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "そんなことを考えてた",
            "ko": "그런 생각을 하고 있었어",
            "romaji": "sonnakotowokangaeteta",
            "charRomaji": [
              "so",
              "n",
              "na",
              "ko",
              "to",
              "wo",
              "kanga",
              "e",
              "te",
              "ta"
            ]
          },
          {
            "ja": "空に歌えば届く気がして",
            "ko": "하늘을 향해 노래하면 닿을 것만 같아서",
            "romaji": "soraniutaebatodokukigashite",
            "charRomaji": [
              "sora",
              "ni",
              "uta",
              "e",
              "ba",
              "todo",
              "ku",
              "ki",
              "ga",
              "shi",
              "te"
            ]
          },
          {
            "ja": "力一杯叫び続けた",
            "ko": "온 힘을 다해 계속 소리쳤어",
            "romaji": "chikaraippaisakebitsuzuketa",
            "charRomaji": [
              "chikara",
              "i",
              "ppai",
              "sake",
              "bi",
              "tsuzu",
              "ke",
              "ta"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (サビ・ラスト)",
        "lines": [
          {
            "ja": "泥まみれの靴を見つめて",
            "ko": "진흙투성이인 신발을 바라보며",
            "romaji": "nazumamirenokutsuwomitsumete",
            "charRomaji": [
              "nazu",
              "ma",
              "mi",
              "re",
              "no",
              "kutsu",
              "wo",
              "mi",
              "tsu",
              "me",
              "te"
            ]
          },
          {
            "ja": "歩いてきた道を振り返る",
            "ko": "걸어온 길을 되돌아봐",
            "romaji": "aruitekitamichiwofurikaeru",
            "charRomaji": [
              "aru",
              "i",
              "te",
              "ki",
              "ta",
              "michi",
              "wo",
              "fu",
              "ri",
              "kae",
              "ru"
            ]
          },
          {
            "ja": "諦めることばかり上手になって",
            "ko": "포기하는 것만 익숙해져서",
            "romaji": "akiramerukotobakarijouzuninatte",
            "charRomaji": [
              "akira",
              "me",
              "ru",
              "ko",
              "to",
              "ba",
              "ka",
              "ri",
              "",
              "jouzu",
              "ni",
              "na",
              "t",
              "te"
            ]
          },
          {
            "ja": "それでも消えない炎があった",
            "ko": "그럼에도 꺼지지 않는 불꽃이 있었어",
            "romaji": "soredemokienaihonoogaatta",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "ki",
              "e",
              "na",
              "i",
              "honoo",
              "ga",
              "a",
              "t",
              "ta"
            ]
          },
          {
            "ja": "雨上がりの青空の下",
            "ko": "비 갠 뒤의 푸른 하늘 아래",
            "romaji": "ameagarinoaozoranoshita",
            "charRomaji": [
              "ame",
              "a",
              "ga",
              "ri",
              "no",
              "ao",
              "zora",
              "no",
              "shita"
            ]
          },
          {
            "ja": "もう一度僕らは走り出す",
            "ko": "다시 한 번 우리는 달려나가네",
            "romaji": "mouichidobokurawahashiridasu",
            "charRomaji": [
              "mo",
              "u",
              "ichi",
              "do",
              "boku",
              "ra",
              "wa",
              "hashi",
              "ri",
              "da",
              "su"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "zattouboku",
    "title": "雑踏、僕らの街",
    "reading": "ざっとうぼくらのまち",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "9fH4DBvi5pE",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (1番・サビ)",
        "lines": [
          {
            "ja": "人混みを掻き分けて進む",
            "ko": "인파를 헤치며 나아가는",
            "romaji": "hitogomiwokakiwaketesusumu",
            "charRomaji": [
              "hi",
              "togo",
              "mi",
              "wo",
              "ka",
              "ki",
              "wa",
              "ke",
              "te",
              "susu",
              "mu"
            ]
          },
          {
            "ja": "誰の目にも映らないまま",
            "ko": "누구의 눈에도 띄지 않은 채",
            "romaji": "darenomenimoutsuranaimama",
            "charRomaji": [
              "dare",
              "no",
              "me",
              "ni",
              "mo",
              "utsu",
              "ra",
              "na",
              "i",
              "ma",
              "ma"
            ]
          },
          {
            "ja": "冷たい風が頬をかすめて",
            "ko": "차가운 바람이 볼을 스치고",
            "romaji": "tsumetaikazegahoowokasumete",
            "charRomaji": [
              "tsume",
              "ta",
              "i",
              "kaze",
              "ga",
              "hoo",
              "wo",
              "ka",
              "su",
              "me",
              "te"
            ]
          },
          {
            "ja": "孤独の重さを噛み締めた",
            "ko": "고독의 무게를 곱씹었지",
            "romaji": "kodokunoomosawokamishimeta",
            "charRomaji": [
              "ko",
              "doku",
              "no",
              "omo",
              "sa",
              "wo",
              "ka",
              "mi",
              "shi",
              "me",
              "ta"
            ]
          },
          {
            "ja": "雑踏の中で響く叫びは",
            "ko": "북적이는 거리 속에 울리는 외침은",
            "romaji": "zattounonakadehibikusakebiwa",
            "charRomaji": [
              "zat",
              "tou",
              "no",
              "naka",
              "de",
              "hibi",
              "ku",
              "sake",
              "bi",
              "wa"
            ]
          },
          {
            "ja": "誰に届くこともなく消えてく",
            "ko": "누구에게도 닿지 못한 채 사라져 가",
            "romaji": "darenitodokukotomonakukieteku",
            "charRomaji": [
              "dare",
              "ni",
              "todo",
              "ku",
              "ko",
              "to",
              "mo",
              "na",
              "ku",
              "ki",
              "e",
              "te",
              "ku"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (サビ・ラスト)",
        "lines": [
          {
            "ja": "偽りの笑顔なんてもういらない",
            "ko": "거짓된 미소 따윈 이젠 필요 없어",
            "romaji": "itsuwarinoegaonantemouiranai",
            "charRomaji": [
              "itsuwa",
              "ri",
              "no",
              "e",
              "gao",
              "na",
              "n",
              "te",
              "mo",
              "u",
              "i",
              "ra",
              "na",
              "i"
            ]
          },
          {
            "ja": "本音だけでぶつかり合いたい",
            "ko": "진심만으로 온전히 부딪히고 싶어",
            "romaji": "honnedakedebutsukariaitai",
            "charRomaji": [
              "hon",
              "ne",
              "da",
              "ke",
              "de",
              "bu",
              "tsu",
              "ka",
              "ri",
              "a",
              "i",
              "ta",
              "i"
            ]
          },
          {
            "ja": "傷つくことを恐れないで",
            "ko": "상처받는 것을 두려워하지 마",
            "romaji": "kizutsukukotowoosorenaide",
            "charRomaji": [
              "kizu",
              "tsu",
              "ku",
              "ko",
              "to",
              "wo",
              "oso",
              "re",
              "na",
              "i",
              "de"
            ]
          },
          {
            "ja": "この街の片隅から叫べ",
            "ko": "이 거리의 구석에서 외쳐라",
            "romaji": "konomachinokatasumikarasakebe",
            "charRomaji": [
              "ko",
              "no",
              "machi",
              "no",
              "kata",
              "sumi",
              "ka",
              "ra",
              "sake",
              "be"
            ]
          },
          {
            "ja": "間違ってなんかいないと",
            "ko": "결코 틀리지 않았다고",
            "romaji": "machigattenankainaito",
            "charRomaji": [
              "ma",
              "chiga",
              "t",
              "te",
              "na",
              "n",
              "ka",
              "i",
              "na",
              "i",
              "to"
            ]
          },
          {
            "ja": "僕らのロックを響かせろ",
            "ko": "우리들의 록을 울려 퍼지게 해라",
            "romaji": "bokuranorokkuwohibikasero",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "ro",
              "k",
              "ku",
              "wo",
              "hibi",
              "ka",
              "se",
              "ro"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "kakowokurau",
    "title": "過去を喰らう",
    "reading": "かこをくらう",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "ZwDx3We2qL8",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (1番・サビ)",
        "lines": [
          {
            "ja": "思い出なんていらないよ",
            "ko": "추억 따윈 필요 없어",
            "romaji": "omoidenanteiranaiyo",
            "charRomaji": [
              "omo",
              "i",
              "de",
              "na",
              "n",
              "te",
              "i",
              "ra",
              "na",
              "i",
              "yo"
            ]
          },
          {
            "ja": "振り返るたびに痛むから",
            "ko": "뒤돌아볼 때마다 아프니까",
            "romaji": "furikaerutabiniitamukara",
            "charRomaji": [
              "fu",
              "ri",
              "kae",
              "ru",
              "ta",
              "bi",
              "ni",
              "ita",
              "mu",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "過去を喰らって生きていく",
            "ko": "과거를 집어삼키며 살아가리라",
            "romaji": "kakowokuratteikiteiku",
            "charRomaji": [
              "ka",
              "ko",
              "wo",
              "ku",
              "ra",
              "t",
              "te",
              "i",
              "ki",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "化け物になっても構わない",
            "ko": "괴물이 되어도 상관없어",
            "romaji": "bakemononinattemokamawanai",
            "charRomaji": [
              "ba",
              "ke",
              "mono",
              "ni",
              "na",
              "t",
              "te",
              "mo",
              "kama",
              "wa",
              "na",
              "i"
            ]
          },
          {
            "ja": "忘れたいことばかり溢れて",
            "ko": "잊고 싶은 것들만 넘쳐나서",
            "romaji": "wasuretaikotobakariafurete",
            "charRomaji": [
              "wasu",
              "re",
              "ta",
              "i",
              "ko",
              "to",
              "ba",
              "ka",
              "ri",
              "afu",
              "re",
              "te"
            ]
          },
          {
            "ja": "胸の奥が張り裂けそうだ",
            "ko": "가슴속이 찢어질 것만 같아",
            "romaji": "munenookugaharisakesouda",
            "charRomaji": [
              "mune",
              "no",
              "oku",
              "ga",
              "ha",
              "ri",
              "sa",
              "ke",
              "so",
              "u",
              "da"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (サビ・ラスト)",
        "lines": [
          {
            "ja": "誰かの言葉に惑わされず",
            "ko": "누군가의 말에 현혹되지 않고",
            "romaji": "darekanokotobanimadowasarezu",
            "charRomaji": [
              "dare",
              "ka",
              "no",
              "ko",
              "toba",
              "ni",
              "mado",
              "wa",
              "sa",
              "re",
              "zu"
            ]
          },
          {
            "ja": "自分の足で立っていたい",
            "ko": "내 두 발로 서 있고 싶어",
            "romaji": "jibunnoashidetatteitai",
            "charRomaji": [
              "ji",
              "bun",
              "no",
              "ashi",
              "de",
              "ta",
              "t",
              "te",
              "i",
              "ta",
              "i"
            ]
          },
          {
            "ja": "暗闇の中で見つけた光を",
            "ko": "어둠 속에서 찾아낸 빛을",
            "romaji": "kurayaminonakademitsuketahikariwo",
            "charRomaji": [
              "kura",
              "yami",
              "no",
              "naka",
              "de",
              "mi",
              "tsu",
              "ke",
              "ta",
              "hikariw",
              "o"
            ]
          },
          {
            "ja": "決して手放さないように",
            "ko": "결코 손에서 놓지 않도록",
            "romaji": "kesshitetebanasanaiyouni",
            "charRomaji": [
              "kes",
              "shi",
              "te",
              "te",
              "bana",
              "sa",
              "na",
              "i",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "過去を喰らって前を向け",
            "ko": "과거를 집어삼키고 앞을 향해라",
            "romaji": "kakowokurattemaewomuke",
            "charRomaji": [
              "ka",
              "ko",
              "wo",
              "ku",
              "ra",
              "t",
              "te",
              "mae",
              "wo",
              "mu",
              "ke"
            ]
          },
          {
            "ja": "新しい明日が始まるから",
            "ko": "새로운 내일이 시작될 테니까",
            "romaji": "atarashiiashitagahajimarukara",
            "charRomaji": [
              "atara",
              "shi",
              "i",
              "a",
              "shita",
              "ga",
              "haji",
              "ma",
              "ru",
              "ka",
              "ra"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "darekanoshinzou",
    "title": "だれかの心臓になれたなら",
    "reading": "だれかのしんぞうになれたなら",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "IAlgjg6D8Vc",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (1番・サビ)",
        "lines": [
          {
            "ja": "こんな世界と嘆く誰かの",
            "ko": "이런 세상이라며 한탄하는 누군가의",
            "romaji": "konnasekaitonagekudarekano",
            "charRomaji": [
              "ko",
              "n",
              "na",
              "se",
              "kai",
              "to",
              "nage",
              "ku",
              "dare",
              "ka",
              "no"
            ]
          },
          {
            "ja": "心臓になりたかったんだ",
            "ko": "심장이 되고 싶었어",
            "romaji": "shinzouninaritakattanda",
            "charRomaji": [
              "shin",
              "zou",
              "ni",
              "na",
              "ri",
              "ta",
              "ka",
              "t",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "優しさなんて役に立たない",
            "ko": "상냥함 따윈 쓸모도 없는",
            "romaji": "yasashisananteyakunitatanai",
            "charRomaji": [
              "yasa",
              "shi",
              "sa",
              "na",
              "n",
              "te",
              "yaku",
              "ni",
              "ta",
              "ta",
              "na",
              "i"
            ]
          },
          {
            "ja": "そんな現実に抗って",
            "ko": "그런 현실에 맞서 싸우며",
            "romaji": "sonnagenjitsuniaragatte",
            "charRomaji": [
              "so",
              "n",
              "na",
              "gen",
              "jitsu",
              "ni",
              "araga",
              "t",
              "te"
            ]
          },
          {
            "ja": "君の涙を拭うためなら",
            "ko": "너의 눈물을 닦아주기 위해서라면",
            "romaji": "kiminonamidawonuguutamenara",
            "charRomaji": [
              "kimi",
              "no",
              "namidaw",
              "o",
              "nugu",
              "u",
              "ta",
              "me",
              "na",
              "ra"
            ]
          },
          {
            "ja": "僕の命など惜しくない",
            "ko": "내 목숨 따위 아깝지 않아",
            "romaji": "bokunoinochinadooshikunai",
            "charRomaji": [
              "boku",
              "no",
              "inochi",
              "na",
              "do",
              "o",
              "shi",
              "ku",
              "na",
              "i"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (サビ・ラスト)",
        "lines": [
          {
            "ja": "生きる意味を見失っても",
            "ko": "살아가는 의미를 잃어버린대도",
            "romaji": "ikiruimiwomiushinattemo",
            "charRomaji": [
              "i",
              "ki",
              "ru",
              "i",
              "mi",
              "wo",
              "mi",
              "ushina",
              "t",
              "te",
              "mo"
            ]
          },
          {
            "ja": "君の手だけは握りしめる",
            "ko": "너의 손만은 꽉 쥐고 놓지 않아",
            "romaji": "kiminotedakehanigirishimeru",
            "charRomaji": [
              "kimi",
              "no",
              "te",
              "da",
              "ke",
              "ha",
              "nigi",
              "ri",
              "shi",
              "me",
              "ru"
            ]
          },
          {
            "ja": "痛みを分け合える友がいれば",
            "ko": "아픔을 함께 나눌 친구가 있다면",
            "romaji": "itamiwowakeaerutomogaireba",
            "charRomaji": [
              "ita",
              "mi",
              "wo",
              "wa",
              "ke",
              "a",
              "e",
              "ru",
              "tomo",
              "ga",
              "i",
              "re",
              "ba"
            ]
          },
          {
            "ja": "どんな夜も越えていける",
            "ko": "어떤 밤이라도 헤쳐나갈 수 있어",
            "romaji": "donnayorumokoeteikeru",
            "charRomaji": [
              "do",
              "n",
              "na",
              "yoru",
              "mo",
              "ko",
              "e",
              "te",
              "i",
              "ke",
              "ru"
            ]
          },
          {
            "ja": "だれかの心臓になれたなら",
            "ko": "누군가의 심장이 될 수만 있다면",
            "romaji": "darekanoshinzouninaretanara",
            "charRomaji": [
              "da",
              "re",
              "ka",
              "no",
              "shin",
              "zou",
              "ni",
              "na",
              "re",
              "ta",
              "na",
              "ra"
            ]
          },
          {
            "ja": "それだけで僕は救われる",
            "ko": "그것만으로 나는 구원받을 테니까",
            "romaji": "soredakedebokuhasukuwareru",
            "charRomaji": [
              "so",
              "re",
              "da",
              "ke",
              "de",
              "boku",
              "ha",
              "suku",
              "wa",
              "re",
              "ru"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "harukakanata",
    "title": "遙か彼方",
    "reading": "はるかかなた",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "qti2NHsaCu4",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (1番・サビ)",
        "lines": [
          {
            "ja": "踏み込むぜアクセル",
            "ko": "밟아버려 엑셀을",
            "romaji": "fumikomuzeakuseru",
            "charRomaji": [
              "fu",
              "mi",
              "ko",
              "mu",
              "ze",
              "a",
              "ku",
              "se",
              "ru"
            ]
          },
          {
            "ja": "駆け引きなどはいらないさ",
            "ko": "밀고 당기기 따윈 필요 없어",
            "romaji": "kakehikinadohairanaisa",
            "charRomaji": [
              "ka",
              "ke",
              "hi",
              "ki",
              "na",
              "do",
              "ha",
              "i",
              "ra",
              "na",
              "i",
              "sa"
            ]
          },
          {
            "ja": "生き急いで擦り減らして",
            "ko": "삶을 서두르며 닳고 닳아도",
            "romaji": "ikiisoidesuriherashite",
            "charRomaji": [
              "i",
              "ki",
              "iso",
              "i",
              "de",
              "su",
              "ri",
              "he",
              "ra",
              "shi",
              "te"
            ]
          },
          {
            "ja": "点と点を繋ぎ合わせて",
            "ko": "점과 점을 서로 이어붙이며",
            "romaji": "tentotenwotsunagiawasete",
            "charRomaji": [
              "ten",
              "to",
              "ten",
              "wo",
              "tsuna",
              "gi",
              "a",
              "wa",
              "se",
              "te"
            ]
          },
          {
            "ja": "遥か彼方へと飛び出すんだ",
            "ko": "아득한 저 너머로 뛰쳐나가는 거야",
            "romaji": "harukakanatahetotobidasunda",
            "charRomaji": [
              "haru",
              "ka",
              "ka",
              "nata",
              "he",
              "to",
              "to",
              "bi",
              "da",
              "su",
              "n",
              "da"
            ]
          },
          {
            "ja": "迷いなど吹き飛ばして",
            "ko": "망설임 따윈 다 날려버리고",
            "romaji": "mayoinadofukitobashite",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "do",
              "fu",
              "ki",
              "to",
              "ba",
              "shi",
              "te"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (サビ・ラスト)",
        "lines": [
          {
            "ja": "偽りのない景色の中で",
            "ko": "거짓 없는 풍경 속에서",
            "romaji": "itsuwarinonaikeshikinonakade",
            "charRomaji": [
              "itsuwa",
              "ri",
              "no",
              "na",
              "i",
              "ke",
              "shiki",
              "no",
              "naka",
              "de"
            ]
          },
          {
            "ja": "新しい風を感じてる",
            "ko": "새로운 바람을 느끼고 있어",
            "romaji": "atarashiikazewokanjiteru",
            "charRomaji": [
              "atara",
              "shi",
              "i",
              "kaze",
              "wo",
              "kan",
              "ji",
              "te",
              "ru"
            ]
          },
          {
            "ja": "転んだって立ち上がればいい",
            "ko": "넘어진대도 다시 일어서면 돼",
            "romaji": "korondattetachiagarebaii",
            "charRomaji": [
              "koro",
              "n",
              "da",
              "t",
              "te",
              "ta",
              "chi",
              "a",
              "ga",
              "re",
              "ba",
              "i",
              "i"
            ]
          },
          {
            "ja": "失うものなど何もない",
            "ko": "잃을 것 따위 아무것도 없어",
            "romaji": "ushinaumononadonanimonai",
            "charRomaji": [
              "ushina",
              "u",
              "mo",
              "no",
              "na",
              "do",
              "nani",
              "mo",
              "na",
              "i"
            ]
          },
          {
            "ja": "遥か彼方を目指して走れ",
            "ko": "아득한 저 너머를 향해 달려라",
            "romaji": "harukakanatawomezashitehashire",
            "charRomaji": [
              "haru",
              "ka",
              "ka",
              "nata",
              "wo",
              "me",
              "za",
              "shi",
              "te",
              "hashi",
              "re"
            ]
          },
          {
            "ja": "僕らの物語は続く",
            "ko": "우리들의 이야기는 계속된다",
            "romaji": "bokuranomonogatariwatsuzuku",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "mono",
              "gatari",
              "wa",
              "tsuzu",
              "ku"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "egakumirai",
    "title": "エガクミライ",
    "reading": "えがくみらい",
    "category": "original",
    "album": "Digital Single (2025), 3rd Album『致並跡』",
    "youtubeId": "55QclsX-8dg",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "行方不明の本音を探して",
            "romaji": "yukuefumeinohonnewosagashite",
            "ko": "행방불명인 속마음을 찾아서",
            "charRomaji": [
              "yu",
              "kue",
              "fu",
              "mei",
              "no",
              "hon",
              "ne",
              "wo",
              "saga",
              "shi",
              "te"
            ]
          },
          {
            "ja": "迷うからジグザグに降る雨",
            "romaji": "mayoukarajiguzagunifuruame",
            "ko": "방황하기에 지그재그로 내리는 비",
            "charRomaji": [
              "mayo",
              "u",
              "ka",
              "ra",
              "ji",
              "gu",
              "za",
              "gu",
              "ni",
              "fu",
              "ru",
              "ame"
            ]
          },
          {
            "ja": "上り坂の自転車は重くて",
            "romaji": "noborizakanojitenshawaomokute",
            "ko": "오르막길의 자전거는 무거워서",
            "charRomaji": [
              "nobo",
              "ri",
              "zaka",
              "no",
              "ji",
              "ten",
              "sha",
              "wa",
              "omo",
              "ku",
              "te"
            ]
          },
          {
            "ja": "言葉が追いつくまで",
            "romaji": "kotobagaoitsukumade",
            "ko": "말이 따라잡을 때까지",
            "charRomaji": [
              "ko",
              "toba",
              "ga",
              "o",
              "i",
              "tsu",
              "ku",
              "ma",
              "de"
            ]
          },
          {
            "ja": "もう少し待っていて",
            "romaji": "mousukoshimatteite",
            "ko": "조금만 더 기다려줘",
            "charRomaji": [
              "mo",
              "u",
              "suko",
              "shi",
              "ma",
              "t",
              "te",
              "i",
              "te"
            ]
          },
          {
            "ja": "希望に似た何かを",
            "romaji": "kibouninitananikawo",
            "ko": "희망을 닮은 무언가를",
            "charRomaji": [
              "ki",
              "bou",
              "ni",
              "ni",
              "ta",
              "nani",
              "ka",
              "wo"
            ]
          },
          {
            "ja": "勇気に似た何かを",
            "romaji": "yuukininitananikawo",
            "ko": "용기를 닮은 무언가를",
            "charRomaji": [
              "yuu",
              "ki",
              "ni",
              "ni",
              "ta",
              "nani",
              "ka",
              "wo"
            ]
          },
          {
            "ja": "見つけられたらきっと",
            "romaji": "mitsukeraretarakitto",
            "ko": "찾아낼 수 있다면 분명",
            "charRomaji": [
              "mi",
              "tsu",
              "ke",
              "ra",
              "re",
              "ta",
              "ra",
              "ki",
              "t",
              "to"
            ]
          },
          {
            "ja": "なんて夢見て足が震えるほど",
            "romaji": "nanteyumemiteashigafurueruhodo",
            "ko": "그런 꿈을 꾸며 발이 떨릴 정도로",
            "charRomaji": [
              "na",
              "n",
              "te",
              "yume",
              "mi",
              "te",
              "ashi",
              "ga",
              "furu",
              "e",
              "ru",
              "ho",
              "do"
            ]
          },
          {
            "ja": "勇気を奮う事はもう恥ずかしい事じゃないのに",
            "romaji": "yuukiwofuruukotohamouhazukashiikotojanainoni",
            "ko": "용기를 내는 일은 이제 부끄러운 일이 아닌데도",
            "charRomaji": [
              "yuu",
              "ki",
              "wo",
              "furu",
              "u",
              "koto",
              "ha",
              "mo",
              "u",
              "ha",
              "zu",
              "ka",
              "shi",
              "i",
              "koto",
              "j",
              "a",
              "na",
              "i",
              "no",
              "ni"
            ]
          },
          {
            "ja": "描く未来広がる世界",
            "romaji": "egakumiraihirogarusekai",
            "ko": "그려갈 미래, 펼쳐지는 세상",
            "charRomaji": [
              "ega",
              "ku",
              "mi",
              "rai",
              "hiro",
              "ga",
              "ru",
              "se",
              "kai"
            ]
          },
          {
            "ja": "約束の花は散れども僕らはきっと",
            "romaji": "yakusokunohanawachiredomobokurahakitto",
            "ko": "약속의 꽃은 질지라도 우리들은 분명",
            "charRomaji": [
              "yaku",
              "soku",
              "no",
              "hana",
              "wa",
              "chi",
              "re",
              "do",
              "mo",
              "boku",
              "ra",
              "ha",
              "ki",
              "t",
              "to"
            ]
          },
          {
            "ja": "大丈夫だよ君にそう言って欲しかっただけなの",
            "romaji": "daijoubudayokiminisouittehoshikattadakenano",
            "ko": "괜찮아, 네가 그렇게 말해주길 바랐을 뿐이야",
            "charRomaji": [
              "da",
              "i",
              "joubu",
              "da",
              "yo",
              "kimi",
              "ni",
              "so",
              "u",
              "i",
              "t",
              "te",
              "ho",
              "shi",
              "ka",
              "t",
              "ta",
              "da",
              "ke",
              "na",
              "no"
            ]
          },
          {
            "ja": "その声に包まれてみたかったの",
            "romaji": "sonokoenitsutsumaretemitakattano",
            "ko": "그 목소리에 감싸여보고 싶었어",
            "charRomaji": [
              "so",
              "no",
              "koe",
              "ni",
              "tsutsu",
              "ma",
              "re",
              "te",
              "mi",
              "ta",
              "ka",
              "t",
              "ta",
              "no"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "競争の中に身を置く者として",
            "romaji": "kyousounonakanimiwookumonotoshite",
            "ko": "경쟁 속에 몸을 두는 자로서",
            "charRomaji": [
              "kyou",
              "sou",
              "no",
              "naka",
              "ni",
              "mi",
              "wo",
              "o",
              "ku",
              "mono",
              "to",
              "shi",
              "te"
            ]
          },
          {
            "ja": "甘えやか弱さを洗い落として",
            "romaji": "amaeyakayowasawoaraiotoshite",
            "ko": "응석이나 나약함을 씻어내고",
            "charRomaji": [
              "ama",
              "e",
              "ya",
              "ka",
              "yowa",
              "sa",
              "wo",
              "ara",
              "i",
              "o",
              "to",
              "shi",
              "te"
            ]
          },
          {
            "ja": "驕りはなく誇りを灯して",
            "romaji": "ogorihanakuhokoriwotomoshite",
            "ko": "오만함 없이 자부심을 밝히며",
            "charRomaji": [
              "ogo",
              "ri",
              "ha",
              "na",
              "ku",
              "hoko",
              "ri",
              "wo",
              "tomo",
              "shi",
              "te"
            ]
          },
          {
            "ja": "踊り明かすため今振り絞るだけ",
            "romaji": "odoriakasutameimafurishiborudake",
            "ko": "밤새워 춤추기 위해 지금 쥐어짜 낼 뿐",
            "charRomaji": [
              "odo",
              "ri",
              "a",
              "ka",
              "su",
              "ta",
              "me",
              "ima",
              "fu",
              "ri",
              "shibo",
              "ru",
              "da",
              "ke"
            ]
          },
          {
            "ja": "願い事はあるのに",
            "romaji": "negaigotohaarunoni",
            "ko": "이루고픈 소원은 있는데",
            "charRomaji": [
              "nega",
              "i",
              "goto",
              "ha",
              "a",
              "ru",
              "no",
              "ni"
            ]
          },
          {
            "ja": "意地悪な人の空に",
            "romaji": "ijiwarunahitonosorani",
            "ko": "심술궂은 사람들의 하늘에",
            "charRomaji": [
              "i",
              "ji",
              "waru",
              "na",
              "hito",
              "no",
              "sora",
              "ni"
            ]
          },
          {
            "ja": "土砂降りの嘘で道を固められて",
            "romaji": "doshaburinousodemichiwokatamerarete",
            "ko": "억수같이 쏟아지는 거짓말로 길이 굳어져",
            "charRomaji": [
              "do",
              "s",
              "habu",
              "ri",
              "no",
              "uso",
              "de",
              "michi",
              "wo",
              "kata",
              "me",
              "ra",
              "re",
              "te"
            ]
          },
          {
            "ja": "言われた通りにただ歩くだけならば",
            "romaji": "iwaretatourinitadaarukudakenaraba",
            "ko": "그저 시키는 대로 걸어가기만 한다면",
            "charRomaji": [
              "i",
              "wa",
              "re",
              "ta",
              "tou",
              "ri",
              "ni",
              "ta",
              "da",
              "aru",
              "ku",
              "da",
              "ke",
              "na",
              "ra",
              "ba"
            ]
          },
          {
            "ja": "僕らは何のために生きるの",
            "romaji": "bokurawanannotameniikiruno",
            "ko": "우리들은 무엇을 위해 살아가는 걸까",
            "charRomaji": [
              "boku",
              "ra",
              "wa",
              "nan",
              "no",
              "ta",
              "me",
              "ni",
              "i",
              "ki",
              "ru",
              "no"
            ]
          },
          {
            "ja": "描く未来広がる世界",
            "romaji": "egakumiraihirogarusekai",
            "ko": "그려갈 미래, 펼쳐지는 세상",
            "charRomaji": [
              "ega",
              "ku",
              "mi",
              "rai",
              "hiro",
              "ga",
              "ru",
              "se",
              "kai"
            ]
          },
          {
            "ja": "約束の花は散れども僕らはきっと",
            "romaji": "yakusokunohanawachiredomobokurahakitto",
            "ko": "약속의 꽃은 질지라도 우리들은 분명",
            "charRomaji": [
              "yaku",
              "soku",
              "no",
              "hana",
              "wa",
              "chi",
              "re",
              "do",
              "mo",
              "boku",
              "ra",
              "ha",
              "ki",
              "t",
              "to"
            ]
          },
          {
            "ja": "大丈夫だよ君にそう言って欲しかっただけなの",
            "romaji": "daijoubudayokiminisouittehoshikattadakenano",
            "ko": "괜찮아, 네가 그렇게 말해주길 바랐을 뿐이야",
            "charRomaji": [
              "da",
              "i",
              "joubu",
              "da",
              "yo",
              "kimi",
              "ni",
              "so",
              "u",
              "i",
              "t",
              "te",
              "ho",
              "shi",
              "ka",
              "t",
              "ta",
              "da",
              "ke",
              "na",
              "no"
            ]
          },
          {
            "ja": "その声に包まれていたかったの",
            "romaji": "sonokoenitsutsumareteitakattano",
            "ko": "그 목소리에 감싸여 있고 싶었어",
            "charRomaji": [
              "so",
              "no",
              "koe",
              "ni",
              "tsutsu",
              "ma",
              "re",
              "te",
              "i",
              "ta",
              "ka",
              "t",
              "ta",
              "no"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "shoushinshoumei",
    "title": "掌心正銘",
    "reading": "ショウシンショウメイ",
    "category": "original",
    "album": "6th Single『聿日箋秋』c/w, 3rd Album『致並跡』",
    "youtubeId": "Aww91itH5cQ",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "守りたいと思うほどにこれでいいの",
            "romaji": "mamoritaitoomouhodonikoredeiino",
            "ko": "지키고 싶다 생각할수록 이걸로 괜찮은 걸까",
            "charRomaji": [
              "mamo",
              "ri",
              "ta",
              "i",
              "to",
              "omo",
              "u",
              "ho",
              "do",
              "ni",
              "ko",
              "re",
              "de",
              "i",
              "i",
              "no"
            ]
          },
          {
            "ja": "わからなくなってしまうんだ",
            "romaji": "wakaranakunatteshimaunda",
            "ko": "점점 알 수 없게 되어버리고 말아",
            "charRomaji": [
              "wa",
              "ka",
              "ra",
              "na",
              "ku",
              "na",
              "t",
              "te",
              "shi",
              "ma",
              "u",
              "n",
              "da"
            ]
          },
          {
            "ja": "疑心暗鬼めぐらせて無くさないように",
            "romaji": "gishinankimegurasetenakusanaiyouni",
            "ko": "의심암귀를 품고 잃어버리지 않도록",
            "charRomaji": [
              "gi",
              "shin",
              "an",
              "ki",
              "me",
              "gu",
              "ra",
              "se",
              "te",
              "na",
              "ku",
              "sa",
              "na",
              "i",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "手の中強く握りしめては",
            "romaji": "tenonakatsuyokunigirishimeteha",
            "ko": "손안에 너무나 강하게 꽉 쥐어서는",
            "charRomaji": [
              "te",
              "no",
              "naka",
              "tsuyo",
              "ku",
              "nigi",
              "ri",
              "shi",
              "me",
              "te",
              "ha"
            ]
          },
          {
            "ja": "押しつぶしてしまいそうになる",
            "romaji": "oshitsubushiteshimaisouninaru",
            "ko": "그대로 짓눌러 부숴버릴 것만 같아져",
            "charRomaji": [
              "o",
              "shi",
              "tsu",
              "bu",
              "shi",
              "te",
              "shi",
              "ma",
              "i",
              "so",
              "u",
              "ni",
              "na",
              "ru"
            ]
          },
          {
            "ja": "たいせつなんだと伝えたいのに",
            "romaji": "taisetsunandatotsutaetainoni",
            "ko": "소중한 것이라고 전하고 싶은데도",
            "charRomaji": [
              "ta",
              "i",
              "se",
              "tsu",
              "na",
              "n",
              "da",
              "to",
              "tsuta",
              "e",
              "ta",
              "i",
              "no",
              "ni"
            ]
          },
          {
            "ja": "まごついた言葉宙に浮かんでいる",
            "romaji": "magotsuitakotobachuuniukandeiru",
            "ko": "머뭇거린 말들은 허공에 둥둥 떠 있어",
            "charRomaji": [
              "ma",
              "go",
              "tsu",
              "i",
              "ta",
              "ko",
              "toba",
              "chuu",
              "ni",
              "u",
              "ka",
              "n",
              "de",
              "i",
              "ru"
            ]
          },
          {
            "ja": "本当なんだと言えば言うほどに",
            "romaji": "hontounandatoiebaiuhodoni",
            "ko": "진짜라고 말하면 말할수록",
            "charRomaji": [
              "hon",
              "tou",
              "na",
              "n",
              "da",
              "to",
              "i",
              "e",
              "ba",
              "i",
              "u",
              "ho",
              "do",
              "ni"
            ]
          },
          {
            "ja": "ああ偽物になるみたいで",
            "romaji": "aanisemononinarumitaide",
            "ko": "아아 가짜가 되어버리는 것만 같아서",
            "charRomaji": [
              "a",
              "a",
              "nise",
              "mono",
              "ni",
              "na",
              "ru",
              "mi",
              "ta",
              "i",
              "de"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "迷いながらも手繰り寄せた糸",
            "romaji": "mayoinagaramotaguriyosetaito",
            "ko": "방황하면서도 손으로 끌어당긴 인연의 실",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ga",
              "ra",
              "mo",
              "ta",
              "gu",
              "ri",
              "yo",
              "se",
              "ta",
              "ito"
            ]
          },
          {
            "ja": "離してしまえば二度と掴めない",
            "romaji": "hanashiteshimaebanidototsukamenai",
            "ko": "놓쳐버린다면 두 번 다시 잡을 수 없어",
            "charRomaji": [
              "hana",
              "shi",
              "te",
              "shi",
              "ma",
              "e",
              "ba",
              "ni",
              "do",
              "to",
              "tsuka",
              "me",
              "na",
              "i"
            ]
          },
          {
            "ja": "痛みを恐れてちゃ何も始まらない",
            "romaji": "itamiwoosoretechananimohajimaranai",
            "ko": "아픔을 두려워하고만 있어선 아무것도 시작되지 않아",
            "charRomaji": [
              "ita",
              "mi",
              "wo",
              "oso",
              "re",
              "te",
              "ch",
              "a",
              "nani",
              "mo",
              "haji",
              "ma",
              "ra",
              "na",
              "i"
            ]
          },
          {
            "ja": "この掌の熱を信じろ",
            "romaji": "konotenohiranonetsuwoshinjiro",
            "ko": "이 손바닥의 뜨거운 열기를 믿어라",
            "charRomaji": [
              "ko",
              "no",
              "tenohira",
              "no",
              "netsu",
              "wo",
              "shin",
              "ji",
              "ro"
            ]
          },
          {
            "ja": "正真正銘の僕らの声を",
            "romaji": "shoushinshoumeinobokuranokoewo",
            "ko": "정정당당한 우리들의 진실한 목소리를",
            "charRomaji": [
              "s",
              "hou",
              "shinshou",
              "mei",
              "no",
              "boku",
              "ra",
              "no",
              "koe",
              "wo"
            ]
          },
          {
            "ja": "誰にも否定させはしないから",
            "romaji": "darenimohiteisasehashinaikara",
            "ko": "그 누구에게도 부정하게 두지 않을 테니까",
            "charRomaji": [
              "dare",
              "ni",
              "mo",
              "hi",
              "tei",
              "sa",
              "se",
              "ha",
              "shi",
              "na",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "握りしめた想いを解き放て",
            "romaji": "nigirishimetaomoiwotokihoutte",
            "ko": "꽉 쥐고 있던 마음을 시원하게 해방해라",
            "charRomaji": [
              "nigi",
              "ri",
              "shi",
              "me",
              "ta",
              "omo",
              "i",
              "wo",
              "to",
              "ki",
              "hout",
              "te"
            ]
          },
          {
            "ja": "響け未来へ掌心正銘のメロディ",
            "romaji": "hibikemiraihetenohirakokoroshoumeinomerodi",
            "ko": "울려 퍼져라 미래를 향해 진심 어린 멜로디여",
            "charRomaji": [
              "hibi",
              "ke",
              "mi",
              "rai",
              "he",
              "tenohira",
              "kokoro",
              "shou",
              "mei",
              "no",
              "me",
              "ro",
              "d",
              "i"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "zankonji",
    "title": "残痕字",
    "reading": "ページ",
    "category": "original",
    "album": "7th Single『往欄印』c/w, 3rd Album『致並跡』",
    "youtubeId": "lfDO7bvUtn8",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "あの日の記憶消し取ろうと擦ったって",
            "romaji": "anonichinokiokukeshitoroutosatsuttatte",
            "ko": "그날의 기억을 지워 없애려 박박 문질러보아도",
            "charRomaji": [
              "a",
              "no",
              "nichi",
              "no",
              "ki",
              "oku",
              "ke",
              "shi",
              "to",
              "ro",
              "u",
              "to",
              "satsu",
              "t",
              "ta",
              "t",
              "te"
            ]
          },
          {
            "ja": "書きつけた感情痕まだ読めてしまう",
            "romaji": "kakitsuketakanjouatomadayometeshimau",
            "ko": "꾹꾹 눌러쓴 감정의 흔적이 아직 읽히고 말아",
            "charRomaji": [
              "ka",
              "ki",
              "tsu",
              "ke",
              "ta",
              "kan",
              "jou",
              "ato",
              "ma",
              "da",
              "yo",
              "me",
              "te",
              "shi",
              "ma",
              "u"
            ]
          },
          {
            "ja": "無理やり次へめくって書き換えようとしても",
            "romaji": "muriyaritsugihemekuttekakikaeyoutoshitemo",
            "ko": "억지로 다음으로 넘겨 고쳐 쓰려고 해보아도",
            "charRomaji": [
              "mu",
              "ri",
              "ya",
              "ri",
              "tsugi",
              "he",
              "me",
              "ku",
              "t",
              "te",
              "ka",
              "ki",
              "ka",
              "e",
              "yo",
              "u",
              "to",
              "shi",
              "te",
              "mo"
            ]
          },
          {
            "ja": "拭いきれないよ薄雲りが透けてみえて",
            "romaji": "nuguikirenaiyousugumorigasuketemiete",
            "ko": "다 닦아낼 수 없어, 엷은 구름이 비쳐 보여서",
            "charRomaji": [
              "nugu",
              "i",
              "ki",
              "re",
              "na",
              "i",
              "yo",
              "u",
              "sugumo",
              "ri",
              "ga",
              "su",
              "ke",
              "te",
              "mi",
              "e",
              "te"
            ]
          },
          {
            "ja": "怖い夢をみた朝のように揺らいで",
            "romaji": "kowaiyumewomitaasanoyouniyuraide",
            "ko": "무서운 꿈을 꾸고 난 아침처럼 위태롭게 흔들리며",
            "charRomaji": [
              "kowa",
              "i",
              "yume",
              "wo",
              "mi",
              "ta",
              "asa",
              "no",
              "yo",
              "u",
              "ni",
              "yu",
              "ra",
              "i",
              "de"
            ]
          },
          {
            "ja": "残像と知っていてもぐたり弱り果て",
            "romaji": "zanzoutoshitteitemogutariyowarihate",
            "ko": "잔상인 걸 알고 있어도 축 늘어져 맥없이",
            "charRomaji": [
              "zan",
              "zou",
              "to",
              "shi",
              "t",
              "te",
              "i",
              "te",
              "mo",
              "gu",
              "ta",
              "ri",
              "yowa",
              "ri",
              "ha",
              "te"
            ]
          },
          {
            "ja": "動けなくなるんだよ",
            "romaji": "ugokenakunarundayo",
            "ko": "도무지 움직일 수 없게 되어버려",
            "charRomaji": [
              "ugo",
              "ke",
              "na",
              "ku",
              "na",
              "ru",
              "n",
              "da",
              "yo"
            ]
          },
          {
            "ja": "許しきれやしない僕を許せなくて",
            "romaji": "yurushikireyashinaibokuwoyurusenakute",
            "ko": "온전히 용서할 수 없는 나 자신을 용서할 수 없어서",
            "charRomaji": [
              "yuru",
              "shi",
              "ki",
              "re",
              "ya",
              "shi",
              "na",
              "i",
              "boku",
              "wo",
              "yuru",
              "se",
              "na",
              "ku",
              "te"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "大丈夫と笑えない僕は間違いかい",
            "romaji": "daijoubutowaraenaibokuhamachigaikai",
            "ko": "괜찮다며 웃지 못하는 나는 틀려먹은 걸까",
            "charRomaji": [
              "da",
              "i",
              "joubu",
              "to",
              "wara",
              "e",
              "na",
              "i",
              "boku",
              "ha",
              "ma",
              "chiga",
              "i",
              "ka",
              "i"
            ]
          },
          {
            "ja": "だとしても飲み込めないままいるよ",
            "romaji": "datoshitemonomikomenaimamairuyo",
            "ko": "설령 그렇다 해도 차마 삼켜내지 못한 채 있어",
            "charRomaji": [
              "da",
              "to",
              "shi",
              "te",
              "mo",
              "no",
              "mi",
              "ko",
              "me",
              "na",
              "i",
              "ma",
              "ma",
              "i",
              "ru",
              "yo"
            ]
          },
          {
            "ja": "愚かでもきれいな嘘なんかまるで似合わなくて",
            "romaji": "orokademokireinausonankamarudeniawanakute",
            "ko": "어리석을지라도 그럴싸한 거짓말 따윈 전혀 어울리지 않아서",
            "charRomaji": [
              "oro",
              "ka",
              "de",
              "mo",
              "ki",
              "re",
              "i",
              "na",
              "uso",
              "na",
              "n",
              "ka",
              "ma",
              "ru",
              "de",
              "ni",
              "a",
              "wa",
              "na",
              "ku",
              "te"
            ]
          },
          {
            "ja": "ビリビリになった昨日を捨てないで",
            "romaji": "biribirininattakinouwosutenaide",
            "ko": "산산이 찢겨버린 어제를 내버리지 마",
            "charRomaji": [
              "bi",
              "ri",
              "bi",
              "ri",
              "ni",
              "na",
              "t",
              "ta",
              "ki",
              "nou",
              "wo",
              "su",
              "te",
              "na",
              "i",
              "de"
            ]
          },
          {
            "ja": "そっと張り合わせて腕に抱きとめているよ",
            "romaji": "sottohariawaseteudenidakitometeiruyo",
            "ko": "가만히 이어 붙여 품 안에 꼭 껴안고 있어",
            "charRomaji": [
              "so",
              "t",
              "to",
              "ha",
              "ri",
              "a",
              "wa",
              "se",
              "te",
              "ude",
              "ni",
              "da",
              "ki",
              "to",
              "me",
              "te",
              "i",
              "ru",
              "yo"
            ]
          },
          {
            "ja": "まだここにいて",
            "romaji": "madakokoniite",
            "ko": "「아직 여기에 있어 줘」",
            "charRomaji": [
              "ma",
              "da",
              "ko",
              "ko",
              "ni",
              "i",
              "te"
            ]
          },
          {
            "ja": "誤りを消すたびに擦りむけてすすけながら",
            "romaji": "ayamariwokesutabinisurimuketesusukenagara",
            "ko": "잘못을 지울 때마다 살갗이 벗겨지고 그을리면서도",
            "charRomaji": [
              "ayama",
              "ri",
              "wo",
              "ke",
              "su",
              "ta",
              "bi",
              "ni",
              "su",
              "ri",
              "mu",
              "ke",
              "te",
              "su",
              "su",
              "ke",
              "na",
              "ga",
              "ra"
            ]
          },
          {
            "ja": "新しい頁をひらりめくる前に",
            "romaji": "atarashiipeejiwohirarimekurumaeni",
            "ko": "새로운 페이지를 팔랑 넘기기 전에",
            "charRomaji": [
              "atara",
              "shi",
              "i",
              "peeji",
              "wo",
              "hi",
              "ra",
              "ri",
              "me",
              "ku",
              "ru",
              "mae",
              "ni"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "shoujoray",
    "title": "少女レイ",
    "reading": "しょうじょれい",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "DEXX5zBkRjQ",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "本能が狂い始める",
            "romaji": "honnougakuruihajimeru",
            "ko": "본능이 미쳐 날뛰기 시작해",
            "charRomaji": [
              "hon",
              "nou",
              "ga",
              "kuru",
              "i",
              "haji",
              "me",
              "ru"
            ]
          },
          {
            "ja": "追い詰められたハツカネズミ",
            "romaji": "oitsumeraretahatsukanezumi",
            "ko": "막다른 길에 몰려버린 흰생쥐",
            "charRomaji": [
              "o",
              "i",
              "tsu",
              "me",
              "ra",
              "re",
              "ta",
              "ha",
              "tsu",
              "ka",
              "ne",
              "zu",
              "mi"
            ]
          },
          {
            "ja": "今絶望の淵に立って",
            "romaji": "imazetsubounofuchinitatte",
            "ko": "지금 절망의 벼랑 끝에 서서",
            "charRomaji": [
              "ima",
              "zetsu",
              "bou",
              "no",
              "fuchi",
              "ni",
              "ta",
              "t",
              "te"
            ]
          },
          {
            "ja": "踏切へと飛び出した",
            "romaji": "fumikirihetotobidashita",
            "ko": "건널목을 향해 훌쩍 뛰어들었어",
            "charRomaji": [
              "fu",
              "mikirih",
              "e",
              "to",
              "to",
              "bi",
              "da",
              "shi",
              "ta"
            ]
          },
          {
            "ja": "そう君は友達",
            "romaji": "soukimiwatomodachi",
            "ko": "그래, 너는 소중한 친구야",
            "charRomaji": [
              "so",
              "u",
              "kimi",
              "wa",
              "tomo",
              "dachi"
            ]
          },
          {
            "ja": "僕の手を掴めよ",
            "romaji": "bokunotewotsukameyo",
            "ko": "내 손을 꼭 붙잡아",
            "charRomaji": [
              "boku",
              "no",
              "te",
              "wo",
              "tsuka",
              "me",
              "yo"
            ]
          },
          {
            "ja": "そう君は独りさ",
            "romaji": "soukimiwahitorisa",
            "ko": "그래, 너는 철저히 혼자야",
            "charRomaji": [
              "so",
              "u",
              "kimi",
              "wa",
              "hito",
              "ri",
              "sa"
            ]
          },
          {
            "ja": "居場所なんて無いだろ",
            "romaji": "ibashonantenaidaro",
            "ko": "네가 머무를 곳 따윈 어디에도 없잖아",
            "charRomaji": [
              "i",
              "ba",
              "sho",
              "na",
              "n",
              "te",
              "na",
              "i",
              "da",
              "ro"
            ]
          },
          {
            "ja": "涼しい風空を泳ぐ鳥",
            "romaji": "suzushiikazesorawooyogutori",
            "ko": "선선한 바람, 푸른 하늘을 유영하는 새",
            "charRomaji": [
              "suzu",
              "shi",
              "i",
              "kaze",
              "sora",
              "wo",
              "oyo",
              "gu",
              "tori"
            ]
          },
          {
            "ja": "だから哀しくなんかないよ",
            "romaji": "dakarakanashikunankanaiyo",
            "ko": "그러니까 슬프거나 하진 않아",
            "charRomaji": [
              "da",
              "ka",
              "ra",
              "kana",
              "shi",
              "ku",
              "na",
              "n",
              "ka",
              "na",
              "i",
              "yo"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "一つ二つと増えていく",
            "romaji": "hitotsufutattofueteiku",
            "ko": "하나, 둘씩 늘어만 가는",
            "charRomaji": [
              "hito",
              "tsu",
              "futa",
              "t",
              "to",
              "fu",
              "e",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "擦りむいた傷口",
            "romaji": "surimuitakizuguchi",
            "ko": "까져버린 생채기들",
            "charRomaji": [
              "su",
              "ri",
              "mu",
              "i",
              "ta",
              "kizu",
              "guchi"
            ]
          },
          {
            "ja": "痛む胸を隠しながら",
            "romaji": "itamumunewokakushinagara",
            "ko": "욱신대는 가슴을 남몰래 숨기며",
            "charRomaji": [
              "ita",
              "mu",
              "mune",
              "wo",
              "kaku",
              "shi",
              "na",
              "ga",
              "ra"
            ]
          },
          {
            "ja": "笑ってみせた夏の日",
            "romaji": "warattemisetanatsunonichi",
            "ko": "애써 씩 웃어 보였던 눈부신 여름날",
            "charRomaji": [
              "wara",
              "t",
              "te",
              "mi",
              "se",
              "ta",
              "natsu",
              "no",
              "nichi"
            ]
          },
          {
            "ja": "遮断機が降りる音",
            "romaji": "shadankigaoriruoto",
            "ko": "철컥 차단기가 내려가는 소리",
            "charRomaji": [
              "sha",
              "dan",
              "ki",
              "ga",
              "o",
              "ri",
              "ru",
              "oto"
            ]
          },
          {
            "ja": "カンカンと鳴り響いて",
            "romaji": "kankantonarihibiite",
            "ko": "땡땡 소리 내며 울려 퍼지고",
            "charRomaji": [
              "ka",
              "n",
              "ka",
              "n",
              "to",
              "na",
              "ri",
              "hibi",
              "i",
              "te"
            ]
          },
          {
            "ja": "嘘つきな君の影",
            "romaji": "usotsukinakiminokage",
            "ko": "거짓말쟁이였던 너의 아련한 그림자",
            "charRomaji": [
              "uso",
              "tsu",
              "ki",
              "na",
              "kimi",
              "no",
              "kage"
            ]
          },
          {
            "ja": "陽炎の中に消えていく",
            "romaji": "kagerounonakanikieteiku",
            "ko": "아지랑이 낀 공기 속으로 스러져가네",
            "charRomaji": [
              "ka",
              "gerou",
              "no",
              "naka",
              "ni",
              "ki",
              "e",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "少女レイ君のいた夏へ",
            "romaji": "shoujoreikiminoitanatsuhe",
            "ko": "소녀 레이, 네가 머물던 그 여름을 향해",
            "charRomaji": [
              "sho",
              "ujo",
              "re",
              "i",
              "kimi",
              "no",
              "i",
              "ta",
              "natsu",
              "he"
            ]
          },
          {
            "ja": "届かない声を叫ぶんだ",
            "romaji": "todokanaikoewosakebunda",
            "ko": "가닿지 못할 목소리를 외치는 거야",
            "charRomaji": [
              "todo",
              "ka",
              "na",
              "i",
              "koe",
              "wo",
              "sake",
              "bu",
              "n",
              "da"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "pamela",
    "title": "パメラ",
    "reading": "パメラ",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "wbbcQokPgLM",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "長い夜は貴方の事ばかり考えて時を過ごす",
            "romaji": "nagaiyoruwaanatanokotobakarikangaetetokiwosugosu",
            "ko": "길고 긴 밤은 오직 당신 생각만으로 시간을 보내",
            "charRomaji": [
              "naga",
              "i",
              "yoru",
              "wa",
              "a",
              "nata",
              "no",
              "koto",
              "ba",
              "ka",
              "ri",
              "kanga",
              "e",
              "te",
              "toki",
              "wo",
              "su",
              "go",
              "su"
            ]
          },
          {
            "ja": "近づいた夏の気配が",
            "romaji": "chikazuitanatsunokehaiga",
            "ko": "성큼 다가온 여름의 냄새가",
            "charRomaji": [
              "chika",
              "zu",
              "i",
              "ta",
              "natsu",
              "no",
              "ke",
              "hai",
              "ga"
            ]
          },
          {
            "ja": "仄かに鼻を掠めていく",
            "romaji": "honokanihanawokasumeteiku",
            "ko": "은은하게 코끝을 스치고 지나가",
            "charRomaji": [
              "hono",
              "ka",
              "ni",
              "hana",
              "wo",
              "kasu",
              "me",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "曖昧な言葉じゃなくて",
            "romaji": "aimainakotobajanakute",
            "ko": "두루뭉술한 말 따위가 아니라",
            "charRomaji": [
              "ai",
              "mai",
              "na",
              "ko",
              "toba",
              "j",
              "a",
              "na",
              "ku",
              "te"
            ]
          },
          {
            "ja": "確かなものが欲しかった",
            "romaji": "tashikanamonogahosshikatta",
            "ko": "명확하고 확실한 무언가를 원했어",
            "charRomaji": [
              "tashi",
              "ka",
              "na",
              "mo",
              "no",
              "ga",
              "hos",
              "shi",
              "ka",
              "t",
              "ta"
            ]
          },
          {
            "ja": "爛々とした街の灯り",
            "romaji": "ranrantoshitamachinoakari",
            "ko": "휘황찬란하게 번뜩이는 도심의 불빛",
            "charRomaji": [
              "ranra",
              "n",
              "to",
              "shi",
              "ta",
              "machi",
              "no",
              "aka",
              "ri"
            ]
          },
          {
            "ja": "影法師が伸びていく",
            "romaji": "kageboushiganobiteiku",
            "ko": "길쭉한 그림자가 슬며시 늘어져 가",
            "charRomaji": [
              "kage",
              "bou",
              "shi",
              "ga",
              "no",
              "bi",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "パメラ君の言う通り",
            "romaji": "pamerakiminoiutouri",
            "ko": "파멜라, 너의 말대로",
            "charRomaji": [
              "pa",
              "me",
              "ra",
              "kimi",
              "no",
              "i",
              "u",
              "tou",
              "ri"
            ]
          },
          {
            "ja": "くだらない愛を歌おうか",
            "romaji": "kudaranaiaiwoutaouka",
            "ko": "시시껄렁한 사랑 따위를 노래해 볼까",
            "charRomaji": [
              "ku",
              "da",
              "ra",
              "na",
              "i",
              "ai",
              "wo",
              "uta",
              "o",
              "u",
              "ka"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "揺らぐ水面に映る月",
            "romaji": "yuragusuimenniutsurugatsu",
            "ko": "출렁이는 수면에 어리는 달 그림자",
            "charRomaji": [
              "yu",
              "ra",
              "gu",
              "sui",
              "men",
              "ni",
              "utsu",
              "ru",
              "gatsu"
            ]
          },
          {
            "ja": "手を伸ばせば消えてしまう",
            "romaji": "tewonobasebakieteshimau",
            "ko": "손을 뻗으면 허무하게 흩어져버려",
            "charRomaji": [
              "te",
              "wo",
              "no",
              "ba",
              "se",
              "ba",
              "ki",
              "e",
              "te",
              "shi",
              "ma",
              "u"
            ]
          },
          {
            "ja": "狂おしいほどの熱情が",
            "romaji": "kuruoshiihodononetsujouga",
            "ko": "미쳐버릴 것만 같은 격렬한 열정이",
            "charRomaji": [
              "kuru",
              "o",
              "shi",
              "i",
              "ho",
              "do",
              "no",
              "netsu",
              "jou",
              "ga"
            ]
          },
          {
            "ja": "僕の胸を締め付ける",
            "romaji": "bokunomunewoshimetsukeru",
            "ko": "나의 가슴을 빈틈없이 옥죄어와",
            "charRomaji": [
              "boku",
              "no",
              "mune",
              "wo",
              "shi",
              "me",
              "tsu",
              "ke",
              "ru"
            ]
          },
          {
            "ja": "忘れてしまえぬ記憶なら",
            "romaji": "wasureteshimaenukiokunara",
            "ko": "도저히 잊을 수 없는 기억이라면",
            "charRomaji": [
              "wasu",
              "re",
              "te",
              "shi",
              "ma",
              "e",
              "nu",
              "ki",
              "oku",
              "na",
              "ra"
            ]
          },
          {
            "ja": "いっそ全て焼き尽くして",
            "romaji": "issosubeteyakitsukushite",
            "ko": "차라리 몽땅 새하얗게 불태워줘",
            "charRomaji": [
              "i",
              "s",
              "so",
              "sube",
              "te",
              "ya",
              "ki",
              "tsu",
              "ku",
              "shi",
              "te"
            ]
          },
          {
            "ja": "パメラ踊り明かそうよ",
            "romaji": "pameraodoriakasouyo",
            "ko": "파멜라, 날이 밝도록 춤추자꾸나",
            "charRomaji": [
              "pa",
              "me",
              "ra",
              "odo",
              "ri",
              "a",
              "ka",
              "so",
              "u",
              "yo"
            ]
          },
          {
            "ja": "夜が明けてしまう前に",
            "romaji": "yorugaaketeshimaumaeni",
            "ko": "이 밤이 다 새어버리기 전에",
            "charRomaji": [
              "yoru",
              "ga",
              "a",
              "ke",
              "te",
              "shi",
              "ma",
              "u",
              "mae",
              "ni"
            ]
          },
          {
            "ja": "寂しさも孤独も引き連れて",
            "romaji": "sabishisamokodokumohikitsurete",
            "ko": "서글픔도 외로움도 전부 다 끌어안고서",
            "charRomaji": [
              "sabi",
              "shi",
              "sa",
              "mo",
              "ko",
              "doku",
              "mo",
              "hi",
              "ki",
              "tsu",
              "re",
              "te"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "nisokuhokou",
    "title": "二息歩行",
    "reading": "にそくほこう",
    "category": "cover",
    "album": "1st LIVE「僕たちじゃなくなる日」",
    "youtubeId": "q7lbzmTw8RM",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "これは僕の進化の過程の1ページ目です",
            "romaji": "korehabokunoshinkanokateinoichipeejimedesu",
            "ko": "이것은 저의 진화 과정의 첫 번째 페이지입니다",
            "charRomaji": [
              "ko",
              "re",
              "ha",
              "boku",
              "no",
              "shin",
              "ka",
              "no",
              "ka",
              "tei",
              "no",
              "ichi",
              "pee",
              "",
              "ji",
              "me",
              "de",
              "su"
            ]
          },
          {
            "ja": "抱きしめたいから2本足で歩く",
            "romaji": "dakishimetaikaranihonashidearuku",
            "ko": "와락 끌어안고 싶어서 두 발로 걷기 시작해",
            "charRomaji": [
              "da",
              "ki",
              "shi",
              "me",
              "ta",
              "i",
              "ka",
              "ra",
              "ni",
              "hon",
              "ashi",
              "de",
              "aru",
              "ku"
            ]
          },
          {
            "ja": "一人じゃ寂しいから君と息するよ",
            "romaji": "hitorijasabishiikarakimitoikisuruyo",
            "ko": "혼자서는 쓸쓸하니까 너와 함께 숨을 쉬어",
            "charRomaji": [
              "hi",
              "tori",
              "j",
              "a",
              "sabi",
              "shi",
              "i",
              "ka",
              "ra",
              "kimi",
              "to",
              "iki",
              "su",
              "ru",
              "yo"
            ]
          },
          {
            "ja": "ねえママ僕好きな人が出来たんだ",
            "romaji": "neemamabokusukinahitogadekitanda",
            "ko": "있잖아 엄마, 나 좋아하는 사람이 생겼어요",
            "charRomaji": [
              "ne",
              "e",
              "ma",
              "ma",
              "boku",
              "su",
              "ki",
              "na",
              "hito",
              "ga",
              "de",
              "ki",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "おめでとう",
            "romaji": "omedetou",
            "ko": "「축하한단다」",
            "charRomaji": [
              "o",
              "me",
              "de",
              "to",
              "u"
            ]
          },
          {
            "ja": "会いたいよ ねえ君は今頃誰の乳を吸って生きてるの",
            "romaji": "aitaiyoneekimiwaimagorodarenochichiwosutteikiteruno",
            "ko": "보고 싶어, 있잖아 넌 지금쯤 누구의 젖을 빨며 살아가고 있니",
            "charRomaji": [
              "a",
              "i",
              "ta",
              "i",
              "yo",
              "",
              "ne",
              "e",
              "kimi",
              "wa",
              "ima",
              "goro",
              "dare",
              "no",
              "chichiw",
              "o",
              "su",
              "t",
              "te",
              "i",
              "ki",
              "te",
              "ru",
              "no"
            ]
          },
          {
            "ja": "言葉はもう覚えたかな",
            "romaji": "kotobahamouoboetakana",
            "ko": "말은 이제 제법 배웠으려나",
            "charRomaji": [
              "ko",
              "toba",
              "ha",
              "mo",
              "u",
              "obo",
              "e",
              "ta",
              "ka",
              "na"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "パパママごめんねありがとうさようなら",
            "romaji": "papamamagomennearigatousayounara",
            "ko": "아빠 엄마 죄송해요, 고마워요, 안녕히 계세요",
            "charRomaji": [
              "pa",
              "pa",
              "ma",
              "ma",
              "go",
              "me",
              "n",
              "ne",
              "a",
              "ri",
              "ga",
              "to",
              "u",
              "sa",
              "yo",
              "u",
              "na",
              "ra"
            ]
          },
          {
            "ja": "重たいよって泣いてばかりの君を",
            "romaji": "omotaiyottenaitebakarinokimiwo",
            "ko": "「무거워」라며 울기만 하던 너를",
            "charRomaji": [
              "omo",
              "ta",
              "i",
              "yo",
              "t",
              "te",
              "na",
              "i",
              "te",
              "ba",
              "ka",
              "ri",
              "no",
              "kimi",
              "wo"
            ]
          },
          {
            "ja": "抱きしめたのは僕なんだよ",
            "romaji": "dakishimetanohabokunandayo",
            "ko": "품에 꼭 껴안았던 것은 바로 나였어",
            "charRomaji": [
              "da",
              "ki",
              "shi",
              "me",
              "ta",
              "no",
              "ha",
              "boku",
              "na",
              "n",
              "da",
              "yo"
            ]
          },
          {
            "ja": "息を吸って吐いて生きている",
            "romaji": "ikiwosuttehaiteikiteiru",
            "ko": "숨을 들이쉬고 내쉬며 살아가고 있어",
            "charRomaji": [
              "iki",
              "wo",
              "su",
              "t",
              "te",
              "ha",
              "i",
              "te",
              "i",
              "ki",
              "te",
              "i",
              "ru"
            ]
          },
          {
            "ja": "君の言葉に傷ついて",
            "romaji": "kiminokotobanikizutsuite",
            "ko": "네가 던진 말 한마디에 상처 입으면서도",
            "charRomaji": [
              "kimi",
              "no",
              "ko",
              "toba",
              "ni",
              "kizu",
              "tsu",
              "i",
              "te"
            ]
          },
          {
            "ja": "それでも手を繋いで歩いていく",
            "romaji": "soredemotewotsunaidearuiteiku",
            "ko": "그럼에도 손을 꼭 잡고 걸어나가",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "te",
              "wo",
              "tsuna",
              "i",
              "de",
              "aru",
              "i",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "二息歩行の物語",
            "romaji": "niikihokounomonogatari",
            "ko": "두 번 숨 쉬며 걷는 우리들의 이야기",
            "charRomaji": [
              "ni",
              "iki",
              "ho",
              "kou",
              "no",
              "mono",
              "gatari"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "meigenon",
    "title": "明弦音",
    "reading": "アゲイン",
    "category": "original",
    "album": "Digital Single (2024), 2nd Album『跡暖空』",
    "youtubeId": "80n3z8EHRtU",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "まあいいかつぶやく僕は",
            "romaji": "maaiikatsubuyakubokuha",
            "ko": "「뭐 괜찮겠지」 중얼거리는 나는",
            "charRomaji": [
              "ma",
              "a",
              "i",
              "i",
              "ka",
              "tsu",
              "bu",
              "ya",
              "ku",
              "boku",
              "ha"
            ]
          },
          {
            "ja": "諦めたわけじゃなくて",
            "romaji": "akirametawakejanakute",
            "ko": "결코 포기한 게 아니라",
            "charRomaji": [
              "akira",
              "me",
              "ta",
              "wa",
              "ke",
              "j",
              "a",
              "na",
              "ku",
              "te"
            ]
          },
          {
            "ja": "傷つくのが怖くてそっと",
            "romaji": "kizutsukunogakowakutesotto",
            "ko": "상처받는 것이 두려워서 살며시",
            "charRomaji": [
              "kizu",
              "tsu",
              "ku",
              "no",
              "ga",
              "kowa",
              "ku",
              "te",
              "so",
              "t",
              "to"
            ]
          },
          {
            "ja": "予防線を張っていたんだ",
            "romaji": "yobousenwohatteitanda",
            "ko": "예방선을 치고 있었던 거야",
            "charRomaji": [
              "yo",
              "bou",
              "sen",
              "wo",
              "ha",
              "t",
              "te",
              "i",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "転んだ膝をさすりながら",
            "romaji": "korondahizawosasurinagara",
            "ko": "넘어진 무릎을 가만히 어루만지며",
            "charRomaji": [
              "koro",
              "n",
              "da",
              "hiza",
              "wo",
              "sa",
              "su",
              "ri",
              "na",
              "ga",
              "ra"
            ]
          },
          {
            "ja": "また立ち上がれる強さを",
            "romaji": "matatachiagarerutsuyosawo",
            "ko": "다시 일어설 수 있는 강인함을",
            "charRomaji": [
              "ma",
              "ta",
              "ta",
              "chi",
              "a",
              "ga",
              "re",
              "ru",
              "tsuyo",
              "sa",
              "wo"
            ]
          },
          {
            "ja": "探して迷う日々の先へ",
            "romaji": "sagashitemayouhibinosakihe",
            "ko": "찾아 헤매는 나날의 저편으로",
            "charRomaji": [
              "saga",
              "shi",
              "te",
              "mayo",
              "u",
              "hi",
              "bi",
              "no",
              "saki",
              "he"
            ]
          },
          {
            "ja": "鳴り響く明弦音",
            "romaji": "narihibikumeitsuruoto",
            "ko": "울려 퍼지는 어게인의 선율이여",
            "charRomaji": [
              "na",
              "ri",
              "hibi",
              "ku",
              "mei",
              "tsuru",
              "oto"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "弦を弾くたび溢れる想い",
            "romaji": "genwohikutabiafureruomoi",
            "ko": "현을 뜯을 때마다 넘쳐흐르는 진심",
            "charRomaji": [
              "gen",
              "wo",
              "hi",
              "ku",
              "ta",
              "bi",
              "afu",
              "re",
              "ru",
              "omo",
              "i"
            ]
          },
          {
            "ja": "言葉にならなくても伝わる",
            "romaji": "kotobaninaranakutemotsutawaru",
            "ko": "말로 다 되지 않아도 전해질 거야",
            "charRomaji": [
              "ko",
              "toba",
              "ni",
              "na",
              "ra",
              "na",
              "ku",
              "te",
              "mo",
              "tsuta",
              "wa",
              "ru"
            ]
          },
          {
            "ja": "もう一度と叫ぶ心",
            "romaji": "mouichidotosakebukokoro",
            "ko": "「다시 한번」이라고 외치는 마음",
            "charRomaji": [
              "mo",
              "u",
              "ichi",
              "do",
              "to",
              "sake",
              "bu",
              "kokoro"
            ]
          },
          {
            "ja": "アゲイン響かせて進もう",
            "romaji": "ageinhibikasetesusumou",
            "ko": "어게인을 울려 퍼뜨리며 나아가자",
            "charRomaji": [
              "a",
              "ge",
              "i",
              "n",
              "hibi",
              "ka",
              "se",
              "te",
              "susu",
              "mo",
              "u"
            ]
          },
          {
            "ja": "昨日の後悔を抱きしめて",
            "romaji": "kinounokoukaiwodakishimete",
            "ko": "어제의 후회를 품에 꽉 끌어안고",
            "charRomaji": [
              "ki",
              "nou",
              "no",
              "kou",
              "kai",
              "wo",
              "da",
              "ki",
              "shi",
              "me",
              "te"
            ]
          },
          {
            "ja": "新しい朝を迎えに行こう",
            "romaji": "atarashiiasawomukaeniikou",
            "ko": "새로운 아침을 맞이하러 가자",
            "charRomaji": [
              "atara",
              "shi",
              "i",
              "asa",
              "wo",
              "muka",
              "e",
              "ni",
              "i",
              "ko",
              "u"
            ]
          },
          {
            "ja": "僕らの旅路は止まらない",
            "romaji": "bokuranotabijiwatomaranai",
            "ko": "우리들의 여정은 멈추지 않아",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "tabi",
              "ji",
              "wa",
              "to",
              "ma",
              "ra",
              "na",
              "i"
            ]
          },
          {
            "ja": "明日へと響く歌",
            "romaji": "ashitahetohibikuuta",
            "ko": "내일을 향해 울리는 노래",
            "charRomaji": [
              "a",
              "shita",
              "he",
              "to",
              "hibi",
              "ku",
              "uta"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "adayume",
    "title": "過惰幻",
    "reading": "あだゆめ",
    "category": "original",
    "album": "2nd Album『跡暖空』",
    "youtubeId": "aggmsIQMR4I",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "ひたひたと押し寄せてく",
            "romaji": "hitahitatooshiyoseteku",
            "ko": "차츰차츰 서서히 밀려오는",
            "charRomaji": [
              "hi",
              "ta",
              "hi",
              "ta",
              "to",
              "o",
              "shi",
              "yo",
              "se",
              "te",
              "ku"
            ]
          },
          {
            "ja": "憂鬱はおかえりと僕を包み込む",
            "romaji": "yuuutsuhaokaeritobokuwotsutsumikomu",
            "ko": "우울함은 「어서 와」라며 나를 감싸 안아",
            "charRomaji": [
              "yuu",
              "utsu",
              "ha",
              "o",
              "ka",
              "e",
              "ri",
              "to",
              "boku",
              "wo",
              "tsutsu",
              "mi",
              "ko",
              "mu"
            ]
          },
          {
            "ja": "仄暗く冷ややかな空き缶の底で",
            "romaji": "sokukurakuhiyayakanaakikannosokode",
            "ko": "어둑어둑하고 서늘한 빈 캔의 바닥에서",
            "charRomaji": [
              "soku",
              "kura",
              "ku",
              "hi",
              "ya",
              "ya",
              "ka",
              "na",
              "a",
              "ki",
              "kan",
              "no",
              "soko",
              "de"
            ]
          },
          {
            "ja": "雨垂れがぽたぽたと水面を震わせ",
            "romaji": "ametaregapotapotatosuimenwoshinwase",
            "ko": "빗방울이 똑똑 떨어지며 수면을 떨게 해",
            "charRomaji": [
              "ame",
              "ta",
              "re",
              "ga",
              "po",
              "ta",
              "po",
              "ta",
              "to",
              "sui",
              "men",
              "wo",
              "shin",
              "wa",
              "se"
            ]
          },
          {
            "ja": "かなしみに浸かる",
            "romaji": "kanashiminishinkaru",
            "ko": "슬픔 속에 푹 잠겨드네",
            "charRomaji": [
              "ka",
              "na",
              "shi",
              "mi",
              "ni",
              "shin",
              "ka",
              "ru"
            ]
          },
          {
            "ja": "きっと過ぎた夢を見てた",
            "romaji": "kittosugitayumewomiteta",
            "ko": "분명 분에 넘치는 헛된 꿈을 꾸었어",
            "charRomaji": [
              "ki",
              "t",
              "to",
              "su",
              "gi",
              "ta",
              "yume",
              "wo",
              "mi",
              "te",
              "ta"
            ]
          },
          {
            "ja": "到底似合わないのに",
            "romaji": "touteiniawanainoni",
            "ko": "도무지 어울리지도 않는데",
            "charRomaji": [
              "to",
              "utei",
              "ni",
              "a",
              "wa",
              "na",
              "i",
              "no",
              "ni"
            ]
          },
          {
            "ja": "ああ美しい約束がふやけてく",
            "romaji": "aautsukushiiyakusokugafuyaketeku",
            "ko": "아아, 아름다웠던 약속이 퉁퉁 불어터져 가",
            "charRomaji": [
              "a",
              "a",
              "utsuku",
              "shi",
              "i",
              "yaku",
              "soku",
              "ga",
              "fu",
              "ya",
              "ke",
              "te",
              "ku"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "あやまちに気づいても後戻りも出来なくて",
            "romaji": "ayamachinikizuitemoatomodorimodekinakute",
            "ko": "잘못을 깨닫더라도 되돌릴 수조차 없어서",
            "charRomaji": [
              "a",
              "ya",
              "ma",
              "chi",
              "ni",
              "ki",
              "zu",
              "i",
              "te",
              "mo",
              "a",
              "tomodo",
              "ri",
              "mo",
              "de",
              "ki",
              "na",
              "ku",
              "te"
            ]
          },
          {
            "ja": "くずおれる",
            "romaji": "kuzuoreru",
            "ko": "그대로 주저앉고 말아",
            "charRomaji": [
              "ku",
              "zu",
              "o",
              "re",
              "ru"
            ]
          },
          {
            "ja": "どうして飛べそうなんて思ってたんだろう",
            "romaji": "doushitetobesounanteomottetandarou",
            "ko": "어째서 날아오를 수 있을 거라 생각했던 걸까",
            "charRomaji": [
              "do",
              "u",
              "shi",
              "te",
              "to",
              "be",
              "so",
              "u",
              "na",
              "n",
              "te",
              "omo",
              "t",
              "te",
              "ta",
              "n",
              "da",
              "ro",
              "u"
            ]
          },
          {
            "ja": "嬉しかった分だけ苦しみは濃くなって",
            "romaji": "ureshikattafundakekurushimihakokunatte",
            "ko": "기뻤던 그만큼 고통은 더 짙어져서",
            "charRomaji": [
              "ure",
              "shi",
              "ka",
              "t",
              "ta",
              "fun",
              "da",
              "ke",
              "kuru",
              "shi",
              "mi",
              "ha",
              "ko",
              "ku",
              "na",
              "t",
              "te"
            ]
          },
          {
            "ja": "思い知る拙い勘違い",
            "romaji": "omoishiruttanaikanchigai",
            "ko": "뼈저리게 깨닫는 서툰 착각",
            "charRomaji": [
              "omo",
              "i",
              "shi",
              "ru",
              "ttana",
              "i",
              "kan",
              "chiga",
              "i"
            ]
          },
          {
            "ja": "全部まぼろしだったんだね",
            "romaji": "zenbumaboroshidattandane",
            "ko": "모든 게 그저 한낱 환상이었던 거네",
            "charRomaji": [
              "zen",
              "bu",
              "ma",
              "bo",
              "ro",
              "shi",
              "da",
              "t",
              "ta",
              "n",
              "da",
              "ne"
            ]
          },
          {
            "ja": "心の奥へと匿って僕を見せない",
            "romaji": "kokoronookuhetokakuttebokuwomisenai",
            "ko": "마음 깊은 곳으로 숨어들어 나를 보이지 않아",
            "charRomaji": [
              "kokoro",
              "no",
              "oku",
              "he",
              "to",
              "kaku",
              "t",
              "te",
              "boku",
              "wo",
              "mi",
              "se",
              "na",
              "i"
            ]
          },
          {
            "ja": "微塵も望まないはずだった",
            "romaji": "mijinmonozomanaihazudatta",
            "ko": "티끌만큼도 바라지 않았을 터였는데",
            "charRomaji": [
              "mi",
              "jin",
              "mo",
              "nozo",
              "ma",
              "na",
              "i",
              "ha",
              "zu",
              "da",
              "t",
              "ta"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "bokuwa",
    "title": "僕は...",
    "reading": "ぼくは",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "xMyMt9UJaN4",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "言葉にできない感情ばかりが",
            "romaji": "kotobanidekinaikanjoubakariga",
            "ko": "말로 다 표현 못할 감정들만이",
            "charRomaji": [
              "ko",
              "toba",
              "ni",
              "de",
              "ki",
              "na",
              "i",
              "kan",
              "jou",
              "ba",
              "ka",
              "ri",
              "ga"
            ]
          },
          {
            "ja": "胸の奥で渦を巻いているよ",
            "romaji": "munenookudeuzuwomaiteiruyo",
            "ko": "가슴 깊은 곳에서 소용돌이치고 있어",
            "charRomaji": [
              "mune",
              "no",
              "oku",
              "de",
              "uzu",
              "wo",
              "ma",
              "i",
              "te",
              "i",
              "ru",
              "yo"
            ]
          },
          {
            "ja": "君の前だと上手く笑えない",
            "romaji": "kiminomaedatoumakuwaraenai",
            "ko": "너의 앞에서는 잘 웃을 수가 없어",
            "charRomaji": [
              "kimi",
              "no",
              "mae",
              "da",
              "to",
              "u",
              "ma",
              "ku",
              "wara",
              "e",
              "na",
              "i"
            ]
          },
          {
            "ja": "不器用すぎる僕を許してほしい",
            "romaji": "bukiyousugirubokuwoyurushitehoshii",
            "ko": "너무나 서툰 나를 용서해 줬으면 해",
            "charRomaji": [
              "bu",
              "ki",
              "you",
              "su",
              "gi",
              "ru",
              "boku",
              "wo",
              "yuru",
              "shi",
              "te",
              "ho",
              "shi",
              "i"
            ]
          },
          {
            "ja": "伝えたいことはたくさんあるのに",
            "romaji": "tsutaetaikotohatakusanarunoni",
            "ko": "전하고 싶은 말은 너무나 많은데",
            "charRomaji": [
              "tsuta",
              "e",
              "ta",
              "i",
              "ko",
              "to",
              "ha",
              "ta",
              "ku",
              "sa",
              "n",
              "a",
              "ru",
              "no",
              "ni"
            ]
          },
          {
            "ja": "喉の奥でつかえて声にならない",
            "romaji": "nodonookudetsukaetekoeninaranai",
            "ko": "목구멍에서 막혀 목소리가 되질 않아",
            "charRomaji": [
              "nodo",
              "no",
              "oku",
              "de",
              "tsu",
              "ka",
              "e",
              "te",
              "koe",
              "ni",
              "na",
              "ra",
              "na",
              "i"
            ]
          },
          {
            "ja": "それでも君を見つめている",
            "romaji": "soredemokimiwomitsumeteiru",
            "ko": "그럼에도 너를 바라보고 있어",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "kimi",
              "wo",
              "mi",
              "tsu",
              "me",
              "te",
              "i",
              "ru"
            ]
          },
          {
            "ja": "僕の心は叫んでいるんだ",
            "romaji": "bokunokokorohasakendeirunda",
            "ko": "나의 마음은 온 힘을 다해 외치고 있어",
            "charRomaji": [
              "boku",
              "no",
              "kokoro",
              "ha",
              "sake",
              "n",
              "de",
              "i",
              "ru",
              "n",
              "da"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "どんなに格好悪い姿でもいい",
            "romaji": "donnanikakkouwaruisugatademoii",
            "ko": "아무리 꼴사나운 모습이라도 괜찮아",
            "charRomaji": [
              "do",
              "n",
              "na",
              "ni",
              "kak",
              "kou",
              "waru",
              "i",
              "sugata",
              "de",
              "mo",
              "i",
              "i"
            ]
          },
          {
            "ja": "君にだけはこの想いを届けたい",
            "romaji": "kiminidakehakonoomoiwotodoketai",
            "ko": "너에게만큼은 이 진심을 전하고 싶어",
            "charRomaji": [
              "kimi",
              "ni",
              "da",
              "ke",
              "ha",
              "ko",
              "no",
              "omo",
              "i",
              "wo",
              "todo",
              "ke",
              "ta",
              "i"
            ]
          },
          {
            "ja": "僕が僕でいられる理由を",
            "romaji": "bokugabokudeirareruriyuuwo",
            "ko": "내가 나로 존재할 수 있는 이유를",
            "charRomaji": [
              "boku",
              "ga",
              "boku",
              "de",
              "i",
              "ra",
              "re",
              "ru",
              "ri",
              "yuu",
              "wo"
            ]
          },
          {
            "ja": "君が教えてくれたから",
            "romaji": "kimigaoshietekuretakara",
            "ko": "네가 가르쳐 주었으니까",
            "charRomaji": [
              "kimi",
              "ga",
              "oshi",
              "e",
              "te",
              "ku",
              "re",
              "ta",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "溢れ出すメロディに乗せて",
            "romaji": "afuredasumerodininosete",
            "ko": "넘쳐흐르는 멜로디에 실어서",
            "charRomaji": [
              "afu",
              "re",
              "da",
              "su",
              "me",
              "ro",
              "d",
              "i",
              "ni",
              "no",
              "se",
              "te"
            ]
          },
          {
            "ja": "世界で一番眩しい君へ",
            "romaji": "sekaideichibanmabushiikimihe",
            "ko": "세상에서 가장 눈부신 너에게로",
            "charRomaji": [
              "se",
              "kai",
              "de",
              "ichi",
              "ban",
              "mabu",
              "shi",
              "i",
              "kimi",
              "he"
            ]
          },
          {
            "ja": "僕は歌うよありのままに",
            "romaji": "bokuhautauyoarinomamani",
            "ko": "나는 노래할게, 있는 모습 그대로",
            "charRomaji": [
              "boku",
              "ha",
              "uta",
              "u",
              "yo",
              "a",
              "ri",
              "no",
              "ma",
              "ma",
              "ni"
            ]
          },
          {
            "ja": "君の隣で歩んでいきたい",
            "romaji": "kiminotonarideayundeikitai",
            "ko": "너의 곁에서 함께 걸어가고 싶어",
            "charRomaji": [
              "kimi",
              "no",
              "tonari",
              "de",
              "ayu",
              "n",
              "de",
              "i",
              "ki",
              "ta",
              "i"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "tadashikunarenai",
    "title": "正しくなれない",
    "reading": "ただしくなれない",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "azECAVAWRxI",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "正しくなれない僕らの言い訳を",
            "romaji": "tadashikunarenaibokuranoiiwakewo",
            "ko": "올바르게 살지 못하는 우리들의 변명을",
            "charRomaji": [
              "tada",
              "shi",
              "ku",
              "na",
              "re",
              "na",
              "i",
              "boku",
              "ra",
              "no",
              "i",
              "i",
              "wake",
              "wo"
            ]
          },
          {
            "ja": "夜空に撒き散らして笑い飛ばそう",
            "romaji": "yozoranimakichirashitewaraitobasou",
            "ko": "밤하늘에 흩뿌리고 웃어넘기자",
            "charRomaji": [
              "yo",
              "zora",
              "ni",
              "ma",
              "ki",
              "chi",
              "ra",
              "shi",
              "te",
              "wara",
              "i",
              "to",
              "ba",
              "so",
              "u"
            ]
          },
          {
            "ja": "誰かの理想通りになんて",
            "romaji": "darekanorisoutourininante",
            "ko": "누군가의 이상적인 모습대로 따위",
            "charRomaji": [
              "dare",
              "ka",
              "no",
              "ri",
              "sou",
              "tou",
              "ri",
              "ni",
              "na",
              "n",
              "te"
            ]
          },
          {
            "ja": "生きていける器用さはないから",
            "romaji": "ikiteikerukiyousahanaikara",
            "ko": "살아갈 수 있을 만큼 약삭빠르지 않으니까",
            "charRomaji": [
              "i",
              "ki",
              "te",
              "i",
              "ke",
              "ru",
              "ki",
              "you",
              "sa",
              "ha",
              "na",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "歪んだままの感情を抱いて",
            "romaji": "hizundamamanokanjouwodaite",
            "ko": "비뚤어진 채의 감정을 끌어안고",
            "charRomaji": [
              "hizu",
              "n",
              "da",
              "ma",
              "ma",
              "no",
              "kan",
              "jou",
              "wo",
              "da",
              "i",
              "te"
            ]
          },
          {
            "ja": "間違いだらけの道を走る",
            "romaji": "machigaidarakenomichiwohashiru",
            "ko": "실수투성이인 길을 달려간다",
            "charRomaji": [
              "ma",
              "chiga",
              "i",
              "da",
              "ra",
              "ke",
              "no",
              "michi",
              "wo",
              "hashi",
              "ru"
            ]
          },
          {
            "ja": "正しさなんて基準は捨てて",
            "romaji": "tadashisanantekijunwasutete",
            "ko": "올바름이라는 잣대 따윈 던져버려",
            "charRomaji": [
              "tada",
              "shi",
              "sa",
              "na",
              "n",
              "te",
              "ki",
              "jun",
              "wa",
              "su",
              "te",
              "te"
            ]
          },
          {
            "ja": "自分だけの答えを探すんだ",
            "romaji": "jibundakenokotaewosagasunda",
            "ko": "나 자신만의 정답을 찾는 거야",
            "charRomaji": [
              "ji",
              "bun",
              "da",
              "ke",
              "no",
              "kota",
              "e",
              "wo",
              "saga",
              "su",
              "n",
              "da"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "綺麗に整えられた世界に",
            "romaji": "kireinitotonoeraretasekaini",
            "ko": "말끔하게 정돈된 세상에",
            "charRomaji": [
              "ki",
              "rei",
              "ni",
              "totono",
              "e",
              "ra",
              "re",
              "ta",
              "se",
              "kai",
              "ni"
            ]
          },
          {
            "ja": "僕たちの居場所がなくても",
            "romaji": "bokutachinoibashoganakutemo",
            "ko": "우리들이 머물 자리가 없을지라도",
            "charRomaji": [
              "boku",
              "ta",
              "chi",
              "no",
              "i",
              "ba",
              "sho",
              "ga",
              "na",
              "ku",
              "te",
              "mo"
            ]
          },
          {
            "ja": "はみ出した傷だらけの手で",
            "romaji": "hamidashitakizudarakenotede",
            "ko": "삐져나온 상처투성이 손으로",
            "charRomaji": [
              "ha",
              "mi",
              "da",
              "shi",
              "ta",
              "kizu",
              "da",
              "ra",
              "ke",
              "no",
              "te",
              "de"
            ]
          },
          {
            "ja": "新しい音を鳴らし続ける",
            "romaji": "atarashiiotowonarashitsuzukeru",
            "ko": "새로운 소리를 계속 울려 퍼뜨려",
            "charRomaji": [
              "atara",
              "shi",
              "i",
              "oto",
              "wo",
              "na",
              "ra",
              "shi",
              "tsuzu",
              "ke",
              "ru"
            ]
          },
          {
            "ja": "正しくなれないこの生き方を",
            "romaji": "tadashikunarenaikonoikikatawo",
            "ko": "올바르게 살지 못하는 이 삶의 방식을",
            "charRomaji": [
              "tada",
              "shi",
              "ku",
              "na",
              "re",
              "na",
              "i",
              "ko",
              "no",
              "i",
              "ki",
              "kata",
              "wo"
            ]
          },
          {
            "ja": "誇らしく叫んでやろうぜ",
            "romaji": "hokorashikusakendeyarouze",
            "ko": "자랑스럽게 외쳐주자꾸나",
            "charRomaji": [
              "hoko",
              "ra",
              "shi",
              "ku",
              "sake",
              "n",
              "de",
              "ya",
              "ro",
              "u",
              "ze"
            ]
          },
          {
            "ja": "迷いながら創り出す僕らの",
            "romaji": "mayoinagaratsukuridasubokurano",
            "ko": "방황하며 만들어내는 우리들의",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ga",
              "ra",
              "tsuku",
              "ri",
              "da",
              "su",
              "boku",
              "ra",
              "no"
            ]
          },
          {
            "ja": "唯一無二の物語を",
            "romaji": "yuiitsumuninomonogatariwo",
            "ko": "유일무이한 이야기를",
            "charRomaji": [
              "yu",
              "iitsu",
              "mu",
              "ni",
              "no",
              "mono",
              "gatariw",
              "o"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "moshimoinochi",
    "title": "もしも命が描けたら",
    "reading": "もしもいのちがえがけたら",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "uVGIGeTPQVM",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "もしも命が描けたらなら",
            "romaji": "moshimoinochigaegaketaranara",
            "ko": "만약 생명을 그려낼 수 있다면",
            "charRomaji": [
              "mo",
              "shi",
              "mo",
              "inochi",
              "ga",
              "ega",
              "ke",
              "ta",
              "ra",
              "na",
              "ra"
            ]
          },
          {
            "ja": "僕は何を描くだろうか",
            "romaji": "bokuhananiwoegakudarouka",
            "ko": "나는 무엇을 그릴 것인가",
            "charRomaji": [
              "boku",
              "ha",
              "nani",
              "wo",
              "ega",
              "ku",
              "da",
              "ro",
              "u",
              "ka"
            ]
          },
          {
            "ja": "枯れてしまった花のような心に",
            "romaji": "kareteshimattahananoyounakokoroni",
            "ko": "시들어버린 꽃과 같은 마음에",
            "charRomaji": [
              "ka",
              "re",
              "te",
              "shi",
              "ma",
              "t",
              "ta",
              "hana",
              "no",
              "yo",
              "u",
              "na",
              "kokoro",
              "ni"
            ]
          },
          {
            "ja": "色鮮やかな命を吹き込みたい",
            "romaji": "irosenyakanainochiwofukikomitai",
            "ko": "선명한 생명의 빛을 불어넣고 싶어",
            "charRomaji": [
              "iro",
              "sen",
              "ya",
              "ka",
              "na",
              "inochiw",
              "o",
              "fu",
              "ki",
              "ko",
              "mi",
              "ta",
              "i"
            ]
          },
          {
            "ja": "大切な人を笑顔にするため",
            "romaji": "taisetsunahitowoegaonisurutame",
            "ko": "소중한 사람을 웃게 만들기 위해",
            "charRomaji": [
              "tai",
              "setsu",
              "na",
              "hito",
              "wo",
              "e",
              "gao",
              "ni",
              "su",
              "ru",
              "ta",
              "me"
            ]
          },
          {
            "ja": "この命を削ってでも描くよ",
            "romaji": "konoinochiwokezuttedemoegakuyo",
            "ko": "이 목숨을 깎아서라도 그릴 거야",
            "charRomaji": [
              "ko",
              "no",
              "inochiw",
              "o",
              "kezu",
              "t",
              "te",
              "de",
              "mo",
              "ega",
              "ku",
              "yo"
            ]
          },
          {
            "ja": "キャンバスに広がる奇跡",
            "romaji": "kyanbasunihirogarukiseki",
            "ko": "캔버스 위로 번져나가는 기적",
            "charRomaji": [
              "ky",
              "a",
              "n",
              "ba",
              "su",
              "ni",
              "hiro",
              "ga",
              "ru",
              "ki",
              "seki"
            ]
          },
          {
            "ja": "愛の温もりを信じながら",
            "romaji": "ainoatatamoriwoshinjinagara",
            "ko": "사랑의 따스함을 굳게 믿으며",
            "charRomaji": [
              "ai",
              "no",
              "atata",
              "mo",
              "ri",
              "wo",
              "shin",
              "ji",
              "na",
              "ga",
              "ra"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "描いた命が動き出して",
            "romaji": "egaitainochigaugokidashite",
            "ko": "그려낸 생명이 움직이기 시작해",
            "charRomaji": [
              "ega",
              "i",
              "ta",
              "inochi",
              "ga",
              "ugo",
              "ki",
              "da",
              "shi",
              "te"
            ]
          },
          {
            "ja": "君の涙を優しく拭うんだ",
            "romaji": "kiminonamidawoyasashikunuguunda",
            "ko": "너의 눈물을 다정하게 닦아주네",
            "charRomaji": [
              "kimi",
              "no",
              "namidaw",
              "o",
              "yasa",
              "shi",
              "ku",
              "nugu",
              "u",
              "n",
              "da"
            ]
          },
          {
            "ja": "孤独な夜を照らす月のように",
            "romaji": "kodokunayoruwoterasugatsunoyouni",
            "ko": "고독한 밤을 비추는 달빛처럼",
            "charRomaji": [
              "ko",
              "doku",
              "na",
              "yoru",
              "wo",
              "te",
              "ra",
              "su",
              "gatsu",
              "no",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "ずっと君を守り続けたい",
            "romaji": "zuttokimiwomamoritsuzuketai",
            "ko": "줄곧 너를 지켜주고 싶어",
            "charRomaji": [
              "zu",
              "t",
              "to",
              "kimi",
              "wo",
              "mamo",
              "ri",
              "tsuzu",
              "ke",
              "ta",
              "i"
            ]
          },
          {
            "ja": "命を懸けて届けた祈りが",
            "romaji": "inochiwokaketetodoketainoriga",
            "ko": "생명을 걸고 전했던 간절한 기도가",
            "charRomaji": [
              "inochiw",
              "o",
              "ka",
              "ke",
              "te",
              "todo",
              "ke",
              "ta",
              "ino",
              "ri",
              "ga"
            ]
          },
          {
            "ja": "君の明日を明るく照らすなら",
            "romaji": "kiminoashitawoakarukuterasunara",
            "ko": "너의 내일을 환하게 비출 수 있다면",
            "charRomaji": [
              "kimi",
              "no",
              "a",
              "shita",
              "wo",
              "aka",
              "ru",
              "ku",
              "te",
              "ra",
              "su",
              "na",
              "ra"
            ]
          },
          {
            "ja": "僕は何も後悔しないよ",
            "romaji": "bokuhananimokoukaishinaiyo",
            "ko": "나는 그 어떤 후회도 남기지 않아",
            "charRomaji": [
              "boku",
              "ha",
              "nani",
              "mo",
              "kou",
              "kai",
              "shi",
              "na",
              "i",
              "yo"
            ]
          },
          {
            "ja": "永遠に続く愛の歌を",
            "romaji": "eiennitsuzukuainoutawo",
            "ko": "영원히 이어지는 사랑의 노래를",
            "charRomaji": [
              "ei",
              "en",
              "ni",
              "tsuzu",
              "ku",
              "ai",
              "no",
              "uta",
              "wo"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "cinderellaboy",
    "title": "シンデレラボーイ",
    "reading": "シンデレラボーイ",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "SKyIh9ddvck",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "シンデレラボーイ０時を回って",
            "romaji": "shindererabooizerotokiwomawatte",
            "ko": "신데렐라 보이 자정을 넘겨서",
            "charRomaji": [
              "shi",
              "n",
              "de",
              "re",
              "ra",
              "boo",
              "",
              "i",
              "zero",
              "toki",
              "wo",
              "mawa",
              "t",
              "te"
            ]
          },
          {
            "ja": "魔法が解けていく部屋の隅で",
            "romaji": "mahougatoketeikuheyanosumide",
            "ko": "마법이 풀려가는 방 한구석에서",
            "charRomaji": [
              "ma",
              "hou",
              "ga",
              "to",
              "ke",
              "te",
              "i",
              "ku",
              "he",
              "ya",
              "no",
              "sumi",
              "de"
            ]
          },
          {
            "ja": "冷めきった言葉を並べても",
            "romaji": "samekittakotobawonabetemo",
            "ko": "차게 식어버린 말들을 늘어놓아도",
            "charRomaji": [
              "sa",
              "me",
              "ki",
              "t",
              "ta",
              "ko",
              "toba",
              "wo",
              "na",
              "be",
              "te",
              "mo"
            ]
          },
          {
            "ja": "胸の穴は埋まらないままだね",
            "romaji": "munenoanawaumaranaimamadane",
            "ko": "가슴의 빈자리는 채워지지 않네",
            "charRomaji": [
              "mune",
              "no",
              "ana",
              "wa",
              "u",
              "ma",
              "ra",
              "na",
              "i",
              "ma",
              "ma",
              "da",
              "ne"
            ]
          },
          {
            "ja": "都合のいい優しさばかりで",
            "romaji": "tsugounoiiyasashisabakaride",
            "ko": "형편 좋은 다정함뿐으로",
            "charRomaji": [
              "tsu",
              "gou",
              "no",
              "i",
              "i",
              "yasa",
              "shi",
              "sa",
              "ba",
              "ka",
              "ri",
              "de"
            ]
          },
          {
            "ja": "期待させては突き落とされて",
            "romaji": "kitaisasetehatsukiotosarete",
            "ko": "기대하게 만들고선 밀어 떨어뜨려",
            "charRomaji": [
              "ki",
              "tai",
              "sa",
              "se",
              "te",
              "ha",
              "tsu",
              "ki",
              "o",
              "to",
              "sa",
              "re",
              "te"
            ]
          },
          {
            "ja": "馬鹿みたいに信じていた僕の",
            "romaji": "bakamitainishinjiteitabokuno",
            "ko": "바보처럼 믿고 있었던 나의",
            "charRomaji": [
              "ba",
              "ka",
              "mi",
              "ta",
              "i",
              "ni",
              "shin",
              "ji",
              "te",
              "i",
              "ta",
              "boku",
              "no"
            ]
          },
          {
            "ja": "青い恋はガラスのように割れた",
            "romaji": "aoikoiwagarasunoyouniwareta",
            "ko": "푸르른 사랑은 유리처럼 산산조각 났어",
            "charRomaji": [
              "ao",
              "i",
              "koi",
              "wa",
              "ga",
              "ra",
              "su",
              "no",
              "yo",
              "u",
              "ni",
              "wa",
              "re",
              "ta"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "もう二度と戻らない時間を",
            "romaji": "mounidotomodoranaijikanwo",
            "ko": "더 이상 되돌릴 수 없는 시간을",
            "charRomaji": [
              "mo",
              "u",
              "ni",
              "do",
              "to",
              "modo",
              "ra",
              "na",
              "i",
              "ji",
              "kan",
              "wo"
            ]
          },
          {
            "ja": "泣きながら振り返るのはやめよう",
            "romaji": "nakinagarafurikaerunohayameyou",
            "ko": "울면서 뒤돌아보는 것은 그만두자",
            "charRomaji": [
              "na",
              "ki",
              "na",
              "ga",
              "ra",
              "fu",
              "ri",
              "kae",
              "ru",
              "no",
              "ha",
              "ya",
              "me",
              "yo",
              "u"
            ]
          },
          {
            "ja": "痛みを引き裂いて歌うメロディ",
            "romaji": "itamiwohikisaiteutaumerodi",
            "ko": "아픔을 찢어발기며 부르는 멜로디",
            "charRomaji": [
              "ita",
              "mi",
              "wo",
              "hi",
              "ki",
              "sa",
              "i",
              "te",
              "uta",
              "u",
              "me",
              "ro",
              "d",
              "i"
            ]
          },
          {
            "ja": "君のいない明日へ踏み出すよ",
            "romaji": "kiminoinaiashitahefumidasuyo",
            "ko": "네가 없는 내일을 향해 발을 내딛어",
            "charRomaji": [
              "kimi",
              "no",
              "i",
              "na",
              "i",
              "a",
              "shita",
              "he",
              "fu",
              "mi",
              "da",
              "su",
              "yo"
            ]
          },
          {
            "ja": "シンデレラボーイさよならだね",
            "romaji": "shindererabooisayonaradane",
            "ko": "신데렐라 보이 이제 작별이네",
            "charRomaji": [
              "shi",
              "n",
              "de",
              "re",
              "ra",
              "boo",
              "",
              "i",
              "sa",
              "yo",
              "na",
              "ra",
              "da",
              "ne"
            ]
          },
          {
            "ja": "僕らは違う夜を歩いていく",
            "romaji": "bokurawachigauyoruwoaruiteiku",
            "ko": "우리들은 서로 다른 밤을 걸어간다",
            "charRomaji": [
              "boku",
              "ra",
              "wa",
              "chiga",
              "u",
              "yoru",
              "wo",
              "aru",
              "i",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "強く生きていく誓いを胸に",
            "romaji": "tsuyokuikiteikuchikaiwomuneni",
            "ko": "강인하게 살아가겠다는 맹세를 품고",
            "charRomaji": [
              "tsuyo",
              "ku",
              "i",
              "ki",
              "te",
              "i",
              "ku",
              "chika",
              "i",
              "wo",
              "mune",
              "ni"
            ]
          },
          {
            "ja": "新しい朝を迎えに行こう",
            "romaji": "atarashiiasawomukaeniikou",
            "ko": "새로운 아침을 맞이하러 가자",
            "charRomaji": [
              "atara",
              "shi",
              "i",
              "asa",
              "wo",
              "muka",
              "e",
              "ni",
              "i",
              "ko",
              "u"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "teenageriot",
    "title": "TEENAGE RIOT",
    "reading": "ティーンエイジライオット",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "Hm90Otiz8u8",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "誰の指図も受けないぜ",
            "romaji": "darenosashizumoukenaize",
            "ko": "누구의 명령도 따르지 않아",
            "charRomaji": [
              "dare",
              "no",
              "sashi",
              "zu",
              "mo",
              "u",
              "ke",
              "na",
              "i",
              "ze"
            ]
          },
          {
            "ja": "歪んだ街を蹴り飛ばして走れ",
            "romaji": "hizundamachiwokeritobashitehashire",
            "ko": "뒤틀린 거리를 걷어차며 달려라",
            "charRomaji": [
              "hizu",
              "n",
              "da",
              "machi",
              "wo",
              "ke",
              "ri",
              "to",
              "ba",
              "shi",
              "te",
              "hashi",
              "re"
            ]
          },
          {
            "ja": "退屈な日常をブッ壊すように",
            "romaji": "taikutsunanichijouwobutsukowasuyouni",
            "ko": "지루한 일상을 박살 내버리듯이",
            "charRomaji": [
              "tai",
              "kutsu",
              "na",
              "nichi",
              "jou",
              "wo",
              "buts",
              "u",
              "kowa",
              "su",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "ギターを掻き鳴らす十代の衝動",
            "romaji": "gitaawokakinarasujuudainoshoudou",
            "ko": "기타를 긁어대는 십 대의 폭발적인 충동",
            "charRomaji": [
              "gi",
              "taa",
              "",
              "wo",
              "ka",
              "ki",
              "na",
              "ra",
              "su",
              "juu",
              "dai",
              "no",
              "shou",
              "dou"
            ]
          },
          {
            "ja": "正しさばかり押し付ける大人に",
            "romaji": "tadashisabakarioshitsukeruotonani",
            "ko": "올바름만을 강요하는 어른들에게",
            "charRomaji": [
              "tada",
              "shi",
              "sa",
              "ba",
              "ka",
              "ri",
              "o",
              "shi",
              "tsu",
              "ke",
              "ru",
              "o",
              "tona",
              "ni"
            ]
          },
          {
            "ja": "唾を吐きかけて中指を立てろ",
            "romaji": "tsubawohakikaketenakayubiwotatero",
            "ko": "침을 뱉어주고 가운뎃손가락을 세워라",
            "charRomaji": [
              "tsuba",
              "wo",
              "ha",
              "ki",
              "ka",
              "ke",
              "te",
              "naka",
              "yubi",
              "wo",
              "ta",
              "te",
              "ro"
            ]
          },
          {
            "ja": "僕らの怒りと情熱の火は",
            "romaji": "bokuranoikaritojounetsunohiwa",
            "ko": "우리들의 분노와 뜨거운 열정의 불길은",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "ika",
              "ri",
              "to",
              "jou",
              "netsu",
              "no",
              "hi",
              "wa"
            ]
          },
          {
            "ja": "誰にも消せやしないんだから",
            "romaji": "darenimokeseyashinaindakara",
            "ko": "그 누구도 결코 끌 수 없을 테니까",
            "charRomaji": [
              "dare",
              "ni",
              "mo",
              "ke",
              "se",
              "ya",
              "shi",
              "na",
              "i",
              "n",
              "da",
              "ka",
              "ra"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "ティーンエイジライオット暴れまわれ",
            "romaji": "teiineijiraiottoabaremaware",
            "ko": "틴에이지 라이엇 마음껏 날뛰어라",
            "charRomaji": [
              "t",
              "eii",
              "",
              "n",
              "e",
              "i",
              "ji",
              "ra",
              "i",
              "o",
              "t",
              "to",
              "aba",
              "re",
              "ma",
              "wa",
              "re"
            ]
          },
          {
            "ja": "この歪な夜を切り裂いて行け",
            "romaji": "konohizunayoruwokirisaiteike",
            "ko": "이 일그러진 밤을 찢어 가르고 가거라",
            "charRomaji": [
              "ko",
              "no",
              "hizu",
              "na",
              "yoru",
              "wo",
              "ki",
              "ri",
              "sa",
              "i",
              "te",
              "i",
              "ke"
            ]
          },
          {
            "ja": "傷だらけのスニーカーで踏み鳴らす",
            "romaji": "kizudarakenosuniikaadefuminarasu",
            "ko": "상처투성이 스니커즈로 힘차게 발을 굴러",
            "charRomaji": [
              "kizu",
              "da",
              "ra",
              "ke",
              "no",
              "su",
              "ni",
              "",
              "ikaa",
              "",
              "de",
              "fu",
              "mi",
              "na",
              "ra",
              "su"
            ]
          },
          {
            "ja": "自由へのカウントダウンが始まる",
            "romaji": "jiyuuhenokauntodaungahajimaru",
            "ko": "자유를 향한 카운트다운이 시작된다",
            "charRomaji": [
              "ji",
              "yuu",
              "he",
              "no",
              "ka",
              "u",
              "n",
              "to",
              "da",
              "u",
              "n",
              "ga",
              "haji",
              "ma",
              "ru"
            ]
          },
          {
            "ja": "迷いながら叫び狂え",
            "romaji": "mayoinagarasakebikyoue",
            "ko": "방황하며 미친 듯이 외쳐라",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ga",
              "ra",
              "sake",
              "bi",
              "kyou",
              "e"
            ]
          },
          {
            "ja": "これが僕らの反逆のビート",
            "romaji": "koregabokuranohangyakunobiito",
            "ko": "이것이 우리들의 반역의 비트",
            "charRomaji": [
              "ko",
              "re",
              "ga",
              "boku",
              "ra",
              "no",
              "han",
              "gyaku",
              "no",
              "bii",
              "",
              "to"
            ]
          },
          {
            "ja": "世界を変えてみせるその日まで",
            "romaji": "sekaiwokaetemiserusononichimade",
            "ko": "세상을 바꾸어 보일 바로 그날까지",
            "charRomaji": [
              "se",
              "kai",
              "wo",
              "ka",
              "e",
              "te",
              "mi",
              "se",
              "ru",
              "so",
              "no",
              "nichi",
              "ma",
              "de"
            ]
          },
          {
            "ja": "僕らの暴動は止まらない",
            "romaji": "bokuranoboudouwatomaranai",
            "ko": "우리들의 폭동은 멈추지 않아",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "bou",
              "dou",
              "wa",
              "to",
              "ma",
              "ra",
              "na",
              "i"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "ransoumetsuretsu",
    "title": "乱躁滅裂ガール",
    "reading": "らんそうめつれつガール",
    "category": "cover",
    "album": "ガルパ カバーコレクション",
    "youtubeId": "T3Ar3Wn9VOY",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "狂い咲け感情の乱反射",
            "romaji": "kuruisakekanjounoranhansha",
            "ko": "미쳐 피어나라 감정의 난반사",
            "charRomaji": [
              "kuru",
              "i",
              "sa",
              "ke",
              "kan",
              "jou",
              "no",
              "ran",
              "han",
              "sha"
            ]
          },
          {
            "ja": "頭の中で鳴り響くノイズを蹴散らせ",
            "romaji": "atamanonakadenarihibikunoizuwokechirase",
            "ko": "머릿속에서 울려 퍼지는 소음을 걷어차라",
            "charRomaji": [
              "atama",
              "no",
              "naka",
              "de",
              "na",
              "ri",
              "hibi",
              "ku",
              "no",
              "i",
              "zu",
              "wo",
              "ke",
              "chi",
              "ra",
              "se"
            ]
          },
          {
            "ja": "理屈じゃない衝動の嵐に",
            "romaji": "rikutsujanaishoudounoarashini",
            "ko": "이론 따위가 아닌 충동의 폭풍에",
            "charRomaji": [
              "ri",
              "kutsu",
              "j",
              "a",
              "na",
              "i",
              "shou",
              "dou",
              "no",
              "arashi",
              "ni"
            ]
          },
          {
            "ja": "身を任せて暴れ狂うステージ",
            "romaji": "miwomakaseteabarekuruusuteeji",
            "ko": "몸을 맡기고 미쳐 날뛰는 스테이지",
            "charRomaji": [
              "mi",
              "wo",
              "maka",
              "se",
              "te",
              "aba",
              "re",
              "kuru",
              "u",
              "su",
              "tee",
              "",
              "ji"
            ]
          },
          {
            "ja": "息つく暇もないスピード感で",
            "romaji": "ikitsukuhimamonaisupiidokande",
            "ko": "숨 쉴 틈도 없는 엄청난 스피드감으로",
            "charRomaji": [
              "iki",
              "tsu",
              "ku",
              "hima",
              "mo",
              "na",
              "i",
              "su",
              "pii",
              "",
              "do",
              "kan",
              "de"
            ]
          },
          {
            "ja": "世界を震撼させる僕らの音",
            "romaji": "sekaiwoshinkansaserubokuranooto",
            "ko": "세상을 뒤흔드는 우리들의 사운드",
            "charRomaji": [
              "se",
              "kai",
              "wo",
              "shin",
              "kan",
              "sa",
              "se",
              "ru",
              "boku",
              "ra",
              "no",
              "oto"
            ]
          },
          {
            "ja": "滅茶苦茶なビートに乗せて叫べ",
            "romaji": "mechakuchanabiitoninosetesakebe",
            "ko": "엉망진창인 비트에 실어 외쳐라",
            "charRomaji": [
              "me",
              "cha",
              "ku",
              "cha",
              "na",
              "bii",
              "",
              "to",
              "ni",
              "no",
              "se",
              "te",
              "sake",
              "be"
            ]
          },
          {
            "ja": "乱躁滅裂な少女たちの歌",
            "romaji": "ransoumetsuretsunashoujotachinouta",
            "ko": "난조멸렬한 소녀들의 노랫소리",
            "charRomaji": [
              "ran",
              "sou",
              "metsu",
              "retsu",
              "na",
              "sho",
              "ujo",
              "ta",
              "chi",
              "no",
              "uta"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "誰にも止められないこのテンションで",
            "romaji": "darenimoyamerarenaikonotenshonde",
            "ko": "그 누구도 멈출 수 없는 이 텐션으로",
            "charRomaji": [
              "dare",
              "ni",
              "mo",
              "ya",
              "me",
              "ra",
              "re",
              "na",
              "i",
              "ko",
              "no",
              "te",
              "n",
              "sh",
              "o",
              "n",
              "de"
            ]
          },
          {
            "ja": "限界の壁を突き破っていく",
            "romaji": "genkainokabewotsukiyabutteiku",
            "ko": "한계의 벽을 시원하게 뚫고 나아간다",
            "charRomaji": [
              "gen",
              "kai",
              "no",
              "kabe",
              "wo",
              "tsu",
              "ki",
              "yabu",
              "t",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "混沌の渦に巻き込まれながら",
            "romaji": "kontonnouzunimakikomarenagara",
            "ko": "혼돈의 소용돌이에 휘말려 들면서도",
            "charRomaji": [
              "kon",
              "ton",
              "no",
              "uzu",
              "ni",
              "ma",
              "ki",
              "ko",
              "ma",
              "re",
              "na",
              "ga",
              "ra"
            ]
          },
          {
            "ja": "僕らは最高の瞬間を生きてる",
            "romaji": "bokurawasaikounoshunkanwoikiteru",
            "ko": "우리들은 최고의 한순간을 살아가고 있어",
            "charRomaji": [
              "boku",
              "ra",
              "wa",
              "sa",
              "ikou",
              "no",
              "shun",
              "kan",
              "wo",
              "i",
              "ki",
              "te",
              "ru"
            ]
          },
          {
            "ja": "狂乱の夜を駆け抜けろ",
            "romaji": "kyourannoyoruwokakenukero",
            "ko": "광란의 밤을 전속력으로 내달려라",
            "charRomaji": [
              "kyou",
              "ran",
              "no",
              "yoru",
              "wo",
              "ka",
              "ke",
              "nu",
              "ke",
              "ro"
            ]
          },
          {
            "ja": "燃え尽きるまで音を鳴らし続けろ",
            "romaji": "moekotogotokirumadeotowonarashitsuzukero",
            "ko": "새하얗게 불태울 때까지 소리를 울려라",
            "charRomaji": [
              "mo",
              "e",
              "kotogoto",
              "ki",
              "ru",
              "ma",
              "de",
              "oto",
              "wo",
              "na",
              "ra",
              "shi",
              "tsuzu",
              "ke",
              "ro"
            ]
          },
          {
            "ja": "迷子たちの爆発的なエネルギー",
            "romaji": "maigotachinobakuhattekinaenerugii",
            "ko": "미아들의 폭발적인 에너지",
            "charRomaji": [
              "ma",
              "igo",
              "ta",
              "chi",
              "no",
              "baku",
              "hat",
              "teki",
              "na",
              "e",
              "ne",
              "ru",
              "gii",
              ""
            ]
          },
          {
            "ja": "響け世界中の果てまで",
            "romaji": "hibikesekaijuunohatemade",
            "ko": "울려라 온 세상 끝까지",
            "charRomaji": [
              "hibi",
              "ke",
              "se",
              "ka",
              "ijuu",
              "no",
              "ha",
              "te",
              "ma",
              "de"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "raeisen",
    "title": "羅永線",
    "reading": "らえいせん",
    "category": "original",
    "album": "3rd Album『致並跡』",
    "youtubeId": "4as52H1v3XI",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "どこまでも続く羅針盤の針",
            "romaji": "dokomademotsuzukurashinbannohari",
            "ko": "어디까지고 이어지는 나침반 바늘",
            "charRomaji": [
              "do",
              "ko",
              "ma",
              "de",
              "mo",
              "tsuzu",
              "ku",
              "ra",
              "shin",
              "ban",
              "no",
              "hari"
            ]
          },
          {
            "ja": "迷いなき未来を指し示すように",
            "romaji": "mayoinakimiraiwosashishimesuyouni",
            "ko": "망설임 없는 미래를 가리키듯이",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ki",
              "mi",
              "rai",
              "wo",
              "sa",
              "shi",
              "shime",
              "su",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "永い夜を越えて進む僕らの",
            "romaji": "nagaiyoruwokoetesusumubokurano",
            "ko": "길고 긴 밤을 넘어 나아가는 우리들의",
            "charRomaji": [
              "naga",
              "i",
              "yoru",
              "wo",
              "ko",
              "e",
              "te",
              "susu",
              "mu",
              "boku",
              "ra",
              "no"
            ]
          },
          {
            "ja": "軌跡がひとつの線になっていく",
            "romaji": "kisekigahitotsunosenninatteiku",
            "ko": "궤적이 하나의 선이 되어가",
            "charRomaji": [
              "ki",
              "seki",
              "ga",
              "hi",
              "to",
              "tsu",
              "no",
              "sen",
              "ni",
              "na",
              "t",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "果てしない航海に出航するんだ",
            "romaji": "hateshinaikoukainishukkousurunda",
            "ko": "끝없는 항해로 출항하는 거야",
            "charRomaji": [
              "ha",
              "te",
              "shi",
              "na",
              "i",
              "ko",
              "ukai",
              "ni",
              "shuk",
              "kou",
              "su",
              "ru",
              "n",
              "da"
            ]
          },
          {
            "ja": "荒れ狂う嵐さえ恐れずに",
            "romaji": "arekuruuarashisaeosorezuni",
            "ko": "거칠게 몰아치는 폭풍조차 두려워하지 않고",
            "charRomaji": [
              "a",
              "re",
              "kuru",
              "u",
              "arashi",
              "sa",
              "e",
              "oso",
              "re",
              "zu",
              "ni"
            ]
          },
          {
            "ja": "掴み取れ僕らだけの運命を",
            "romaji": "tsukamitorebokuradakenounmeiwo",
            "ko": "움켜쥐어라 우리들만의 운명을",
            "charRomaji": [
              "tsuka",
              "mi",
              "to",
              "re",
              "boku",
              "ra",
              "da",
              "ke",
              "no",
              "un",
              "mei",
              "wo"
            ]
          },
          {
            "ja": "羅永線が導く光の先へ",
            "romaji": "raeisengamichibikuhikarinosakihe",
            "ko": "라영선이 이끄는 빛의 끝으로",
            "charRomaji": [
              "ra",
              "ei",
              "sen",
              "ga",
              "michibi",
              "ku",
              "hikari",
              "no",
              "saki",
              "he"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "擦り切れた地図など捨て去って",
            "romaji": "surikiretachizunadosutesatte",
            "ko": "너덜너덜해진 지도 따윈 내던져버리고",
            "charRomaji": [
              "su",
              "ri",
              "ki",
              "re",
              "ta",
              "chi",
              "zu",
              "na",
              "do",
              "su",
              "te",
              "sa",
              "t",
              "te"
            ]
          },
          {
            "ja": "心の羅針盤を信じるんだ",
            "romaji": "kokoronorashinbanwoshinjirunda",
            "ko": "마음속 나침반을 굳게 믿는 거야",
            "charRomaji": [
              "kokoro",
              "no",
              "ra",
              "shin",
              "ban",
              "wo",
              "shin",
              "ji",
              "ru",
              "n",
              "da"
            ]
          },
          {
            "ja": "誰のものでもない僕らの海を",
            "romaji": "darenomonodemonaibokuranoumiwo",
            "ko": "그 누구의 것도 아닌 우리들의 바다를",
            "charRomaji": [
              "dare",
              "no",
              "mo",
              "no",
              "de",
              "mo",
              "na",
              "i",
              "boku",
              "ra",
              "no",
              "umi",
              "wo"
            ]
          },
          {
            "ja": "全速力で切り拓いていく",
            "romaji": "zensokuryokudekiritakuiteiku",
            "ko": "전속력으로 헤쳐 나간다",
            "charRomaji": [
              "zen",
              "soku",
              "ryoku",
              "de",
              "ki",
              "ri",
              "taku",
              "i",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "響き渡れ僕らの鬨の声",
            "romaji": "hibikiwatarebokuranokounokoe",
            "ko": "울려 퍼져라 우리들의 함성 소리",
            "charRomaji": [
              "hibi",
              "ki",
              "wata",
              "re",
              "boku",
              "ra",
              "no",
              "kou",
              "no",
              "koe"
            ]
          },
          {
            "ja": "永遠に途切れない絆の線",
            "romaji": "eiennitogirenaikizunanosen",
            "ko": "영원히 끊어지지 않는 인연의 선",
            "charRomaji": [
              "ei",
              "en",
              "ni",
              "to",
              "gi",
              "re",
              "na",
              "i",
              "kizuna",
              "no",
              "sen"
            ]
          },
          {
            "ja": "羅永線の彼方にある明日へ",
            "romaji": "raeisennokanataniaruashitahe",
            "ko": "라영선 저편에 있는 내일을 향해",
            "charRomaji": [
              "ra",
              "ei",
              "sen",
              "no",
              "ka",
              "nata",
              "ni",
              "a",
              "ru",
              "a",
              "shita",
              "he"
            ]
          },
          {
            "ja": "僕らは歌いながら進み続ける",
            "romaji": "bokurawautainagarasusumitsuzukeru",
            "ko": "우리들은 노래하며 계속 나아간다",
            "charRomaji": [
              "boku",
              "ra",
              "wa",
              "uta",
              "i",
              "na",
              "ga",
              "ra",
              "susu",
              "mi",
              "tsuzu",
              "ke",
              "ru"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "seikousou",
    "title": "静降想",
    "reading": "せいこうそう",
    "category": "original",
    "album": "3rd Album『致並跡』",
    "youtubeId": "9mYY2ZU5-HU",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "静かに降り積もる白い雪のように",
            "romaji": "shizukanioritsumorushiroiyukinoyouni",
            "ko": "고요하게 내려 쌓이는 하얀 눈처럼",
            "charRomaji": [
              "shizu",
              "ka",
              "ni",
              "o",
              "ri",
              "tsu",
              "mo",
              "ru",
              "shiro",
              "i",
              "yuki",
              "no",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "心の奥底に積もる想い",
            "romaji": "kokoronookusokonitsumoruomoi",
            "ko": "마음 깊은 곳에 차곡차곡 쌓이는 생각들",
            "charRomaji": [
              "kokoro",
              "no",
              "oku",
              "soko",
              "ni",
              "tsu",
              "mo",
              "ru",
              "omo",
              "i"
            ]
          },
          {
            "ja": "言葉にできずに飲み込んだ吐息",
            "romaji": "kotobanidekizuninomikondatoiki",
            "ko": "차마 말로 하지 못하고 삼켜낸 한숨",
            "charRomaji": [
              "ko",
              "toba",
              "ni",
              "de",
              "ki",
              "zu",
              "ni",
              "no",
              "mi",
              "ko",
              "n",
              "da",
              "to",
              "iki"
            ]
          },
          {
            "ja": "白く染まる街の片隅で",
            "romaji": "shirokusomarumachinokatasumide",
            "ko": "하얗게 물드는 거리 한구석에서",
            "charRomaji": [
              "shiro",
              "ku",
              "so",
              "ma",
              "ru",
              "machi",
              "no",
              "kata",
              "sumi",
              "de"
            ]
          },
          {
            "ja": "冷たい風が頬をかすめても",
            "romaji": "tsumetaikazegahoowokasumetemo",
            "ko": "차가운 바람이 뺨을 스쳐 지나가도",
            "charRomaji": [
              "tsume",
              "ta",
              "i",
              "kaze",
              "ga",
              "hoo",
              "wo",
              "ka",
              "su",
              "me",
              "te",
              "mo"
            ]
          },
          {
            "ja": "消えない温もりを抱きしめている",
            "romaji": "kienaiatatamoriwodakishimeteiru",
            "ko": "식지 않는 온기를 끌어안고 있어",
            "charRomaji": [
              "ki",
              "e",
              "na",
              "i",
              "atata",
              "mo",
              "ri",
              "wo",
              "da",
              "ki",
              "shi",
              "me",
              "te",
              "i",
              "ru"
            ]
          },
          {
            "ja": "降り止まない静寂の中で",
            "romaji": "oritomanaiseijakunonakade",
            "ko": "그치지 않는 고요함 속에서",
            "charRomaji": [
              "o",
              "ri",
              "to",
              "ma",
              "na",
              "i",
              "sei",
              "jaku",
              "no",
              "naka",
              "de"
            ]
          },
          {
            "ja": "響くのは僕らの微かな鼓動",
            "romaji": "hibikunohabokuranokasukanakodou",
            "ko": "울리는 것은 우리들의 희미한 고동",
            "charRomaji": [
              "hibi",
              "ku",
              "no",
              "ha",
              "boku",
              "ra",
              "no",
              "kasu",
              "ka",
              "na",
              "ko",
              "dou"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "静降想の夜が明けていく",
            "romaji": "seikousounoyorugaaketeiku",
            "ko": "정강상의 밤이 밝아온다",
            "charRomaji": [
              "sei",
              "kou",
              "sou",
              "no",
              "yoru",
              "ga",
              "a",
              "ke",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "積もった雪を溶かす光のように",
            "romaji": "tsumottayukiwotokasuhikarinoyouni",
            "ko": "소복이 쌓인 눈을 녹이는 햇살처럼",
            "charRomaji": [
              "tsu",
              "mo",
              "t",
              "ta",
              "yuki",
              "wo",
              "to",
              "ka",
              "su",
              "hikari",
              "no",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "優しく包み込む音の温もり",
            "romaji": "yasashikutsutsumikomuotonoatatamori",
            "ko": "다정하게 감싸 안는 소리의 따스함",
            "charRomaji": [
              "yasa",
              "shi",
              "ku",
              "tsutsu",
              "mi",
              "ko",
              "mu",
              "oto",
              "no",
              "atata",
              "mo",
              "ri"
            ]
          },
          {
            "ja": "僕らはまた歩き出せるんだ",
            "romaji": "bokurahamataarukidaserunda",
            "ko": "우리들은 다시 걸어나갈 수 있어",
            "charRomaji": [
              "boku",
              "ra",
              "ha",
              "ma",
              "ta",
              "aru",
              "ki",
              "da",
              "se",
              "ru",
              "n",
              "da"
            ]
          },
          {
            "ja": "凍えた指先を重ね合えば",
            "romaji": "kogoetayubisakiwoomoneaeba",
            "ko": "얼어붙은 손끝을 마주 잡으면",
            "charRomaji": [
              "kogo",
              "e",
              "ta",
              "yubi",
              "saki",
              "wo",
              "omo",
              "ne",
              "a",
              "e",
              "ba"
            ]
          },
          {
            "ja": "どんな寒さも乗り越えられる",
            "romaji": "donnasamusamonorikoerareru",
            "ko": "어떤 추위도 이겨낼 수 있어",
            "charRomaji": [
              "do",
              "n",
              "na",
              "samu",
              "sa",
              "mo",
              "no",
              "ri",
              "ko",
              "e",
              "ra",
              "re",
              "ru"
            ]
          },
          {
            "ja": "静かに降る想いを歌に乗せて",
            "romaji": "shizukanifuruomoiwoutaninosete",
            "ko": "고요히 내리는 마음을 노래에 실어",
            "charRomaji": [
              "shizu",
              "ka",
              "ni",
              "fu",
              "ru",
              "omo",
              "i",
              "wo",
              "uta",
              "ni",
              "no",
              "se",
              "te"
            ]
          },
          {
            "ja": "明日へと届くように奏でよう",
            "romaji": "ashitahetotodokuyounikanadeyou",
            "ko": "내일로 닿을 수 있게 연주하자",
            "charRomaji": [
              "a",
              "shita",
              "he",
              "to",
              "todo",
              "ku",
              "yo",
              "u",
              "ni",
              "kana",
              "de",
              "yo",
              "u"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "sokikyoku",
    "title": "素寄曲",
    "reading": "そききょく",
    "category": "original",
    "album": "3rd Album『致並跡』",
    "youtubeId": "uZSAArx6jKM",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "飾らない素朴な旋律を奏でる",
            "romaji": "kazaranaisobokunasenritsuwokanaderu",
            "ko": "꾸밈없는 소박한 선율을 연주해",
            "charRomaji": [
              "kaza",
              "ra",
              "na",
              "i",
              "so",
              "boku",
              "na",
              "sen",
              "ritsu",
              "wo",
              "kana",
              "de",
              "ru"
            ]
          },
          {
            "ja": "寄り添うように寄り添いながら",
            "romaji": "yorisouyouniyorisoinagara",
            "ko": "서로에게 기대듯이 곁을 내어주며",
            "charRomaji": [
              "yo",
              "ri",
              "so",
              "u",
              "yo",
              "u",
              "ni",
              "yo",
              "ri",
              "so",
              "i",
              "na",
              "ga",
              "ra"
            ]
          },
          {
            "ja": "ありのままの姿で歌いたい",
            "romaji": "arinomamanosugatadeutaitai",
            "ko": "있는 그대로의 모습으로 노래하고 싶어",
            "charRomaji": [
              "a",
              "ri",
              "no",
              "ma",
              "ma",
              "no",
              "sugata",
              "de",
              "uta",
              "i",
              "ta",
              "i"
            ]
          },
          {
            "ja": "嘘や偽りのないこの場所で",
            "romaji": "usoyaitsuwarinonaikonobashode",
            "ko": "거짓이나 꾸밈없는 바로 이 자리에서",
            "charRomaji": [
              "uso",
              "ya",
              "itsuwa",
              "ri",
              "no",
              "na",
              "i",
              "ko",
              "no",
              "ba",
              "sho",
              "de"
            ]
          },
          {
            "ja": "不器用なコード進行の隙間に",
            "romaji": "bukiyounakoodoshinkounosukimani",
            "ko": "서툰 코드 진행의 틈새 속에",
            "charRomaji": [
              "bu",
              "ki",
              "you",
              "na",
              "koo",
              "",
              "do",
              "shi",
              "nkou",
              "no",
              "su",
              "kima",
              "ni"
            ]
          },
          {
            "ja": "溢れ出す僕らの本音たち",
            "romaji": "afuredasubokuranohonnetachi",
            "ko": "넘쳐흘러 나오는 우리들의 진심들",
            "charRomaji": [
              "afu",
              "re",
              "da",
              "su",
              "boku",
              "ra",
              "no",
              "hon",
              "ne",
              "ta",
              "chi"
            ]
          },
          {
            "ja": "素直になれる素寄曲よ",
            "romaji": "sunaoninarerumotoyorikyokuyo",
            "ko": "솔직해질 수 있는 소기곡이여",
            "charRomaji": [
              "su",
              "nao",
              "ni",
              "na",
              "re",
              "ru",
              "moto",
              "yori",
              "kyoku",
              "yo"
            ]
          },
          {
            "ja": "君の心へそっと届いてほしい",
            "romaji": "kiminokokorohesottotodoitehoshii",
            "ko": "너의 마음에 가만히 닿아주길 바라",
            "charRomaji": [
              "kimi",
              "no",
              "kokoroh",
              "e",
              "so",
              "t",
              "to",
              "todo",
              "i",
              "te",
              "ho",
              "shi",
              "i"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "華やかなスポットライトがなくても",
            "romaji": "hanayakanasupottoraitoganakutemo",
            "ko": "화려한 스포트라이트가 없더라도",
            "charRomaji": [
              "hana",
              "ya",
              "ka",
              "na",
              "su",
              "po",
              "t",
              "to",
              "ra",
              "i",
              "to",
              "ga",
              "na",
              "ku",
              "te",
              "mo"
            ]
          },
          {
            "ja": "僕らにはこの音楽があるから",
            "romaji": "bokuranihakonoongakugaarukara",
            "ko": "우리에게는 이 음악이 있으니까",
            "charRomaji": [
              "boku",
              "ra",
              "ni",
              "ha",
              "ko",
              "no",
              "o",
              "ngaku",
              "ga",
              "a",
              "ru",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "寄り添い合って奏でる一瞬が",
            "romaji": "yorisoiattekanaderuisshunga",
            "ko": "서로 기대어 연주하는 이 한순간이",
            "charRomaji": [
              "yo",
              "ri",
              "so",
              "i",
              "a",
              "t",
              "te",
              "kana",
              "de",
              "ru",
              "is",
              "shun",
              "ga"
            ]
          },
          {
            "ja": "何よりも尊い宝物なんだ",
            "romaji": "naniyorimotoutoitakaramononanda",
            "ko": "그 무엇보다 소중한 보물이야",
            "charRomaji": [
              "nani",
              "yo",
              "ri",
              "mo",
              "touto",
              "i",
              "takara",
              "mono",
              "na",
              "n",
              "da"
            ]
          },
          {
            "ja": "擦れ違った日々の痛みさえも",
            "romaji": "surechigattahibinoitamisaemo",
            "ko": "엇갈렸던 나날의 아픔조차도",
            "charRomaji": [
              "su",
              "re",
              "chiga",
              "t",
              "ta",
              "hi",
              "bi",
              "no",
              "ita",
              "mi",
              "sa",
              "e",
              "mo"
            ]
          },
          {
            "ja": "優しいハーモニーに変えていこう",
            "romaji": "yasashiihaamoniinikaeteikou",
            "ko": "다정한 하모니로 바꾸어 가자",
            "charRomaji": [
              "yasa",
              "shi",
              "i",
              "haa",
              "",
              "mo",
              "nii",
              "",
              "ni",
              "ka",
              "e",
              "te",
              "i",
              "ko",
              "u"
            ]
          },
          {
            "ja": "素朴で温かいこの調べを",
            "romaji": "sobokudeatatakaikonoshirabewo",
            "ko": "소박하고 따스한 이 선율을",
            "charRomaji": [
              "so",
              "boku",
              "de",
              "atata",
              "ka",
              "i",
              "ko",
              "no",
              "shira",
              "be",
              "wo"
            ]
          },
          {
            "ja": "永遠に鳴らし続けたいんだ",
            "romaji": "eienninarashitsuzuketainda",
            "ko": "영원히 울려 퍼뜨리고 싶어",
            "charRomaji": [
              "ei",
              "en",
              "ni",
              "na",
              "ra",
              "shi",
              "tsuzu",
              "ke",
              "ta",
              "i",
              "n",
              "da"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "soukonshutsu",
    "title": "騒混出",
    "reading": "そうこんしゅつ",
    "category": "original",
    "album": "3rd Album『致並跡』",
    "youtubeId": "LBM-sIZGJlo",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "騒がしい街の雑音に紛れて",
            "romaji": "sawagashiimachinozatsuonnimagirete",
            "ko": "시끄러운 거리의 소음에 묻혀서",
            "charRomaji": [
              "sawa",
              "ga",
              "shi",
              "i",
              "machi",
              "no",
              "zatsu",
              "on",
              "ni",
              "magi",
              "re",
              "te"
            ]
          },
          {
            "ja": "混ざり合う感情が吹き出す瞬間",
            "romaji": "mazariaukanjougafukidasushunkan",
            "ko": "뒤섞이는 감정들이 뿜어져 나오는 순간",
            "charRomaji": [
              "ma",
              "za",
              "ri",
              "a",
              "u",
              "kan",
              "jou",
              "ga",
              "fu",
              "ki",
              "da",
              "su",
              "shun",
              "kan"
            ]
          },
          {
            "ja": "抑えきれない衝動の叫び",
            "romaji": "osaekirenaishoudounosakebi",
            "ko": "억누를 수 없는 충동의 외침",
            "charRomaji": [
              "osa",
              "e",
              "ki",
              "re",
              "na",
              "i",
              "shou",
              "dou",
              "no",
              "sake",
              "bi"
            ]
          },
          {
            "ja": "ノイズを突き破り飛び出していく",
            "romaji": "noizuwotsukiyaburitobidashiteiku",
            "ko": "노이즈를 뚫고 박차고 뛰어나간다",
            "charRomaji": [
              "no",
              "i",
              "zu",
              "wo",
              "tsu",
              "ki",
              "yabu",
              "ri",
              "to",
              "bi",
              "da",
              "shi",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "混沌とした頭の中を",
            "romaji": "kontontoshitaatamanonakawo",
            "ko": "혼돈으로 가득 찬 머릿속을",
            "charRomaji": [
              "kon",
              "ton",
              "to",
              "shi",
              "ta",
              "atama",
              "no",
              "naka",
              "wo"
            ]
          },
          {
            "ja": "掻き乱すギターのディストーション",
            "romaji": "kakimidasugitaanodisutooshon",
            "ko": "뒤흔들어 놓는 기타의 디스토션",
            "charRomaji": [
              "ka",
              "ki",
              "mida",
              "su",
              "gi",
              "taa",
              "",
              "no",
              "d",
              "i",
              "su",
              "too",
              "",
              "sh",
              "o",
              "n"
            ]
          },
          {
            "ja": "混ざり合って爆発する熱量",
            "romaji": "mazariattebakuhatsusurunetsuryou",
            "ko": "뒤섞이며 폭발하는 열량",
            "charRomaji": [
              "ma",
              "za",
              "ri",
              "a",
              "t",
              "te",
              "baku",
              "hatsu",
              "su",
              "ru",
              "netsu",
              "ryou"
            ]
          },
          {
            "ja": "騒混出のビートを刻み込め",
            "romaji": "soukondenobiitowokizamikome",
            "ko": "소혼출의 비트를 깊이 새겨 넣어라",
            "charRomaji": [
              "sou",
              "kon",
              "de",
              "no",
              "bii",
              "",
              "to",
              "wo",
              "kiza",
              "mi",
              "ko",
              "me"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "綺麗に整った調和なんて壊せ",
            "romaji": "kireinitotonottachouwanantekowase",
            "ko": "깔끔하게 정돈된 조화 따윈 부숴버려",
            "charRomaji": [
              "ki",
              "rei",
              "ni",
              "totono",
              "t",
              "ta",
              "chou",
              "wa",
              "na",
              "n",
              "te",
              "kowa",
              "se"
            ]
          },
          {
            "ja": "歪んだ音こそが僕らのリアル",
            "romaji": "hizundaotokosogabokuranoriaru",
            "ko": "비뚤어진 소리야말로 우리들의 리얼",
            "charRomaji": [
              "hizu",
              "n",
              "da",
              "oto",
              "ko",
              "so",
              "ga",
              "boku",
              "ra",
              "no",
              "ri",
              "a",
              "ru"
            ]
          },
          {
            "ja": "混ざり合うカオスを抱きしめて",
            "romaji": "mazariaukaosuwodakishimete",
            "ko": "뒤섞이는 카오스를 힘껏 끌어안고",
            "charRomaji": [
              "ma",
              "za",
              "ri",
              "a",
              "u",
              "ka",
              "o",
              "su",
              "wo",
              "da",
              "ki",
              "shi",
              "me",
              "te"
            ]
          },
          {
            "ja": "ステージの上で暴れまわるんだ",
            "romaji": "suteejinouedeabaremawarunda",
            "ko": "무대 위에서 미친 듯이 날뛰는 거야",
            "charRomaji": [
              "su",
              "tee",
              "",
              "ji",
              "no",
              "ue",
              "de",
              "aba",
              "re",
              "ma",
              "wa",
              "ru",
              "n",
              "da"
            ]
          },
          {
            "ja": "騒がしさを力に変えて行け",
            "romaji": "sawagashisawochikaranikaeteike",
            "ko": "소란스러움을 에너지로 바꾸어 가라",
            "charRomaji": [
              "sawa",
              "ga",
              "shi",
              "sa",
              "wo",
              "chikara",
              "ni",
              "ka",
              "e",
              "te",
              "i",
              "ke"
            ]
          },
          {
            "ja": "誰にも真似できない僕らの轟音",
            "romaji": "darenimomanedekinaibokuranogouon",
            "ko": "그 누구도 흉내 낼 수 없는 우리들의 굉음",
            "charRomaji": [
              "dare",
              "ni",
              "mo",
              "ma",
              "ne",
              "de",
              "ki",
              "na",
              "i",
              "boku",
              "ra",
              "no",
              "go",
              "uon"
            ]
          },
          {
            "ja": "混ざり合い吹き出す衝動の先へ",
            "romaji": "mazariaifukidasushoudounosakihe",
            "ko": "서로 뒤섞여 뿜어져 나오는 충동의 끝으로",
            "charRomaji": [
              "ma",
              "za",
              "ri",
              "a",
              "i",
              "fu",
              "ki",
              "da",
              "su",
              "shou",
              "dou",
              "no",
              "saki",
              "he"
            ]
          },
          {
            "ja": "全力で突き進め僕らのロック",
            "romaji": "zenryokudetsukisusumebokuranorokku",
            "ko": "전력으로 돌진하라 우리들의 록",
            "charRomaji": [
              "zen",
              "ryoku",
              "de",
              "tsu",
              "ki",
              "susu",
              "me",
              "boku",
              "ra",
              "no",
              "ro",
              "k",
              "ku"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "itsujitsusenshuu",
    "title": "聿日箋秋",
    "reading": "いつじつせんしゅう",
    "category": "original",
    "album": "6th Single『聿日箋秋』, 3rd Album『致並跡』",
    "youtubeId": "XqfXJl9IUGg",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "こころ写す言葉剥がして連れて行って",
            "romaji": "kokoroutsusukotobahagashitetsureteitte",
            "ko": "마음을 비추는 말을 벗겨내어 데려가 줘",
            "charRomaji": [
              "ko",
              "ko",
              "ro",
              "utsu",
              "su",
              "ko",
              "toba",
              "ha",
              "ga",
              "shi",
              "te",
              "tsu",
              "re",
              "te",
              "i",
              "t",
              "te"
            ]
          },
          {
            "ja": "わかれ道の先へ僕らは歩き出す",
            "romaji": "wakaremichinosakihebokurawaarukidasu",
            "ko": "갈림길 저편으로 우리들은 걸어나가",
            "charRomaji": [
              "wa",
              "ka",
              "re",
              "michi",
              "no",
              "saki",
              "he",
              "boku",
              "ra",
              "wa",
              "aru",
              "ki",
              "da",
              "su"
            ]
          },
          {
            "ja": "どうしたらいいのか巡らせてる間に",
            "romaji": "doushitaraiinokameguraseterumani",
            "ko": "어떻게 해야 할지 머리를 굴리는 사이에",
            "charRomaji": [
              "do",
              "u",
              "shi",
              "ta",
              "ra",
              "i",
              "i",
              "no",
              "ka",
              "megu",
              "ra",
              "se",
              "te",
              "ru",
              "ma",
              "ni"
            ]
          },
          {
            "ja": "季節も変わるよ僕もそうかな",
            "romaji": "kisetsumokawaruyobokumosoukana",
            "ko": "계절도 바뀌어가, 나 역시 그럴까",
            "charRomaji": [
              "ki",
              "setsu",
              "mo",
              "ka",
              "wa",
              "ru",
              "yo",
              "boku",
              "mo",
              "so",
              "u",
              "ka",
              "na"
            ]
          },
          {
            "ja": "ゆらゆら今日も曲がり角に立つ",
            "romaji": "yurayurakyoumomagarikakunitatsu",
            "ko": "흔들흔들 오늘도 길모퉁이에 서서",
            "charRomaji": [
              "yu",
              "ra",
              "yu",
              "ra",
              "k",
              "you",
              "mo",
              "ma",
              "ga",
              "ri",
              "kaku",
              "ni",
              "ta",
              "tsu"
            ]
          },
          {
            "ja": "右左どっちも選べないまま",
            "romaji": "migihidaridotchimoerabenaimama",
            "ko": "오른쪽 왼쪽 어느 쪽도 고르지 못한 채",
            "charRomaji": [
              "migi",
              "hidari",
              "do",
              "t",
              "chi",
              "mo",
              "era",
              "be",
              "na",
              "i",
              "ma",
              "ma"
            ]
          },
          {
            "ja": "ふらふらな僕の行方はわからない",
            "romaji": "furafuranabokunonamegatahawakaranai",
            "ko": "비틀거리는 나의 행방은 알 수 없어",
            "charRomaji": [
              "fu",
              "ra",
              "fu",
              "ra",
              "na",
              "boku",
              "no",
              "na",
              "megata",
              "ha",
              "wa",
              "ka",
              "ra",
              "na",
              "i"
            ]
          },
          {
            "ja": "だけどちょっと先へ行くつもりさ",
            "romaji": "dakedochottosakiheikutsumorisa",
            "ko": "하지만 조금 더 앞을 향해 나아갈 생각이야",
            "charRomaji": [
              "da",
              "ke",
              "do",
              "ch",
              "o",
              "t",
              "to",
              "saki",
              "he",
              "i",
              "ku",
              "tsu",
              "mo",
              "ri",
              "sa"
            ]
          },
          {
            "ja": "筋書きのない日々を生きてく僕らは",
            "romaji": "sujigakinonaihibiwoikitekubokurawa",
            "ko": "각본 없는 나날을 살아가는 우리들은",
            "charRomaji": [
              "suji",
              "ga",
              "ki",
              "no",
              "na",
              "i",
              "hi",
              "bi",
              "wo",
              "i",
              "ki",
              "te",
              "ku",
              "boku",
              "ra",
              "wa"
            ]
          },
          {
            "ja": "慣れない感情にうろたえてる",
            "romaji": "narenaikanjouniurotaeteru",
            "ko": "익숙지 않은 감정에 당황하고 있어",
            "charRomaji": [
              "na",
              "re",
              "na",
              "i",
              "kan",
              "jou",
              "ni",
              "u",
              "ro",
              "ta",
              "e",
              "te",
              "ru"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "自分のこともまるでわからないのに",
            "romaji": "jibunnokotomomarudewakaranainoni",
            "ko": "자기 자신조차 전혀 알지 못하면서",
            "charRomaji": [
              "ji",
              "bun",
              "no",
              "ko",
              "to",
              "mo",
              "ma",
              "ru",
              "de",
              "wa",
              "ka",
              "ra",
              "na",
              "i",
              "no",
              "ni"
            ]
          },
          {
            "ja": "それでも君のことわかりたかったんだよ",
            "romaji": "soredemokiminokotowakaritakattandayo",
            "ko": "그럼에도 너에 대해서 알고 싶었어",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "kimi",
              "no",
              "ko",
              "to",
              "wa",
              "ka",
              "ri",
              "ta",
              "ka",
              "t",
              "ta",
              "n",
              "da",
              "yo"
            ]
          },
          {
            "ja": "手のひらにのせた便箋はあたたかい",
            "romaji": "tenohiraninosetabinsenhaatatakai",
            "ko": "손바닥 위에 올려둔 편지지는 따스해",
            "charRomaji": [
              "te",
              "no",
              "hi",
              "ra",
              "ni",
              "no",
              "se",
              "ta",
              "bin",
              "sen",
              "ha",
              "a",
              "ta",
              "ta",
              "ka",
              "i"
            ]
          },
          {
            "ja": "君と手つないでいるみたいで",
            "romaji": "kimitotetsunaideirumitaide",
            "ko": "너와 손을 맞잡고 있는 것만 같아서",
            "charRomaji": [
              "kimi",
              "to",
              "te",
              "tsu",
              "na",
              "i",
              "de",
              "i",
              "ru",
              "mi",
              "ta",
              "i",
              "de"
            ]
          },
          {
            "ja": "もう戻らない欠片を集めてみても",
            "romaji": "moumodoranaikakerawoatsumetemitemo",
            "ko": "이제 돌아오지 않는 조각들을 모아보아도",
            "charRomaji": [
              "mo",
              "u",
              "modo",
              "ra",
              "na",
              "i",
              "ka",
              "kera",
              "wo",
              "atsu",
              "me",
              "te",
              "mi",
              "te",
              "mo"
            ]
          },
          {
            "ja": "二度と同じ瞬間に帰れなくて",
            "romaji": "nidotoonajishunkannikaerenakute",
            "ko": "두 번 다시 똑같은 순간으로 돌아갈 수 없어서",
            "charRomaji": [
              "ni",
              "do",
              "to",
              "ona",
              "ji",
              "shun",
              "kan",
              "ni",
              "kae",
              "re",
              "na",
              "ku",
              "te"
            ]
          },
          {
            "ja": "はぐれた道がもう一度交わるなら",
            "romaji": "haguretamichigamouichidomajiwarunara",
            "ko": "갈라진 길이 다시 한번 이 앞길에서 만난다면",
            "charRomaji": [
              "ha",
              "gu",
              "re",
              "ta",
              "michi",
              "ga",
              "mo",
              "u",
              "ichi",
              "do",
              "maji",
              "wa",
              "ru",
              "na",
              "ra"
            ]
          },
          {
            "ja": "うつむかずうたうよ君を見つけたいから",
            "romaji": "utsumukazuutauyokimiwomitsuketaikara",
            "ko": "고개 숙이지 않고 노래할게, 너를 찾고 싶으니까",
            "charRomaji": [
              "u",
              "tsu",
              "mu",
              "ka",
              "zu",
              "u",
              "ta",
              "u",
              "yo",
              "kimi",
              "wo",
              "mi",
              "tsu",
              "ke",
              "ta",
              "i",
              "ka",
              "ra"
            ]
          },
          {
            "ja": "ああ僕らにしか迷えないたった今を",
            "romaji": "aabokuranishikamayoenaitattaimawo",
            "ko": "아아, 오직 우리만이 헤맬 수 있는 바로 지금을",
            "charRomaji": [
              "a",
              "a",
              "boku",
              "ra",
              "ni",
              "shi",
              "ka",
              "mayo",
              "e",
              "na",
              "i",
              "ta",
              "t",
              "ta",
              "ima",
              "wo"
            ]
          },
          {
            "ja": "忘れたくないからうたっている",
            "romaji": "wasuretakunaikarautatteiru",
            "ko": "결코 잊고 싶지 않으니까 노래하고 있어",
            "charRomaji": [
              "wasu",
              "re",
              "ta",
              "ku",
              "na",
              "i",
              "ka",
              "ra",
              "u",
              "ta",
              "t",
              "te",
              "i",
              "ru"
            ]
          }
        ]
      }
    ]
  },
  {
    "id": "ouran'in",
    "title": "往欄印",
    "reading": "おうらんいん",
    "category": "original",
    "album": "7th Single『往欄印』, 3rd Album『致並跡』",
    "youtubeId": "ypcMuQhWdZA",
    "parts": [
      {
        "id": "part1",
        "name": "Part 1 (前半・1番)",
        "lines": [
          {
            "ja": "分厚く巻いた緩衝材の中",
            "romaji": "funatsukumaitakanshouzainonaka",
            "ko": "두껍게 둘러 감은 완충재 속에서",
            "charRomaji": [
              "fun",
              "atsu",
              "ku",
              "ma",
              "i",
              "ta",
              "kan",
              "shou",
              "zai",
              "no",
              "naka"
            ]
          },
          {
            "ja": "僕は僕を守ろうとした",
            "romaji": "bokuhabokuwomamoroutoshita",
            "ko": "나는 나 자신을 지키려고 했어",
            "charRomaji": [
              "boku",
              "ha",
              "boku",
              "wo",
              "mamo",
              "ro",
              "u",
              "to",
              "shi",
              "ta"
            ]
          },
          {
            "ja": "それは壊れやすいものなんだって",
            "romaji": "sorehakowareyasuimononandatte",
            "ko": "그것은 너무나 깨지기 쉬운 거라며",
            "charRomaji": [
              "so",
              "re",
              "ha",
              "kowa",
              "re",
              "ya",
              "su",
              "i",
              "mo",
              "no",
              "na",
              "n",
              "da",
              "t",
              "te"
            ]
          },
          {
            "ja": "張り巡らした予防線",
            "romaji": "harimegurashitayobousen",
            "ko": "사방에 촘촘히 쳐두었던 예방선",
            "charRomaji": [
              "ha",
              "ri",
              "megu",
              "ra",
              "shi",
              "ta",
              "yo",
              "bou",
              "sen"
            ]
          },
          {
            "ja": "ズンズンと振動に突き動かされて",
            "romaji": "zunzuntoshindounitsukiugokasarete",
            "ko": "쿵쾅쿵쾅 진동에 떠밀리고 뒤흔들려",
            "charRomaji": [
              "zu",
              "n",
              "zu",
              "n",
              "to",
              "shin",
              "dou",
              "ni",
              "tsu",
              "ki",
              "ugo",
              "ka",
              "sa",
              "re",
              "te"
            ]
          },
          {
            "ja": "一枚また一枚と振り落ちた",
            "romaji": "ichimaimataichimaitofuriochita",
            "ko": "한 장, 또 한 장씩 떨어져 나갔어",
            "charRomaji": [
              "ichi",
              "mai",
              "ma",
              "ta",
              "ichi",
              "mai",
              "to",
              "fu",
              "ri",
              "o",
              "chi",
              "ta"
            ]
          },
          {
            "ja": "安心する場所から顔を出して",
            "romaji": "anshinsurubashokarakaowodashite",
            "ko": "안심할 수 있는 둥지에서 고개를 내밀고",
            "charRomaji": [
              "an",
              "shin",
              "su",
              "ru",
              "ba",
              "sho",
              "ka",
              "ra",
              "kao",
              "wo",
              "da",
              "shi",
              "te"
            ]
          },
          {
            "ja": "僕は僕に傷つくことを許した",
            "romaji": "bokuhabokunikizutsukukotowoyurushita",
            "ko": "나는 나 자신에게 상처 입는 것을 허락했어",
            "charRomaji": [
              "boku",
              "ha",
              "boku",
              "ni",
              "kizu",
              "tsu",
              "ku",
              "ko",
              "to",
              "wo",
              "yuru",
              "shi",
              "ta"
            ]
          }
        ]
      },
      {
        "id": "part2",
        "name": "Part 2 (後半・2番~ラスト)",
        "lines": [
          {
            "ja": "ここからじゃなきゃ見えない気がしたんだ",
            "romaji": "kokokarajanakyamienaikigashitanda",
            "ko": "여기서가 아니면 보이지 않을 것만 같았어",
            "charRomaji": [
              "ko",
              "ko",
              "ka",
              "ra",
              "j",
              "a",
              "na",
              "ky",
              "a",
              "mi",
              "e",
              "na",
              "i",
              "ki",
              "ga",
              "shi",
              "ta",
              "n",
              "da"
            ]
          },
          {
            "ja": "手すりの無い端っこに立って",
            "romaji": "tesurinonaihajikkonitatte",
            "ko": "난간조차 없는 가장자리 끝에 서서",
            "charRomaji": [
              "te",
              "su",
              "ri",
              "no",
              "na",
              "i",
              "haji",
              "k",
              "ko",
              "ni",
              "ta",
              "t",
              "te"
            ]
          },
          {
            "ja": "些細な風にバランスを崩しながら",
            "romaji": "sasainakazenibaransuwokuzushinagara",
            "ko": "사소한 바람에도 휘청 균형을 잃으면서도",
            "charRomaji": [
              "sa",
              "sai",
              "na",
              "kaze",
              "ni",
              "ba",
              "ra",
              "n",
              "su",
              "wo",
              "kuzu",
              "shi",
              "na",
              "ga",
              "ra"
            ]
          },
          {
            "ja": "それでも伝い歩いていく",
            "romaji": "soredemotsudaiaruiteiku",
            "ko": "그럼에도 더듬어가며 한 걸음씩 걸어가",
            "charRomaji": [
              "so",
              "re",
              "de",
              "mo",
              "tsuda",
              "i",
              "aru",
              "i",
              "te",
              "i",
              "ku"
            ]
          },
          {
            "ja": "往欄印を押した消印のように",
            "romaji": "ouraninwooshitakeshiinnoyouni",
            "ko": "왕란인을 찍어 누른 소인처럼",
            "charRomaji": [
              "ou",
              "ran",
              "in",
              "wo",
              "o",
              "shi",
              "ta",
              "keshi",
              "in",
              "no",
              "yo",
              "u",
              "ni"
            ]
          },
          {
            "ja": "決して消えない僕らの足跡",
            "romaji": "kesshitekienaibokuranosokuseki",
            "ko": "결코 지워지지 않는 우리들의 발자국",
            "charRomaji": [
              "kes",
              "shi",
              "te",
              "ki",
              "e",
              "na",
              "i",
              "boku",
              "ra",
              "no",
              "so",
              "kuseki"
            ]
          },
          {
            "ja": "迷いながらも進み続ける",
            "romaji": "mayoinagaramosusumitsuzukeru",
            "ko": "헤매고 방황할지라도 계속 나아가리라",
            "charRomaji": [
              "mayo",
              "i",
              "na",
              "ga",
              "ra",
              "mo",
              "susu",
              "mi",
              "tsuzu",
              "ke",
              "ru"
            ]
          },
          {
            "ja": "僕らの道は此処から始まる",
            "romaji": "bokuranomichiwakokokarahajimaru",
            "ko": "우리들의 눈부신 길은 바로 이곳에서 시작돼",
            "charRomaji": [
              "boku",
              "ra",
              "no",
              "michi",
              "wa",
              "ko",
              "ko",
              "ka",
              "ra",
              "haji",
              "ma",
              "ru"
            ]
          }
        ]
      }
    ]
  }
];
