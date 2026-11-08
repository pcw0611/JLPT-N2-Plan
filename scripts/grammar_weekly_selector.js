const BASE_PATTERNS = ALL_PATTERNS.map(item => ({...item}));
const setParams = new URLSearchParams(location.search);
const requestedSetDate = setParams.get('date'); // Preserve the older Monday link.
const kstSetDate = new Intl.DateTimeFormat('sv-SE', {timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
function validSetDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) return false;
  const parsed = new Date(value + 'T12:00:00Z');
  return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0,10) === value;
}
const sentenceSetDate = kstSetDate; // Practice is recorded on the actual KST date.
const templateDate = validSetDate(requestedSetDate) ? requestedSetDate : kstSetDate;
const automaticBank = WEEKLY_SENTENCES.banks.find(b => b.weekday === new Date(kstSetDate+'T12:00:00Z').getUTCDay());
const legacyBank = WEEKLY_SENTENCES.banks.find(b => b.weekday === new Date(templateDate+'T12:00:00Z').getUTCDay());
const validSetKeys = new Set(['auto','baseline',...WEEKLY_SENTENCES.banks.map(b=>b.key)]);
let selectedSetKey = validSetKeys.has(setParams.get('set')) ? setParams.get('set') :
  (!setParams.has('set') && validSetDate(requestedSetDate) ? legacyBank.key : 'auto');
let sentenceSetId = 'baseline';
let sentenceSetLabel = '基本例文200';
function selectSentenceSet(key) {
  selectedSetKey = validSetKeys.has(key) ? key : 'auto';
  const bank = selectedSetKey === 'auto' ? automaticBank : WEEKLY_SENTENCES.banks.find(b=>b.key===selectedSetKey);
  sentenceSetId = bank ? bank.id : 'baseline';
  sentenceSetLabel = bank ? bank.label : '基本例文200';
  const overrides = new Map((bank?.items || []).map(item=>[item.id,item]));
  ALL_PATTERNS.splice(0, ALL_PATTERNS.length, ...BASE_PATTERNS.map(base=>({...base,...overrides.get(base.id)})));
  const label = document.getElementById('sentenceSetLabel');
  if (label) label.textContent = sentenceSetDate+' · '+sentenceSetLabel+(selectedSetKey==='auto' ? ' · 自動' : ' · 復習');
}
selectSentenceSet(selectedSetKey);
document.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('sentenceSetSelect');
  if (!select) return;
  select.value = selectedSetKey;
  select.onchange = () => {
    selectSentenceSet(select.value);
    const url = new URL(location.href);
    url.searchParams.set('set',selectedSetKey);
    url.searchParams.delete('date');
    history.replaceState(null,'',url);
  };
});
