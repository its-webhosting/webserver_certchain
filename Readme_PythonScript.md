# Webserver Certchain

`webserver_certchain.py` is a Python script designed to retrieve and display the certificate chain of a specified web server. The script leverages OpenSSL to extract certificate details such as subject, issuer, expiration date (notAfter), and Subject Alternative Names (SANs).

## Features

- Extracts and displays information from a web server's certificate chain:
  - Subject
  - Issuer
  - Expiration Date (`notAfter`)
  - Subject Alternative Names (`subjectAlternativeName`)

## Requirements

- Python 3.x
- OpenSSL installed and accessible in your system's PATH

## Installation

1. Ensure you have Python installed on your system.
2. Ensure OpenSSL is available in your system's PATH.
3. Download the script or clone the repository.

## Usage

The script can be run directly via the command line. The basic syntax is:

```
python webserver_certchain.py <website_fqdn> [webserver_ip|webserver_fqdn] [port]
```