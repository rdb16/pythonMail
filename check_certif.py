import ssl
import socket
import requests
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import ExtensionOID


def get_server_certificate(host, port):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
    conn.connect((host, port))
    pem_cert = ssl.DER_cert_to_PEM_cert(conn.getpeercert(binary_form=True))
    conn.close()
    return pem_cert


def is_certificate_valid(cert_pem):
    cert = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'), default_backend())
    not_before = cert.not_valid_before
    not_after = cert.not_valid_after
    print('not_before: ', not_before)
    print('not_after: ',not_after)
    current_time = datetime.utcnow()
    return not_before <= current_time <= not_after



def is_certificate_in_crl(cert_pem):
    cert = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'), default_backend())

    # Chercher l'extension CRL Distribution Points
    try:
        dist_points = cert.extensions.get_extension_for_oid(ExtensionOID.CRL_DISTRIBUTION_POINTS)
    except x509.ExtensionNotFound:
        return False  # Pas de points de distribution CRL trouvés

    print("dist_point : ", dist_points.value)

    for dist_point in dist_points.value:
        for full_name in dist_point.full_name:
            crl_url = full_name.value

            # Télécharger la CRL
            crl_data = requests.get(crl_url).content
            crl = x509.load_der_x509_crl(crl_data, default_backend())

            # Vérifier si le certificat est révoqué
            for revoked_cert in crl:
                if revoked_cert.serial_number == cert.serial_number:
                    return True  # Le certificat est révoqué

    return False


if __name__ == "__main__":
    # host = "www.google.com"
    host = "www.instamed.fr"
    port = 443

    cert_pem = get_server_certificate(host, port)
    print(cert_pem)

    if not is_certificate_valid(cert_pem):
        print("Le certificat n'est pas valide ou a expiré.")
    else:
        print('le certificat est valide et pas expiré')

    if is_certificate_in_crl(cert_pem):
        print("Le certificat a été révoqué.")
    else:
        print("Le certificat n'a pas été révoqué.")
