import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Helper function to generate clean units from ja and romaji
# Each line has: ja, romaji, ko, units: [{ja: '...', romaji: '...'}]

songs = []

# 1. 迷星叫 (Mayoiuta)
songs.append({
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
            "units": [
                {"ja": "交", "romaji": "kou"},
                {"ja": "差", "romaji": "sa"},
                {"ja": "点", "romaji": "ten"},
                {"ja": "の", "romaji": "no"},
                {"ja": "真", "romaji": "man"},
                {"ja": "ん", "romaji": "n"},
                {"ja": "中", "romaji": "naka"}
            ]
        },
        {
            "ja": "急ぐ人に紛れて",
            "romaji": "isoguhitonimagirete",
            "ko": "서두르는 사람들에 뒤섞여",
            "units": [
                {"ja": "急", "romaji": "isogu"},
                {"ja": "ぐ", "romaji": ""},
                {"ja": "人", "romaji": "hito"},
                {"ja": "に", "romaji": "ni"},
                {"ja": "紛", "romaji": "magire"},
                {"ja": "れ", "romaji": ""},
                {"ja": "て", "romaji": "te"}
            ]
        },
        {
            "ja": "僕だけがあてもなく",
            "romaji": "bokudakegaatemonaku",
            "ko": "나만이 정처도 없이",
            "units": [
                {"ja": "僕", "romaji": "boku"},
                {"ja": "だ", "romaji": "da"},
                {"ja": "け", "romaji": "ke"},
                {"ja": "が", "romaji": "ga"},
                {"ja": "あ", "romaji": "a"},
                {"ja": "て", "romaji": "te"},
                {"ja": "も", "romaji": "mo"},
                {"ja": "な", "romaji": "na"},
                {"ja": "く", "romaji": "ku"}
            ]
        },
        {
            "ja": "漂うみたいだ",
            "romaji": "tadayoumaitada",
            "ko": "떠도는 것만 같아",
            "units": [
                {"ja": "漂", "romaji": "tadayou"},
                {"ja": "う", "romaji": ""},
                {"ja": "み", "romaji": "mi"},
                {"ja": "た", "romaji": "tai"},
                {"ja": "い", "romaji": ""},
                {"ja": "だ", "romaji": "da"}
            ]
        },
        {
            "ja": "流行りの歌はいつも",
            "romaji": "hayarinoutawaitsumo",
            "ko": "유행하는 노래는 언제나",
            "units": [
                {"ja": "流", "romaji": "hayari"},
                {"ja": "行", "romaji": ""},
                {"ja": "り", "romaji": ""},
                {"ja": "の", "romaji": "no"},
                {"ja": "歌", "romaji": "uta"},
                {"ja": "は", "romaji": "wa"},
                {"ja": "い", "romaji": "i"},
                {"ja": "つ", "romaji": "tsu"},
                {"ja": "も", "romaji": "mo"}
            ]
        },
        {
            "ja": "僕のことは歌ってない",
            "romaji": "bokunokotowautattenai",
            "ko": "내 이야기는 노래하지 않아",
            "units": [
                {"ja": "僕", "romaji": "boku"},
                {"ja": "の", "romaji": "no"},
                {"ja": "こ", "romaji": "ko"},
                {"ja": "と", "romaji": "to"},
                {"ja": "は", "romaji": "wa"},
                {"ja": "歌", "romaji": "utatte"},
                {"ja": "っ", "romaji": ""},
                {"ja": "て", "romaji": ""},
                {"ja": "な", "romaji": "na"},
                {"ja": "い", "romaji": "i"}
            ]
        },
        {
            "ja": "ねえビジョンの中から",
            "romaji": "neebijonnonakanakara",
            "ko": "저기, 전광판 속에서",
            "units": [
                {"ja": "ね", "romaji": "ne"},
                {"ja": "え", "romaji": "e"},
                {"ja": "ビ", "romaji": "bi"},
                {"ja": "ジ", "romaji": "jo"},
                {"ja": "ョ", "romaji": ""},
                {"ja": "ン", "romaji": "n"},
                {"ja": "の", "romaji": "no"},
                {"ja": "中", "romaji": "naka"},
                {"ja": "か", "romaji": "ka"},
                {"ja": "ら", "romaji": "ra"}
            ]
        },
        {
            "ja": "笑いかけないで",
            "romaji": "waraikakenaide",
            "ko": "웃는 얼굴로 바라보지 마",
            "units": [
                {"ja": "笑", "romaji": "warai"},
                {"ja": "い", "romaji": ""},
                {"ja": "か", "romaji": "ka"},
                {"ja": "け", "romaji": "ke"},
                {"ja": "な", "romaji": "na"},
                {"ja": "い", "romaji": "i"},
                {"ja": "で", "romaji": "de"}
            ]
        },
        {
            "ja": "また今日も声にならずに",
            "romaji": "matakyoumokoeninarazuni",
            "ko": "또 오늘도 목소리가 되지 못한 채",
            "units": [
                {"ja": "ま", "romaji": "ma"},
                {"ja": "た", "romaji": "ta"},
                {"ja": "今", "romaji": "kyou"},
                {"ja": "日", "romaji": ""},
                {"ja": "も", "romaji": "mo"},
                {"ja": "声", "romaji": "koe"},
                {"ja": "に", "romaji": "ni"},
                {"ja": "な", "romaji": "na"},
                {"ja": "ら", "romaji": "ra"},
                {"ja": "ず", "romaji": "zu"},
                {"ja": "に", "romaji": "ni"}
            ]
        },
        {
            "ja": "飲み込んだ感情",
            "romaji": "nomikondakanjou",
            "ko": "삼켜버린 감정",
            "units": [
                {"ja": "飲", "romaji": "nomi"},
                {"ja": "み", "romaji": ""},
                {"ja": "込", "romaji": "konda"},
                {"ja": "ん", "romaji": ""},
                {"ja": "だ", "romaji": ""},
                {"ja": "感", "romaji": "kan"},
                {"ja": "情", "romaji": "jou"}
            ]
        },
        {
            "ja": "下書き埋め尽くして",
            "romaji": "shitagakiumetsukushite",
            "ko": "임시 저장을 가득 채우고",
            "units": [
                {"ja": "下", "romaji": "shita"},
                {"ja": "書", "romaji": "gaki"},
                {"ja": "き", "romaji": ""},
                {"ja": "埋", "romaji": "ume"},
                {"ja": "め", "romaji": ""},
                {"ja": "尽", "romaji": "tsuku"},
                {"ja": "く", "romaji": ""},
                {"ja": "し", "romaji": "shi"},
                {"ja": "て", "romaji": "te"}
            ]
        },
        {
            "ja": "迷子でもいい迷子でも進め",
            "romaji": "maigodemoiimaigodemosusume",
            "ko": "미아라도 좋아, 미아라도 나아가라",
            "units": [
                {"ja": "迷", "romaji": "mai"},
                {"ja": "子", "romaji": "go"},
                {"ja": "で", "romaji": "de"},
                {"ja": "も", "romaji": "mo"},
                {"ja": "い", "romaji": "i"},
                {"ja": "い", "romaji": "i"},
                {"ja": "迷", "romaji": "mai"},
                {"ja": "子", "romaji": "go"},
                {"ja": "で", "romaji": "de"},
                {"ja": "も", "romaji": "mo"},
                {"ja": "進", "romaji": "susu"},
                {"ja": "め", "romaji": "me"}
            ]
        }
    ]
})

print("Song 1 done")
