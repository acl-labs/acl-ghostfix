# Contributing to ACL GhostFix

Thanks for considering a contribution — this project only gets better with more
people working on it, the same way tools like
[HackRF Mayhem](https://github.com/portapack-mayhem/mayhem-firmware) grew through
community contributions.

## Ground rules

- Be respectful in issues and PRs.
- This is an RF security research tool — please don't submit features whose only
  purpose is to make unauthorized transmission easier or to evade detection systems.
  Defensive/research-oriented features are always welcome.
- Keep the legal disclaimer in the README intact in any fork/derivative.

## How to contribute

1. **Fork** the repo and create your branch from `main`:
   ```bash
   git checkout -b feature/my-improvement
   ```
2. Make your changes. Try to keep the existing code style (the file is organized
   into clear sections: config/RINEX logic, `SmartLocationFinder`, `SettingsWindow`,
   main app class).
3. Test locally:
   - Does the app still launch without a HackRF connected? (it should degrade
     gracefully and just show a warning in the terminal log)
   - Does it still launch without `gps-sdr-sim.exe` configured? (auto-discovery /
     manual fallback should still work)
   - If you touched RINEX download logic, test with **and without** Earthdata
     credentials configured.
4. Commit with a clear message (`git commit -m "Add: Galileo constellation support"`).
5. Push and open a **Pull Request** against `main`, describing:
   - What problem it solves / what it adds
   - How you tested it
   - Any new dependencies introduced

## Reporting bugs

Open an issue with:
- Your OS / Python version
- Steps to reproduce
- The relevant lines from the terminal log panel (color-coded errors are usually
  the fastest way to diagnose RINEX/HackRF issues)

## Feature ideas welcome, especially:

- Linux/macOS compatibility
- New RINEX mirror sources or improved Earthdata OAuth handling
- Multi-GNSS constellation support (GLONASS / Galileo / BeiDou)
- UI/UX polish, additional language translations
- Signal preview / spectrum visualization before transmission

If you're not sure whether an idea fits, open an issue first to discuss before
investing time in a PR.
