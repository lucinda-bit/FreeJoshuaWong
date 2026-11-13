// PRESS COVERAGE. Add new pieces anywhere; the page sorts by date.
// date: YYYY-MM-DD. type: news | opinion | rights. region: UK | US | Asia | Europe | Global
// moment: charge | plea | film | birthday | sentence. paywall: true if the outlet may ask readers to subscribe.
// We only show the outlet, date and headline and link to the original. Never copy article text here.
window.MOMENTS = [
  {id:"charge",   label:"Charged again",      when:"June 2025"},
  {id:"plea",     label:"Pleads guilty",      when:"September 2026"},
  {id:"film",     label:"Film targeted",      when:"September 2026"},
  {id:"birthday", label:"Turns 30 in prison", when:"October 2026"},
  {id:"sentence", label:"Ten more years",     when:"November 2026"}
];
window.PRESS = [
  // ---- Sentence, November 2026
  {date:"2026-11-09", outlet:"Taipei Times", type:"opinion", region:"Asia", moment:"sentence", title:"Taipei Times editorial on Joshua Wong’s ten-year sentence", url:"https://www.taipeitimes.com/News/editorials/archives/2026/11/09/2003867391"},
  {date:"2026-11-08", outlet:"Free Press Journal", type:"opinion", region:"Asia", moment:"sentence", title:"Joshua Wong: A beacon of freedom brought down", url:"https://www.freepressjournal.in/analysis/joshua-wong-a-beacon-of-freedom-brought-down"},
  {date:"2026-11-07", outlet:"Taipei Times", type:"opinion", region:"Asia", moment:"sentence", title:"Editorial: Joshua Wong was due for release in January", url:"https://www.taipeitimes.com/News/editorials/archives/2026/11/07/2003867296"},
  {date:"2026-11-07", outlet:"Taipei Times", type:"opinion", region:"Asia", moment:"sentence", title:"Taipei Times editorial on Joshua Wong’s letters from prison", url:"https://www.taipeitimes.com/News/editorials/archives/2026/11/07/2003867298"},
  {date:"2026-11-06", outlet:"Reuters / CTV", type:"news", region:"Global", moment:"sentence", title:"Canada, US, UK and others condemn 10-year sentence for Joshua Wong", url:"https://www.ctvnews.ca/world/article/canada-us-uk-and-others-condemn-10-year-sentence-for-hong-kong-activist-joshua-wong/"},
  {date:"2026-11-06", outlet:"The Nation Thailand", type:"news", region:"Asia", moment:"sentence", title:"Hong Kong jails Joshua Wong for 10 years", url:"https://www.nationthailand.com/news/world/40073179"},
  {date:"2026-11-05", outlet:"The Spectator", type:"opinion", region:"UK", moment:"sentence", paywall:true, feature:true, by:"Benedict Rogers", title:"Joshua Wong’s imprisonment shows China is running scared", url:"https://www.spectator.com.au/?p=10947071"},
  {date:"2026-11-05", outlet:"CNN", type:"news", region:"US", moment:"sentence", title:"Hong Kong democracy campaigner Joshua Wong handed another 10 years in jail", url:"https://keyt.com/?p=1498735"},
  {date:"2026-11-05", outlet:"Associated Press", type:"news", region:"US", moment:"sentence", title:"Hong Kong activist Joshua Wong is sentenced to 10 more years in prison", url:"https://www.wamc.org/2026-11-05/hong-kong-activist-joshua-wong-is-sentenced-to-10-more-years-in-prison"},
  {date:"2026-11-05", outlet:"Reuters", type:"news", region:"Global", moment:"sentence", title:"Hong Kong activist Joshua Wong gets 10 years in jail on national security charge", url:"https://koreatimes.co.kr/world/20261105/hong-kong-activist-joshua-wong-gets-10-years-in-jail-on-national-security-charge"},
  {date:"2026-11-05", outlet:"AFP", type:"news", region:"Global", moment:"sentence", title:"Hong Kong activist Joshua Wong given 10 more years for collusion", url:"https://www.courthousenews.com/hong-kong-activist-joshua-wong-given-10-more-years-for-collusion/"},
  {date:"2026-11-05", outlet:"ITV News", type:"news", region:"UK", moment:"sentence", title:"Hong Kong activist Joshua Wong sentenced to 10 more years in prison", url:"https://www.itv.com/news/2026-11-04/joshua-wong-sentenced-to-10-more-years-in-prison"},
  {date:"2026-11-05", outlet:"South China Morning Post", type:"news", region:"Asia", moment:"sentence", paywall:true, title:"Joshua Wong jailed for 10 years over bid to instigate sanctions", url:"https://www.scmp.com/news/hong-kong/law-and-crime/article/3373335/joshua-wong-jailed-10-years-over-bid-instigate-sanctions-beijing-hong-kong"},
  {date:"2026-11-05", outlet:"Radio Free Asia", type:"news", region:"US", moment:"sentence", title:"International community condemns Joshua Wong’s 10-year sentence", url:"https://rfa.org/english/china/2026/11/05/joshua-wong-hong-kong-sentence/"},
  {date:"2026-11-05", outlet:"Focus Taiwan", type:"news", region:"Asia", moment:"sentence", title:"Taiwan condemns 10-year sentence for Hong Kong activist Joshua Wong", url:"https://focustaiwan.tw/politics/202611050018"},
  {date:"2026-11-05", outlet:"UCA News", type:"news", region:"Asia", moment:"sentence", title:"Hong Kong activist Joshua Wong jailed for another 10 years", url:"https://www.ucanews.com/news/hong-kong-activist-joshua-wong-jailed-for-another-10-years/116033"},
  {date:"2026-11-05", outlet:"Newsweek", type:"opinion", region:"US", moment:"sentence", by:"Didi Kirsten Tatlow and John Feng", title:"The long death of Hong Kong democracy", url:"https://newsweek.com/the-long-death-of-hong-kong-democracy-12679637"},
  {date:"2026-11-05", outlet:"Human Rights Watch", type:"rights", region:"Global", moment:"sentence", title:"Joshua Wong gets nearly 10 more years in prison", url:"https://www.hrw.org/news/2026/11/05/hong-kong-joshua-wong-gets-nearly-10-more-years-in-prison"},
  {date:"2026-11-05", outlet:"Amnesty International", type:"rights", region:"Global", moment:"sentence", title:"Cruel Joshua Wong sentence a grim reminder of authorities’ disdain for human rights", url:"https://www.amnestyusa.org/press-releases/hong-kong-cruel-joshua-wong-sentence-a-grim-reminder-of-authorities-disdain-for-human-rights/"},
  // ---- 30th birthday, October 2026
  {date:"2026-10-13", outlet:"The Spectator", type:"opinion", region:"UK", moment:"birthday", paywall:true, by:"Benedict Rogers", title:"The bravery of Joshua Wong, on his 30th birthday", url:"https://www.spectator.com.au/?p=10944836"},
  // ---- Film, September 2026
  {date:"2026-09-15", outlet:"Dimsum Daily", type:"news", region:"Asia", moment:"film", title:"Security Bureau reviewing Netflix film on Joshua Wong", url:"https://www.dimsumdaily.hk/security-bureau-reviewing-netflix-film-on-joshua-wong/"},
  // ---- Plea, September 2026
  {date:"2026-09-03", outlet:"Taipei Times", type:"news", region:"Asia", moment:"plea", title:"Taiwanese civic groups call for Joshua Wong’s immediate release", url:"https://www.taipeitimes.com/News/taiwan/archives/2026/09/03/2003863605"},
  {date:"2026-09-02", outlet:"Channel 4 News", type:"news", region:"UK", moment:"plea", title:"Joshua Wong pleads guilty to colluding with foreign entities", url:"https://www.channel4.com/news/hong-kong-pro-democracy-activist-joshua-wong-pleads-guilty-to-colluding-with-foreign-entities"},
  {date:"2026-09-02", outlet:"Sky News", type:"news", region:"UK", moment:"plea", title:"Joshua Wong pleads guilty under Hong Kong’s security law", url:"https://www.heart.co.uk/news/uk-world/joshua-wong-pleads-guilty-under-hong-kongs-se/"},
  {date:"2026-09-02", outlet:"Reuters", type:"news", region:"Global", moment:"plea", title:"Hong Kong activist Joshua Wong pleads guilty to collusion with foreign entities", url:"https://theprint.in/world/hong-kong-activist-joshua-wong-pleads-guilty-to-collusion-with-foreign-entities/3031356/"},
  {date:"2026-09-02", outlet:"Associated Press", type:"news", region:"US", moment:"plea", title:"Prominent Hong Kong activist Joshua Wong pleads guilty in second national security case", url:"https://abcnews.com/International/wireStory/prominent-hong-kong-activist-joshua-wong-pleads-guilty-136132039"},
  {date:"2026-09-02", outlet:"Euronews", type:"news", region:"Europe", moment:"plea", title:"Joshua Wong pleads guilty in second national security case", url:"https://euronews.com/2026/09/02/prominent-pro-democracy-hong-kong-activist-joshua-wong-pleads-guilty-in-second-national-se"},
  {date:"2026-09-02", outlet:"CNN", type:"news", region:"US", moment:"plea", title:"Joshua Wong faces longer prison sentence after second guilty plea", url:"https://keyt.com/news/national-world/cnn-world/2026/09/01/hong-kong-democracy-activist-joshua-wong-faces-longer-prison-sentence-after-second-national-security-guilty-plea/"},
  {date:"2026-09-02", outlet:"Focus Taiwan", type:"news", region:"Asia", moment:"plea", title:"Taiwan groups call for Joshua Wong’s release after guilty plea", url:"https://focustaiwan.tw/politics/202609020024"},
  {date:"2026-09-02", outlet:"UCA News", type:"news", region:"Asia", moment:"plea", title:"Joshua Wong pleads guilty to Hong Kong national security charge", url:"https://www.ucanews.com/news/joshua-wong-pleads-guilty-to-hong-kong-national-security-charge/115111"},
  {date:"2026-09-02", outlet:"AsiaNews", type:"opinion", region:"Europe", moment:"plea", title:"Joshua Wong pleads “guilty” in Hong Kong’s sham trial", url:"https://www.asianews.it/en/east-asia/hong-kong/joshua-wong-pleads-guilty-in-hong-kong-s-sham-trial"},
  {date:"2026-09-02", outlet:"Hong Kong Watch", type:"rights", region:"UK", moment:"plea", title:"Joshua Wong pleads guilty in second National Security Law trial", url:"https://www.hongkongwatch.org/all-posts/2026/9/2/joshua-wong-joshua-wong-pleads-guilty-in-second-hong-kong-national-security-law-trial"},
  {date:"2026-09-01", outlet:"Hong Kong Labour Rights Monitor", type:"rights", region:"UK", moment:"plea", title:"Jailed at 24, still not free at 30: the endless prosecution of Joshua Wong", url:"https://hklabourrights.org/?p=15288"},
  // ---- Charge, June 2025
  {date:"2025-06-13", outlet:"Committee for Freedom in Hong Kong", type:"rights", region:"US", moment:"charge", title:"Jailed activist Joshua Wong arrested on National Security Law charges", url:"https://thecfhk.org/?p=6311"},
  {date:"2025-06-10", outlet:"E-International Relations", type:"opinion", region:"UK", moment:"charge", title:"Joshua Wong and Hong Kong’s right to self-determination", url:"https://www.e-ir.info/2025/06/10/opinion-joshua-wong-and-hong-kongs-right-to-self-determination/"},
  {date:"2025-06-09", outlet:"Global Voices", type:"news", region:"Global", moment:"charge", title:"Jailed Hong Kong activist Joshua Wong faces new foreign collusion charges", url:"https://globalvoices.org/2025/06/09/jailed-hong-kong-activist-joshua-wong-faces-new-foreign-collusion-charges/"},
  {date:"2025-06-06", outlet:"Amnesty International", type:"rights", region:"Global", moment:"charge", title:"New charges against Joshua Wong designed to prolong his stay behind bars", url:"https://www.amnestyusa.org/press-releases/hong-kong-new-charges-against-joshua-wong-designed-to-prolong-his-stay-behind-bars/"},
  {date:"2025-06-06", outlet:"Reuters / The Star", type:"news", region:"Asia", moment:"charge", title:"Joshua Wong charged under Beijing-imposed security law for second time", url:"https://www.thestar.com.my/aseanplus/aseanplus-news/2025/06/06/hong-kong-activist-joshua-wong-charged-under-beijing-imposed-security-law-for-second-time"},
  {date:"2025-06-06", outlet:"RTHK", type:"news", region:"Asia", moment:"charge", title:"Joshua Wong in court over collusion conspiracy", url:"https://news.rthk.hk/rthk/en/component/k2/1807894-20250606.htm"}
];
