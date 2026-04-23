import wget
import os
import requests
import subprocess


def download_file_wget(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.basename(url)
    wget.download(url, out=output_folder + "/" + filename, bar=False)
    print(f"File downloaded to {output_folder + '/' + filename}")
    return os.path.join(output_folder, filename)


def download_file_subprocess(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.basename(url)

    with subprocess.Popen(['curl', '-L', url], stdout=subprocess.PIPE) as curl_pipe:
        with open(os.path.join(output_folder, filename), 'wb') as output_file:
            for chunk in iter(lambda: curl_pipe.stdout.read(1024), b""):
                output_file.write(chunk)

    print(f"File downloaded with curl-subproc to {output_folder + '/' + filename}")
    return os.path.join(output_folder, filename)


def download_file_requests(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.basename(url)

    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    with open(os.path.join(output_folder, filename), 'wb') as output_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                output_file.write(chunk)

    print(f"File downloaded with requests to {output_folder + '/' + filename}")
    return os.path.join(output_folder, filename)

# if __name__ == "__main__":
#     IRIS_download_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
#     input_folder = 'input_data'
#     output_folder = 'output_data'

#     download_file_wget(IRIS_download_URL, output_folder=input_folder)
