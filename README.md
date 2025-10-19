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

- Always available fields: date and time, home and away teams, and result.  
- Optional fields: yellow/red cards, penalties, and match statistics may not always be present.  
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

### How  to run

#### 1) Virtual environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
pip install -r requirements.txt
```
#### 2) .env variables

**Windows (PowerShell):**
```powershell
$env:API_KEY = ""
$env:MODEL = ""     # default gemini-2.5-flash
```

#### 3) Start the script in CLI

```powershell
 python .\scraper\scrape_stats_section.py
 python .\nlg\generate_summary_gemini_300w.py 
```

### Output
A **short article** (Czech) containing a match summary that highlights the main characteristics.

> **Ukázkový výstup (CZ)**
>
>Dne 02.04.2023 v 16:00 se na domácí půdě utkala Sparta Praha se Zbrojovkou Brno. Zápas skončil vítězstvím domácích 3:1. Během utkání byly rozdány celkem tři žluté karty pro Spartu Praha a tři žluté karty pro Zbrojovku Brno. Žádné červené karty nebyly uděleny a v zápase nebyly nařízeny žádné penalty. Co se týče dalších statistik, držení míče bylo výrazně na straně Sparty Praha s 65 % oproti 35 % Zbrojovky Brno. Sparta celkem vystřelila 14krát, z toho 7 střel mířilo na branku, zatímco Zbrojovka zaznamenala 8 střel celkem a 2 na branku. Rohových kopů měla Sparta 7, hosté pouze 1. Mimo branku letělo 6 střel Sparty a 4 střely Zbrojovky. Zblokovaných střel měla Sparta 1, Zbrojovka 2. Ofsajdy byly pískány 2x Spartě a 4x Zbrojovce. Přímých kopů bylo pro Spartu 14 a pro Zbrojovku 18. Vhazování bylo shodně 25 pro oba týmy. Faulů se dopustila Sparta 16krát a Zbrojovka 9krát. Brankář Sparty si připsal 1 zákrok, zatímco brankář Zbrojovky musel zasahovat 4krát. Sparta Praha si tak připsala důležité vítězství, které bylo podpořeno výraznou převahou v držení míče a počtu střel na branku, což se nakonec projevilo i na konečném skóre.