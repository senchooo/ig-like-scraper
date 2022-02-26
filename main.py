import requests
import json

url = 'https://www.instagram.com/graphql/query/'
short_code = input('enter your source code: ')
variabel = {"shortcode": short_code, "first": 50}
params = {
    'query_hash': 'd5d763b1e2acf209d62d22d184488e57',
    'variables': json.dumps(variabel)
}
# untuk mengataasi status code 429: too many request, head menggunakan cookie dan ambil sesionid nya
head = {'cookie': 'sessionid=48309527837%3AOheC1jResji5V7%3A25'}

req = requests.get(url, headers=head, params=params).json()

user = req['data']['shortcode_media']['edge_liked_by']['edges']

for i in user:
    username = i['node']['username']
    fullname = i['node']['full_name']
    profilpic = i['node']['profile_pic_url']
    pivate = i['node']['is_private']
    print(f'{username} full name: {fullname}\nprofil pic link: {profilpic}\nprivate? {pivate}')
