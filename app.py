from flask import Flask, render_template
import requests
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# ==========================================
# KONFIGURASI API
# ==========================================
API_FOOTBALL_KEY = "" 
API_FOOTBALL_URL = "https://v3.football.api-sports.io/fixtures?live=all"
API_WINNERS = "https://dummyjson.com/users"

# DATABASE SLOT UTAMA (Data Home & Pragmatic Asli)
SLOTS_DB = [
    {"id": "slot1", "name": "GATES OF OLYMPUS 1000", "provider": "PRAGMATIC", "rtp": 98, "img": "https://mediumrare.imgix.net/c064ef9ce4a6caedeca1d76665b5ae31df2147ef84c0f0f8288556dfa94478f4?w=180&h=236&fit=min&auto=format"},
    {"id": "slot2", "name": "SWEET BONANZA 1000", "provider": "PRAGMATIC", "rtp": 97, "img": "https://mediumrare.imgix.net/73754d4bf421b78fbd3895bbc7890d379797588cb699d6cbe47f3656aa93613b?w=180&h=236&fit=min&auto=format"},
    {"id": "slot3", "name": "SUGAR RUSH 1000", "provider": "PRAGMATIC", "rtp": 99, "img": "https://mediumrare.imgix.net/14d5410c6cf4c303d291262a10e949dc14b0ac2eca2a7a730b0401919c01358e?w=180&h=236&fit=min&auto=format"},
    {"id": "slot4", "name": "GATES OF OLYMPUS SCATTER", "provider": "PRAGMATIC", "rtp": 96, "img": "https://mediumrare.imgix.net/73318f9e220e1637c4b11338d10f377cd997d0232636f5f5a1940167ad0451cd?w=180&h=236&fit=min&auto=format"},
    {"id": "slot5", "name": "DRAGONSPIRE", "provider": "PAPERCLIP", "rtp": 95, "img": "https://mediumrare.imgix.net/a746f89526bc0e9e64526d37793f234dfecef3c07f8df27ec09994ca0f08a8f5?w=180&h=236&fit=min&auto=format"},
    {"id": "slot6", "name": "JOKER'S JEWELS", "provider": "PRAGMATIC", "rtp": 94, "img": "https://mediumrare.imgix.net/2859df47036f5c6d3f33fead0d26c9538046589c90d5b59621306d9e4e7bfcc0?w=180&h=236&fit=min&auto=format"},
]

