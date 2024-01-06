import requests, json, yaml

with open('extensions.txt') as f:
    extensions = f.read().splitlines()

def download_vscode_extension(extension_id, version='latest'):
    url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{extension_id.split('.')[0]}/vsextensions/{extension_id.split('.')[1]}/{version}/vspackage"
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        file_name = f"extensions/{extension_id.replace('.', '-')}-{version}.vsix"
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_name}")
    elif response.status_code == 500:
        print(f"failed to download {extension_id} resource is not found")
    elif response.status_code == 429:
        print(f"failed to download {extension_id} due to rate limiting, wait 5 minutes before trying again")
        with open(f'errors/{extension_id}-error.txt', 'a') as file:
            file.write(f"{response.text}\n")
        exit(1)
    else:
        print(f"Failed to download. Status code: {response.status_code}")
        with open(f'errors/{extension_id}-error.txt', 'a') as file:
            file.write(f"{response.text}\n")

def main():
    for extension in extensions:
        download_vscode_extension(extension)

if __name__ == '__main__':
    main()
