// MyGO!!!!! Song Database for Lyrics Typing Practice
// Enhanced with Korean translations, Romaji mappings, and verified YouTube IDs

export interface SongLine {
  ja: string;
  romaji: string;
  ko: string;
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
        "ja": "泣きそうな空見上げて",
        "romaji": "nakisounasoramiawete",
        "ko": "울 것 같은 하늘을 올려다보며"
      },
      {
        "ja": "立ち止まる交差点で",
        "romaji": "tachidomarukousatende",
        "ko": "멈춰 서는 교차로에서"
      },
      {
        "ja": "迷子のままの僕たちは",
        "romaji": "maigonomamanobokutachiwa",
        "ko": "미아인 그대로인 우리들은"
      },
      {
        "ja": "どこへ向かって走ればいい",
        "romaji": "dokoemukattehashirebaii",
        "ko": "어디를 향해 달려야 할까"
      },
      {
        "ja": "胸の奥で叫んでる声",
        "romaji": "munenookudesakenderukoe",
        "ko": "가슴 깊은 곳에서 외치는 목소리"
      },
      {
        "ja": "誰にも届かないままで",
        "romaji": "darenimotodokanaimamade",
        "ko": "누구에게도 닿지 않은 채로"
      },
      {
        "ja": "それでも手を伸ばしたくて",
        "romaji": "soredemotewonobashitakute",
        "ko": "그럼에도 손을 뻗고 싶어서"
      },
      {
        "ja": "夜空に光る星を探す",
        "romaji": "yozoranihikaruhoshiwosagasu",
        "ko": "밤하늘에 빛나는 별을 찾아"
      },
      {
        "ja": "僕らは迷いながら生きていく",
        "romaji": "bokurawamayoinagaraikiteiku",
        "ko": "우리는 헤매면서 살아갈 거야"
      },
      {
        "ja": "叫び続けるこの場所から",
        "romaji": "sakebitsuzukerukonobashokara",
        "ko": "계속 외칠 거야 이 자리에서"
      }
    ]
  },
  {
    "id": "nanashigoe",
    "title": "名無声",
    "reading": "ななしごえ",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "2mM64qcBYg8",
    "lines": [
      {
        "ja": "言葉にならない感情が",
        "romaji": "kotobaninaranaikanjouga",
        "ko": "말이 되지 않는 감정들이"
      },
      {
        "ja": "喉の奥で震えている",
        "romaji": "nodonookudefurueteiru",
        "ko": "목구멍 깊은 곳에서 떨리고 있어"
      },
      {
        "ja": "名前のないこの痛みを",
        "romaji": "namaenonaikonoitamiwo",
        "ko": "이름 없는 이 아픔을"
      },
      {
        "ja": "誰が分かってくれるだろう",
        "romaji": "daregawakattekerudarou",
        "ko": "누가 알아줄 수 있을까"
      },
      {
        "ja": "消えてしまいたい夜にも",
        "romaji": "kieteshimaitaiyorunimo",
        "ko": "사라져 버리고 싶은 밤에도"
      },
      {
        "ja": "歌だけは傍にあった",
        "romaji": "utadakewasobaniatta",
        "ko": "노래만은 곁에 있어 주었어"
      },
      {
        "ja": "響け名もなき僕らの声",
        "romaji": "hibikenamonakibokuranokoe",
        "ko": "울려 퍼져라 이름 없는 우리들의 목소리"
      },
      {
        "ja": "明日へと繋ぐ祈りのように",
        "romaji": "asitawotsunaguinorinoyouni",
        "ko": "내일로 이어지는 기도처럼"
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
        "ja": "一瞬の出会いの中で",
        "romaji": "isshunnodeainonakade",
        "ko": "한순간의 만남 속에서"
      },
      {
        "ja": "重なり合ったこのメロディ",
        "romaji": "kasanariattakonomerodi",
        "ko": "겹쳐진 이 멜로디"
      },
      {
        "ja": "偶然じゃない奇跡を今",
        "romaji": "guuzenjanaikisekiwoima",
        "ko": "우연이 아닌 기적을 지금"
      },
      {
        "ja": "信じてみたいと思ったんだ",
        "romaji": "shinjitemitaitoomottanda",
        "ko": "믿어보고 싶다고 생각했어"
      },
      {
        "ja": "君と鳴らしたコードは",
        "romaji": "kimitonarashitakoudowa",
        "ko": "너와 함께 울린 코드는"
      },
      {
        "ja": "どこまでも遠く響いていく",
        "romaji": "dokomadetookuhibiiteiku",
        "ko": "어디까지나 멀리 울려 퍼져가"
      },
      {
        "ja": "音一会のこの瞬間を",
        "romaji": "otoichienokonoshunkanwo",
        "ko": "음일회의 이 순간을"
      },
      {
        "ja": "永遠に刻みつけよう",
        "romaji": "eiennikizamitsukeyou",
        "ko": "영원히 새겨 넣자"
      }
    ]
  },
  {
    "id": "senzaihyoumei",
    "title": "潜在表明",
    "reading": "せんざいひょうめい",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "bkUqxpb_vYY",
    "lines": [
      {
        "ja": "隠していた本当の自分",
        "romaji": "kakushiteitahontounojibun",
        "ko": "숨기고 있던 진짜 나 자신"
      },
      {
        "ja": "暴き出されるのが怖くて",
        "romaji": "abakidasarerunogakowakute",
        "ko": "들통나는 것이 너무 두려워서"
      },
      {
        "ja": "仮面をつけて笑ってた",
        "romaji": "kamenwotsuketewaratteta",
        "ko": "가면을 쓰고 웃고 있었어"
      },
      {
        "ja": "だけどもう限界なんだよ",
        "romaji": "dakedomougenkainandayo",
        "ko": "하지만 이젠 한계란 말이야"
      },
      {
        "ja": "潜在していた感情を",
        "romaji": "senzaishiteitakanjouwo",
        "ko": "잠재되어 있던 감정을"
      },
      {
        "ja": "今ここで解き放て",
        "romaji": "imakokodetokihanate",
        "ko": "지금 여기서 해방해라"
      },
      {
        "ja": "歪なままで生きてやる",
        "romaji": "ibitsunamamadeikiteyaru",
        "ko": "일그러진 채로 살아주겠어"
      },
      {
        "ja": "これが僕の表明だ",
        "romaji": "koregabokunohyoumeida",
        "ko": "이것이 나의 표명이다"
      }
    ]
  },
  {
    "id": "kageiromai",
    "title": "影色舞",
    "reading": "かげいろまい",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "iFIXi6zzCls",
    "lines": [
      {
        "ja": "踊り明かせ影の色",
        "romaji": "odoriakasekagenoiro",
        "ko": "밤새 춤춰라 그림자의 색이여"
      },
      {
        "ja": "光と闇が溶け合う場所で",
        "romaji": "hikaritoyamigatokeaubashode",
        "ko": "빛과 어둠이 녹아드는 곳에서"
      },
      {
        "ja": "ステップを踏んで回れ",
        "romaji": "suteppuwofundemaware",
        "ko": "스텝을 밟으며 돌아라"
      },
      {
        "ja": "誰も追いつけない速さで",
        "romaji": "daremooitsukenaihayasade",
        "ko": "누구도 따라잡을 수 없는 속도로"
      },
      {
        "ja": "影色舞い散る夜に",
        "romaji": "kageiromaichiruyoruni",
        "ko": "그림자 색 흩날리는 밤에"
      },
      {
        "ja": "解き放たれる衝動",
        "romaji": "tokihanatarerushoudou",
        "ko": "해방되는 충동"
      },
      {
        "ja": "息が切れるまで叫べ",
        "romaji": "ikigakirerumadesakebe",
        "ko": "숨이 턱 끝까지 찰 때까지 외쳐라"
      },
      {
        "ja": "僕らがここにいる証を",
        "romaji": "bokuragakokoniiruakashiwo",
        "ko": "우리가 여기에 있다는 증표를"
      }
    ]
  },
  {
    "id": "hitoshizuku",
    "title": "壱雫空",
    "reading": "ひとしずく",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "Q0HMCtKbbm0",
    "lines": [
      {
        "ja": "雨上がりの空を見上げて",
        "romaji": "ameagarinosorawomiawete",
        "ko": "비 갠 뒤의 하늘을 올려다보며"
      },
      {
        "ja": "落ちてくる一雫の涙",
        "romaji": "ochitekuruhitoshizukunonamida",
        "ko": "떨어져 내리는 한 방울의 눈물"
      },
      {
        "ja": "滲んでいく世界の中で",
        "romaji": "nijindeikusekainonakade",
        "ko": "번져가는 세상 속에서"
      },
      {
        "ja": "君の声を探している",
        "romaji": "kiminokoewosagashiteiru",
        "ko": "너의 목소리를 찾고 있어"
      },
      {
        "ja": "どんなに遠く離れても",
        "romaji": "donnanitookuhanaretemo",
        "ko": "아무리 멀리 떨어져 있어도"
      },
      {
        "ja": "あの日の誓いは消えない",
        "romaji": "anohinochikaiwakienai",
        "ko": "그날의 맹세는 사라지지 않아"
      },
      {
        "ja": "壱雫の空の下で",
        "romaji": "hitoshizukunosoranoshitade",
        "ko": "한 방울 눈물 어린 하늘 아래서"
      },
      {
        "ja": "僕らはまた走り出す",
        "romaji": "bokurawamatahashiridasu",
        "ko": "우리는 다시 달려 나간다"
      }
    ]
  },
  {
    "id": "shiori",
    "title": "栞",
    "reading": "しおり",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "wuUZjdiUCj0",
    "lines": [
      {
        "ja": "ページをめくる指が止まる",
        "romaji": "peijiwomekuruyubigatomaru",
        "ko": "페이지를 넘기던 손가락이 멈춰"
      },
      {
        "ja": "挟んだ栞のその場所に",
        "romaji": "hasandashiorinonobashoni",
        "ko": "끼워둔 책갈피 그 자리에"
      },
      {
        "ja": "忘れられない記憶がある",
        "romaji": "wasurerarenaikiokugaaru",
        "ko": "잊을 수 없는 기억이 있어"
      },
      {
        "ja": "君と過ごした日々の跡",
        "romaji": "kimitosugoshitahibinoato",
        "ko": "너와 함께 보냈던 나날의 흔적"
      },
      {
        "ja": "物語は続いていく",
        "romaji": "monogatariwatsuzuiteiku",
        "ko": "이야기는 계속 이어져 가"
      },
      {
        "ja": "たとえ結末が違っても",
        "romaji": "tatoeketsumatsugachigattemo",
        "ko": "설령 결말이 달라진다 해도"
      },
      {
        "ja": "この栞はずっとここに",
        "romaji": "konoshioriwayuttokokoni",
        "ko": "이 책갈피는 언제나 여기에"
      }
    ]
  },
  {
    "id": "tanebi",
    "title": "焚音打",
    "reading": "たねび",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "mNEbrOEoAHg",
    "lines": [
      {
        "ja": "胸の奥で燻る火花",
        "romaji": "munenookudekusuburuhibana",
        "ko": "가슴 깊은 곳에서 연기 피우는 불꽃"
      },
      {
        "ja": "まだ消えてなんかいないよ",
        "romaji": "madakietenankainaiyo",
        "ko": "아직 꺼진 것 따위 아니야"
      },
      {
        "ja": "叩きつけるようなビートで",
        "romaji": "tatakitsukeruyounabiitode",
        "ko": "내리치는 듯한 강렬한 비트로"
      },
      {
        "ja": "燃え上がらせてみせるから",
        "romaji": "moeagarasetemiserukara",
        "ko": "타오르게 만들어 보일 테니까"
      },
      {
        "ja": "焚音打鳴り響け今",
        "romaji": "tanebinarihibikeima",
        "ko": "타네비 울려 퍼져라 지금"
      },
      {
        "ja": "僕らの命の鼓動よ",
        "romaji": "bokuranoinochinokodouyo",
        "ko": "우리들 생명의 고동이여"
      },
      {
        "ja": "灰になるまで叫び続けろ",
        "romaji": "haininarumadesakebitsuzukero",
        "ko": "재가 될 때까지 계속 외쳐라"
      }
    ]
  },
  {
    "id": "hekitenbansou",
    "title": "碧天伴走",
    "reading": "へきてんばんそう",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "AxJBNUisMrc",
    "lines": [
      {
        "ja": "青く澄み渡る空の下",
        "romaji": "aokusumiwatarusoranoshita",
        "ko": "푸르고 맑게 갠 하늘 아래"
      },
      {
        "ja": "君の隣を走り抜ける",
        "romaji": "kiminotonariwohashirinukeru",
        "ko": "너의 곁을 달려 나가"
      },
      {
        "ja": "息を切らして笑い合おう",
        "romaji": "ikiwokirashitewaraiaou",
        "ko": "숨을 헐떡이며 함께 웃자"
      },
      {
        "ja": "どんな坂道だって怖くない",
        "romaji": "donnasakamichidattekowakunai",
        "ko": "그 어떤 언덕길이라도 두렵지 않아"
      },
      {
        "ja": "碧天伴走どこまでも",
        "romaji": "hekitenbansoudokomademo",
        "ko": "벽천반주 어디까지라도"
      },
      {
        "ja": "風を追い越して行こう",
        "romaji": "kazewooikoshiteikou",
        "ko": "바람을 앞질러 나아가자"
      },
      {
        "ja": "僕らの旅は始まったばかり",
        "romaji": "bokuranotabiwahajimattabakari",
        "ko": "우리들의 여행은 이제 막 시작됐어"
      },
      {
        "ja": "手を繋いでさあ前を向け",
        "romaji": "tewotsunaidesaamaewomuke",
        "ko": "손을 잡고 자, 앞을 향해라"
      }
    ]
  },
  {
    "id": "utaimashou",
    "title": "歌いましょう鳴らしましょう",
    "reading": "うたいましょうならしましょう",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "_0FI8xSgI1s",
    "lines": [
      {
        "ja": "歌いましょう鳴らしましょう",
        "romaji": "utaimashounarashimashou",
        "ko": "노래합시다 울려 퍼트립시다"
      },
      {
        "ja": "世界中に響くように",
        "romaji": "sekaijuunihibikuyouni",
        "ko": "온 세상에 울려 퍼지도록"
      },
      {
        "ja": "悲しい涙を拭い去って",
        "romaji": "kanashiinamidawonuguisatte",
        "ko": "슬픈 눈물을 닦아내고"
      },
      {
        "ja": "笑顔の花を咲かせよう",
        "romaji": "egaonohanawosakaseyou",
        "ko": "웃음의 꽃을 피워보자"
      },
      {
        "ja": "下手くそだって構わない",
        "romaji": "hetakusodattekamawanai",
        "ko": "서툴러도 상관없어"
      },
      {
        "ja": "心が震えていればいい",
        "romaji": "kokorogafurueteirebaii",
        "ko": "마음이 떨리고 있다면 그걸로 돼"
      },
      {
        "ja": "さあ一緒に声を出して",
        "romaji": "saaisshonikoewodashite",
        "ko": "자 함께 소리를 내어봐"
      }
    ]
  },
  {
    "id": "haruhikage",
    "title": "春日影 (MyGO!!!!! ver.)",
    "reading": "はるひかげ",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "NycFr6D6DSw",
    "lines": [
      {
        "ja": "やわらかな光が差し込む",
        "romaji": "yawarakanahikarigasashikomu",
        "ko": "부드러운 햇살이 비쳐 드는"
      },
      {
        "ja": "春の木漏れ日の中で",
        "romaji": "harunokomorebinonakade",
        "ko": "봄날 나뭇잎 사이 햇살 속에서"
      },
      {
        "ja": "君と交わしたあの約束",
        "romaji": "kimitokawashitaanoyakusoku",
        "ko": "너와 나누었던 그 약속"
      },
      {
        "ja": "今も胸に咲いているよ",
        "romaji": "imamomunenisaiteiruyo",
        "ko": "지금도 가슴속에 피어 있어"
      },
      {
        "ja": "どうして春日影をやったの",
        "romaji": "doushiteharuhikagewoyattano",
        "ko": "어째서 하루히카게를 연주한 거야"
      },
      {
        "ja": "迷いながらも歩き出す",
        "romaji": "mayoinagaramourukidasu",
        "ko": "방황하면서도 걸어 나가"
      },
      {
        "ja": "暖かな影に包まれて",
        "romaji": "atatakakakagenitsutsumarete",
        "ko": "따스한 그림자에 감싸여"
      },
      {
        "ja": "また逢える日を信じてる",
        "romaji": "mataaeruhiwoshinjiteru",
        "ko": "다시 만날 날을 믿고 있어"
      }
    ]
  },
  {
    "id": "utakotoba",
    "title": "詩超絆",
    "reading": "うたことば",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "wJ-OebTVyvk",
    "lines": [
      {
        "ja": "声にならない叫びを",
        "romaji": "koeninaranaisakebiwo",
        "ko": "목소리가 되지 않는 외침을"
      },
      {
        "ja": "詩に乗せて届けるんだ",
        "romaji": "utaninosetetodokerunda",
        "ko": "시에 실어서 전하는 거야"
      },
      {
        "ja": "千切れそうな絆を今",
        "romaji": "chigiresounakizunawoima",
        "ko": "끊어질 것 같은 인연을 지금"
      },
      {
        "ja": "もう一度結び直すために",
        "romaji": "mouichidomusubinaosutameni",
        "ko": "다시 한번 묶어내기 위해서"
      },
      {
        "ja": "不器用だっていいじゃないか",
        "romaji": "bukiyoudatteiijanaika",
        "ko": "서툴러도 괜찮지 않나"
      },
      {
        "ja": "僕らは迷子なんだから",
        "romaji": "bokurawamaigonandakara",
        "ko": "우리들은 미아니까"
      },
      {
        "ja": "詩超絆どこまでも",
        "romaji": "utakotobadokomademo",
        "ko": "우타코토바 어디까지라도"
      },
      {
        "ja": "魂をぶつけ合え",
        "romaji": "tamashiiwobutsukeae",
        "ko": "영혼을 서로 부딪쳐라"
      }
    ]
  },
  {
    "id": "meirohibi",
    "title": "迷路日々",
    "reading": "めいろひび",
    "category": "original",
    "album": "4th Single",
    "youtubeId": "STgVa-reZkM",
    "lines": [
      {
        "ja": "迷路のような毎日を",
        "romaji": "meironoyounamainichiwo",
        "ko": "미로와도 같은 매일을"
      },
      {
        "ja": "手探りで進んでいる",
        "romaji": "tesaguridesusundeiru",
        "ko": "더듬거리며 나아가고 있어"
      },
      {
        "ja": "出口が見つからなくても",
        "romaji": "deguchigamitsukaranakutemo",
        "ko": "출구를 찾지 못하더라도"
      },
      {
        "ja": "君がいるなら怖くないよ",
        "romaji": "kimigairunarakowakunaiyo",
        "ko": "네가 있다면 무섭지 않아"
      },
      {
        "ja": "壁にぶつかって泣いたって",
        "romaji": "kabenibutsukattenaitatte",
        "ko": "벽에 부딪혀 울더라도"
      },
      {
        "ja": "また立ち上がればいい",
        "romaji": "matatachiagarebaii",
        "ko": "다시 일어서면 돼"
      },
      {
        "ja": "迷路日々を愛そう",
        "romaji": "meirohibiwoaisou",
        "ko": "미로 같은 나날을 사랑하자"
      }
    ]
  },
  {
    "id": "noroshi",
    "title": "無路矢",
    "reading": "のろし",
    "category": "original",
    "album": "2nd Single",
    "youtubeId": "JZ2e_LVe6sU",
    "lines": [
      {
        "ja": "暗闇を射抜く矢のように",
        "romaji": "kurayamiwoinukuyanoyouni",
        "ko": "어둠을 꿰뚫는 화살처럼"
      },
      {
        "ja": "真っ直ぐに放たれた情熱",
        "romaji": "massugunihanataretajounetsu",
        "ko": "곧게 쏘아 올려진 정열"
      },
      {
        "ja": "道なき道を切り開け",
        "romaji": "michinakimichiwokirihirake",
        "ko": "길 없는 길을 개척해 나가라"
      },
      {
        "ja": "恐れるものは何もない",
        "romaji": "osorerumonowananimonai",
        "ko": "두려워할 것은 아무것도 없어"
      },
      {
        "ja": "無路矢放て高らかに",
        "romaji": "noroshihanatetakarakani",
        "ko": "노로시를 쏘아 올려라 드높이"
      },
      {
        "ja": "未来を照らし出す光となれ",
        "romaji": "miraiwoterashidasuhikaritonare",
        "ko": "미래를 밝혀내는 빛이 되어라"
      },
      {
        "ja": "僕らの覚悟を見せてやる",
        "romaji": "bokuranokakugowomisetheyaru",
        "ko": "우리들의 각오를 보여주마"
      }
    ]
  },
  {
    "id": "sasunso",
    "title": "砂寸奏",
    "reading": "さすんそう",
    "category": "original",
    "album": "4th Single",
    "youtubeId": "uiWLU577gYY",
    "lines": [
      {
        "ja": "砂時計の砂のように",
        "romaji": "sunadokeinosunanoyouni",
        "ko": "모래시계의 모래알처럼"
      },
      {
        "ja": "こぼれ落ちていく時間",
        "romaji": "koboreochiteikujikan",
        "ko": "흘러내려 떨어지는 시간"
      },
      {
        "ja": "一寸の狂いもなく奏でる",
        "romaji": "issunnokuruimonakukanaderu",
        "ko": "한 치의 오차도 없이 연주하는"
      },
      {
        "ja": "僕らの刹那の調べ",
        "romaji": "bokuranosetsunanoshirabe",
        "ko": "우리들의 찰나의 선율"
      },
      {
        "ja": "砂寸奏鳴り響かせて",
        "romaji": "sasunsonarihibikasete",
        "ko": "사순소 울려 퍼지게 하여"
      },
      {
        "ja": "今この瞬間を生きる",
        "romaji": "imakonoshunkanwoikiru",
        "ko": "지금 이 순간을 살아가"
      }
    ]
  },
  {
    "id": "kaisoufu",
    "title": "回層浮",
    "reading": "かいそうふ",
    "category": "original",
    "album": "5th Single",
    "youtubeId": "k5u1nueXES8",
    "lines": [
      {
        "ja": "記憶の底へ沈んでいく",
        "romaji": "kiokunosokoeshizundeiku",
        "ko": "기억의 밑바닥으로 가라앉아 가"
      },
      {
        "ja": "幾重にも重なる想い",
        "romaji": "ikuenimokasanaruomoi",
        "ko": "겹겹이 쌓여가는 마음들"
      },
      {
        "ja": "水面へと浮かび上がる",
        "romaji": "minamoetoukabiagaru",
        "ko": "수면 위로 떠올라 오는"
      },
      {
        "ja": "あの日の君の微笑み",
        "romaji": "anohinokiminohohoemi",
        "ko": "그날 너의 미소"
      },
      {
        "ja": "回層浮揺らめきながら",
        "romaji": "kaisoufuyuramekinagara",
        "ko": "회층부 일렁이면서"
      },
      {
        "ja": "光を求めて泳いでいく",
        "romaji": "hikariwomotometeoyoideiku",
        "ko": "빛을 찾아 헤엄쳐 가"
      }
    ]
  },
  {
    "id": "shokyuusei",
    "title": "処救生",
    "reading": "しょきゅうせい",
    "category": "original",
    "album": "5th Single",
    "youtubeId": "1_XZ0VJIpwI",
    "lines": [
      {
        "ja": "息苦しいこの世界で",
        "romaji": "ikigurushiikonosekaide",
        "ko": "숨 막히는 이 세상에서"
      },
      {
        "ja": "必死に酸素を求めてる",
        "romaji": "hisshinosansowomotometeru",
        "ko": "필사적으로 산소를 찾고 있어"
      },
      {
        "ja": "生きている実感が欲しい",
        "romaji": "ikiteirujikkangahoshii",
        "ko": "살아있다는 실감을 원해"
      },
      {
        "ja": "ただ呼吸をするだけじゃなく",
        "romaji": "tadakokyuuwosurudakejanaku",
        "ko": "그저 숨만 쉬는 것이 아니라"
      },
      {
        "ja": "処救生救いを叫べ",
        "romaji": "shokyuuseisukuiwosakebe",
        "ko": "처구생 구원을 외쳐라"
      },
      {
        "ja": "生き延びるための歌を",
        "romaji": "ikinobirutamenoutawo",
        "ko": "살아남기 위한 노래를"
      }
    ]
  },
  {
    "id": "hashidoyama",
    "title": "端程山",
    "reading": "はしどやま",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "1c2uSrAGF9Q",
    "lines": [
      {
        "ja": "険しい山のいただきへ",
        "romaji": "kewashiizamanoitadakihe",
        "ko": "험준한 산봉우리를 향해"
      },
      {
        "ja": "一歩ずつ踏みしめていく",
        "romaji": "ippozutsufumishimeteiku",
        "ko": "한 걸음씩 굳세게 내딛어 가"
      },
      {
        "ja": "見渡す限りのパノラマ",
        "romaji": "miwatasukagirinopanorama",
        "ko": "끝없이 펼쳐지는 파노라마"
      },
      {
        "ja": "風が頬を撫でていくよ",
        "romaji": "kazegahohowonadetekuyo",
        "ko": "바람이 뺨을 스쳐 지나가"
      },
      {
        "ja": "端程山登りつめたら",
        "romaji": "hashidoyamanoboritsumetara",
        "ko": "하시도야마 끝까지 올라선다면"
      },
      {
        "ja": "新しい朝が待っている",
        "romaji": "atarashiiasagamatteiru",
        "ko": "새로운 아침이 기다리고 있어"
      }
    ]
  },
  {
    "id": "rinpuu",
    "title": "輪符雨",
    "reading": "りんぷう",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "xNF9semW-Ng",
    "lines": [
      {
        "ja": "降りしきる雨のリフレイン",
        "romaji": "furishikiruamenorifurein",
        "ko": "줄기차게 쏟아지는 비의 리프레인"
      },
      {
        "ja": "街の音をかき消していく",
        "romaji": "machinootowokakikeshiteiku",
        "ko": "거리의 소음을 지워가"
      },
      {
        "ja": "輪を描いて落ちる雫",
        "romaji": "wawokaitetochirushizuku",
        "ko": "동심원을 그리며 떨어지는 빗방울"
      },
      {
        "ja": "僕の心も濡らしていく",
        "romaji": "bokunokokoromonurashiteiku",
        "ko": "내 마음마저 적셔가고 있어"
      },
      {
        "ja": "輪符雨よ洗い流して",
        "romaji": "rinpuuyoarainagashite",
        "ko": "린푸우여 모두 씻어내어라"
      },
      {
        "ja": "抱えきれない孤独さえも",
        "romaji": "kakaekirenaikodokusaemo",
        "ko": "다 감당할 수 없는 고독마저도"
      }
    ]
  },
  {
    "id": "kokairou",
    "title": "孤壊牢",
    "reading": "こかいろう",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "4Dz3pcgg_Mo",
    "lines": [
      {
        "ja": "閉じこもっていた部屋の窓",
        "romaji": "tojikomotteitaheyanomado",
        "ko": "틀어박혀 있던 방의 창문"
      },
      {
        "ja": "光が怖くてカーテンを閉めた",
        "romaji": "hikarigakowakutekaatenwoshimeta",
        "ko": "빛이 두려워 커튼을 닫았어"
      },
      {
        "ja": "孤独という名の檻を壊せ",
        "romaji": "kodokutoyounanooriwokowase",
        "ko": "고독이라는 이름의 감옥을 부숴라"
      },
      {
        "ja": "ここから抜け出す時が来た",
        "romaji": "kokokaranukedasutokigakita",
        "ko": "이곳에서 빠져나갈 때가 왔다"
      },
      {
        "ja": "孤壊牢打ち破れ今",
        "romaji": "kokairouuchiyabureima",
        "ko": "코카이로를 깨부숴라 지금"
      },
      {
        "ja": "本当の自由を掴むために",
        "romaji": "hontounojiyuuwotsukamutameni",
        "ko": "진정한 자유를 손에 넣기 위해"
      }
    ]
  },
  {
    "id": "hoshuudou",
    "title": "歩拾道",
    "reading": "ほしゅうどう",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "EEeYU4-dhZk",
    "lines": [
      {
        "ja": "落ちていた小さな欠片を",
        "romaji": "ochiteitachiisanakakerawo",
        "ko": "떨어져 있던 작은 조각들을"
      },
      {
        "ja": "一つずつ拾い集めて",
        "romaji": "hitotsuzutsuhiroiatsumete",
        "ko": "하나씩 주워 모아서"
      },
      {
        "ja": "歩き続ける僕らの道",
        "romaji": "arukitsuzukerubokuranomichi",
        "ko": "계속해서 걸어가는 우리들의 길"
      },
      {
        "ja": "無駄なことなんて何もない",
        "romaji": "mudanakotonantenanimonai",
        "ko": "헛된 것 따윈 아무것도 없어"
      },
      {
        "ja": "歩拾道スピードを上げて",
        "romaji": "hoshuudousupiidowoagete",
        "ko": "호슈도 속도를 높여서"
      },
      {
        "ja": "未来の先へと飛び出そう",
        "romaji": "mirainosakietotobidasou",
        "ko": "미래의 저편으로 뛰쳐나가자"
      }
    ]
  },
  {
    "id": "yaonzen",
    "title": "夜隠染",
    "reading": "やおんぜん",
    "category": "original",
    "album": "6th Single",
    "youtubeId": "7kPyHJ2SA9g",
    "lines": [
      {
        "ja": "夜の帳に隠れながら",
        "romaji": "yorunotobarinikakurenagara",
        "ko": "밤의 장막 속에 숨으면서"
      },
      {
        "ja": "染まっていく漆黒の街",
        "romaji": "somatteikushikkokunomachi",
        "ko": "물들어가는 칠흑 같은 거리"
      },
      {
        "ja": "冷たい風が吹き抜けて",
        "romaji": "tsumetaikazegafukinukete",
        "ko": "차가운 바람이 불어와"
      },
      {
        "ja": "心までも凍えそうだよ",
        "romaji": "kokoromademokogoesoudayo",
        "ko": "마음마저 얼어붙을 것 같아"
      },
      {
        "ja": "夜隠染の闇の中で",
        "romaji": "yaonzennoyaminonakade",
        "ko": "야온젠의 어둠 속에서"
      },
      {
        "ja": "確かな温もりを探してる",
        "romaji": "tashikananukumoriwosagashiteru",
        "ko": "확실한 온기를 찾고 있어"
      }
    ]
  },
  {
    "id": "mushuutou",
    "title": "霧周途",
    "reading": "むしゅうと",
    "category": "original",
    "album": "6th Single",
    "youtubeId": "qJPXncScNA4",
    "lines": [
      {
        "ja": "深い霧に包まれた道",
        "romaji": "fukaikirinitsutsumaretamichi",
        "ko": "짙은 안개에 휩싸인 길"
      },
      {
        "ja": "前も見えない迷路の中",
        "romaji": "maemomienaimeirononaka",
        "ko": "앞도 보이지 않는 미로 속"
      },
      {
        "ja": "信じられるのはただ一つ",
        "romaji": "shinjirarerunowatadahitotsu",
        "ko": "믿을 수 있는 것은 단 하나"
      },
      {
        "ja": "握りしめた手のひらの熱",
        "romaji": "nigirishimetatenohiranonetsu",
        "ko": "꼭 쥐어 잡은 손바닥의 열기"
      },
      {
        "ja": "霧周途ミストを抜けて",
        "romaji": "mushuutomisutowonukete",
        "ko": "무슈토 안개를 뚫고"
      },
      {
        "ja": "青空の下へ駆け出そう",
        "romaji": "aozoranoshitaekakedasou",
        "ko": "푸른 하늘 아래로 달려가자"
      }
    ]
  },
  {
    "id": "shoumeisanka",
    "title": "証命讃歌",
    "reading": "しょうめいさんか",
    "category": "original",
    "album": "9th Single",
    "youtubeId": "C_OJtQMU52Y",
    "lines": [
      {
        "ja": "僕らはここで生きていると",
        "romaji": "bokurawakokodeikiteirutou",
        "ko": "우리들은 여기서 살아있다고"
      },
      {
        "ja": "命の証を歌うんだ",
        "romaji": "inochinoakashiwoutaunda",
        "ko": "생명의 증표를 노래하는 거야"
      },
      {
        "ja": "どんな悲しみも越えていけ",
        "romaji": "donnakanashimimokoeteike",
        "ko": "그 어떤 슬픔도 뛰어넘어라"
      },
      {
        "ja": "讃歌を空へと轟かせろ",
        "romaji": "sankawozoraetotodorokasero",
        "ko": "찬가를 하늘로 포효하듯 울려라"
      },
      {
        "ja": "証命讃歌響き渡れ",
        "romaji": "shoumeisankahibikiwatare",
        "ko": "증명찬가 울려 퍼져라"
      },
      {
        "ja": "消えない光を灯すように",
        "romaji": "kienaihikarizotomosuyouni",
        "ko": "꺼지지 않는 빛을 밝히듯이"
      }
    ]
  },
  {
    "id": "nonbreath",
    "title": "ノンブレス・オブリージュ",
    "reading": "のんぶれす・おぶりーじゅ",
    "category": "cover",
    "album": "Cover Collection Extra",
    "youtubeId": "gS5n1i1H-yI",
    "lines": [
      {
        "ja": "息が苦しいなら吐き出せばいい",
        "romaji": "ikigakurushiinarahakidasebaii",
        "ko": "숨이 막힌다면 내뱉으면 돼"
      },
      {
        "ja": "言葉を詰まらせて泣くくらいなら",
        "romaji": "kotobawotsumarasetenakukurainara",
        "ko": "말문이 막혀 울어버릴 바엔"
      },
      {
        "ja": "ノンブレス息を止めたまま",
        "romaji": "nonburesuikiwotometamama",
        "ko": "논브레스 숨을 멈춘 채로"
      },
      {
        "ja": "この世界を駆け抜けていく",
        "romaji": "konosekaiwokakenuketeiku",
        "ko": "이 세상을 힘껏 달려 나가"
      },
      {
        "ja": "義務なんて投げ捨ててしまえ",
        "romaji": "gimunantenagesteteshimae",
        "ko": "의무 따위는 집어던져 버려"
      },
      {
        "ja": "僕らは僕らのために歌う",
        "romaji": "bokurawabokuranotameniutau",
        "ko": "우리들은 우리를 위해 노래한다"
      }
    ]
  },
  {
    "id": "kiminokamisama",
    "title": "君の神様になりたい。",
    "reading": "きみのかみさまになりたい",
    "category": "cover",
    "album": "Cover Collection Vol.10",
    "youtubeId": "W8bWP-E7IJE",
    "lines": [
      {
        "ja": "僕の命で君を救えるなら",
        "romaji": "bokunoinochidekimiwosukuerunara",
        "ko": "내 목숨으로 너를 구할 수 있다면"
      },
      {
        "ja": "喜んでこの命を差し出そう",
        "romaji": "yorokondekonoinochiwosashidasou",
        "ko": "기꺼이 이 목숨을 바치겠어"
      },
      {
        "ja": "君の神様になりたかった",
        "romaji": "kiminokamisamaninaritakatta",
        "ko": "너의 신이 되고 싶었어"
      },
      {
        "ja": "君の悲しみを全部背負って",
        "romaji": "kiminokanashimiwozenbuseotte",
        "ko": "너의 슬픔을 전부 짊어지고서"
      },
      {
        "ja": "僕が代わりに泣いてあげるよ",
        "romaji": "bokugakawarininaiteageruyo",
        "ko": "내가 대신 울어줄게"
      },
      {
        "ja": "どうか笑顔で生きていてほしい",
        "romaji": "doukaegaodeikiteitehoshii",
        "ko": "부디 미소 지으며 살아가 주길"
      }
    ]
  },
  {
    "id": "charles",
    "title": "シャルル",
    "reading": "しゃるる",
    "category": "cover",
    "album": "Cover Single",
    "youtubeId": "IKtjzy0uDkQ",
    "lines": [
      {
        "ja": "さよならはあなたから言った",
        "romaji": "sayonarahaanatakaraitta",
        "ko": "작별 인사는 당신이 먼저 건넸지"
      },
      {
        "ja": "それなのに頬を濡らしてしまうの",
        "romaji": "sorenanonihohowonurashiteshimawuno",
        "ko": "그런데도 뺨을 적셔버리고 마는 거야"
      },
      {
        "ja": "そうやって昨日の事も消してしまうなら",
        "romaji": "souyattekinounokotomokeshiteshimawnara",
        "ko": "그렇게 어제의 일도 지워버릴 거라면"
      },
      {
        "ja": "もういいよ 笑ってくれよ",
        "romaji": "mouiiyo warattekureyo",
        "ko": "이젠 됐어, 웃어줘"
      },
      {
        "ja": "愛を謳って謳って雲の上",
        "romaji": "aiwooutatteoutattekumonoue",
        "ko": "사랑을 노래하고 노래하며 구름 위로"
      },
      {
        "ja": "濁りきっては見えないや",
        "romaji": "nigorikittewamienaiya",
        "ko": "완전히 탁해져선 보이질 않네"
      }
    ]
  },
  {
    "id": "swim",
    "title": "swim",
    "reading": "すいむ",
    "category": "cover",
    "album": "Cover Single",
    "youtubeId": "Vs5YmJ6f6Ds",
    "lines": [
      {
        "ja": "泳いでいく冷たい波を掻き分けて",
        "romaji": "oyoideikutsumetainamiwokakiwakete",
        "ko": "헤엄쳐 나가 차가운 파도를 헤치며"
      },
      {
        "ja": "息継ぎさえも忘れるくらいに",
        "romaji": "ikitsugisaemowasurerukuraini",
        "ko": "숨을 고르는 것조차 잊어버릴 만큼"
      },
      {
        "ja": "向こう岸にあるはずの光へ",
        "romaji": "mukougishinianruhazunohikarie",
        "ko": "건너편 언덕에 있을 터인 빛을 향해"
      },
      {
        "ja": "止まることなく進み続けろ",
        "romaji": "tomarukotonakususumitsudukero",
        "ko": "멈추지 말고 계속 나아가라"
      },
      {
        "ja": "僕らのスウィムは終わらない",
        "romaji": "bokuranosuwimuwawaowaranai",
        "ko": "우리들의 헤엄은 끝나지 않아"
      }
    ]
  },
  {
    "id": "seishuncomplex",
    "title": "青春コンプレックス",
    "reading": "せいしゅんこんぷれっくす",
    "category": "cover",
    "album": "Cover Single",
    "youtubeId": "V_PDo4_K8OI",
    "lines": [
      {
        "ja": "暗がりから覗く眩しい世界",
        "romaji": "kuragarikaranozokumabushiisekai",
        "ko": "어둠 속에서 훔쳐보는 눈부신 세상"
      },
      {
        "ja": "僕には関係ないと思ってた",
        "romaji": "bokunihakankeinaitoomotteta",
        "ko": "나와는 상관없는 일이라 생각했어"
      },
      {
        "ja": "かき鳴らせギター歪んだ音で",
        "romaji": "kakinarasegitaahizundaoode",
        "ko": "마구 긁어 울려라 기타여, 일그러진 소리로"
      },
      {
        "ja": "青春コンプレックスを吹き飛ばせ",
        "romaji": "seishunkonpurekkusuwofukitobase",
        "ko": "청춘 콤플렉스를 날려버려라"
      },
      {
        "ja": "これが僕らのロックンロールだ",
        "romaji": "koregabokuranorokkunrooruda",
        "ko": "이것이 우리들의 로큰롤이다"
      }
    ]
  }
];
