import {dateKey, monthCells, chooseRange, nights} from './calendar-model.mjs';
import {locale, words, requestText} from './locale.js';
const parts = new Intl.DateTimeFormat('en', {timeZone:'Europe/Rome', year:'numeric', month:'2-digit', day:'2-digit'}).formatToParts(new Date());
const part = type => parts.find(p => p.type === type).value;
const today = `${part('year')}-${part('month')}-${part('day')}`;
let year = Number(part('year')), month = Number(part('month')) - 1;
const firstMonth = year * 12 + month;
const arrival = document.querySelector('#arrival'), departure = document.querySelector('#departure');
const grid = document.querySelector('#calendar-days'), heading = document.querySelector('#calendar-month');
const previous = document.querySelector('#month-prev'), next = document.querySelector('#month-next');
const send = document.querySelector('#booking-send'), summary = document.querySelector('#date-summary');
const guests = document.querySelector('#guest-count');
arrival.min = today; departure.min = today;
const format = key => new Intl.DateTimeFormat(locale, {day:'numeric', month:'long', year:'numeric', timeZone:'UTC'}).format(new Date(`${key}T12:00:00Z`));
function render() {
  heading.textContent = new Intl.DateTimeFormat(locale, {month:'long', year:'numeric', timeZone:'UTC'}).format(new Date(Date.UTC(year, month, 1)));
  previous.disabled = year * 12 + month <= firstMonth;
  grid.replaceChildren();
  monthCells(year, month).forEach(key => {
    if (!key) { grid.append(document.createElement('span')); return; }
    const button = document.createElement('button'); button.type = 'button';
    button.textContent = Number(key.slice(-2)); button.disabled = key < today;
    button.setAttribute('aria-label', format(key));
    const selected = key === arrival.value || key === departure.value;
    button.setAttribute('aria-pressed', String(selected));
    if (selected) button.classList.add('selected');
    else if (arrival.value && departure.value && key > arrival.value && key < departure.value) button.classList.add('in-range');
    button.onclick = () => {
      [arrival.value, departure.value] = chooseRange(arrival.value, departure.value, key);
      update();
      [...grid.querySelectorAll('button')].find(b => b.getAttribute('aria-label') === format(key))?.focus();
    };
    grid.append(button);
  });
}
function update() {
  departure.min = arrival.value ? dateKey(...(() => {const d=new Date(`${arrival.value}T12:00:00Z`);d.setUTCDate(d.getUTCDate()+1);return [d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate()];})()) : today;
  const count = nights(arrival.value, departure.value);
  send.disabled = Boolean(arrival.value || departure.value) && (!count || arrival.value < today);
  summary.textContent = count ? `${count} ${count === 1 ? words.night : words.nights} · ${guests.value} ${guests.value === '1' ? words.guest : words.guests}` : arrival.value ? words.departure : words.empty;
  render();
}
previous.onclick = () => { if (year * 12 + month <= firstMonth) return; if (--month < 0) {month=11;year--;} render(); };
next.onclick = () => { if (++month > 11) {month=0;year++;} render(); };
arrival.onchange = () => { if (departure.value && departure.value <= arrival.value) departure.value=''; if(arrival.value){year=Number(arrival.value.slice(0,4));month=Number(arrival.value.slice(5,7))-1;} update(); };
departure.onchange = update; guests.onchange = update;
document.querySelector('#contact-form').addEventListener('submit', event => {
  event.preventDefault();
  if (send.disabled || !event.currentTarget.reportValidity()) return;
  const name = document.querySelector('#contact-name').value.trim();
  const email = document.querySelector('#contact-email').value.trim();
  const message = document.querySelector('#contact-message').value.trim();
  const validDates = nights(arrival.value, departure.value);
  const text = requestText({name,email,message,arrival:validDates?format(arrival.value):'',departure:validDates?format(departure.value):'',guests:guests.value});
  window.open(`https://wa.me/393356055109?text=${encodeURIComponent(text)}`, '_blank', 'noopener,noreferrer');
});
update();
