from googlesearch import search

def get_google_search_results(query, num_results=10):
    links = []
    for result in search(query, num=num_results, stop=num_results, pause=2):
        links.append(result)
    return links

def main():
    # Get user input for the search query
    query = input("Enter your search query: ")
    num_results = int(input("Enter the number of results you want to retrieve: "))  # Ensure input is an integer
    
    links = get_google_search_results(query, num_results)
    
    print("\nFound links:")
    for link in links:
        print(link)

if __name__ == "__main__":
    main()
