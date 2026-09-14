import fs from "node:fs/promises";
import { Workbook } from "@oai/artifact-tool";

const outputDir = "C:/Users/pcw06/.codex/.chatgpt-projects/g-p-6a8d95cbc5688191afbbf91726e79bbb/outputs/01a03950-660f-7031-874b-4f1c8485d2da";
const csvPath = `${outputDir}/jlpt-n3-listening-words-2026-08-27.csv`;
const previewPath = `${outputDir}/jlpt-n3-listening-words-preview.png`;

const cards = [
  ["会議", "<b>かいぎ</b><br>회의<br><br>十二時は会議があります。<br>12시에는 회의가 있습니다."],
  ["資料", "<b>しりょう</b><br>자료<br><br>会議の資料を準備します。<br>회의 자료를 준비합니다."],
  ["内容", "<b>ないよう</b><br>내용<br><br>資料の内容はできました。<br>자료의 내용은 완성됐습니다."],
  ["印刷する", "<b>いんさつする</b><br>인쇄하다<br><br>資料を十部印刷してください。<br>자료를 10부 인쇄해 주세요."],
  ["会議室", "<b>かいぎしつ</b><br>회의실<br><br>会議室へ行きます。<br>회의실로 갑니다."],
  ["十部", "<b>じゅうぶ</b><br>10부<br><br>「部」は 책자·자료의 부수를 세는 단위입니다.<br>資料を十部印刷します。"],
  ["まだ～ていません", "<b>まだ～ていません</b><br>아직 ~하지 않았습니다<br><br>まだ印刷していません。<br>아직 인쇄하지 않았습니다."],
  ["～前に", "<b>～まえに</b><br>~하기 전에<br><br>会議室へ行く前に印刷します。<br>회의실에 가기 전에 인쇄합니다."],
  ["すぐにします", "<b>すぐにします</b><br>바로 하겠습니다<br><br>はい、すぐにします。<br>네, 바로 하겠습니다."],
  ["明日の昼", "<b>あしたのひる</b><br>내일 점심때<br><br>明日の昼、一緒に行きませんか。<br>내일 점심에 함께 가지 않을래요?"],
  ["一緒に", "<b>いっしょに</b><br>함께<br><br>一緒に新しい店へ行きましょう。<br>함께 새로운 가게에 갑시다."],
  ["新しい店", "<b>あたらしいみせ</b><br>새로운 가게<br><br>新しい店へ行きませんか。<br>새로운 가게에 가지 않을래요?"],
  ["～ませんか", "<b>～ませんか</b><br>~하지 않겠습니까? / ~하지 않을래요?<br><br>一緒に行きませんか。<br>함께 가지 않을래요?"],
  ["～があります", "<b>～があります</b><br>~이 있습니다<br><br>十二時は会議があります。<br>12시에는 회의가 있습니다."],
  ["終わる", "<b>おわる</b><br>끝나다<br><br>会議は一時に終わります。<br>회의는 1시에 끝납니다."],
  ["～てから", "<b>～てから</b><br>~한 후에<br><br>会議が終わってから行きましょう。<br>회의가 끝난 후에 갑시다."],
  ["一時ごろ", "<b>いちじごろ</b><br>1시쯤<br><br>一時ごろ店へ行きます。<br>1시쯤 가게에 갑니다."],
  ["そうしましょう", "<b>そうしましょう</b><br>그렇게 합시다<br><br>一時ごろですね。そうしましょう。<br>1시쯤이군요. 그렇게 합시다."],
  ["でも", "<b>でも</b><br>하지만<br><br>いいですね。でも、十二時は会議があります。<br>좋네요. 하지만 12시에는 회의가 있습니다."],
  ["じゃあ", "<b>じゃあ</b><br>그러면 / 그럼<br><br>じゃあ、会議が終わってから行きましょう。<br>그럼 회의가 끝난 후에 갑시다."]
];

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Anki");
sheet.getRange(`A1:B${cards.length + 1}`).values = [["Front", "Back"], ...cards];
sheet.getRange("A1:B1").format = {
  fill: "#25476A",
  font: { bold: true, color: "#FFFFFF" }
};
sheet.getRange(`A1:B${cards.length + 1}`).format.wrapText = true;
sheet.getRange("A:A").format.columnWidth = 24;
sheet.getRange("B:B").format.columnWidth = 72;
sheet.freezePanes.freezeRows(1);
sheet.showGridLines = false;

const inspect = await workbook.inspect({
  kind: "table",
  range: `Anki!A1:B${cards.length + 1}`,
  include: "values",
  tableMaxRows: 25,
  tableMaxCols: 2,
  maxChars: 6000
});
console.log(inspect.ndjson);

const preview = await workbook.render({
  sheetName: "Anki",
  range: "A1:B8",
  scale: 1,
  format: "png"
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const csvEscape = value => `"${String(value).replaceAll('"', '""')}"`;
const rows = cards.map(row => row.map(csvEscape).join(","));
const csv = `#separator:Comma\r\n#html:true\r\n${rows.join("\r\n")}\r\n`;
await fs.writeFile(csvPath, `\uFEFF${csv}`, "utf8");

console.log(JSON.stringify({ csvPath, previewPath, cards: cards.length }));
