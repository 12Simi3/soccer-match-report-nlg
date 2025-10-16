# soccer-match-report-nlg

## Football Match Report Generator

This repository contains a small Python prototype that automatically generates a **short article (~300 words)** summarizing a football match from **scraped data**.

The goal is to create a **concise and readable match summary** that includes:

- When and where the match was played  
- Which teams competed  
- The final score  
- Key moments (goals, yellow/red cards)  
- Whether penalties were taken  

The prototype includes a **script that scrapes match data** (e.g., from *Livesport.cz*) and transforms it into a **natural-sounding text report**. 
It is designed to be modular and easy to extend.

### Assumption for this Case study
**Data Assumptions**

- Always available fields: date and time**, home and away teams, and result.  
- Optional fields: yellow/red cards, penalties**, and match statistics may not always be present.  
- If these optional fields are missing, it is assumed that the corresponding events did not occur (e.g., no red cards were issued).  
- All fields are in absolute counts.
- Home is always on right and Away is always on left side.
- The web scraper outputs data in JSON format with UTF-8 encoding.
- The page’s HTML/DOM structure and selectors used by the scraper remain unchanged across future match pages. Any breaking changes to the DOM may require selector updates.
- All text is assumed to be in Czech.

**Technical Prerequisites**
- Python 3.10.11
- Libraries: Install from requirements.txt
- API key from aistudio.google.com

### Output
A **short article** (one paragraph, Czech) containing a match summary that highlights the main characteristics.

> **Ukázkový výstup (CZ)**
>
> V neděli **2. dubna 2023 v 16:00** hostila **Sparta Praha** tým **Zbrojovky Brno** a po vydařeném výkonu zvítězila **3:1**. Utkání se obešlo bez červených karet; hlavní rozhodčí udělil **šest žlutých** – po **třech** na každé straně – a **pokutové kopy** nařízeny nebyly. Statistický obraz hry vyznívá jednoznačně pro Spartu: domácí drželi míč **65 %** času (Brno **35 %**), vyslali **14 střel**, z toho **7 na branku** (Brno **8/2**). Z rohů vytěžila Sparta **7** pokusů proti **1** brněnskému, mimo tyče mířilo **6** domácích a **4** hostujících střel. Zblokované pokusy byly rozděleny **1 : 2** (Sparta : Brno). V ofsajdu se domácí ocitli **2×**, hosté **4×**. Rozhodčí pískl Spartě **14** přímých kopů, Brnu **18**; vhazování byla vyrovnaná **25 : 25**. V osobních soubojích si Sparta připsala **16 faulů**, Zbrojovka **9**. Brankář Sparty musel zasahovat pouze **1×**, jeho protějšek v brněnské brance **4×**, což podtrhuje převahu Letenských v klíčových momentech i efektivitu v zakončení.
