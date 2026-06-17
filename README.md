# ACL GhostFix

**A HackRF-based GPS/GNSS signal simulation & spoofing toolkit with a modern GUI.**

ACL GhostFix wraps [gps-sdr-sim](https://github.com/osqzss/gps-sdr-sim) and HackRF's
`hackrf_transfer` into a single, easy-to-use desktop application — no command-line
juggling, no manual RINEX hunting. Pick a location on a map (or type a city name),
hit one button, and the tool downloads the navigation data, generates the IF signal,
and transmits it.

Built for RF security research, GNSS spoofing detection R&D, and educational labs.

![status](https://img.shields.io/badge/status-active-brightgreen)
![license](https://img.shields.io/badge/license-GPLv3-blue)
![platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## ✨ Features

- 🎯 **Smart Location Finder** — search by city/place name, or paste a Google Maps
  link and the coordinates are extracted automatically
- 🛰 **Automatic RINEX download** with a 4-source fallback chain (NASA CDDIS HTTPS,
  BKG IGS Mirror, NASA CDDIS FTP, GAGE/UNAVCO) — so it keeps working even when one
  mirror is down or requires authentication
- 🔍 **Auto-discovery of `gps-sdr-sim.exe`** — no need to manually configure the path;
  the app scans common install locations and, if needed, your drives
- 🌐 **Bilingual UI** — English (default) and Turkish, switchable in Settings
- ⚡ **One-click automatic mode** — RINEX → .bin generation → transmission, in sequence
- 📟 Live terminal-style log panel with color-coded output
- 🗺 12 built-in location presets (Istanbul, Ankara, Tokyo, Dubai, London...)

---

## ⚠️ Legal Disclaimer — Read Before Using

GPS/GNSS spoofing **transmits RF signals on protected frequencies (1575.42 MHz, L1
band)** and can interfere with navigation systems used by aircraft, ships, emergency
services, and other safety-critical infrastructure.

- In most countries (including Turkey, the EU, and the US) transmitting on GNSS
  frequencies without authorization is **illegal** and can carry serious criminal
  penalties.
- This tool is intended **strictly for**:
  - Use inside a **shielded RF chamber / Faraday cage**
  - Licensed research environments with proper spectrum authorization
  - **Receive-only** GNSS security research where you do not actually key up the HackRF
  - Educational study of the GPS-SDR-SIM signal generation pipeline
- **Never transmit outdoors or in any environment where the signal can propagate
  beyond your controlled test setup.**
- The authors and contributors of this project assume **no liability** for misuse.
  You are solely responsible for complying with the laws and spectrum regulations of
  your country.

If you're not 100% sure your use case is legal where you are — don't transmit.

---

## 🔧 Requirements

| Component | Notes |
|---|---|
| **Windows 10/11** | Currently Windows-only (uses `os.startfile`, `hackrf_transfer` via shell) |
| **Python 3.10+** | https://python.org |
| **HackRF One** | With drivers installed ([HackRF tools](https://github.com/greatscottgadgets/hackrf/releases)) |
| **gps-sdr-sim.exe** | You build this yourself from source — see step-by-step guide below, it only takes a few minutes |
| **NASA Earthdata account** *(optional)* | Free at [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov) — improves RINEX download reliability, but the tool has fallback mirrors that often work without it |

---

## 🛰 Building gps-sdr-sim.exe (one-time setup)

> ⚠️ **Note:** the original [osqzss/gps-sdr-sim](https://github.com/osqzss/gps-sdr-sim) repo is
> archived and does **not** provide a ready-made `.exe` on its Releases page — you build it
> yourself from the C source. It's quick and there's no reason to trust a random
> pre-built binary from a stranger when compiling it yourself takes 5 minutes and only
> requires free, official tools.

**If you've never used Visual Studio before, follow these steps exactly:**

1. Download **Visual Studio Community** (free) from
   [visualstudio.microsoft.com](https://visualstudio.microsoft.com/) and run the installer.
   In the installer, check the **"Desktop development with C++"** workload, then click Install.
2. Download the gps-sdr-sim source code:
   - Go to [github.com/osqzss/gps-sdr-sim](https://github.com/osqzss/gps-sdr-sim)
   - Click the green **`<> Code`** button → **Download ZIP**
   - Extract the ZIP anywhere (e.g. your Desktop)
3. Open Visual Studio → **Create a new project** → **Empty Project** (C++) → name it
   `gps-sdr-sim` → Create.
4. In the **Solution Explorer** panel (usually on the right):
   - Right-click **Source Files** → **Add → Existing Item...**
   - Navigate to the extracted gps-sdr-sim folder and select **`gpssim.c`** and
     **`getopt.c`** → Add.
5. At the top toolbar, change the dropdown from **Debug** to **Release**.
6. Click **Build → Build Solution** (or press `Ctrl+Shift+B`).
7. Your compiled file will be at:
   `<project folder>\x64\Release\gps-sdr-sim.exe`
   (or `Release\gps-sdr-sim.exe` if you're building x86)
8. Copy that `gps-sdr-sim.exe` into `C:\ACL-GhostFix\` — ACL GhostFix's auto-discovery
   will find it automatically on next launch (or use the 🔍 **Auto** button in Settings).

That's it — you only need to do this once.

---

## 📦 Installation

```bash
git clone https://github.com/acl-labs/acl-ghostfix.git
cd acl-ghostfix
pip install -r requirements.txt
python main.py
```

On first launch:

1. The app creates `C:\ACL-GhostFix\` with two subfolders:
   - `rinex\` — downloaded/cached navigation files
   - `bin\` — generated IF signal files ready for transmission
2. It automatically scans common locations (and, as a fallback, your drives) for
   `gps-sdr-sim.exe`. If you haven't built it yet, see the **Building gps-sdr-sim.exe**
   section above first. Once built, drop it into `C:\ACL-GhostFix\` or point to it
   manually in **Settings → gps-sdr-sim.exe Path** (there's also a 🔍 **Auto** re-scan
   button there).
3. *(Optional)* Add your NASA Earthdata credentials in **Settings** for more reliable
   RINEX downloads.

---

## 🚀 Usage

1. **Pick a location** — use the Smart Location Finder, a quick preset, or type
   coordinates manually.
2. **Step 1 — RINEX**: click *Download/Select RINEX*. Auto mode tries 4 sources in
   order; if all fail, point it to a local `.nav`/`.rnx` file via *Manual* mode.
3. **Step 2 — Generate .bin**: builds the IF signal file with `gps-sdr-sim` for your
   chosen coordinates and duration.
4. **Step 3 — Transmit**: sends the signal via `hackrf_transfer`. **Only do this inside
   a shielded enclosure** (see disclaimer above).
5. Or just hit **⚡ AUTO** to run all three steps back-to-back.

---

## 🗂 Project Structure

```
acl-ghostfix/
├── main.py              # entire application (GUI + logic)
├── requirements.txt
├── LICENSE               # GPLv3
├── CONTRIBUTING.md
└── .gitignore
```

> Note: `acl_config.json` (created at runtime in `C:\ACL-GhostFix\`) stores your
> local settings, including Earthdata credentials if you choose to save them. It is
> **never** committed to this repo — see `.gitignore`. Do not share this file.

---

## 🤝 Contributing

Contributions are very welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for
guidelines. Some ideas if you're looking for where to start:

- Linux/macOS support (replace `os.startfile`, shell-based subprocess calls)
- Additional RINEX mirrors / better Earthdata OAuth flow
- Multi-constellation support (GLONASS, Galileo, BeiDou) via gps-sdr-sim's options
- More language translations
- Waveform/spectrum preview before transmission

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0** — see
[LICENSE](LICENSE) for details. In short: you're free to use, study, modify, and
redistribute this software, but any modified version you distribute must also be
open-sourced under GPLv3. This keeps the project and its derivatives open for the
whole RF security community.

---

## 🙏 Credits

- [gps-sdr-sim](https://github.com/osqzss/gps-sdr-sim) by osqzss — the GNSS signal
  generation engine this tool wraps
- [HackRF](https://github.com/greatscottgadgets/hackrf) by Great Scott Gadgets
- Built and maintained by **ACL Labs**
