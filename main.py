import requests
from bs4 import BeautifulSoup


def main():
    # Ask for URL
    url = input("Enter Zippyshare URL: ")

    # If url doesnt have protocol, add it
    if url[:6] != 'https:' and url[:6] != 'http:/':
        if url[:2] == '//':
            url = 'https:' + url
        elif url[:3] == 'www':
            url = 'https://' + url
        else:
            print('Invalid URL!')
            exit()

    # Start scrapper
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Parse main url domain and protocol
    final_url = url[:url.rfind('/')]
    final_url = final_url[:final_url.rfind('/')]
    final_url = final_url[:final_url.rfind('/')]

    # Parse href script function
    for script in soup.findAll('script'):
        if script.text.strip()[:40] == "document.getElementById('dlbutton').href":
            url_parse = script.text.strip()[44:script.text.find(";")].strip()[:-2]

            final_url += url_parse.split('" + (')[0]
            url_parse = url_parse.replace(url_parse.split('" + (')[0] + '" + (', '')
            token_string = url_parse.split(') + "')[0]
            url_parse = url_parse.replace(url_parse.split(') + "')[0] + ') + "', '')

            first_half = token_string.split(" + ")[0]
            second_half = token_string.split(" + ")[1]

            parsed_token = int(first_half.split(" % ")[0]) % int(first_half.split(" % ")[1]) + \
                 int(second_half.split(" % ")[0]) % int(second_half.split(" % ")[1])

            final_url += str(parsed_token) + url_parse
            break

    print('Direct URL:\n' + final_url)


if __name__ == '__main__':
    main()
