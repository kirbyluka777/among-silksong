from . import teams
from . import countries
from . import details
from . import expeditions

def search_c() -> bool:
    entries = ""
    for expedition in expeditions.read_expeditions():
        team_names = [expedition.team_name_1, expedition.team_name_2]
        for i in range(0, 2, +1):
            team = teams.search_team_by_name(team_names[i])
            country = countries.search_country_by_code(team.country_code)
            km_total = details.get_total_km_from_expedition(expedition.id, i)
            if km_total > 0:
                km_total_sort = str(km_total).rjust(20, "0")
                entries += f"{km_total_sort:<20}{expedition.id:<8} | {team.name:<20} | {country.name:<20} | {km_total*1000:>12} km\n"
    entries = quicksort(entries.split("\n"))

    file = open('reports/Reporte_c.txt', 'w', encoding="utf-8")

    dash = "-"
    headers = ["VIAJE", "EQUIPO", "PAÍS", "TOTAL KM"]
    file.write(f"REPORTE: TOP 10\n"
               f"{dash*72}\n"
               f"{headers[0]:<8} | {headers[1]:<20} | {headers[2]:<20} | {headers[3]:<15}\n"
               f"{dash*72}\n")
    
    base_index = len(entries) - 1
    for i in range(0, min(10, len(entries)), +1):
        entry = entries[base_index - i][20:]
        file.write(f"{entry}\n")
    
    file.close()

    return True

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quicksort(left) + [pivot] + quicksort(right)