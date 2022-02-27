import csv
import requests
import json
import time
import os

url = 'https://www.instagram.com/graphql/query/'
short_code = input('enter your source code: ')

end_crusor = ''
count = 0
start_file = 1
per_file = 10000

try:
    os.mkdir('resultfile')
except FileExistsError:
    pass

# create csv file
writer = csv.writer(open(f'resultfile/{short_code} {start_file}.csv', 'w', newline=''))
headers = ['Username', 'Full Name', 'private account', 'Profil Pic']
writer.writerow(headers)

while True:
    variabel = {
        "shortcode": short_code,
        "first": 50,
        "after": end_crusor
    }
    params = {
        'query_hash': 'd5d763b1e2acf209d62d22d184488e57',
        'variables': json.dumps(variabel)
    }
    # untuk mengataasi status code 429: too many request, head menggunakan cookie dan ambil sesionid nya
    head = {'cookie': 'sessionid=48309527837%3AOheC1jResji5V7%3A25'}

    req = requests.get(url, headers=head, params=params).json()

    # untuk handling limitasi, maka kasih jeda waktu jika gagal mengambil data
    try:
        user = req['data']['shortcode_media']['edge_liked_by']['edges']
    except:
        print('wait for 20 sec')
        time.sleep(30)
        continue

    for i in user:
        # for splitting file
        if count % per_file == 0 and count != 0:
            start_file += 1
            writer = csv.writer(open(f'resultfile/{short_code} {start_file}.csv', 'w', newline=''))
            headers = ['Username', 'Full Name', 'private account', 'Profil Pic']
            writer.writerow(headers)
        username = i['node']['username']
        fullname = i['node']['full_name']
        private = i['node']['is_private']
        profilpic = i['node']['profile_pic_url']
        count += 1
        print(f'{count}. {username} full name: {fullname}. profil pic link: {profilpic}. private? {private}')

        # live update data
        writer = csv.writer(open(f'resultfile/{short_code} {start_file}.csv', 'a', newline='', encoding='utf-8'))
        data = [username, fullname, private, profilpic]
        writer.writerow(data)

    # search all data
    end_crusor = req['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']
    has_next_page = req['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']
    if not has_next_page:
        break

    # untuk handling limitasi, maka kasih jeda waktu
    time.sleep(2)
