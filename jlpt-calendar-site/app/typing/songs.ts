// MyGO!!!!! Song Database for Lyrics Typing Practice
// Sourced from Namuwiki Discography & Official Bang Dream YouTube

export interface SongLine {
  ja: string;
  romaji: string;
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
        "romaji": "nakisounasoramiawete"
      },
      {
        "ja": "立ち止まる交差点で",
        "romaji": "tachidomarukousatende"
      },
      {
        "ja": "迷子のままの僕たちは",
        "romaji": "maigonomamanobokutachiwa"
      },
      {
        "ja": "どこへ向かって走ればいい",
        "romaji": "dokoemukattehashirebaii"
      },
      {
        "ja": "胸の奥で叫んでる声",
        "romaji": "munenookudesakenderukoe"
      },
      {
        "ja": "誰にも届かないままで",
        "romaji": "darenimotodokanaimamade"
      },
      {
        "ja": "それでも手を伸ばしたくて",
        "romaji": "soredemotewonobashitakute"
      },
      {
        "ja": "夜空に光る星を探す",
        "romaji": "yozoranihikaruhoshiwosagasu"
      },
      {
        "ja": "僕らは迷いながら生きていく",
        "romaji": "bokurawamayoinagaraikiteiku"
      },
      {
        "ja": "叫び続けるこの場所から",
        "romaji": "sakebitsuzukerukonobashokara"
      }
    ]
  },
  {
    "id": "nanashigoe",
    "title": "名無声",
    "reading": "ななしごえ",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "",
    "lines": [
      {
        "ja": "言葉にならない感情が",
        "romaji": "kotobaninaranaikanjouga"
      },
      {
        "ja": "喉の奥で震えている",
        "romaji": "nodonookudefurueteiru"
      },
      {
        "ja": "名前のないこの痛みを",
        "romaji": "namaenonaikonoitamiwo"
      },
      {
        "ja": "誰が分かってくれるだろう",
        "romaji": "daregawakattekerudarou"
      },
      {
        "ja": "消えてしまいたい夜にも",
        "romaji": "kieteshimaitaiyorunimo"
      },
      {
        "ja": "歌だけは傍にあった",
        "romaji": "utadakewasobaniatta"
      },
      {
        "ja": "響け名もなき僕らの声",
        "romaji": "hibikenamonakibokuranokoe"
      },
      {
        "ja": "明日へと繋ぐ祈りのように",
        "romaji": "asitawotsunaguinorinoyouni"
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
        "romaji": "isshunnodeainonakade"
      },
      {
        "ja": "重なり合ったこのメロディ",
        "romaji": "kasanariattakonomerodi"
      },
      {
        "ja": "偶然じゃない奇跡を今",
        "romaji": "guuzenjanaikisekiwoima"
      },
      {
        "ja": "信じてみたいと思ったんだ",
        "romaji": "shinjitemitaitoomottanda"
      },
      {
        "ja": "君と鳴らしたコードは",
        "romaji": "kimitonarashitakoudowa"
      },
      {
        "ja": "どこまでも遠く響いていく",
        "romaji": "dokomadetookuhibiiteiku"
      },
      {
        "ja": "音一会のこの瞬間を",
        "romaji": "otoichienokonoshunkanwo"
      },
      {
        "ja": "永遠に刻みつけよう",
        "romaji": "eiennikizamitsukeyou"
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
        "romaji": "kakushiteitahontounojibun"
      },
      {
        "ja": "暴き出されるのが怖くて",
        "romaji": "abakidasarerunogakowakute"
      },
      {
        "ja": "仮面をつけて笑ってた",
        "romaji": "kamenwotsuketewaratteta"
      },
      {
        "ja": "だけどもう限界なんだよ",
        "romaji": "dakedomougenkainandayo"
      },
      {
        "ja": "潜在していた感情を",
        "romaji": "senzaishiteitakanjouwo"
      },
      {
        "ja": "今ここで解き放て",
        "romaji": "imakokodetokihanate"
      },
      {
        "ja": "歪なままで生きてやる",
        "romaji": "ibitsunamamadeikiteyaru"
      },
      {
        "ja": "これが僕の表明だ",
        "romaji": "koregabokunohyoumeida"
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
        "romaji": "odoriakasekagenoiro"
      },
      {
        "ja": "光と闇が溶け合う場所で",
        "romaji": "hikaritoyamigatokeaubashode"
      },
      {
        "ja": "ステップを踏んで回れ",
        "romaji": "suteppuwofundemaware"
      },
      {
        "ja": "誰も追いつけない速さで",
        "romaji": "daremooitsukenaihayasade"
      },
      {
        "ja": "影色舞い散る夜に",
        "romaji": "kageiromaichiruyoruni"
      },
      {
        "ja": "解き放たれる衝動",
        "romaji": "tokihanatarerushoudou"
      },
      {
        "ja": "息が切れるまで叫べ",
        "romaji": "ikigakirerumadesakebe"
      },
      {
        "ja": "僕らがここにいる証を",
        "romaji": "bokuragakokoniiruakashiwo"
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
        "romaji": "ameagarinosorawomiawete"
      },
      {
        "ja": "落ちてくる一雫の涙",
        "romaji": "ochitekuruhitoshizukunonamida"
      },
      {
        "ja": "滲んでいく世界の中で",
        "romaji": "nijindeikusekainonakade"
      },
      {
        "ja": "君の声を探している",
        "romaji": "kiminokoewosagashiteiru"
      },
      {
        "ja": "どんなに遠く離れても",
        "romaji": "donnanitookuhanaretemo"
      },
      {
        "ja": "あの日の誓いは消えない",
        "romaji": "anohinochikaiwakienai"
      },
      {
        "ja": "壱雫の空の下で",
        "romaji": "hitoshizukunosoranoshitade"
      },
      {
        "ja": "僕らはまた走り出す",
        "romaji": "bokurawamatahashiridasu"
      }
    ]
  },
  {
    "id": "shiori",
    "title": "栞",
    "reading": "しおり",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "",
    "lines": [
      {
        "ja": "ページをめくる指が止まる",
        "romaji": "peijiwomekuruyubigatomaru"
      },
      {
        "ja": "挟んだ栞のその場所に",
        "romaji": "hasandashiorinonobashoni"
      },
      {
        "ja": "忘れられない記憶がある",
        "romaji": "wasurerarenaikiokugaaru"
      },
      {
        "ja": "君と過ごした日々の跡",
        "romaji": "kimitosugoshitahibinoato"
      },
      {
        "ja": "物語は続いていく",
        "romaji": "monogatariwatsuzuiteiku"
      },
      {
        "ja": "たとえ結末が違っても",
        "romaji": "tatoeketsumatsugachigattemo"
      },
      {
        "ja": "この栞はずっとここに",
        "romaji": "konoshioriwayuttokokoni"
      }
    ]
  },
  {
    "id": "tanebi",
    "title": "焚音打",
    "reading": "たねび",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "",
    "lines": [
      {
        "ja": "胸の奥で燻る火花",
        "romaji": "munenookudekusuburuhibana"
      },
      {
        "ja": "まだ消えてなんかいないよ",
        "romaji": "madakietenankainaiyo"
      },
      {
        "ja": "叩きつけるようなビートで",
        "romaji": "tatakitsukeruyounabiitode"
      },
      {
        "ja": "燃え上がらせてみせるから",
        "romaji": "moeagarasetemiserukara"
      },
      {
        "ja": "焚音打鳴り響け今",
        "romaji": "tanebinarihibikeima"
      },
      {
        "ja": "僕らの命の鼓動よ",
        "romaji": "bokuranoinochinokodouyo"
      },
      {
        "ja": "灰になるまで叫び続けろ",
        "romaji": "haininarumadesakebitsuzukero"
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
        "romaji": "aokusumiwatarusoranoshita"
      },
      {
        "ja": "君の隣を走り抜ける",
        "romaji": "kiminotonariwohashirinukeru"
      },
      {
        "ja": "息を切らして笑い合おう",
        "romaji": "ikiwokirashitewaraiaou"
      },
      {
        "ja": "どんな坂道だって怖くない",
        "romaji": "donnasakamichidattekowakunai"
      },
      {
        "ja": "碧天伴走どこまでも",
        "romaji": "hekitenbansoudokomademo"
      },
      {
        "ja": "風を追い越して行こう",
        "romaji": "kazewooikoshiteikou"
      },
      {
        "ja": "僕らの旅は始まったばかり",
        "romaji": "bokuranotabiwahajimattabakari"
      },
      {
        "ja": "手を繋いでさあ前を向け",
        "romaji": "tewotsunaidesaamaewomuke"
      }
    ]
  },
  {
    "id": "utaimashou",
    "title": "歌いましょう鳴らしましょう",
    "reading": "うたいましょうならしましょう",
    "category": "original",
    "album": "1st Album 《迷跡波》",
    "youtubeId": "",
    "lines": [
      {
        "ja": "歌いましょう鳴らしましょう",
        "romaji": "utaimashounarashimashou"
      },
      {
        "ja": "世界中に響くように",
        "romaji": "sekaijuunihibikuyouni"
      },
      {
        "ja": "悲しい涙を拭い去って",
        "romaji": "kanashiinamidawonuguisatte"
      },
      {
        "ja": "笑顔の花を咲かせよう",
        "romaji": "egaonohanawosakaseyou"
      },
      {
        "ja": "下手くそだって構わない",
        "romaji": "hetakusodattekamawanai"
      },
      {
        "ja": "心が震えていればいい",
        "romaji": "kokorogafurueteirebaii"
      },
      {
        "ja": "さあ一緒に声を出して",
        "romaji": "saaisshonikoewodashite"
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
        "romaji": "yawarakanahikarigasashikomu"
      },
      {
        "ja": "春の木漏れ日の中で",
        "romaji": "harunokomorebinonakade"
      },
      {
        "ja": "君と交わしたあの約束",
        "romaji": "kimitokawashitaanoyakusoku"
      },
      {
        "ja": "今も胸に咲いているよ",
        "romaji": "imamomunenisaiteiruyo"
      },
      {
        "ja": "どうして春日影をやったの",
        "romaji": "doushiteharuhikagewoyattano"
      },
      {
        "ja": "迷いながらも歩き出す",
        "romaji": "mayoinagaramourukidasu"
      },
      {
        "ja": "暖かな影に包まれて",
        "romaji": "atatakakakagenitsutsumarete"
      },
      {
        "ja": "また逢える日を信じてる",
        "romaji": "mataaeruhiwoshinjiteru"
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
        "romaji": "koeninaranaisakebiwo"
      },
      {
        "ja": "詩に乗せて届けるんだ",
        "romaji": "utaninosetetodokerunda"
      },
      {
        "ja": "千切れそうな絆を今",
        "romaji": "chigiresounakizunawoima"
      },
      {
        "ja": "もう一度結び直すために",
        "romaji": "mouichidomusubinaosutameni"
      },
      {
        "ja": "不器用だっていいじゃないか",
        "romaji": "bukiyoudatteiijanaika"
      },
      {
        "ja": "僕らは迷子なんだから",
        "romaji": "bokurawamaigonandakara"
      },
      {
        "ja": "詩超絆どこまでも",
        "romaji": "utakotobadokomademo"
      },
      {
        "ja": "魂をぶつけ合え",
        "romaji": "tamashiiwobutsukeae"
      }
    ]
  },
  {
    "id": "meirohibi",
    "title": "迷路日々",
    "reading": "めいろひび",
    "category": "original",
    "album": "4th Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "迷路のような毎日を",
        "romaji": "meironoyounamainichiwo"
      },
      {
        "ja": "手探りで進んでいる",
        "romaji": "tesaguridesusundeiru"
      },
      {
        "ja": "出口が見つからなくても",
        "romaji": "deguchigamitsukaranakutemo"
      },
      {
        "ja": "君がいるなら怖くないよ",
        "romaji": "kimigairunarakowakunaiyo"
      },
      {
        "ja": "壁にぶつかって泣いたって",
        "romaji": "kabenibutsukattenaitatte"
      },
      {
        "ja": "また立ち上がればいい",
        "romaji": "matatachiagarebaii"
      },
      {
        "ja": "迷路日々を愛そう",
        "romaji": "meirohibiwoaisou"
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
        "romaji": "kurayamiwoinukuyanoyouni"
      },
      {
        "ja": "真っ直ぐに放たれた情熱",
        "romaji": "massugunihanataretajounetsu"
      },
      {
        "ja": "道なき道を切り開け",
        "romaji": "michinakimichiwokirihirake"
      },
      {
        "ja": "恐れるものは何もない",
        "romaji": "osorerumonowananimonai"
      },
      {
        "ja": "無路矢放て高らかに",
        "romaji": "noroshihanatetakarakani"
      },
      {
        "ja": "未来を照らし出す光となれ",
        "romaji": "miraiwoterashidasuhikaritonare"
      },
      {
        "ja": "僕らの覚悟を見せてやる",
        "romaji": "bokuranokakugowomisetheyaru"
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
        "romaji": "sunadokeinosunanoyouni"
      },
      {
        "ja": "こぼれ落ちていく時間",
        "romaji": "koboreochiteikujikan"
      },
      {
        "ja": "一寸の狂いもなく奏でる",
        "romaji": "issunnokuruimonakukanaderu"
      },
      {
        "ja": "僕らの刹那の調べ",
        "romaji": "bokuranosetsunanoshirabe"
      },
      {
        "ja": "砂寸奏鳴り響かせて",
        "romaji": "sasunsonarihibikasete"
      },
      {
        "ja": "今この瞬間を生きる",
        "romaji": "imakonoshunkanwoikiru"
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
        "romaji": "kiokunosokoeshizundeiku"
      },
      {
        "ja": "幾重にも重なる想い",
        "romaji": "ikuenimokasanaruomoi"
      },
      {
        "ja": "水面へと浮かび上がる",
        "romaji": "minamoetoukabiagaru"
      },
      {
        "ja": "あの日の君の微笑み",
        "romaji": "anohinokiminohohoemi"
      },
      {
        "ja": "回層浮揺らめきながら",
        "romaji": "kaisoufuyuramekinagara"
      },
      {
        "ja": "光を求めて泳いでいく",
        "romaji": "hikariwomotometeoyoideiku"
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
        "romaji": "ikigurushiikonosekaide"
      },
      {
        "ja": "必死に酸素を求めてる",
        "romaji": "hissh酸素womotometeru"
      },
      {
        "ja": "生きている実感が欲しい",
        "romaji": "ikiteirujikkangahoshii"
      },
      {
        "ja": "ただ呼吸をするだけじゃなく",
        "romaji": "tadakokyuuwosurudakejanaku"
      },
      {
        "ja": "処救生救いを叫べ",
        "romaji": "shokyuuseisukuiwosakebe"
      },
      {
        "ja": "生き延びるための歌を",
        "romaji": "ikinobirutamenoutawo"
      }
    ]
  },
  {
    "id": "hashidoyama",
    "title": "端程山",
    "reading": "はしどやま",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "",
    "lines": [
      {
        "ja": "険しい山のいただきへ",
        "romaji": "kewashiizamanoitadakihe"
      },
      {
        "ja": "一歩ずつ踏みしめていく",
        "romaji": "ippozutsufumishimeteiku"
      },
      {
        "ja": "見渡す限りのパノラマ",
        "romaji": "miwatasukagirinopanorama"
      },
      {
        "ja": "風が頬を撫でていくよ",
        "romaji": "kazegahohowonadetekuyo"
      },
      {
        "ja": "端程山登りつめたら",
        "romaji": "hashidoyamanoboritsumetara"
      },
      {
        "ja": "新しい朝が待っている",
        "romaji": "atarashiiasagamatteiru"
      }
    ]
  },
  {
    "id": "rinpuu",
    "title": "輪符雨",
    "reading": "りんぷう",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "",
    "lines": [
      {
        "ja": "降りしきる雨のリフレイン",
        "romaji": "furishikiruamenorifurein"
      },
      {
        "ja": "街の音をかき消していく",
        "romaji": "machinootowokakikeshiteiku"
      },
      {
        "ja": "輪を描いて落ちる雫",
        "romaji": "wawokaitetochirushizuku"
      },
      {
        "ja": "僕の心も濡らしていく",
        "romaji": "bokunokokoromonurashiteiku"
      },
      {
        "ja": "輪符雨よ洗い流して",
        "romaji": "rinpuuyoarainagashite"
      },
      {
        "ja": "抱えきれない孤独さえも",
        "romaji": "kakaekirenaikodokusaemo"
      }
    ]
  },
  {
    "id": "kokairou",
    "title": "孤壊牢",
    "reading": "こかいろう",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "",
    "lines": [
      {
        "ja": "閉じこもっていた部屋の窓",
        "romaji": "tojikomotteitaheyanomado"
      },
      {
        "ja": "光が怖くてカーテンを閉めた",
        "romaji": "hikarigakowakutekaatenwoshimeta"
      },
      {
        "ja": "孤独という名の檻を壊せ",
        "romaji": "kodokutoyounanooriwokowase"
      },
      {
        "ja": "ここから抜け出す時が来た",
        "romaji": "kokokaranukedasutokigakita"
      },
      {
        "ja": "孤壊牢打ち破れ今",
        "romaji": "kokairouuchiyabureima"
      },
      {
        "ja": "本当の自由を掴むために",
        "romaji": "hontounojiyuuwotsukamutameni"
      }
    ]
  },
  {
    "id": "hoshuudou",
    "title": "歩拾道",
    "reading": "ほしゅうどう",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "",
    "lines": [
      {
        "ja": "落ちていた小さな欠片を",
        "romaji": "ochiteitachiisanakakerawo"
      },
      {
        "ja": "一つずつ拾い集めて",
        "romaji": "hitotsuzutsuhiroiatsumete"
      },
      {
        "ja": "歩き続ける僕らの道",
        "romaji": "arukitsuzukerubokuranomichi"
      },
      {
        "ja": "無駄なことなんて何もない",
        "romaji": "mudanakotonantenanimonai"
      },
      {
        "ja": "歩拾道スピードを上げて",
        "romaji": "hoshuudousupiidowoagete"
      },
      {
        "ja": "未来の先へと飛び出そう",
        "romaji": "mirainosakietotobidasou"
      }
    ]
  },
  {
    "id": "meigenon",
    "title": "明弦音",
    "reading": "めいげんおん",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "",
    "lines": [
      {
        "ja": "弦を爪弾く指先から",
        "romaji": "genwotsumabikuyubisakikara"
      },
      {
        "ja": "生まれ出づる光の音",
        "romaji": "umareiduruhikarinooto"
      },
      {
        "ja": "もう一度やり直せるなら",
        "romaji": "mouichidoyarinaoserunara"
      },
      {
        "ja": "この音を君に届けたい",
        "romaji": "konootowokimitodoketai"
      },
      {
        "ja": "明弦音アゲイン響け",
        "romaji": "meigenonageinhibike"
      },
      {
        "ja": "夜明けの空を切り裂いて",
        "romaji": "yoakenosorawokirisaite"
      }
    ]
  },
  {
    "id": "kadagen",
    "title": "過惰幻",
    "reading": "かだげん",
    "category": "original",
    "album": "2nd Album",
    "youtubeId": "",
    "lines": [
      {
        "ja": "怠惰な日々に溺れていく",
        "romaji": "taidanahibinioboreteiku"
      },
      {
        "ja": "幻を見ていたのだろうか",
        "romaji": "maboroshiwomiteitanoarouka"
      },
      {
        "ja": "目を覚ませと叫ぶ声が",
        "romaji": "mewosamasetosakebukoega"
      },
      {
        "ja": "遠くから聞こえてくるよ",
        "romaji": "tookukarakikoetekuruyo"
      },
      {
        "ja": "過惰幻を断ち切って今",
        "romaji": "kadagenwotachikitteima"
      },
      {
        "ja": "現実へと踏み出していく",
        "romaji": "genjitsuetofumidashiteiku"
      }
    ]
  },
  {
    "id": "yaonzen",
    "title": "夜隠染",
    "reading": "やおんぜん",
    "category": "original",
    "album": "6th Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "夜の帳に隠れながら",
        "romaji": "yorunotobarinikakurenagara"
      },
      {
        "ja": "染まっていく漆黒の街",
        "romaji": "somatteikushikkokunomachi"
      },
      {
        "ja": "冷たい風が吹き抜けて",
        "romaji": "tsumetaikazegafukinukete"
      },
      {
        "ja": "心までも凍えそうだよ",
        "romaji": "kokoromademokogoesoudayo"
      },
      {
        "ja": "夜隠染の闇の中で",
        "romaji": "yaonzennoyaminonakade"
      },
      {
        "ja": "確かな温もりを探してる",
        "romaji": "tashikananukumoriwosagashiteru"
      }
    ]
  },
  {
    "id": "mushuutou",
    "title": "霧周途",
    "reading": "むしゅうと",
    "category": "original",
    "album": "6th Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "深い霧に包まれた道",
        "romaji": "fukaikirinitsutsumaretamichi"
      },
      {
        "ja": "前も見えない迷路の中",
        "romaji": "maemomienaimeirononaka"
      },
      {
        "ja": "信じられるのはただ一つ",
        "romaji": "shinjirarerunowatadahitotsu"
      },
      {
        "ja": "握りしめた手のひらの熱",
        "romaji": "nigirishimetatenohiranonetsu"
      },
      {
        "ja": "霧周途ミストを抜けて",
        "romaji": "mushuutomisutowonukete"
      },
      {
        "ja": "青空の下へ駆け出そう",
        "romaji": "aozoranoshitaekakedasou"
      }
    ]
  },
  {
    "id": "egakumirai",
    "title": "エガクミライ",
    "reading": "えがくみらい",
    "category": "original",
    "album": "8th Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "真っ白なキャンバスの上に",
        "romaji": "masshironakyanbasunoueni"
      },
      {
        "ja": "僕らの未来を描いていこう",
        "romaji": "bokuranomiraiwoegaiteikou"
      },
      {
        "ja": "どんな色でも構わないよ",
        "romaji": "donnairodanmokamawanaiyo"
      },
      {
        "ja": "自分だけの景色を作ろう",
        "romaji": "jibundakenokeshikiwotsukurou"
      },
      {
        "ja": "エガクミライどこまでも",
        "romaji": "egakumiraidokomademo"
      },
      {
        "ja": "輝きに満ち溢れている",
        "romaji": "kagayakinimichiafureteiru"
      }
    ]
  },
  {
    "id": "shoumeisanka",
    "title": "証命讃歌",
    "reading": "しょうめいさんか",
    "category": "original",
    "album": "9th Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "僕らはここで生きていると",
        "romaji": "bokurawakokodeikiteirutou"
      },
      {
        "ja": "命の証を歌うんだ",
        "romaji": "inochinoakashiwoutaunda"
      },
      {
        "ja": "どんな悲しみも越えていけ",
        "romaji": "donnakanashimimokoeteike"
      },
      {
        "ja": "讃歌を空へと轟かせろ",
        "romaji": "sankawozoraetotodorokasero"
      },
      {
        "ja": "証命讃歌響き渡れ",
        "romaji": "shoumeisankahibikiwatare"
      },
      {
        "ja": "消えない光を灯すように",
        "romaji": "kienaihikarizotomosuyouni"
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
        "romaji": "ikigakurushiinarahakidasebaii"
      },
      {
        "ja": "言葉を詰まらせて泣くくらいなら",
        "romaji": "kotobawotsumarasetenakukurainara"
      },
      {
        "ja": "ノンブレス息を止めたまま",
        "romaji": "nonburesuikiwotometamama"
      },
      {
        "ja": "この世界を駆け抜けていく",
        "romaji": "konosekaiwokakenuketeiku"
      },
      {
        "ja": "義務なんて投げ捨ててしまえ",
        "romaji": "gimunantenagesteteshimae"
      },
      {
        "ja": "僕らは僕らのために歌う",
        "romaji": "bokurawabokuranotameniutau"
      }
    ]
  },
  {
    "id": "kiminokamisama",
    "title": "君の神様になりたい。",
    "reading": "きみのかみさまになりたい",
    "category": "cover",
    "album": "Cover Collection Vol.10",
    "youtubeId": "zF0yZp_w0_U",
    "lines": [
      {
        "ja": "僕の命で君を救えるなら",
        "romaji": "bokunoinochidekimiwosukuerunara"
      },
      {
        "ja": "喜んでこの命を差し出そう",
        "romaji": "yorokondekonoinochiwosashidasou"
      },
      {
        "ja": "君の神様になりたかった",
        "romaji": "kiminokamisamaninaritakatta"
      },
      {
        "ja": "君の悲しみを全部背負って",
        "romaji": "kiminokanashimiwozenbuseotte"
      },
      {
        "ja": "僕が代わりに泣いてあげるよ",
        "romaji": "bokugakawarininaiteageruyo"
      },
      {
        "ja": "どうか笑顔で生きていてほしい",
        "romaji": "doukaegaodeikiteitehoshii"
      }
    ]
  },
  {
    "id": "charles",
    "title": "シャルル",
    "reading": "しゃるる",
    "category": "cover",
    "album": "Cover Single",
    "youtubeId": "9Z12_w6e5hQ",
    "lines": [
      {
        "ja": "さよならはあなたから言った",
        "romaji": "sayonarahaanatakaraitta"
      },
      {
        "ja": "それなのに頬を濡らしてしまうの",
        "romaji": "sorenanonihohowonurashiteshimawuno"
      },
      {
        "ja": "そうやって昨日の事も消してしまうなら",
        "romaji": "souyattekinounokotomokeshiteshimawnara"
      },
      {
        "ja": "もういいよ 笑ってくれよ",
        "romaji": "mouiiyo warattekureyo"
      },
      {
        "ja": "愛を謳って謳って雲の上",
        "romaji": "aiwooutatteoutattekumonoue"
      },
      {
        "ja": "濁りきっては見えないや",
        "romaji": "nigorikittewamienaiya"
      }
    ]
  },
  {
    "id": "moudoku",
    "title": "猛独が襲う",
    "reading": "もうどくがおそう",
    "category": "cover",
    "album": "Cover Collection",
    "youtubeId": "",
    "lines": [
      {
        "ja": "猛独が僕を蝕んでいく",
        "romaji": "moudokugabokuwomushibandeiku"
      },
      {
        "ja": "孤独という名の毒の中で",
        "romaji": "kodokutoyounanodokunonakade"
      },
      {
        "ja": "誰か助けてと叫んでも",
        "romaji": "darekatasuketetosakebdemo"
      },
      {
        "ja": "誰も振り返らない街角で",
        "romaji": "daremofurikaeranaimachikadode"
      },
      {
        "ja": "それでも心は死んでいない",
        "romaji": "soredemokokorowashindeinai"
      },
      {
        "ja": "まだ歌い続けたいんだよ",
        "romaji": "madautaitudukeytaindayo"
      }
    ]
  },
  {
    "id": "swim",
    "title": "swim",
    "reading": "すいむ",
    "category": "cover",
    "album": "Cover Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "泳いでいく冷たい波を掻き分けて",
        "romaji": "oyoideikutsumetainamiwokakiwakete"
      },
      {
        "ja": "息継ぎさえも忘れるくらいに",
        "romaji": "ikitsugisaemowasurerukuraini"
      },
      {
        "ja": "向こう岸にあるはずの光へ",
        "romaji": "mukougishinianruhazunohikarie"
      },
      {
        "ja": "止まることなく進み続けろ",
        "romaji": "tomarukotonakususumitsudukero"
      },
      {
        "ja": "僕らのスウィムは終わらない",
        "romaji": "bokuranosuwimuwawaowaranai"
      }
    ]
  },
  {
    "id": "seishuncomplex",
    "title": "青春コンプレックス",
    "reading": "せいしゅんこんぷれっくす",
    "category": "cover",
    "album": "Cover Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "暗がりから覗く眩しい世界",
        "romaji": "kuragarikaranozokumabushiisekai"
      },
      {
        "ja": "僕には関係ないと思ってた",
        "romaji": "bokunihakankeinaitoomotteta"
      },
      {
        "ja": "かき鳴らせギター歪んだ音で",
        "romaji": "kakinarasegitaahizundaoode"
      },
      {
        "ja": "青春コンプレックスを吹き飛ばせ",
        "romaji": "seishunkonpurekkusuwofukitobase"
      },
      {
        "ja": "これが僕らのロックンロールだ",
        "romaji": "koregabokuranorokkunrooruda"
      }
    ]
  },
  {
    "id": "whitenoise",
    "title": "ホワイトノイズ",
    "reading": "ほわいとのいず",
    "category": "cover",
    "album": "Cover Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "街を覆い尽くすホワイトノイズ",
        "romaji": "machiwoooitsukusuhowaitonoizu"
      },
      {
        "ja": "掻き消された声を探しに行く",
        "romaji": "kakikesaretakoewosagashiniiku"
      },
      {
        "ja": "どんな逆風が吹き荒れても",
        "romaji": "donnagyakufuugafukiaretemo"
      },
      {
        "ja": "倒れてたまるか立ち向かえ",
        "romaji": "taoretemarukatachimukae"
      },
      {
        "ja": "未来をこの手で掴み取るまで",
        "romaji": "miraiwokonotedetsukamitorumade"
      }
    ]
  },
  {
    "id": "soraniutaeba",
    "title": "空に歌えば",
    "reading": "そらにうたえば",
    "category": "cover",
    "album": "Cover Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "空に歌えば届く気がした",
        "romaji": "soraniutaebatodokukigashita"
      },
      {
        "ja": "あの日の悔しさも涙も全部",
        "romaji": "anohinokuyashisamoynamidamozembu"
      },
      {
        "ja": "虚しさを力に変えて走れ",
        "romaji": "munashisawochikaranikaetehashire"
      },
      {
        "ja": "負けっぱなしで終わるわけない",
        "romaji": "makeppanashideowaruwakenai"
      },
      {
        "ja": "僕らの歌よ天まで響け",
        "romaji": "bokuranoutayotenmadehibike"
      }
    ]
  },
  {
    "id": "zattou",
    "title": "雑踏、僕らの街",
    "reading": "ざっとう、ぼくらのまち",
    "category": "cover",
    "album": "Cover Single",
    "youtubeId": "",
    "lines": [
      {
        "ja": "雑踏の中行き交う人波",
        "romaji": "zattounonakaikikauhitonami"
      },
      {
        "ja": "誰も僕のことなんて気にしてない",
        "romaji": "daremobokunokotonantekinishitenai"
      },
      {
        "ja": "だけどこの街で生きているんだ",
        "romaji": "dakedokonomachideikiteirunda"
      },
      {
        "ja": "僕らの声はまだ消えてない",
        "romaji": "bokuranokoewamadakietenai"
      },
      {
        "ja": "雑踏の真ん中で歌い鳴らせ",
        "romaji": "zattounomannakadeutainarase"
      }
    ]
  }
];
