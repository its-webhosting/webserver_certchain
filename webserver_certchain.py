import subprocess
import sys
import re

def get_cert_chain(fqdn, webserver_ip=None, port=443):
    if fqdn in ['--help', '-help', '-h']:
        print("Usage: webserver_certchain.py website_fqdn [webserver_ip|webserver_fqdn] [port]")
        return

    # Determine the connection endpoint
    endpoint = f"{webserver_ip or fqdn}:{port}"

    # Execute the openssl command to retrieve certificates
    try:
        openssl_output = subprocess.run(
            ['openssl', 's_client', '-connect', endpoint, '-servername', fqdn, '-showcerts'],
            input='', text=True, capture_output=True, check=True
        ).stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing OpenSSL: {e.stderr}", file=sys.stderr)
        return

    certificate = ""
    extracting_cert = False
    for line in openssl_output.splitlines():
        if 'BEGIN CERTIFICATE' in line:
            extracting_cert = True
            certificate = line + "\n"
        elif 'END CERTIFICATE' in line:
            certificate += line + "\n"
            # Process the current certificate
            try:
                x509_process = subprocess.run(
                    ['openssl', 'x509', '-noout', '-subject', '-issuer', '-enddate', '-text'],
                    input=certificate, text=True, capture_output=True, check=True
                )
                x509_output = x509_process.stdout

                # Extract required fields
                subject = re.search(r"Subject: (.*)", x509_output)
                issuer = re.search(r"Issuer: (.*)", x509_output)
                not_after = re.search(r"Not After : (.*)", x509_output)
                
                # Manually parse the SAN section
                san_section_start = x509_output.find("X509v3 Subject Alternative Name:")
                if san_section_start != -1:
                    # Find the next section start by looking for a typical section start like "X509v3 Key Usage:"
                    san_section_end = x509_output.find("X509v3", san_section_start + 1)
                    san_section = x509_output[san_section_start:san_section_end].strip()
                    san_entries = re.findall(r"DNS:[^,\n]*", san_section)
                    san_text = ', '.join(san_entries)
                else:
                    san_text = None
                
                output = []
                if subject:
                    output.append(f"subject={subject.group(1).strip()}")
                if issuer:
                    output.append(f"issuer={issuer.group(1).strip()}")
                if not_after:
                    output.append(f"notAfter={not_after.group(1).strip()}")
                if san_text:
                    output.append(f"subjectAlternativeName={san_text}")

                print("\n".join(output))
                print("")  # Add a newline between certificates
            except subprocess.CalledProcessError as e:
                print(f"Error processing certificate: {e.stderr}", file=sys.stderr)
            finally:
                extracting_cert = False
        elif extracting_cert:
            certificate += line + "\n"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python webserver_certchain.py website_fqdn [webserver_ip|webserver_fqdn] [port]")
    else:
        fqdn = sys.argv[1]
        webserver_ip = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else None
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 443
        get_cert_chain(fqdn, webserver_ip, port)