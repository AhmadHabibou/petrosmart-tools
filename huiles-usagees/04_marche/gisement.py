"""Lot 4 : estimation du gisement d'huiles usagees par trois methodes, et part de marche necessaire.

Sortie : 04_marche/gisement.md. Valeurs sourcees : constantes ci-dessous avec [S-xx] ;
valeurs supposees : commun/hypotheses.py.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from commun.hypotheses import val  # noqa: E402
from commun.format import nombre, pct  # noqa: E402

# Donnees sourcees
GISEMENT_ETUDE_T = 70_000          # t/an [S-01]
PART_REGENEREE_ETUDE = 0.64        # [S-01], source primaire inconnue (Q-12)
AFS_LUB_VENDU_L = 350e6            # L/an, Afrique du Sud [S-40]
AFS_HUILE_USAGEE_L = 150e6         # L/an [S-40]
AFS_COLLECTABLE_L = 120e6          # L/an [S-40]
NGA_HUILE_USAGEE_L = 150e6         # L/an, Nigeria [S-50]
PARC_2014 = 675_000                # vehicules [S-43]
ENGINS_CAT_SEM = 6_500             # machines CAT et SEM suivies au Cameroun [S-19]
SEUIL_VAN_NULLE_URBAIN_L = 320_000 # L/an, premier business plan [S-29]
GASOIL_POMPE = 828                 # FCFA/L, novembre 2026 [S-09]
GASOIL_IMPORT = 984.46             # FCFA/L, grille novembre 2026, depot de Douala-Bonaberi [S-09]
IMPORT_MOYEN_T = 389_917           # FCFA/t, carburants et lubrifiants importes, moyenne 2025 [S-63]
PRIX_BP = 400                      # FCFA/L, H-04
SEUIL_PRIX_VAN_NULLE = 250         # FCFA/L [S-29]

CAS = ("bas", "central", "haut")


def methode_parc(cas):
    routier = PARC_2014 * val("H-63", cas) * val("H-61", cas)
    engins = ENGINS_CAT_SEM * val("H-62", cas)
    return routier, engins


def methode_etude_l(cas):
    return GISEMENT_ETUDE_T * 1000 / val("H-60", cas)


def lubrifiant_implicite_t(cas):
    """Consommation de lubrifiants qu'impliquerait le chiffre de 70 000 t, avec le ratio sud-africain."""
    ratio = AFS_HUILE_USAGEE_L / AFS_LUB_VENDU_L
    return GISEMENT_ETUDE_T / ratio


def foret_l(cas):
    return val("H-64", cas) * val("H-01", cas)


def urbain_douala_yaounde_l(cas):
    routier, _ = methode_parc(cas)
    return routier * val("H-65", cas)


def resultats():
    r = {}
    for c in CAS:
        routier, engins = methode_parc(c)
        r[c] = dict(parc_routier=routier, parc_engins=engins, parc_total=routier + engins,
                    etude=methode_etude_l(c), foret=foret_l(c), urbain_dy=urbain_douala_yaounde_l(c))
    return r


def _m(x):
    return nombre(x / 1e6, 1)


