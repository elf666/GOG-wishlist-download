import sys
import requests
import re
import json

''' 
Works only for users that have public wishlist, I have no idea how to make it work for not public wishlists
'''
if __name__ == '__main__':
    if len (sys.argv)<2:
        print("please provide user's name")
        exit()
    # taking out user_name from program arguments
    
    user_name = sys.argv[1]

    # building address to download wishlist
    download_url = 'https://www.gog.com/u/' + user_name + '/wishlist'

    # getting html
    response = requests.get(download_url)

    # If 404 appears, it means that there is no user or user has no wishlist
    if response.status_code == 404:
        print("User " + user_name + " does not exist or has no public wishlist")
        exit()

    # Wishlist is encoded in javascript, I have to parse it to Json
    result = re.search('var gogData = (.*);\n', response.text)
    json_data = json.loads(result.group(1))

    # getting avatar URL
    avatar_url = json_data['userInfo']['avatars']['large']
    print('Avatar url: ' + avatar_url)

    txt_results = 'Wishlist of user ' + user_name + ':\r\n'
    total_sum = 0.0

    # getting wishlist products and adding them to text
    for product in json_data['products']:
        # version with prices:
        # txt_results += ' - ' +  product['title'] + ' ' + product['price']['finalAmount'] + '\r\n'
        txt_results += ' - ' + product['title'] + '\r\n'
        total_sum += float(product['price']['finalAmount'])

    txt_results = txt_results + 'Estimated total price is: ' + str(total_sum) + ' PLN' + '\r\n'
    print(txt_results)

    # saving avatar on disk
    avatar_response = requests.get(avatar_url)
    open('avatar.jpg', 'wb').write(avatar_response.content)

    # saving text on disk
    open('wishlist.txt', 'wb').write(txt_results.encode('utf-8'))
