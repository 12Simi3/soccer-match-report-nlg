import os, json, re
from pathlib import Path
from google import genai

API_KEY = os.getenv("API_KEY")
MODEL   = os.getenv("MODEL", "gemini-2.5-flash")

def limit_words(text: str, n: int = 320) -> str:
    s = " ".join((text or "").split())
    if not s:
        return ""
    cut = " ".join(s.split()[:n])
    last = max(cut.rfind("."), cut.rfind("!"), cut.rfind("?"), cut.rfind("…"))
    if last != -1:
        return cut[:last+1].strip()
    return (cut + ".").strip()

def build_prompt(data: dict) -> str:
    return (
        "Jsi sportovní redaktor. Z následujících DAT napiš česky souvislý článek "
        "o přibližně 300 slovech. Článek musí obsahovat datum, soupeře, "
        "finální skóre, rozdané žluté a červené karty a penalty. "
        "Ve zbytku textu vypiš ostatní statistiky jako držení míče,"
        "střely celkem, střely na branku, rohové kopy, střely mimo branku, obsajdy,"
        "přímé kopy, vhazování, fauly a brankářské zákroky a další statistiky."
        "Nepřidávej nic, co v datech není. Bez nadpisu, žádné odrážky, žádná tabulka.\n"
        f"DATa: {json.dumps(data, ensure_ascii=False)}"
    )

def main():
    if not API_KEY:
        raise RuntimeError("API_KEY env var není nastaven.")

    data = json.loads(Path("data/match_stats.json").read_text(encoding="utf-8"))
    client = genai.Client(api_key=API_KEY)

    resp = client.models.generate_content(
        model=MODEL,
        contents=build_prompt(data),
        config=genai.types.GenerateContentConfig(
            temperature=0.25,
            max_output_tokens=None,
            response_mime_type="text/plain"
        ),
    )
    text = (resp.text or "").strip()
    text = limit_words(text,320)

    print(text)
    Path("data").mkdir(exist_ok=True)
    Path("data/summary_300wl.txt").write_text(text, encoding="utf-8")

if __name__ == "__main__":
    main()
