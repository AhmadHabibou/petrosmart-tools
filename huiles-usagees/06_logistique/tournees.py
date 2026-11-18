"""Lot 6 : optimisation des tournees forestieres (OR-Tools, probleme de tournees avec capacite)
et cout complet par litre selon l'option de flotte, en saison seche et en saison des pluies.

Distances : graphe routier construit sur des distances routieres publiees [S-75] et des distances
a vol d'oiseau [S-76] corrigees par un coefficient de detour cale sur deux paires sourcees (H-120).
Le reseau de travail bloque OpenStreetMap : `matrice_osrm()` permet de remplacer ce graphe par
une matrice OSRM des que l'acces est ouvert.

Sortie : 06_logistique/tournees.md
"""
from pathlib import Path
import itertools
import math
import sys

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.hypotheses import val  # noqa: E402
from commun.format import nombre, pct  # noqa: E402

from ortools.constraint_solver import pywrapcp, routing_enums_pb2  # noqa: E402

CAPACITE_CITERNE_L = 13_390  # IVECO Eurocargo 190EL28 [S-29]
GASOIL_FCFA_L = 828          # [S-09]

# Distances routieres publiees (km) [S-75]
ROUTE = {("Yaoundé", "Bertoua"): 333, ("Douala", "Bertoua"): 572}
# Distances a vol d'oiseau depuis Bertoua (km) [S-76]
VOL = {("Bertoua", "Batouri"): 77, ("Bertoua", "Abong-Mbang"): 86, ("Bertoua", "Yokadouma"): 192,
       ("Bertoua", "Yaoundé"): 253, ("Bertoua", "Douala"): 445}

# Repartition supposee des 15 clients forestiers de l'annee 5 (H-97 central) par ville de reference
REPARTITION = {"Bertoua": 4, "Batouri": 4, "Abong-Mbang": 3, "Yokadouma": 4}


def coefficient_detour_calibre():
    return (ROUTE[("Yaoundé", "Bertoua")] / VOL[("Bertoua", "Yaoundé")] + ROUTE[("Douala", "Bertoua")] / VOL[("Bertoua", "Douala")]) / 2


def graphe(cas="central"):
    k = val("H-120", cas)
    g = {("Yaoundé", "Bertoua"): ROUTE[("Yaoundé", "Bertoua")],
         ("Douala", "Yaoundé"): ROUTE[("Douala", "Bertoua")] - ROUTE[("Yaoundé", "Bertoua")]}  # itineraire par Yaounde
    for (a, b), d in VOL.items():
        if b in ("Batouri", "Abong-Mbang", "Yokadouma"):
            g[(a, b)] = d * k
    noeuds = sorted({x for e in g for x in e})
    dist = {(a, b): (0 if a == b else math.inf) for a in noeuds for b in noeuds}
    for (a, b), d in g.items():
        dist[(a, b)] = dist[(b, a)] = d
    for m, a, b in itertools.product(noeuds, noeuds, noeuds):  # Floyd-Warshall
        if dist[(a, m)] + dist[(m, b)] < dist[(a, b)]:
            dist[(a, b)] = dist[(a, m)] + dist[(m, b)]
    return dist


def matrice_osrm(coords):
    """Remplacement prevu : matrice de distances routieres OSRM (non appele, reseau bloque)."""
    raise NotImplementedError("Acces a router.project-osrm.org bloque dans l'environnement de travail")


def instance(cas="central"):
    dist = graphe(cas)
    piste = val("H-121", cas)
    sites = [("Douala", None)] + [(v, i) for v, n in REPARTITION.items() for i in range(n)]
    n = len(sites)
    route_km = [[0.0] * n for _ in range(n)]
    piste_km = [[0.0] * n for _ in range(n)]
    for i, (vi, _) in enumerate(sites):
        for j, (vj, _) in enumerate(sites):
            if i == j:
                continue
            route_km[i][j] = dist[(vi, vj)]
            piste_km[i][j] = (piste if i > 0 else 0) + (piste if j > 0 else 0)
    return sites, route_km, piste_km


