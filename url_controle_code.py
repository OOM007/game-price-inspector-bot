import requests
from bs4 import BeautifulSoup

def find_games(name):
    urlname = name
    urlname = urlname.replace(" ", "+")
    url = "https://store.steampowered.com/search/?term={0}".format(urlname)
    print(url)
    payload = {'method': 'getQuote', 'format': 'lxml', 'lang': 'en'}
    r = requests.get(url, params=payload)
    game_list = []
    urlcode = r.text

    soup = BeautifulSoup(urlcode, 'lxml')
    games = soup.find('div', class_="search_results").findAll('span', class_='title')
    gameListLen = len(games)

    print("game list lenght: ", gameListLen)
    if gameListLen >= 10:
        gameListLen = 10
    else:
        pass

    if games == []:
        game_list.append(None)
    else:
        for x in range(0, gameListLen):
            need_game = games[x].text
            game_list.append(need_game)

    return game_list

def get_id(code, num_in_list):
    urlname = code
    urlname = urlname.replace(" ", "+")
    url = "https://store.steampowered.com/search/?term={0}".format(urlname)
    print(url)
    payload = {'method': 'getQuote', 'format': 'lxml', 'lang': 'en'}
    r = requests.get(url, params=payload)
    urlcode = r.text

    soup = BeautifulSoup(urlcode, 'lxml')

    warning_lbl = soup.find('div', class_='search_results_filtered_warning')
    print(warning_lbl)

    if warning_lbl == None:
        game_id = soup.find('div', class_="search_results").find_all('a')[num_in_list].get('data-ds-appid')
    else:
        game_id = soup.find('div', class_="search_results").find_all('a')[num_in_list].get('data-ds-appid')#num_in_list+1 if need

    return game_id

finds = 0

def get_data(game_id):
    global finds
    print("Game id: ",game_id)
    url = "https://store.steampowered.com/app/{0}".format(game_id)
    payload = {'method': 'getQuote', 'format': 'lxml', 'lang': 'en'}

    r = requests.get(url, params=payload)
    urlcode = r.text

    game_data = []

    soup = BeautifulSoup(urlcode, 'lxml')

    page_name = soup.find('div', class_='apphub_HomeHeaderContent').find('div', class_='apphub_AppName').text
    all_propose = soup.find('div', class_='game_area_purchase').find_all('div', class_='game_area_purchase_game_wrapper')
    #print(all_propose)
    print(page_name)
    page_name = page_name.replace(" ", "")
    page_name = page_name.replace(":", "")
    page_name.replace("-", "")

    for x in range(0, len(all_propose)):
        print(finds)
        var = soup.find('div', class_='game_area_purchase').find_all('h1')[x].text
        var = var.replace("Buy", "")
        var = var.replace(" ", "")
        var = var.replace(':', '')
        var = var.replace('-', '')

        print(var)

        discount = soup.find_all('div', class_='game_area_purchase_game_wrapper')[x].find('div', class_='discount_pct')

        print(page_name)

        if discount == None and finds == 0:
            print('work')
            if var == page_name:
                print("lap number: ", x)
                print("discount none, work")
                ndata = soup.find_all('div', class_='game_area_purchase_game_wrapper')[x].find('div', class_='game_purchase_action_bg').text
                ndata = ndata.replace('\n', '')
                ndata = ndata.replace('\t', '')
                ndata = ndata.replace('\r', '')
                ndata = ndata.replace('Add to Cart', '')

                game_data.append(ndata)
                finds = 1
                print(finds)
                break
            else:
                pass
        else:
            if finds == 0:
                print("work discount")
                if var == page_name:
                    game_data.append(discount.text)
                    game_data.append(soup.find('div', class_='game_area_purchase').find_all('div', class_='discount_original_price')[x].text)
                    game_data.append(soup.find('div', class_='game_area_purchase').find_all('div', class_='discount_final_price')[x].text)
                    finds = 1
                    break
                else:
                    pass

    finds = 0
    #game_data = game_data.replace('\n', '')
    #game_data = game_data.replace('Add to Cart', '')

    return game_data

#print(get_data(294100))
#print(get_id("farming", 0))
#print(find_games("counter strice"))