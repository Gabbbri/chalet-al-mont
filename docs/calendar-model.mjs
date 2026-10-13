export function dateKey(year, month, day) {
  return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
}
export function monthCells(year, month) {
  const offset = (new Date(Date.UTC(year, month, 1)).getUTCDay() + 6) % 7;
  const count = new Date(Date.UTC(year, month + 1, 0)).getUTCDate();
  return [...Array(offset).fill(null), ...Array.from({length: count}, (_, i) => dateKey(year, month, i + 1))];
}
export function chooseRange(start, end, picked) {
  return !start || end || picked <= start ? [picked, ''] : [start, picked];
}
export function nights(start, end) {
  return start && end && end > start ? Math.round((Date.parse(end) - Date.parse(start)) / 86400000) : 0;
}
