export type ActivityKind = 'anki' | 'review' | 'exam' | 'typing' | 'speed' | 'quiz' | 'activity';
export function activityKind(item: {source?: string; notes?: string}): ActivityKind;
export const activityLabels: Record<ActivityKind, string>;
export const activityIcons: Record<ActivityKind, string>;
