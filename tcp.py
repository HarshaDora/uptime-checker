import ssl
import socket

def certification(host, port):
    try:
        # Create a socket object
        sock = socket.create_connection((host, port), timeout=5)

        # Wrap the socket with an SSL context
        context = ssl.create_default_context()
        secure_sock = context.wrap_socket(sock, server_hostname=host)

        # Check the protocol version and cipher
        print(f'TLS Connection to {host}:{port} successful')
        print(f'Protocol: {secure_sock.version()}')
        print(f'Cipher: {secure_sock.cipher()}')

        # Check if the certificate is valid
        cert = secure_sock.getpeercert()
        if ssl.match_hostname(cert, host):
            print(f'The domain {host} is not certified.')
        else:
            print(f'The domain {host} is certified.')

        secure_sock.close()
    except (socket.error, ssl.SSLError) as e:
        print(f'Error connecting to {host}:{port}: {e}')


tls_host = 'www.youtube.com'
# replace with the desired port for TLS/SSL
tls_port = 443 
certification(tls_host, tls_port)