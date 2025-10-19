import asyncio, json, re, html
from pathlib import Path
from playwright.async_api import async_playwright

URL = "https://www.livesport.cz/zapas/fotbal/sparta-praha-6qA358jH/zbrojovka-brno-4d5TT6i5/?mid=StyIyb9D#/prehled-zapasu/prehled-zapasu"
OUT = Path("data/match_stats.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

ROOT       = ".container__livetable"
TABS_WRAP  = f"{ROOT} [data-testid='wcl-tabs']"
TAB_STATS  = f"{TABS_WRAP} a[data-analytics-alias='match-statistics']"
SCOPE_SUM  = f"{ROOT} [data-analytics-context='tab-match-summary']"

SCOPE_STATS = '[data-analytics-context="tab-match-statistics"]'
ROW         = f'{SCOPE_STATS} [data-testid="wcl-statistics"]'
CAT         = '[data-testid="wcl-statistics-category"]'
VALS        = '[data-testid="wcl-statistics-value"]'

RE_SCORE = re.compile(r"(\d+)\s*[-:]\s*(\d+)")

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()

def clean_desc(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)   # turn <br> into spaces
    s = re.sub(r"<[^>]+>", "", s)                  # drop any remaining HTML tags
    s = html.unescape(s)                           # &nbsp; &amp; etc.
    return re.sub(r"\s+", " ", s).strip()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        try:
            await page.goto(URL, wait_until="networkidle", timeout=60000)

            # Accept cookies
            for sel in [
                "button:has-text('Souhlasím')",
                "button:has-text('Accept all')",
                "[data-testid='uc-accept-all-button']",
            ]:
                try:
                    await page.locator(sel).first.click(timeout=1500)
                except:
                    pass

            await page.locator(SCOPE_SUM).first.wait_for(state="visible", timeout=6000)
            
            # Get penalties
            penalties = await page.evaluate(
                """(scopeSel) => {
                    const scope = document.querySelector(scopeSel);
                    if (!scope) return [];

                    const rowSel = ".smv__participantRow";
                    const incidentSel = ".smv__incident";
                    const subSel = ".smv__subIncident";
                    const timeSel = ".smv__timeBox";
                    const iconTitleSel = ".smv__incidentIcon [title]";

                    const out = [];
                    const rows = scope.querySelectorAll(rowSel);

                    rows.forEach(row => {
                        const cls = row.getAttribute("class") || "";
                        const side = cls.includes("homeParticipant") ? "home" : "away";

                        row.querySelectorAll(incidentSel).forEach(inc => {
                            const sub = inc.querySelector(subSel);
                            if (!sub) return;

                            const subText = (sub.textContent || "").trim();
                            if (!/penalt/i.test(subText)) return;

                            const minute = ((inc.querySelector(timeSel) || {}).textContent || "").trim();
                            const titleEl = inc.querySelector(iconTitleSel);
                            const title = (titleEl && titleEl.getAttribute("title") || "").replace(/\\s+/g, " ").trim();

                            out.push({ side, minute, title, sub_text: subText });
                        });
                    });
                    return out;
                }""",
                SCOPE_SUM,
            )
            
            for item in penalties:
                item["title"] = clean_desc(item.get("title", ""))
                item["sub_text"] = clean_desc(item.get("sub_text", ""))
                m = re.match(r"\s*(\d+)", item.get("minute", ""))
                if m:
                    item["minute"] = int(m.group(1))

            if not penalties:  # True for [] / None
                penalties = "no penalties"

            await page.mouse.wheel(0, 400)  # scroll down
            await page.wait_for_timeout(200)  # small settle
            await page.locator(TAB_STATS).first.click(timeout=4000)
            await page.wait_for_selector(ROW, timeout=8000)

            # get date, home, away, result
            date_txt = (await page.locator(f"{ROOT} .duelParticipant__startTime").first.text_content() or "").strip()
            if not date_txt:
                date_txt = await page.locator(f"{ROOT} time[datetime]").first.get_attribute("datetime")

            home = (await page.locator(f"{ROOT} .duelParticipant__home [class*='participantName']").first.text_content() or "").strip()
            if not home:
                home = norm(await page.locator(f"{ROOT} .duelParticipant__home").first.inner_text() or "")

            away = (await page.locator(f"{ROOT} .duelParticipant__away [class*='participantName']").first.text_content() or "").strip()
            if not away:
                away = norm(await page.locator(f"{ROOT} .duelParticipant__away").first.inner_text() or "")

            score_text = (await page.locator(f"{ROOT} .duelParticipant__score").first.inner_text() or "").strip()
            m = RE_SCORE.search(score_text.replace("\n", " "))
            result = f"{m.group(1)}-{m.group(2)}" if m else ""

            stats = {}
            rows = page.locator(ROW)
            n = await rows.count()

            for i in range(n):
                r = rows.nth(i)
                label = norm(await r.locator(CAT).text_content())

                # Always: first value = home (left), second = away (right)
                cells = r.locator(VALS)
                cnt = await cells.count()
                home_val = norm(await cells.nth(0).text_content()) if cnt > 0 else ""
                away_val = norm(await cells.nth(1).text_content()) if cnt > 1 else ""

                if label:
                    stats[label] = {"home": home_val, "away": away_val}

        finally:
            await browser.close()

    data = {
        "date": date_txt,
        "home": home,
        "away": away,
        "result": result,
        "statistics": stats,
        "penalties": penalties
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
