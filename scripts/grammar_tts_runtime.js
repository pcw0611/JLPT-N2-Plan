// Browser speech synthesis for post-answer review only. No paid API or audio files.
const grammarTts = {
  autoEnabled: true, serial: 0, item: null, pending: null, utterance: null,
  voiceTimer: null, startTimer: null,
  supported() {
    return !!window.speechSynthesis && typeof window.SpeechSynthesisUtterance === 'function';
  },
  status(message) {
    document.querySelectorAll('[data-tts-status]').forEach(el => { el.textContent = message; });
  },
  init() {
    try { this.autoEnabled = localStorage.getItem('n2_speedrun_tts_auto') !== 'false'; } catch (_) {}
    const controls = `<div class="flex flex-wrap items-center gap-2 pt-2">
      <button type="button" data-tts-play class="rounded-lg border border-cyan-600/60 bg-cyan-950/50 px-3 py-2 text-xs font-bold text-cyan-200">🔊 다시 듣기</button>
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
    window.addEventListener('pagehide', () => this.stop());
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
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    if (message) this.status(message);
    return this.serial;
  },
  afterAnswer(item) {
    this.stop(); this.item = item;
    if (this.autoEnabled) this.play(0.95);
    else this.status('자동 읽기 OFF · 다시 듣기 또는 천천히를 눌러주세요.');
  },
  play(rate = 0.95, sample = false) {
    if (!this.canPlay(sample)) return;
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
    } else if (!this.utterance) this.status('일본어 음성: '+voice.name+' · 브라우저 합성 음성');
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
