// Keep sub-minute online sessions until display; never round each session away.
export const addStudySeconds=(minutes,seconds)=>Number(minutes||0)+Number(seconds||0)/60;
export function formatStudyTime(minutes){
  const seconds=Math.max(0,Math.round(Number(minutes||0)*60));
  return `${Math.floor(seconds/3600)}時間${Math.floor(seconds/60)%60}分${seconds%60?`${seconds%60}秒`:''}`;
}
