import time
import requests
import dns.resolver
import ssl
import socket
import threading

def check_uptime(url, interval=60):
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

def check_domain_availability(target_domain, dns_servers):
    results = {}

    for location, dns_server in dns_servers.items():
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [dns_server]

        try:
            answer = resolver.query(target_domain)
            results[location] = [str(ip) for ip in answer]
        except dns.resolver.NXDOMAIN:
            results[location] = None
        except dns.resolver.NoAnswer:
            results[location] = None
        except dns.resolver.Timeout:
            results[location] = 'Timeout'

    print(f"Domain: {target_domain} Availability:")
    for location, result in results.items():
        print(f"{location}: {result}")

def check_tls_certification(host, port):
    try:
        sock = socket.create_connection((host, port), timeout=5)
        context = ssl.create_default_context()
        secure_sock = context.wrap_socket(sock, server_hostname=host)

        print(f'TLS Connection to {host}:{port} successful')
        print(f'Protocol: {secure_sock.version()}')
        print(f'Cipher: {secure_sock.cipher()}')

        cert = secure_sock.getpeercert()
        if ssl.match_hostname(cert, host):
            print(f'The domain {host} is not certified.')
        else:
            print(f'The domain {host} is certified.')

        secure_sock.close()
    except (socket.error, ssl.SSLError) as e:
        print(f'Error connecting to {host}:{port}: {e}')

if __name__ == "__main__":
    website_url = "https://chat.openai.com/c/f05f521a-16aa-42e9-b7b8-f14041fbef0c"

    # Create threads for each function
    thread_uptime = threading.Thread(target=check_uptime, args=(website_url,))
    thread_availability = threading.Thread(target=check_domain_availability, args=('youtube.com', {'US': '8.8.8.8', 'Europe': '8.8.4.4', 'Asia': '1.1.1.1'}))
    thread_tls = threading.Thread(target=check_tls_certification, args=('www.youtube.com', 443))

    # Start threads
    thread_uptime.start()
    thread_availability.start()
    thread_tls.start()

    # Wait for threads to finish
    thread_uptime.join()
    thread_availability.join()
    thread_tls.join()
