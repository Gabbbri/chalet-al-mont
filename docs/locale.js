export const language = ['it','en','de'].includes(document.documentElement.lang) ? document.documentElement.lang : 'it';
export const locale = {it:'it-IT',en:'en-GB',de:'de-DE'}[language];
export const words = {
  it:{night:'notte',nights:'notti',guest:'ospite',guests:'ospiti',empty:'Seleziona le date per preparare la richiesta.',departure:'Ora scegli la data di partenza, successiva all’arrivo.'},
  en:{night:'night',nights:'nights',guest:'guest',guests:'guests',empty:'Choose your dates to prepare your enquiry.',departure:'Now choose a departure date after your arrival.'},
  de:{night:'Nacht',nights:'Nächte',guest:'Gast',guests:'Gäste',empty:'Wähle die Reisedaten für deine Anfrage.',departure:'Wähle nun ein Abreisedatum nach deiner Anreise.'}
}[language];
export function requestText({name,email,message,arrival,departure,guests}) {
  const count=Number(guests),guestWord=count===1?words.guest:words.guests;
  const dates=arrival&&departure;
  let text;
  if(language==='en')text=`Hi Leonardo, my name is ${name}. I would like information about Chalet al Mont${dates?` from ${arrival} to ${departure}`:''}, for ${count} ${guestWord}.`;
  else if(language==='de')text=`Hallo Leonardo, ich heiße ${name}. Ich hätte gerne Informationen zu Chalet al Mont${dates?` vom ${arrival} bis zum ${departure}`:''} für ${count} ${guestWord}.`;
  else text=`Ciao Leonardo, sono ${name}. Vorrei informazioni per Chalet al Mont${dates?` dal ${arrival} al ${departure}`:''}, per ${count} ${guestWord}.`;
  return text+(email?`\n${language==='de'?'E-Mail':'Email'}: ${email}`:'')+(message?`\n\n${message}`:'')+`\n${language==='en'?'Thank you!':language==='de'?'Vielen Dank!':'Grazie!'}`;
}
