from bs4 import BeautifulSoup
import requests
import json


""" Web scraping with Beautifulsoup to get the data and save as Json file """

url = 'https://www.ufc.com/rankings'
data = requests.get(url)

html = BeautifulSoup(data.text, 'html.parser')
content = html.select('.view-grouping')

ufc_data = []


for el in content[:-1]:
    temp_dict = {'fighters': []}
    weight_class = el.select('.view-grouping-header')[0].get_text()
    temp_dict['weight_class'] = weight_class
    grouping_content = el.select('.view-grouping-content')[0]
    table = grouping_content.select('table')

    # Todo: champions
    table_caption = table[0].select('caption')
    champion = table_caption[0].select('a')[0].get_text()
    champion_a = table_caption[0].select('a')
    soup1 = BeautifulSoup(str(champion_a), 'html.parser')
    elem = soup1.find(href=True)
    champion_url = f"https://www.ufc.com/{elem['href']}"
    data2 = requests.get(champion_url)

    soup2 = BeautifulSoup(data2.text, 'html.parser')
    champ_nickname = None
    champ_record = soup2.select('.tz-change-inner')[0].get_text()
    champ_record = champ_record[champ_record.index("•") + 1:].strip()
    champ_img = table_caption[0].select('img')[0]
    champ_img_src = champ_img['src']

    try:
        champ_nickname = soup2.select('.field-name-nickname')[0].get_text()
        champ_nickname = champ_nickname[1:-1]
    except:
        print('nickname not found')

    temp_dict['fighters'].append({'athlete': champion,
                                  'rank': 0, 'img_src': champ_img_src,
                                  'champion': True,

                                  'record': champ_record, 'nickname': champ_nickname})

    # Todo:  fighters
    table_tr = table[0].select('tr')
    for tr in list(table_tr):
        fighter_rank = tr.select('td.views-field-weight-class-rank')[0].get_text()
        fighter_name = tr.select('a')[0].get_text()
        fighter_link = tr.select('a')[0]['href']
        fighter_url = f"https://www.ufc.com/{fighter_link}"
        data3 = requests.get(fighter_url)
        soup3 = BeautifulSoup(data3.text, 'html.parser')
        fighter_nickname = None
        fighter_record = soup3.select('.tz-change-inner')[0].get_text()
        fighter_record = fighter_record[fighter_record.index("•") + 1:].strip()
        fighter_img_src = "#"

        try:
            fighter_nickname = soup3.select('.field-name-nickname')[0].get_text()
            fighter_nickname = fighter_nickname[1:-1]
        except:
            print('nickname not found')

        temp_dict['fighters'].append({'athlete': fighter_name,
                                      'rank': fighter_rank,
                                      'img_src': fighter_img_src,
                                      'champion': False,
                                      'record': fighter_record,
                                      'nickname': fighter_nickname})

    print("*" * 50)

    ufc_data.append(temp_dict)


# new_ufc_data = json.dumps(ufc_data, indent=4)

# Todo: save the data to a json file for later imports
with open('ufc_data.json', 'w') as f:
    json.dump(ufc_data, f, indent=4)