def rapport():
    r = resultats()
    rc = r["central"]
    out = ["# Gisement d'huiles usagées : trois méthodes", "",
           "Fichier généré par `04_marche/gisement.py`. Volumes en millions de litres par an (M L/an). Statut : supposé sauf mention.", "",
           "## Comparaison des méthodes", "",
           "| Méthode | Bas | Central | Haut | Données |", "|---|---:|---:|---:|---|"]
    out.append(f"| 1. Ventes de lubrifiants | non calculable | non calculable | non calculable | aucune statistique de ventes ou d'importations de lubrifiants seuls trouvée (Q-25) |")
    out.append(f"| 2. Parc : véhicules routiers | {_m(r['bas']['parc_routier'])} | {_m(rc['parc_routier'])} | {_m(r['haut']['parc_routier'])} | 675 000 véhicules en 2014 [S-43], H-63, H-61 |")
    out.append(f"| 2. Parc : engins CAT et SEM seuls (minorant des engins) | {_m(r['bas']['parc_engins'])} | {_m(rc['parc_engins'])} | {_m(r['haut']['parc_engins'])} | 6 500 machines [S-19], H-62 |")
    out.append(f"| **2. Parc : total** | **{_m(r['bas']['parc_total'])}** | **{_m(rc['parc_total'])}** | **{_m(r['haut']['parc_total'])}** | |")
    out.append(f"| 3. Étude existante (70 000 t/an) | {_m(r['bas']['etude'])} | {_m(rc['etude'])} | {_m(r['haut']['etude'])} | [S-01], conversion par H-60 |")
    ecart = rc["etude"] / rc["parc_total"]
    out += ["", f"En cas central, le chiffre de l'étude [S-01] vaut {nombre(ecart, 1)} fois l'estimation par le parc.", "",
            "## Tests de cohérence", "",
            f"- Pour produire 70 000 t d'huiles usagées avec le ratio sud-africain (150 M L d'huile usagée pour 350 M L de lubrifiants vendus [S-40]), "
            f"le Cameroun devrait consommer environ {nombre(lubrifiant_implicite_t('central'))} t de lubrifiants par an. Ce chiffre n'a pu être confronté à aucune statistique camerounaise (Q-25).",
            f"- 70 000 t représentent {_m(rc['etude'])} M L/an, soit {pct(rc['etude'] / AFS_HUILE_USAGEE_L)} du volume d'huiles usagées de l'Afrique du Sud [S-40] "
            f"et {pct(rc['etude'] / NGA_HUILE_USAGEE_L)} de celui estimé pour le Nigeria [S-50].",
            "- Conclusion : le chiffre de 70 000 t/an est probablement surestimé, ou couvre d'autres huiles (industrielles, pétrolières, maritimes). Certitude : probable. Le business plan ne doit pas s'appuyer dessus.", "",
            "## Segments utiles au projet", "",
            "| Segment | Bas | Central | Haut | Données |", "|---|---:|---:|---:|---|",
            f"| Forêt et UTB (clients adressables x volume par client) | {_m(r['bas']['foret'])} | {_m(rc['foret'])} | {_m(r['haut']['foret'])} | H-64, H-01 |",
            f"| Parc routier de Douala et Yaoundé | {_m(r['bas']['urbain_dy'])} | {_m(rc['urbain_dy'])} | {_m(r['haut']['urbain_dy'])} | méthode 2, H-65 |", "",
            "## Part de marché nécessaire en zone urbaine", "",
            "| Objectif | Volume (M L/an) | Part du gisement urbain Douala et Yaoundé, cas bas | central | haut |",
            "|---|---:|---:|---:|---:|"]
    for lib, v in (("Collecte urbaine du premier business plan en année 5 (H-02)", val("H-02")),
                   ("Seuil de VAN nulle du premier business plan [S-29]", SEUIL_VAN_NULLE_URBAIN_L)):
        out.append(f"| {lib} | {_m(v)} | {pct(v / r['bas']['urbain_dy'])} | {pct(v / rc['urbain_dy'])} | {pct(v / r['haut']['urbain_dy'])} |")
    out += ["", "Une part supérieure à 20 % du gisement des deux villes, face à un circuit informel installé et à des collecteurs agréés, est jugée irréaliste à 5 ans par le chef de projet (seuil de décision, pas une donnée).", ""]
    out += ["", "## Prix de référence du combustible", "",
            "| Référence | FCFA/L | Source |", "|---|---:|---|",
            f"| Gasoil à la pompe, Douala | {nombre(GASOIL_POMPE)} | [S-09] |",
            f"| Coût d'importation du gasoil, novembre 2026 | {nombre(GASOIL_IMPORT)} | [S-09] |",
            f"| Prix moyen des carburants et lubrifiants importés en 2025, converti (cas bas, central, haut de H-66) | "
            f"{nombre(IMPORT_MOYEN_T / 1000 * val('H-66', 'bas'))} ; {nombre(IMPORT_MOYEN_T / 1000 * val('H-66'))} ; {nombre(IMPORT_MOYEN_T / 1000 * val('H-66', 'haut'))} | [S-63], H-66 |",
            f"| Prix de vente du combustible retenu par le premier business plan | {nombre(PRIX_BP)} | H-04 |",
            f"| Seuil de VAN nulle du premier business plan | {nombre(SEUIL_PRIX_VAN_NULLE)} | [S-29] |", "",
            f"Le prix du premier business plan représente {pct(PRIX_BP / GASOIL_POMPE)} du prix du gasoil à la pompe. "
            "Aucun prix du fioul lourd industriel n'a été trouvé : c'est la référence pertinente pour un acheteur équipé d'un brûleur à fioul (Q-29).", ""]
    return "\n".join(out) + "\n", r


if __name__ == "__main__":
    texte, r = rapport()
    Path(__file__).with_name("gisement.md").write_text(texte, encoding="utf-8")
    print("Lot 4 : gisement parc central (M L)", round(r["central"]["parc_total"] / 1e6, 1))
