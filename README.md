# petrosmart-tools

Educational engineering calculators published by PetroSmart Academy. Each page is a self-contained HTML file.

These tools give screening estimates. They do not replace a design calculation checked against the applicable code, standard or laboratory data.

## Validation

Reference cases are in `tests/`. Run them with Node.js 18 or later:

```
sh tests/run_all.sh
```

Each test loads the calculation code of a page and compares it with a published equation, a textbook chart value or an independent recomputation. `test_syntax.js` checks that every script on every page parses.

## Sources used by the corrected calculators

| Calculator | Main references |
|---|---|
| Drilling hydraulics | Bourgoyne, Millheim, Chenevert and Young, Applied Drilling Engineering, SPE Textbook Series vol. 2 (1986), chapter 4 |
| Cementing | absolute volume method; API Spec 10A water ratios; API RP 10B-2 test methods |
| Pipe wall thickness | ASME B31.3 (eq. 3a, para. 302.3.2), ASME B36.10M, ASME B16.5 Group 1.1 ratings |
| Corrosion rate | de Waard, Lotz and Milliams, Corrosion 47(12), 1991; API RP 14E; NACE SP0775; ISO 15156-2; API 570 |
| Reservoir fluid PVT | Standing (1947); Vasquez and Beggs (1980); Al-Marhoun (1988); Glaso (1980); Beal (1946); Chew and Connally (1959); Hall and Yarborough (1973); Lee, Gonzalez and Eakin (1966); McCain (1990) |
| Pipeline pressure drop | general flow equation, Weymouth and Panhandle A as given by Menon, Gas Pipeline Hydraulics (2005); Colebrook-White |
| Well productivity (gas) | Dranchuk and Abou-Kassem (1975); Sutton (1985); Al-Hussainy, Ramey and Crawford (1966) |
| Heat exchanger | Bowman, Mueller and Nagle (1940) LMTD correction factor |
| Hydrogen cost | IEA, The Future of Hydrogen (2019) for SMR gas use |

## Change log

17 October 2026: correction of the errors listed in the audit of the same date (unit inversions, unit mismatches, mis-transcribed correlations, invented advisory rules). Inputs equal to 0 are no longer replaced by the default value. Emojis and long dashes removed. See the commit history for the detail per calculator.