def resoudre(cas="central"):
    sites, rk, pk = instance(cas)
    n = len(sites)
    vol_site = val("H-01") / val("H-88")
    demande = [0] + [int(vol_site)] * (n - 1)
    nb_vehicules = n - 1
    gestion = pywrapcp.RoutingIndexManager(n, nb_vehicules, 0)
    routage = pywrapcp.RoutingModel(gestion)

    def cout(i, j):
        a, b = gestion.IndexToNode(i), gestion.IndexToNode(j)
        return int(round(rk[a][b] + pk[a][b]))

    cb = routage.RegisterTransitCallback(cout)
    routage.SetArcCostEvaluatorOfAllVehicles(cb)
    dem = routage.RegisterUnaryTransitCallback(lambda i: demande[gestion.IndexToNode(i)])
    routage.AddDimensionWithVehicleCapacity(dem, 0, [CAPACITE_CITERNE_L] * nb_vehicules, True, "Capacite")
    p = pywrapcp.DefaultRoutingSearchParameters()
    p.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    p.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    p.time_limit.seconds = 5
    sol = routage.SolveWithParameters(p)
    tournees = []
    for v in range(nb_vehicules):
        i = routage.Start(v)
        chemin = []
        while not routage.IsEnd(i):
            chemin.append(gestion.IndexToNode(i))
            i = sol.Value(routage.NextVar(i))
        chemin.append(0)
        if len(chemin) > 2:
            km_r = sum(rk[a][b] for a, b in zip(chemin, chemin[1:]))
            km_p = sum(pk[a][b] for a, b in zip(chemin, chemin[1:]))
            tournees.append(dict(sites=[sites[k][0] for k in chemin[1:-1]], km_route=km_r, km_piste=km_p,
                                 nb_sites=len(chemin) - 2, litres=(len(chemin) - 2) * vol_site))
    return tournees


def jours(t, saison, cas="central"):
    v_piste = val("H-123", cas) * (val("H-124", cas) if saison == "pluies" else 1)
    heures = t["km_route"] / val("H-122", cas) + t["km_piste"] / v_piste + t["nb_sites"] * val("H-125", cas)
    return math.ceil(heures / val("H-126", cas))


def couts_par_litre(saison, cas="central"):
    """Cout complet par litre collecte en foret, par option de flotte, sur une annee (H-88 cycles)."""
    tours = resoudre(cas)
    cycles = val("H-88", cas)
    km = sum(t["km_route"] + t["km_piste"] for t in tours) * cycles
    nb_jours = sum(jours(t, saison, cas) for t in tours) * cycles
    litres = sum(t["litres"] for t in tours) * cycles
    carburant = km * val("H-127", cas) / 100 * GASOIL_FCFA_L
    entretien = km * val("H-128", cas)
    equipage = nb_jours * val("H-129", cas)
    duree = val("H-132", cas)
    fixe_neuf = val("H-130", cas) / duree + val("H-133", cas)
    fixe_occ = val("H-131", cas) / (duree / 2) + val("H-133", cas)
    options = {
        "Achat neuf (coûts fixes imputés à 100 % à la forêt)": carburant + entretien + equipage + fixe_neuf,
        "Achat d'occasion (coûts fixes imputés à 100 % à la forêt)": carburant + entretien * val("H-138", cas) + equipage + fixe_occ,
        "Location avec chauffeur (carburant en sus)": nb_jours * val("H-134", cas) + carburant,
        "Sous-traitance à un collecteur agréé (H-48 par enlèvement)": len([s for t in tours for s in t["sites"]]) * cycles * val("H-48", cas),
    }
    return {k: v / litres for k, v in options.items()}, dict(km=km, jours=nb_jours, litres=litres, tours=tours)


