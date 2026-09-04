# Entwicklung und Release

Für Beiträge gilt [CONTRIBUTING.md](../CONTRIBUTING.md), für die Entwicklerarbeit am Skill [WARP.md](../WARP.md). Hier stehen der Verify-Lauf und die Release-Regel.

Für lokale Release-Prüfung:

```bash
make verify
```

Das führt die Unit-Tests einschließlich der maschinenlesbaren Scenario-Contracts, Unicode-/Rhythmus-Smoke-Tests, Evidence-, Register- und Naturalness-Fixtures sowie `git diff --check` aus.

Einzelchecks, Detection-Snapshot, Exit-Codes und das Evidence-Gate einzeln: [pruefskripte.md](pruefskripte.md#einzelchecks).

## Release-Regel

Der Abschnitt **Was ist neu?** zeigt die aktuelle Version und ältere Minor-Reihen als
Meilensteine. Ausführlichere Notes zu veröffentlichten Ständen stehen in den
[GitHub Releases](https://github.com/marmbiz/humanizer-de/releases).

Bei jedem Version-Bump:

1. Version und Changelog synchronisieren.
2. `make verify` ausführen.
3. Änderungen auf `main` bringen, per direktem Push oder Pull Request, und den CI-Lauf auf
   `main` mit `gh run list` prüfen.
4. Erst nach grüner CI den Tag `vX.Y.Z` auf den neuesten Commit setzen und pushen.
5. `make skill-bundle` ausführen und das GitHub Release aus dem Tag mit
   `dist/humanizer-de.zip` als Asset erstellen. Das Asset muss beim Anlegen dabei sein, weil
   Releases danach versiegelt sind. Die Release Notes konkretisieren die Changelog-Zeile,
   behaupten aber keinen breiteren Scope.

Im README bleibt nur die aktuelle Version einzeln stehen. Ältere Releases werden nach
Minor-Reihe zusammengefasst. Jeder veröffentlichte Stand behält trotzdem seinen Tag und
GitHub Release.
