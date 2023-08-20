## USAGE: 
## python random_words_get_requests.py -l 10 -c 10 -o output.txt
## Random kelimelerin geleceği yere göre kod içerisinde endpoint parametresi düzenlenmelidir. Random kelimeler word parametresine atanmıştır.
## -i parametresi kullanılırsa özel olarak hazırlanmış dışarıdan listeyi alır
## -i parametresi kullanılmamışssa kod çalışırken random olarak üretilmiş kısmı input olarak alır
## -o parametresi de çıktıların yazıldığı yerdir.

import sys
import random
import requests
import concurrent.futures
import string
import argparse

def generate_random_word(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def send_request(endpoint, word, output_file=None):
    url = f"{endpoint}/{word}.pdf"
    response = requests.get(url)
    status_code = response.status_code
    output = f"URL: {url} - Status Code: {status_code}"
    print(output)
    if output_file:
        output_file.write(output + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", required=True, type=int, help="Random üretilecek kelimenin uzunluğu")
    parser.add_argument("-c", "--count",  required=True,  type=int, help="Random üretilecek olan kelime sayısı")
    parser.add_argument("-i", "--input", default="random_generated_words.txt", help="Random kelimelerin bulunduğu dosya, -i belirtilmemişse kendisi otomatik olarak ekler.")
    parser.add_argument("-o", "--output", help="Çıktıların yazılacağı dosya")
    args = parser.parse_args()

    if not args.length or not args.count:
        parser.print_help()
        sys.exit(1)

    endpoint = "https://site.com/endpoint"  # İstek göndermek istediğiniz endpoint (sonunda / işareti yok)

    if args.input != "random_generated_words.txt":
        with open(args.input, 'r') as file:
            words = [line.strip() for line in file]
    else:
        words = [generate_random_word(args.length) for _ in range(args.count)]
        with open("random_generated_words.txt", "w") as file:
            for word in words:
               file.write(f"{word}\n")
               #file.write(f"{word}.pdf\n")
    if args.output:
        with open(args.output, "w") as output_file:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [executor.submit(send_request, endpoint, word, output_file) for word in words]

                for result in concurrent.futures.as_completed(results):
                    if result.exception() is not None:
                        print("Hata:", result.exception())
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(send_request, endpoint, word) for word in words]

            for result in concurrent.futures.as_completed(results):
                if result.exception() is not None:
                    print("Hata:", result.exception())

if __name__ == "__main__":
    main()