def cout_urbain_par_litre(cas="central"):
    litres_jour = val("H-135", cas) * val("H-136", cas)
    jour = val("H-137", cas) * (val("H-127", cas) / 100 * GASOIL_FCFA_L + val("H-128", cas)) + val("H-129", cas)
    return jour / litres_jour, litres_jour


def rapport():
    k_cal = coefficient_detour_calibre()
    out = ["# Tournées et coût complet par litre", "",
           "Fichier généré par `06_logistique/tournees.py` (OR-Tools, problème de tournées avec capacité). Statut : supposé (H-48, H-01, H-88, H-120 à H-138), distances partiellement sourcées.", "",
           "## Réseau", "",
           f"- Coefficient de détour calé sur deux paires sourcées : {nombre(k_cal, 2)} (Yaoundé-Bertoua et Douala-Bertoua [S-75][S-76]) ; valeur retenue H-120 : {nombre(val('H-120'), 2)}.",
           "- Douala-Yaoundé est déduit de Douala-Bertoua moins Yaoundé-Bertoua, en supposant l'itinéraire par Yaoundé : "
           f"{nombre(graphe()[('Douala', 'Yaoundé')])} km.",
           f"- Dépôt et déchargement : Douala, où sont situés les collecteurs et éliminateurs identifiés [S-06][S-07]. Capacité de la citerne : {nombre(CAPACITE_CITERNE_L)} L [S-29].",
           f"- Clients : {sum(REPARTITION.values())} sites forestiers (H-97 central), répartis de manière supposée : "
           + ", ".join(f"{v} {n}" for v, n in REPARTITION.items()) + f" ; {nombre(val('H-121'))} km de piste par site (H-121) ; "
           f"{nombre(val('H-01') / val('H-88'))} L par enlèvement.", "",
           "## Tournées optimisées (un cycle d'enlèvement, scénario central)", "",
           "| Tournée | Sites | km route | km piste | Litres | Jours saison sèche | Jours saison des pluies |",
           "|---|---|---:|---:|---:|---:|---:|"]
    tours = resoudre()
    for i, t in enumerate(tours, 1):
        out.append(f"| {i} | {', '.join(t['sites'])} | {nombre(t['km_route'])} | {nombre(t['km_piste'])} | {nombre(t['litres'])} | "
                   f"{jours(t, 'seche')} | {jours(t, 'pluies')} |")
    out += ["", "## Coût complet par litre collecté en forêt (FCFA/L)", "",
            "| Option de flotte | Saison sèche | Saison des pluies |", "|---|---:|---:|"]
    sec, info = couts_par_litre("seche")
    plu, info_p = couts_par_litre("pluies")
    for k in sec:
        out.append(f"| {k} | {nombre(sec[k])} | {nombre(plu[k])} |")
    out += ["", f"Base annuelle : {nombre(info['km'])} km, {nombre(info['jours'])} jours d'équipage en saison sèche "
            f"({nombre(info_p['jours'])} en saison des pluies), {nombre(info['litres'])} L collectés par an.",
            "Les coûts fixes d'un camion possédé sont imputés en totalité à la forêt : ils baissent si le camion sert aussi à la collecte urbaine.", "",
            "## Collecte urbaine (Douala ou Yaoundé)", ""]
    cu, lj = cout_urbain_par_litre()
    out += [f"Coût variable par litre (carburant, entretien, équipage, hors coûts fixes du véhicule) : {nombre(cu)} FCFA/L pour {nombre(lj)} L collectés par jour (H-135 à H-137). "
            f"La valeur de travail H-85 du lot 8 était de {nombre(val('H-85'))} FCFA/L.", ""]
    best = min(sec, key=sec.get)
    out += [f"Option la moins chère en saison sèche : {best}.", ""]
    return "\n".join(out) + "\n", sec, plu


if __name__ == "__main__":
    t, s, p = rapport()
    Path(__file__).with_name("tournees.md").write_text(t, encoding="utf-8")
    print("Lot 6 : couts par litre (seche)", {k[:12]: round(v) for k, v in s.items()})
