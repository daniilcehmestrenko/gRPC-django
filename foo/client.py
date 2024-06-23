import ssl
import json
import http.client
from urllib.parse import urlparse


def post(url, data, headers, cert=None):
    """
    Make POST request
    :param url: endpoint
    :param data: dict with data
    :param headers: dict with headers
    :param cert: (cert_file, key_file)
    :return: Response
    """
    return request('POST', url, headers=headers, cert=cert, data=data)


def request(method, url, headers, cert, data):
    """
    Make request
    :param method:
    :param url:
    :param headers:
    :param cert:
    :param data:
    :return:
    """
    url = urlparse(url)
    data_json = json.dumps(data)
    if isinstance(cert, tuple) and len(cert) == 2:
        cert_file, key_file = cert
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        conn = http.client.HTTPSConnection(url.hostname, context=context)
    else:
        conn = http.client.HTTPConnection(url.hostname)
    try:
        conn.request(method, url.path, data_json, headers=headers)
        response = conn.getresponse()
        if response.status == 301:
            response.read()
            new_url = response.headers.get('Location')
            response = retry_request(conn, method=method, url=new_url, body=data_json, headers=headers)
        return response
    except http.client.HTTPException as e:
        print(f"HTTPException: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def retry_request(conn, retry_count=2, **kwargs):
    count_ = 0
    response = None
    while count_ < retry_count:
        conn.request(**kwargs)
        response = conn.getresponse()
        if response.status == 200:
            break
        count_ += 1
    return response
