export const language = ['it','en','de'].includes(document.documentElement.lang) ? document.documentElement.lang : 'it';
export const locale = {it:'it-IT',en:'en-GB',de:'de-DE'}[language];
export const words = {
  it:{night:'notte',nights:'notti',guest:'ospite',guests:'ospiti',empty:'Seleziona le date per preparare la richiesta.',departure:'Ora scegli la data di partenza, successiva all’arrivo.'},
  en:{night:'night',nights:'nights',guest:'guest',guests:'guests',empty:'Choose your dates to prepare your enquiry.',departure:'Now choose a departure date after your arrival.'},
  de:{night:'Nacht',nights:'Nächte',guest:'Gast',guests:'Gäste',empty:'Wähle die Reisedaten für deine Anfrage.',departure:'Wähle nun ein Abreisedatum nach deiner Anreise.'}
}[language];
export function requestText({name,message,arrival,departure,guests}) {
  const count = Number(guests);
  function block(lang) {
    const guestWord = {it:count===1?'ospite':'ospiti',en:count===1?'guest':'guests',de:count===1?'Gast':'Gäste'}[lang];
    const date = key => new Intl.DateTimeFormat({it:'it-IT',en:'en-GB',de:'de-DE'}[lang], {day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(`${key}T12:00:00Z`));
    const dates = arrival && departure;
    let text;
    if(lang==='en') text=`Hi Leonardo, my name is ${name}. I would like information about Chalet al Mont${dates?` from ${date(arrival)} to ${date(departure)}`:''}, for ${count} ${guestWord}.`;
    else if(lang==='de') text=`Hallo Leonardo, ich heiße ${name}. Ich hätte gerne Informationen zu Chalet al Mont${dates?` vom ${date(arrival)} bis zum ${date(departure)}`:''} für ${count} ${guestWord}.`;
    else text=`Ciao Leonardo, sono ${name}. Vorrei informazioni per Chalet al Mont${dates?` dal ${date(arrival)} al ${date(departure)}`:''}, per ${count} ${guestWord}.`;
    if(message) text+=`\n\n${lang==='it'&&language!=='it'?'Messaggio dell’ospite (testo originale)':{it:'Messaggio',en:'Message',de:'Nachricht'}[lang]}:\n${message}`;
    return text+`\n${{it:'Grazie!',en:'Thank you!',de:'Vielen Dank!'}[lang]}`;
  }
  return block(language)+(language==='it'?'':'\n\n──────────\nITALIANO\n\n'+block('it'));
}
