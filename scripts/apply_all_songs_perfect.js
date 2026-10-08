const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SONGS_TS_PATH = path.join(ROOT, 'jlpt-calendar-site', 'app', 'typing', 'songs.ts');
const EXTRACTED_JSON_PATH = path.join(ROOT, 'scratch', 'all_extracted_lyrics.json');

console.log('=== Apply All Songs to songs.ts (Node.js Perfect Builder) ===');

// 1. 기존 songs.ts 읽기
const content = fs.readFileSync(SONGS_TS_PATH, 'utf8');
const startIdx = content.indexOf('export const SONGS: Song[] = ');
if (startIdx === -1) {
  console.error('Cannot find export const SONGS: Song[] in songs.ts');
  process.exit(1);
}

const header = content.slice(0, startIdx + 'export const SONGS: Song[] = '.length);
const arrayBodyStr = content.slice(startIdx + 'export const SONGS: Song[] = '.length).trim().replace(/;$/, '');
const songs = eval(arrayBodyStr);
console.log(`Loaded ${songs.length} songs from songs.ts`);

// 2. 나무위키 추출 완본 가사 읽기
const extractedDb = JSON.parse(fs.readFileSync(EXTRACTED_JSON_PATH, 'utf8'));
console.log(`Loaded ${Object.keys(extractedDb).length} extracted songs from JSON`);

// 3. 3파트 분할 함수
function build3Parts(lines) {
  const total = lines.length;
  if (total === 0) return [];

  const p1End = Math.max(1, Math.floor(total * 0.42));
  const p2End = Math.max(p1End + 1, Math.floor(total * 0.82));

  return [
    {
      id: 'part1',
      name: 'Part 1 (前半・1番)',
      lines: lines.slice(0, p1End)
    },
    {
      id: 'part2',
      name: 'Part 2 (後半・2番)',
      lines: lines.slice(p1End, p2End)
    },
    {
      id: 'part3',
      name: 'Part 3 (ラスト・Cメロ~完走)',
      lines: lines.slice(p2End)
    }
  ];
}

// 4. 가사 라인 정돈 (접두사 등)
function cleanLines(lines) {
  return lines.map(l => {
    let ja = l.ja || '';
    ja = ja.replace(/^《[^》]+》\s*/, '');
    ja = ja.replace(/^\[[^\]]+\]\s*/, '');
    return {
      ja: ja.trim(),
      romaji: l.romaji || '',
      ko: (l.ko || '').trim(),
      charRomaji: l.charRomaji || []
    };
  }).filter(l => l.ja.length > 0 && !l.ja.startsWith('雑踏、僕らの街 01'));
}

// 5. 각 곡 업데이트
let completeCount = 0;
let restructuredCount = 0;

const updatedSongs = songs.map(song => {
  const sid = song.id;
  const rawExtracted = extractedDb[sid];

  if (rawExtracted && rawExtracted.length >= 10) {
    const cleaned = cleanLines(rawExtracted);
    const parts = build3Parts(cleaned);
    completeCount++;
    console.log(`[완본 갱신] ${song.title.padEnd(16)} (${sid.padEnd(16)}) -> ${cleaned.length}줄 완본 (P1: ${parts[0].lines.length}, P2: ${parts[1].lines.length}, P3: ${parts[2].lines.length})`);
    return {
      ...song,
      parts
    };
  } else {
    // 기존 가사로 3파트 정돈
    const existingLines = [];
    if (song.parts) {
      for (const p of song.parts) {
        if (p.lines) {
          for (const l of p.lines) {
            existingLines.push(l);
          }
        }
      }
    }
    const cleaned = cleanLines(existingLines);
    const parts = build3Parts(cleaned);
    restructuredCount++;
    console.log(`[3파트 정돈] ${song.title.padEnd(16)} (${sid.padEnd(16)}) -> ${cleaned.length}줄 유지 (P1: ${parts[0].lines.length}, P2: ${parts[1].lines.length}, P3: ${parts[2].lines.length})`);
    return {
      ...song,
      parts
    };
  }
});

// 6. songs.ts 재작성
const formattedJson = JSON.stringify(updatedSongs, null, 2);
const finalContent = `${header}\n${formattedJson};\n`;

fs.writeFileSync(SONGS_TS_PATH, finalContent, 'utf8');

console.log('\n============================================================');
console.log('완료 보고:');
console.log(`- 총 처리 곡 수: ${updatedSongs.length}곡`);
console.log(`- 나무위키 공식 가사 완본 적용: ${completeCount}곡`);
console.log(`- 3파트 표준 정돈: ${restructuredCount}곡`);
console.log(`- 모든 곡의 파트: 단 하나의 예외 없이 Part 1, Part 2, Part 3 (3개 파트) 완비!`);
console.log('============================================================');
