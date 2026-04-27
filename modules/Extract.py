import wget
import os
import requests
import subprocess


def download_file_wget(url, output_folder):
    # Opretter output-mappen hvis den ikke allerede findes
    os.makedirs(output_folder, exist_ok=True)

    # Finder filnavnet fra URL'en, fx iris.csv
    filename = os.path.basename(url)

    # Downloader filen med Python-biblioteket wget
    # Filen gemmes i den angivne mappe med originalt filnavn
    wget.download(url, out=output_folder + "/" + filename, bar=False)

    # Udskriver hvor filen blev gemt
    print(f"File downloaded to {output_folder + '/' + filename}")

    # Returnerer den fulde sti til den downloadede fil
    return os.path.join(output_folder, filename)


def download_file_subprocess(url, output_folder):
    # Opretter output-mappen hvis den ikke allerede findes
    os.makedirs(output_folder, exist_ok=True)

    # Finder filnavnet fra URL'en
    filename = os.path.basename(url)

    # Starter det eksterne program curl via subprocess
    # -L betyder at curl følger redirects hvis URL'en viderestiller
    with subprocess.Popen(['curl', '-L', url], stdout=subprocess.PIPE) as curl_pipe:
        # Åbner en lokal fil i binær skrivemodus
        with open(os.path.join(output_folder, filename), 'wb') as output_file:
            # Læser download-data i små bidder på 1024 bytes
            # og skriver dem løbende til filen
            for chunk in iter(lambda: curl_pipe.stdout.read(1024), b""):
                output_file.write(chunk)

    # Udskriver hvor filen blev gemt
    print(f"File downloaded with curl-subproc to {output_folder + '/' + filename}")

    # Returnerer den fulde sti til den downloadede fil
    return os.path.join(output_folder, filename)


def download_file_requests(url, output_folder):
    # Opretter output-mappen hvis den ikke allerede findes
    os.makedirs(output_folder, exist_ok=True)

    # Finder filnavnet fra URL'en
    filename = os.path.basename(url)

    # Sender HTTP GET-request til URL'en
    # stream=True gør at data læses løbende i bidder
    # timeout=30 sætter maks ventetid til 30 sekunder
    response = requests.get(url, stream=True, timeout=30)

    # Stopper med fejl hvis serveren returnerer en fejlstatus
    response.raise_for_status()

    # Åbner den lokale fil i binær skrivemodus
    with open(os.path.join(output_folder, filename), 'wb') as output_file:
        # Skriver indholdet til filen i bidder på 1024 bytes
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                output_file.write(chunk)

    # Udskriver hvor filen blev gemt
    print(f"File downloaded with requests to {output_folder + '/' + filename}")

    # Returnerer den fulde sti til den downloadede fil
    return os.path.join(output_folder, filename)

# if __name__ == "__main__":
#     IRIS_download_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
#     input_folder = 'input_data'
#     output_folder = 'output_data'

#     download_file_wget(IRIS_download_URL, output_folder=input_folder)