import time

def checking(url, interval=60):
    try:
        import requests
    except ImportError:
        print("No 'requests' module found. Please install it to run this program.")
        return

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"{url} is UP - Status Code: {response.status_code}")
            elif response.status_code >= 500:
                print(f"{url} is DOWN - Status Code: {response.status_code}")
            else:
                print(f"{url} is reachable, but returned a non-200 status code: {response.status_code}")
        except requests.ConnectionError:
            print(f"{url} is DOWN - Connection Error")

        time.sleep(interval)

if __name__ == "__main__":
    website_url = "https://chat.openai.com/c/f05f521a-16aa-42e9-b7b8-f14041fbef0c"  # Replace with the URL you want to check
    checking(website_url)
