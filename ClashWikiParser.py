from time import time
from ScraperTools import scraper_tool as st
from ExcelWriter import compile_sheets


def clean(string):
    string = string.strip()
    string = string.replace("\n", "")
    string = " ".join(string.split())
    return string


def validate_header(headers):

    check_inferno_tower = any(header in headers for header in
                              ["Initial", "After 1.5s", "After 5.25s"])
    if check_inferno_tower is True:
        index_DPS = headers.index("Damage per Second")
        del headers[index_DPS], headers[-3:]

        headers.insert(index_DPS, "After 5.25s")
        headers.insert(index_DPS, "After 1.5s")
        headers.insert(index_DPS, "Initial")

    col = ord("A")
    for index, header in enumerate(headers):
        if headers.count(header) > 1:
            headers[index] = header + "_" + chr(col)
            col += 1

    return headers


def parse_clash_wiki(*, website,  file_name):
    my_html = website.get_html(update_cache=False)
    data = my_html.findAll("table", {"class": "wikitable mode-toggle-mode-1"})
    invalid_length = len(data) == 0 or len(data) == 1
    tables = my_html.findAll("table", {"class": "wikitable"}) if invalid_length else data
    for table in tables:
        headers = list(map(lambda x: clean(x.text), table.findAll("th")))

        if "Level" not in headers:
            continue
        elif "Builder Hall Level Required" in headers:
            continue

        headers = validate_header(headers)

        column_size = len(headers)
        table_values = table.findAll("td")
        table_length = int(len(table_values)/column_size)
        table_rows = []

        for start_ind in range(table_length):
            start_ind *= column_size
            end_ind = start_ind + column_size
            table_row = table_values[start_ind:end_ind]
            table_row = list(map(lambda x: clean(x.text), table_row))
            table_rows.append(dict(zip(headers, table_row)))

        website.write_toCSV(file_name, *table_rows)


if __name__ == '__main__':
    query = {
        "Defences":         ["Archer_Tower", "Cannon", "Mortar", "Wizard_Tower",
                             "Air_Sweeper", "Air_Defense", "Inferno_Tower", "Bomb_Tower",
                             "Eagle_Artillery", "X-Bow", "Hidden_Tesla", "Giga_Tesla",
                             "Giga_Inferno", "Scattershot", "Walls",
                             ],

        "Elixer":           ["Archer", "Barbarian", "Goblin", "Giant",
                             "Balloon", "Wall Breaker", "Wizard", "Healer",
                             "Baby Dragon", "Dragon", "P.E.K.K.A", "Miner",
                             "Electro Dragon", "Yeti",
                             ],

        "Dark Elixer":      ["Minion", "Hog Rider", "Valkyrie", "Golem",
                             "Witch", "Lava Hound", "Bowler", "Ice_Golem",
                             "Headhunter",
                             ],

        "Spells":           ["Lightning Spell", "Healing Spell", "Rage_Spell",
                             "Jump_Spell", "Freeze_Spell", "Clone_Spell",
                             ],

        "Dark Spells":      ["Poison_Spell", "Earthquake_Spell", "Haste_Spell",
                             "Skeleton_Spell", "Bat_Spell",
                             ],
    }

    start_time = time()
    for type in query:
        for item in query[type]:
            item = item.strip()
            url = f"https://clashofclans.fandom.com/wiki/{item}"
            print("url", url)
            website = st(url)
            parse_clash_wiki(website=website, file_name=(type+"-"+item))
    for type in query:
        website.group_files(type)
    compile_sheets()

    print(f"Compete! Took: {round(time()-start_time, 2)}s")
