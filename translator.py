import requests
import sys
from bs4 import BeautifulSoup


# def file_write(path_,content):
#    my_file = open(path_, 'a+', encoding='utf-8')
#    my_file.write(content+'\n')
#    my_file.close()


def make_request(url, header):
    try:
        s = requests.session()
        page_ = s.get(url, headers=header)
        if page_.status_code == 200:
            return page_
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        sys.exit()

def get_url(lang1, lang2, w):
    url = f'https://context.reverso.net/translation/{lang1.lower()}-{lang2.lower()}/{w}'
    return url


def get_translations(soup):
    word_translation = soup.find_all('a', {'class': 'translation'})
    return [t.text.strip() for t in word_translation][1:]


def get_example(soup):
    examples = soup.find_all('div', {'class': ['src', 'trg']})
    return [e.text.strip().strip('\n\n\n') for e in examples]


def save_translations(tran, lan, path_):
    my_file = open(path_, 'a+', encoding='utf-8')

    my_file.write(f'{lan} Translations:\n')

    my_file.write(tran[0] + '\n')

    my_file.write('\n')
    my_file.close()


def save_example(exam, lan, path_):
    my_file = open(path_, 'a+', encoding='utf-8')
    my_file.write(f'{lan} Examples:\n')

    my_file.write(exam[0] + ':' + '\n')

    if lan == 'Turkish':
        my_file.write(exam[1])
    else:
        my_file.write(exam[1] + '\n')

    if lan != 'Turkish':
        my_file.write('\n\n')

    my_file.close()


def welcome_message():
    print("Hello, you're welcome to the translator.")
    print('Translator supports:')
    print('1. Arabic')
    print('2. German')
    print('3. English')
    print('4. Spanish')
    print('5. French')
    print('6. Hebrew')
    print('7. Japanese')
    print('8. Dutch')
    print('9. Polish')
    print('10. Portuguese')
    print('11. Romanian')
    print('12. Russian')
    print('13. Turkish')


if __name__ == "__main__":
    args = sys.argv
    lang_list = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish',
                 'Portuguese', 'Romanian', 'Russian', 'Turkish']
    src_language = args[1]

    target_language = args[2]

    if src_language.capitalize() not in lang_list:
        print(f"Sorry,the program doesn't support {src_language}")
        sys.exit()
    if target_language.capitalize() not in lang_list+['All']:
        print(f"Sorry,the program doesn't support {target_language}")
        sys.exit()

    word = args[3]
    path = f'{word}.txt'
    headers = {'User-Agent': 'Chrome-Windows'}

    if target_language == 'all':
        for k in range(len(lang_list)):
            if lang_list[k].lower() == src_language.lower():
                continue
            url1 = get_url(src_language, lang_list[k], word)
            page = make_request(url1, headers)
            try:
                soup_ = BeautifulSoup(page.content, 'html.parser')
            except AttributeError:
                print(f'Sorry, unable to find {word}')
                sys.exit()
            soup_.prettify()
            translation_ = get_translations(soup_)
            example_ = get_example(soup_)

            save_translations(translation_, lang_list[k], path)
            save_example(example_, lang_list[k], path)

    else:
        url1 = get_url(src_language, target_language, word)
        page = make_request(url1, headers)
        try:
            soup_ = BeautifulSoup(page.content, 'html.parser')
        except AttributeError:
            print(f'Sorry, unable to find {word}')
            sys.exit()
        soup_.prettify()
        translation_ = get_translations(soup_)
        example_ = get_example(soup_)

        save_translations(translation_, target_language, path)
        save_example(example_, target_language, path)


    file = open(path, 'r', encoding='utf-8')
    print(file.read())
    file.close()
