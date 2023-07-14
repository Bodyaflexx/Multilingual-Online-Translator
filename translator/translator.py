import sys

import requests
import argparse
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.languages = ["Arabic", "German", "English", "Spanish", "French", "Hebrew",
                          "Japanese", "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish"]
        parser = argparse.ArgumentParser()
        parser.add_argument("source")
        parser.add_argument("target")
        parser.add_argument("word")
        args = parser.parse_args()
        self.source_language = args.source
        self.target_language = args.target
        self.word = args.word
        self.f_name = self.word + '.txt'
        self.translate_word()

    # def choose_language(self):
    #     while True:
    #         print('Hello, welcome to the translator. Translator supports:')
    #         for index, i in enumerate(self.languages):
    #             print(str(index + 1) + '. ' + i)
    #         source_language = input('Type the number of your language: ')
    #         target_language = input("Type the number of a language you want to translate to"
    #                                 " or '0' to translate to all languages:")
    #         if target_language.isdigit() and target_language.isdigit():
    #             self.source_language = self.languages[int(source_language) - 1]
    #             if target_language == "0":
    #                 self.target_language = 'all'
    #             else:
    #                 self.target_language = self.languages[int(target_language) - 1]
    #             break
    #         else:
    #             print('ERROR')
    #
    # @staticmethod
    # def get_word():
    #     return input('Type the word you want to translate: ')

    def translate_word(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        base_url = 'https://context.reverso.net/translation/'
        output_text = ""
        if self.target_language not in self.languages and self.target_language != 'all':
            print(f"Sorry, the program doesn't support {self.target_language}")
            return
        if self.source_language not in self.languages and self.source_language != 'all':
            print(f"Sorry, the program doesn't support {self.source_language}")
            try:
                if self.target_language == 'all':
                    for i in self.languages:
                        if i.lower() == self.source_language.lower():
                            continue
                        url = f'{base_url}{self.source_language.lower()}-{i.lower()}/{self.word}'
                        response = requests.get(url, headers=headers)
                        output_text += self.get_translations_and_examples(response.content.decode(), i)
                else:
                    url = f'{base_url}{self.source_language.lower()}-{self.target_language.lower()}/{self.word}'
                    response = requests.get(url, headers=headers)
                    output_text += self.get_translations_and_examples(response.content.decode(), self.target_language)
            except requests.exceptions.ConnectionError:
                print('Something wrong with your internet connection')

        print(output_text)
        self.write_to_file(output_text)

    def get_translations_and_examples(self, content, lang):
        soup = BeautifulSoup(content, 'html.parser')
        trans_tags = soup.find_all('span', attrs={'class': 'display-term'})
        example_tags = soup.find_all('div', {'class': ['src', 'trg']})
        output_trans = [tag.text.strip() for tag in trans_tags]
        output_examples = [tag.text.strip() for tag in example_tags if tag.text.strip()]
        if len(output_trans) == 0:
            print(f'Sorry, unable to find {self.word}')
            sys.exit()
        str_to_file = lang + ' translations: \n'
        str_to_file += '\n'.join(output_trans[:1]) + '\n'
        str_to_file += lang + ' examples: \n'
        for i in range(0, min(1 * 2, len(output_examples)), 2):
            str_to_file += '\n'.join(output_examples[i:i + 2]) + '\n\n'
        return str_to_file

    def write_to_file(self, data):
        with open(self.f_name, 'w', encoding='utf-8') as f:
            f.write(data)


translation = Translator()
