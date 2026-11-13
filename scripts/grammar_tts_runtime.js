// Play prepared recordings during post-answer review, with browser speech as a fallback.
const grammarTts = {
  autoEnabled: true, serial: 0, item: null, pending: null, utterance: null,
  voiceTimer: null, startTimer: null, audio: null,
  sundayRecordings: {
    "n2-grammar-001": "001-elio.mp3",
    "n2-grammar-002": "002-elio.mp3",
    "n2-grammar-003": "003-elio.mp3",
    "n2-grammar-004": "004-elio.mp3",
    "n2-grammar-005": "005-elio.mp3",
    "n2-grammar-006": "006-elio.mp3",
    "n2-grammar-007": "007-elio.mp3",
    "n2-grammar-008": "008-elio.mp3",
    "n2-grammar-009": "009-elio.mp3",
    "n2-grammar-010": "010-elio.mp3",
    "n2-grammar-011": "011-fola.mp3",
    "n2-grammar-012": "012-fola.mp3",
    "n2-grammar-013": "013-fola.mp3",
    "n2-grammar-014": "014-fola.mp3",
    "n2-grammar-015": "015-fola.mp3",
    "n2-grammar-016": "016-fola.mp3",
    "n2-grammar-017": "017-fola.mp3",
    "n2-grammar-018": "018-fola.mp3",
    "n2-grammar-019": "019-fola.mp3",
    "n2-grammar-020": "020-fola.mp3",
    "n2-grammar-021": "021-fola.mp3",
    "n2-grammar-022": "022-fola.mp3",
    "n2-grammar-023": "023-fola.mp3",
    "n2-grammar-024": "024-fola.mp3",
    "n2-grammar-025": "025-fola.mp3",
    "n2-grammar-026": "026-fola.mp3",
    "n2-grammar-027": "027-fola.mp3",
    "n2-grammar-028": "028-fola.mp3",
    "n2-grammar-029": "029-fola.mp3",
    "n2-grammar-030": "030-fola.mp3",
    "n2-grammar-031": "031-enzo.mp3",
    "n2-grammar-032": "032-enzo.mp3",
    "n2-grammar-033": "033-enzo.mp3",
    "n2-grammar-034": "034-enzo.mp3",
    "n2-grammar-035": "035-enzo.mp3",
    "n2-grammar-036": "036-enzo.mp3",
    "n2-grammar-037": "037-enzo.mp3",
    "n2-grammar-038": "038-enzo.mp3",
    "n2-grammar-039": "039-enzo.mp3",
    "n2-grammar-040": "040-enzo.mp3",
    "n2-grammar-041": "041-enzo.mp3",
    "n2-grammar-042": "042-enzo.mp3",
    "n2-grammar-043": "043-enzo.mp3",
    "n2-grammar-044": "044-enzo.mp3",
    "n2-grammar-045": "045-enzo.mp3",
    "n2-grammar-046": "046-enzo.mp3",
    "n2-grammar-047": "047-enzo.mp3",
    "n2-grammar-048": "048-enzo.mp3",
    "n2-grammar-049": "049-enzo.mp3",
    "n2-grammar-050": "050-enzo.mp3",
    "n2-grammar-051": "051-rina.mp3",
    "n2-grammar-052": "052-rina.mp3",
    "n2-grammar-053": "053-rina.mp3",
    "n2-grammar-054": "054-rina.mp3",
    "n2-grammar-055": "055-rina.mp3",
    "n2-grammar-056": "056-rina.mp3",
    "n2-grammar-057": "057-rina.mp3",
    "n2-grammar-058": "058-rina.mp3",
    "n2-grammar-059": "059-rina.mp3",
    "n2-grammar-060": "060-rina.mp3",
    "n2-grammar-061": "061-rina.mp3",
    "n2-grammar-062": "062-rina.mp3",
    "n2-grammar-063": "063-rina.mp3",
    "n2-grammar-064": "064-rina.mp3",
    "n2-grammar-065": "065-rina.mp3",
    "n2-grammar-066": "066-rina.mp3",
    "n2-grammar-067": "067-rina.mp3",
    "n2-grammar-068": "068-rina.mp3",
    "n2-grammar-069": "069-rina.mp3",
    "n2-grammar-070": "070-rina.mp3",
    "n2-grammar-071": "071-puck.mp3",
    "n2-grammar-072": "072-puck.mp3",
    "n2-grammar-073": "073-puck.mp3",
    "n2-grammar-074": "074-puck.mp3",
    "n2-grammar-075": "075-puck.mp3",
    "n2-grammar-076": "076-puck.mp3",
    "n2-grammar-077": "077-puck.mp3",
    "n2-grammar-078": "078-puck.mp3",
    "n2-grammar-079": "079-puck.mp3",
    "n2-grammar-080": "080-puck.mp3",
    "n2-grammar-081": "081-puck.mp3",
    "n2-grammar-082": "082-puck.mp3",
    "n2-grammar-083": "083-puck.mp3",
    "n2-grammar-084": "084-puck.mp3",
    "n2-grammar-085": "085-puck.mp3",
    "n2-grammar-086": "086-puck.mp3",
    "n2-grammar-087": "087-puck.mp3",
    "n2-grammar-088": "088-puck.mp3",
    "n2-grammar-089": "089-puck.mp3",
    "n2-grammar-090": "090-puck.mp3",
    "n2-grammar-091": "091-zephyr.mp3",
    "n2-grammar-092": "092-zephyr.mp3",
    "n2-grammar-093": "093-zephyr.mp3",
    "n2-grammar-094": "094-zephyr.mp3",
    "n2-grammar-095": "095-zephyr.mp3",
    "n2-grammar-096": "096-zephyr.mp3",
    "n2-grammar-097": "097-zephyr.mp3",
    "n2-grammar-098": "098-zephyr.mp3",
    "n2-grammar-099": "099-zephyr.mp3",
    "n2-grammar-100": "100-zephyr.mp3",
    "n2-grammar-101": "101-zephyr.mp3",
    "n2-grammar-102": "102-zephyr.mp3",
    "n2-grammar-103": "103-zephyr.mp3",
    "n2-grammar-104": "104-zephyr.mp3",
    "n2-grammar-105": "105-zephyr.mp3",
    "n2-grammar-106": "106-zephyr.mp3",
    "n2-grammar-107": "107-zephyr.mp3",
    "n2-grammar-108": "108-zephyr.mp3",
    "n2-grammar-109": "109-zephyr.mp3",
    "n2-grammar-110": "110-zephyr.mp3",
    "n2-grammar-111": "111-elio.mp3",
    "n2-grammar-112": "112-elio.mp3",
    "n2-grammar-113": "113-elio.mp3",
    "n2-grammar-114": "114-elio.mp3",
    "n2-grammar-115": "115-elio.mp3",
    "n2-grammar-116": "116-elio.mp3",
    "n2-grammar-117": "117-elio.mp3",
    "n2-grammar-118": "118-elio.mp3",
    "n2-grammar-119": "119-elio.mp3",
    "n2-grammar-120": "120-elio.mp3",
    "n2-grammar-121": "121-elio.mp3",
    "n2-grammar-122": "122-elio.mp3",
    "n2-grammar-123": "123-elio.mp3",
    "n2-grammar-124": "124-elio.mp3",
    "n2-grammar-125": "125-elio.mp3",
    "n2-grammar-126": "126-elio.mp3",
    "n2-grammar-127": "127-elio.mp3",
    "n2-grammar-128": "128-elio.mp3",
    "n2-grammar-129": "129-elio.mp3",
    "n2-grammar-130": "130-elio.mp3",
    "n2-grammar-131": "131-hali.mp3",
    "n2-grammar-132": "132-hali.mp3",
    "n2-grammar-133": "133-hali.mp3",
    "n2-grammar-134": "134-hali.mp3",
    "n2-grammar-135": "135-hali.mp3",
    "n2-grammar-136": "136-hali.mp3",
    "n2-grammar-137": "137-hali.mp3",
    "n2-grammar-138": "138-hali.mp3",
    "n2-grammar-139": "139-hali.mp3",
    "n2-grammar-140": "140-hali.mp3",
    "n2-grammar-141": "141-hali.mp3",
    "n2-grammar-142": "142-hali.mp3",
    "n2-grammar-143": "143-hali.mp3",
    "n2-grammar-144": "144-hali.mp3",
    "n2-grammar-145": "145-hali.mp3",
    "n2-grammar-146": "146-hali.mp3",
    "n2-grammar-147": "147-hali.mp3",
    "n2-grammar-148": "148-hali.mp3",
    "n2-grammar-149": "149-hali.mp3",
    "n2-grammar-150": "150-hali.mp3",
    "n2-grammar-151": "151-enzo.mp3",
    "n2-grammar-152": "152-enzo.mp3",
    "n2-grammar-153": "153-enzo.mp3",
    "n2-grammar-154": "154-enzo.mp3",
    "n2-grammar-155": "155-enzo.mp3",
    "n2-grammar-156": "156-enzo.mp3",
    "n2-grammar-157": "157-enzo.mp3",
    "n2-grammar-158": "158-enzo.mp3",
    "n2-grammar-159": "159-enzo.mp3",
    "n2-grammar-160": "160-enzo.mp3",
    "n2-grammar-161": "161-enzo.mp3",
    "n2-grammar-162": "162-enzo.mp3",
    "n2-grammar-163": "163-enzo.mp3",
    "n2-grammar-164": "164-enzo.mp3",
    "n2-grammar-165": "165-enzo.mp3",
    "n2-grammar-166": "166-enzo.mp3",
    "n2-grammar-167": "167-enzo.mp3",
    "n2-grammar-168": "168-enzo.mp3",
    "n2-grammar-169": "169-enzo.mp3",
    "n2-grammar-170": "170-enzo.mp3",
    "n2-grammar-171": "171-charon.mp3",
    "n2-grammar-172": "172-charon.mp3",
    "n2-grammar-173": "173-charon.mp3",
    "n2-grammar-174": "174-charon.mp3",
    "n2-grammar-175": "175-charon.mp3",
    "n2-grammar-176": "176-charon.mp3",
    "n2-grammar-177": "177-charon.mp3",
    "n2-grammar-178": "178-charon.mp3",
    "n2-grammar-179": "179-charon.mp3",
    "n2-grammar-180": "180-charon.mp3",
    "n2-grammar-181": "181-charon.mp3",
    "n2-grammar-182": "182-charon.mp3",
    "n2-grammar-183": "183-charon.mp3",
    "n2-grammar-184": "184-charon.mp3",
    "n2-grammar-185": "185-charon.mp3",
    "n2-grammar-186": "186-charon.mp3",
    "n2-grammar-187": "187-charon.mp3",
    "n2-grammar-188": "188-charon.mp3",
    "n2-grammar-189": "189-charon.mp3",
    "n2-grammar-190": "190-charon.mp3",
    "n2-grammar-191": "191-puck.mp3",
    "n2-grammar-192": "192-puck.mp3",
    "n2-grammar-193": "193-puck.mp3",
    "n2-grammar-194": "194-puck.mp3",
    "n2-grammar-195": "195-puck.mp3",
    "n2-grammar-196": "196-puck.mp3",
    "n2-grammar-197": "197-puck.mp3",
    "n2-grammar-198": "198-puck.mp3",
    "n2-grammar-199": "199-puck.mp3",
    "n2-grammar-200": "200-puck.mp3",
  },
  supported() {
    return !!window.speechSynthesis && typeof window.SpeechSynthesisUtterance === 'function';
  },
  status(message) {
    document.querySelectorAll('[data-tts-status]').forEach(el => { el.textContent = message; });
  },
  init() {
    try { this.autoEnabled = localStorage.getItem('n2_speedrun_tts_auto') !== 'false'; } catch (_) {}
    const controls = `<div class="flex flex-wrap items-center gap-2 pt-2">
      <button type="button" data-tts-play aria-keyshortcuts="R" class="rounded-lg border border-cyan-600/60 bg-cyan-950/50 px-3 py-2 text-xs font-bold text-cyan-200">🔊 다시 듣기 <kbd>R</kbd></button>
      <button type="button" data-tts-slow class="rounded-lg border border-slate-600 bg-slate-800 px-3 py-2 text-xs font-bold text-slate-200">🐢 천천히</button>
      <button type="button" data-tts-stop class="rounded-lg border border-slate-600 px-3 py-2 text-xs text-slate-300">⏹ 중지</button>
      <button type="button" data-tts-auto class="rounded-lg border border-slate-600 px-3 py-2 text-xs text-slate-300"></button>
    </div><p data-tts-status role="status" class="pt-1 text-[11px] leading-relaxed text-slate-400">답을 확인한 뒤 완성 문장을 들어요.</p>`;
    document.querySelectorAll('[data-tts-controls]').forEach(el => { el.innerHTML = controls; });
    document.querySelectorAll('[data-tts-play]').forEach(el => { el.onclick = () => this.play(0.95); });
    document.querySelectorAll('[data-tts-slow]').forEach(el => { el.onclick = () => this.play(0.72); });
    document.querySelectorAll('[data-tts-stop]').forEach(el => { el.onclick = () => this.stop('재생을 멈췄어요. 다시 듣기를 누르면 처음부터 들어요.'); });
    document.querySelectorAll('[data-tts-auto]').forEach(el => {
      el[el.type === 'checkbox' ? 'onchange' : 'onclick'] = () => this.setAuto(el.type === 'checkbox' ? el.checked : !this.autoEnabled);
    });
    const sample = document.getElementById('btnTtsSample');
    if (sample) sample.onclick = () => this.play(0.95, true);
    this.syncAuto();
    if (this.supported()) {
      window.speechSynthesis.addEventListener('voiceschanged', () => this.voicesReady());
      const voice = this.voice();
      if (voice) this.status('일본어 음성: '+voice.name+' · 브라우저 합성 음성');
    } else this.status('이 브라우저에서는 음성 읽기를 지원하지 않아요.');
    this.syncSampleLabel();
    document.getElementById('sentenceSetSelect')?.addEventListener?.('change', () => {
      this.stop();
      this.syncSampleLabel();
    });
    window.addEventListener('keydown', event => {
      if (event.code !== 'KeyR' || event.repeat || event.ctrlKey || event.metaKey || event.altKey ||
          event.isComposing || event.target?.closest?.('input, textarea, select, [contenteditable]') ||
          !this.canPlay(false)) return;
      event.preventDefault();
      this.play();
    });
    window.addEventListener('pagehide', () => this.stop());
  },
  syncSampleLabel() {
    const recorded = sentenceSetId === 'sunday-20261103' && this.sundayRecordings['n2-grammar-001'];
    document.querySelectorAll('[data-tts-provider]').forEach(el => {
      el.textContent = recorded ? 'Geminiの日本語音声' : 'ブラウザーの日本語合成音声';
    });
    if (recorded) this.status('Gemini 음성 · 정답을 확인한 뒤 예문을 읽어요.');
    else {
      const voice = this.voice();
      if (voice) this.status('일본어 음성: '+voice.name+' · 브라우저 합성 음성');
    }
  },
  syncAuto() {
    document.querySelectorAll('[data-tts-auto]').forEach(el => {
      if (el.type === 'checkbox') el.checked = this.autoEnabled;
      else { el.textContent = '자동 읽기 '+(this.autoEnabled ? 'ON' : 'OFF'); el.setAttribute('aria-pressed',String(this.autoEnabled)); }
    });
  },
  setAuto(enabled) {
    this.autoEnabled = !!enabled;
    try { localStorage.setItem('n2_speedrun_tts_auto', String(this.autoEnabled)); } catch (_) {}
    this.syncAuto();
    if (!this.autoEnabled) this.stop('자동 읽기 OFF · 다시 듣기는 사용할 수 있어요.');
    else if (this.canPlay(false)) this.play(0.95);
  },
  voice() {
    if (!this.supported()) return null;
    const voices = window.speechSynthesis.getVoices().filter(v => /^ja(?:[-_]|$)/i.test(v.lang));
    return voices.find(v => /natural|neural|online/i.test(v.name)) || voices.find(v => v.default) || voices.find(v => v.localService) || voices[0] || null;
  },
  reading(item) {
    // Read the authored furigana once, never kanji AND furigana or Korean glosses.
    return (item.sentence_ja_ruby || item.sentence_ja || '')
      .replace(/<ruby>([\s\S]*?)<\/ruby>/gi, (_, inside) => inside.match(/<rt>([\s\S]*?)<\/rt>/i)?.[1] || inside)
      .replace(/<rp>[\s\S]*?<\/rp>/gi,'').replace(/<[^>]+>/g,'')
      .replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#x27;/g,"'");
  },
  canPlay(sample) {
    if (sample) return !document.getElementById('screenLobby').classList.contains('hidden');
    return !state.finished && !state.paused && !state.ending && state.waitingConfirm &&
      !!this.item && this.item === state.questions[state.currentIndex]?.item;
  },
  stop(message) {
    this.serial++;
    this.pending = null;
    clearTimeout(this.voiceTimer); clearTimeout(this.startTimer);
    this.utterance = null;
    if (this.audio) {
      this.audio.pause();
      this.audio = null;
    }
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    if (message) this.status(message);
    return this.serial;
  },
  afterAnswer(item) {
    this.stop(); this.item = item;
    document.querySelectorAll('[data-tts-slow]').forEach(el => {
      el.hidden = state.sessionSet?.id === 'sunday-20261103';
    });
    if (this.autoEnabled) this.play(0.95);
    else this.status('자동 읽기 OFF · 다시 듣기 또는 천천히를 눌러주세요.');
  },
  play(rate = 0.95, sample = false) {
    if (!this.canPlay(sample)) return;
    const bankId = sample ? sentenceSetId : state.sessionSet?.id;
    const recording = bankId === 'sunday-20261103'
      ? this.sundayRecordings[sample ? 'n2-grammar-001' : this.item?.id]
      : null;
    if (recording && typeof Audio === 'function') {
      this.playRecording(recording, sample);
      return;
    }
    this.playBrowser(rate, sample);
  },
  playRecording(recording, sample) {
    const serial = this.stop();
    const clip = new Audio('/exams/audio/n2-grammar/sunday-20261103/' + recording);
    this.audio = clip;
    const current = () => serial === this.serial && this.canPlay(sample);
    const fallback = () => {
      if (!current()) return;
      this.stop();
      this.playBrowser(0.95, sample);
    };
    clip.onplaying = () => {
      if (current()) this.status('예문 듣는 중 · Gemini');
    };
    clip.onended = () => {
      if (!current()) return;
      this.audio = null;
      this.status('재생 완료 · Gemini');
    };
    clip.onerror = fallback;
    clip.play().catch(fallback);
  },
  playBrowser(rate, sample) {
    if (!this.supported()) { this.status('이 브라우저에서는 음성 읽기를 지원하지 않아요.'); return; }
    const request = {serial:this.stop(),item:this.item,rate,sample};
    const voice = this.voice();
    if (voice) { this.speak(request,voice); return; }
    this.pending = request;
    this.status('일본어 음성을 준비하고 있어요…');
    this.voiceTimer = setTimeout(() => {
      if (request.serial !== this.serial || !this.canPlay(sample)) return;
      this.pending = null;
      this.status('일본어 음성을 찾지 못했어요. 기기의 일본어 음성 설정을 확인한 뒤 다시 눌러주세요.');
    },1800);
  },
  voicesReady() {
    const voice = this.voice();
    if (!voice) return;
    const request = this.pending;
    if (request && request.serial === this.serial && this.canPlay(request.sample)) {
      clearTimeout(this.voiceTimer); this.pending = null; this.speak(request,voice);
    } else if (!this.utterance && !this.audio) this.syncSampleLabel();
  },
  speak(request,voice) {
    if (request.serial !== this.serial || !this.canPlay(request.sample)) return;
    const utter = new window.SpeechSynthesisUtterance(request.sample ? 'これは日本語の音声です。' : this.reading(request.item));
    utter.lang = voice.lang; utter.voice = voice; utter.rate = request.rate; utter.pitch = 1;
    this.utterance = utter;
    this.status('재생 준비 중 · '+voice.name);
    utter.onstart = () => {
      if (request.serial !== this.serial) return;
      clearTimeout(this.startTimer);
      this.status((request.rate < 0.9 ? '천천히 듣는 중' : '예문 듣는 중')+' · '+voice.name);
    };
    utter.onend = () => {
      if (request.serial !== this.serial) return;
      clearTimeout(this.startTimer); this.utterance = null;
      this.status('재생 완료 · '+voice.name);
    };
    utter.onerror = event => {
      if (request.serial !== this.serial) return;
      clearTimeout(this.startTimer); this.utterance = null;
      this.status(event.error === 'not-allowed' ? '자동 재생이 차단됐어요. 다시 듣기를 눌러주세요.' : '음성을 재생하지 못했어요. 다시 듣기를 눌러주세요.');
    };
    this.startTimer = setTimeout(() => {
      if (request.serial === this.serial && this.utterance === utter) this.stop('음성이 시작되지 않았어요. 다시 듣기를 눌러주세요.');
    },5000);
    try { window.speechSynthesis.speak(utter); }
    catch (_) { this.stop('음성을 재생하지 못했어요. 다시 듣기를 눌러주세요.'); }
  }
};
