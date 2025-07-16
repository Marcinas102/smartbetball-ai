import requests
from datetime import date

# 👉 Wklej swój klucz API tutaj:
api_key = "08955049bf88c4f62ade7ad94cc0ddf1"

# 🔄 Dynamiczna data
today = date.today().strftime("%Y-%m-%d")
url = f"https://v3.football.api-sports.io/fixtures?date={today}"
headers = {
    "x-apisports-key": api_key
}

# 📅 Pobieranie listy meczów
response = requests.get(url, headers=headers)
fixtures = response.json()["response"]

# 📋 Wyświetlanie meczów z numerami
print("\nMecze na dziś:")
for idx, fixture in enumerate(fixtures):
    home = fixture["teams"]["home"]["name"]
    away = fixture["teams"]["away"]["name"]
    print(f"{idx}: {home} vs {away}")

# 🎯 Wybór meczu
selected = int(input("\nPodaj numer meczu do analizy: "))
chosen_fixture = fixtures[selected]
fixture_id = chosen_fixture["fixture"]["id"]

# 📊 Pobieranie statystyk wybranego meczu
stats_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
stats_response = requests.get(stats_url, headers=headers)
stats_data = stats_response.json()

# 🧠 AI: analiza statystyk
home_stats = stats_data["response"][0]["statistics"]
away_stats = stats_data["response"][1]["statistics"]

def typuj_mecz(home_stats, away_stats):
    typy = []

    # Shots on Goal → BTTS / Over 2.5
    shots_home = next((s for s in home_stats if s["type"] == "Shots on Goal"), None)
    shots_away = next((s for s in away_stats if s["type"] == "Shots on Goal"), None)
    if shots_home and shots_away:
        if int(shots_home["value"]) >= 6 and int(shots_away["value"]) >= 6:
            typy.append("Over 2.5 bramki")
        if int(shots_home["value"]) >= 5 and int(shots_away["value"]) >= 5:
            typy.append("BTTS – TAK")

    # Ball Possession → możliwy remis
    poss_home = next((p for p in home_stats if p["type"] == "Ball Possession"), None)
    poss_away = next((p for p in away_stats if p["type"] == "Ball Possession"), None)
    if poss_home and poss_away:
        h_poss = int(poss_home["value"].replace('%',''))
        a_poss = int(poss_away["value"].replace('%',''))
        if abs(h_poss - a_poss) < 10:
            typy.append("Możliwy remis")

    # Fouls → dużo kartek
    fouls_home = next((f for f in home_stats if f["type"] == "Fouls"), None)
    fouls_away = next((f for f in away_stats if f["type"] == "Fouls"), None)
    if fouls_home and fouls_away:
        total_fouls = int(fouls_home["value"]) + int(fouls_away["value"])
        if total_fouls >= 30:
            typy.append("Typ: dużo kartek (powyżej 5)")

    return typy

# 🔍 Wyniki analizy AI
typy = typuj_mecz(home_stats, away_stats)
print("\n🧠 Sugerowane typy AI:")
if typy:
    for typ in typy:
        print(f"– {typ}")
else:
    print("Brak wyraźnych typów. Mecz może być nieprzewidywalny.")