@app.route('/')
def home():
    # A. DATA SLOT
    slots = SLOTS_DB

    # B. DATA WINNERS
    winners = []
    try:
        resp = requests.get(f"{API_WINNERS}?limit=8", timeout=3)
        if resp.status_code == 200:
            users = resp.json().get('users', [])
            for u in users:
                menit_lalu = random.randint(0, 10)
                waktu_win = datetime.now() - timedelta(minutes=menit_lalu)
                jam_cantik = waktu_win.strftime("%H:%M")

                winners.append({
                    'name': u['username'],
                    'img': u['image'],
                    'game': random.choice(["ZEUS", "BONANZA", "MAHJONG"]),
                    'win': f"{random.randint(10, 500)}.000",
                    'time': jam_cantik
                })
    except:
        now_str = datetime.now().strftime("%H:%M")
        winners = [{'name': 'GacorMember', 'img': '', 'game': 'ZEUS', 'win': '15.000.000', 'time': now_str}]

    # C. DATA BOLA
    matches = []
    try:
        if API_FOOTBALL_KEY:
            headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_FOOTBALL_KEY}
            resp = requests.get(API_FOOTBALL_URL, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json().get('response', [])
                for m in data[:5]:
                    matches.append({
                        'id': m['fixture']['id'],
                        'league': m['league']['name'],
                        'time': f"{m['fixture']['status']['elapsed']}'",
                        'home': m['teams']['home']['name'],
                        'home_img': m['teams']['home']['logo'],
                        'away': m['teams']['away']['name'],
                        'away_img': m['teams']['away']['logo'],
                        'odds_h': round(random.uniform(1.5, 3.0), 2),
                        'odds_a': round(random.uniform(1.5, 3.0), 2)
                    })
        
        if not matches:
            raise Exception("Pakai Data Dummy")

    except Exception as e:
        print(f"Menggunakan Data Bola Dummy: {e}")
        dummy_teams = [
            ("MAN. CITY", "ARSENAL", "https://media.api-sports.io/football/teams/50.png", "https://media.api-sports.io/football/teams/42.png"),
            ("REAL MADRID", "BARCELONA", "https://media.api-sports.io/football/teams/541.png", "https://media.api-sports.io/football/teams/529.png"),
            ("LIVERPOOL", "CHELSEA", "https://media.api-sports.io/football/teams/40.png", "https://media.api-sports.io/football/teams/49.png"),
            ("JUVENTUS", "AC MILAN", "https://media.api-sports.io/football/teams/496.png", "https://media.api-sports.io/football/teams/489.png"),
            ("PERSIB", "PERSIJA", "https://upload.wikimedia.org/wikipedia/commons/d/d3/Soccerball.svg", "https://upload.wikimedia.org/wikipedia/commons/d/d3/Soccerball.svg")
        ]
        
        for i, (h, a, img_h, img_a) in enumerate(dummy_teams):
            matches.append({
                'id': f"match-{i}",
                'league': "BIG MATCH SPECIAL",
                'time': "LIVE",
                'home': h, 'home_img': img_h,
                'away': a, 'away_img': img_a,
                'odds_h': 1.90, 'odds_a': 2.10
            })

    return render_template('home_gacor.html', slots=slots, winners=winners, matches=matches)

# ==========================================
# HALAMAN LOBBY SLOTS (GABUNGAN MANUAL & OTOMATIS)
# ==========================================
@app.route('/slots')
def slots_lobby():
    # 1. GAMES MANUAL (Pragmatic yang ada gambarnya)
    # Ini akan muncul paling atas
    manual_games = [
        {"id": "slot1", "name": "GATES OF OLYMPUS 1000", "provider": "PRAGMATIC", "rtp": 98, "img": "https://mediumrare.imgix.net/c064ef9ce4a6caedeca1d76665b5ae31df2147ef84c0f0f8288556dfa94478f4?w=180&h=236&fit=min&auto=format"},
        {"id": "slot2", "name": "SWEET BONANZA 1000", "provider": "PRAGMATIC", "rtp": 97, "img": "https://mediumrare.imgix.net/73754d4bf421b78fbd3895bbc7890d379797588cb699d6cbe47f3656aa93613b?w=180&h=236&fit=min&auto=format"},
        {"id": "slot3", "name": "SUGAR RUSH 1000", "provider": "PRAGMATIC", "rtp": 99, "img": "https://mediumrare.imgix.net/14d5410c6cf4c303d291262a10e949dc14b0ac2eca2a7a730b0401919c01358e?w=180&h=236&fit=min&auto=format"},
        # ... Lu bisa tambah manual lain di sini ...
    ]
    
    # 2. GAMES OTOMATIS (Bungkus Kosong untuk Provider Lain)
    # Kita skip Pragmatic di sini biar gak dobel
    target_providers = ["NOLIMIT CITY", "HACKSAW GAMING", "PLAY'N GO", "VOLTENT"]
    generated_games = []
    
    for prov in target_providers:
        for i in range(1, 11): 
            clean_prov_name = prov.replace(" ", "_").replace("'", "").lower()
            game_id = f"slot_{clean_prov_name}_{i}"
            
            generated_games.append({
                "id": game_id,
                "name": f"{prov} GAME {i}", 
                "provider": prov,
                # Ini gambar placeholder (abu-abu)
                "img": "https://via.placeholder.com/300x400/1a1a1a/f3ce5e?text=GAMBAR+" + str(i), 
                "rtp": random.randint(90, 99)
            })

    # Gabungkan Manual + Otomatis
    final_games = manual_games + generated_games

    return render_template('slots_lobby.html', games=final_games)

@app.route('/play/<id>')
def play_slot(id):
    # 1. Coba cari di DATABASE UTAMA (Manual)
    game = next((item for item in SLOTS_DB if item["id"] == id), None)
    
    # 2. Kalau gak ketemu, Coba cari di list lobby manual (biar aman)
    # (Opsional, tapi bagus buat safety)
    
    # 3. Kalau masih gak ketemu (Berarti game dummy dari Loop), bikin data dadakan
    if not game:
        game = {
            "id": id,
            "name": id.replace("_", " ").replace("slot", "").upper(),
            "provider": "UNKNOWN PROVIDER",
            "img": "https://via.placeholder.com/300x400/000000/ffffff?text=GAME+LOADING",
            "rtp": 95
        }
        
    return render_template('play_slot.html', game=game)

@app.route('/parlay/<id>')
def bet_parlay(id):
    # KONDISI 1: JIKA KLIK MENU BAWAH (BUKA LOBBY NEGARA)
    if id == 'nav-menu':
        # Data Negara & Jumlah Match (Sesuai Request Lu)
        # Kode negara (iso) dipake buat nampilin bendera otomatis
        soccer_categories = [
            {"country": "England", "count": 60, "iso": "gb-eng"},
            {"country": "Spain", "count": 22, "iso": "es"},
            {"country": "Italy", "count": 30, "iso": "it"},
            {"country": "Germany", "count": 9, "iso": "de"},
            {"country": "France", "count": 6, "iso": "fr"},
            {"country": "Netherlands", "count": 19, "iso": "nl"},
            {"country": "Portugal", "count": 4, "iso": "pt"},
            {"country": "Brazil", "count": 10, "iso": "br"},
            {"country": "Argentina", "count": 5, "iso": "ar"},
            {"country": "Australia", "count": 7, "iso": "au"},
            {"country": "Saudi Arabia", "count": 12, "iso": "sa"},
            {"country": "Japan", "count": 8, "iso": "jp"},
            {"country": "Indonesia", "count": 3, "iso": "id"}, # Tambah Indonesia biar bangga
            {"country": "Vietnam", "count": 1, "iso": "vn"},
            {"country": "Thailand", "count": 2, "iso": "th"},
            {"country": "International", "count": 4, "iso": "un"}, # UN flag
        ]
        return render_template('parlay_lobby.html', categories=soccer_categories)
    
    # KONDISI 2: JIKA KLIK ODDS/MATCH (BUKA TIKET TARUHAN)
    else:
        # Data Dummy Match
        selected_match = {
            'league': 'PREMIER LEAGUE', 
            'home': 'MANCHESTER CITY', 
            'away': 'ARSENAL',
            'odds': 1.95
        }
        return render_template('bet_parlay.html', match=selected_match)

if __name__ == '__main__':
    app.run(debug=True, port=5002)