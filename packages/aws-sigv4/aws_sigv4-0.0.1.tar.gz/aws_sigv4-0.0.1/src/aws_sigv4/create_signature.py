import datetime
import hashlib
import hmac
import re
import requests

class Utilities:
    @staticmethod
    def parse_url(url=None):
        if url is None:
            raise Exception("URL is required")
        host = re.search(r'https?://([^/]+)', url).group(1)
        canonical_uri = re.search(r'https?://[^/]+(/.*)', url).group(1)
        return host, canonical_uri

    @staticmethod
    def get_time_fields():
        current_time = datetime.datetime.utcnow()
        amz_date = current_time.strftime('%Y%m%dT%H%M%SZ')
        datestamp = current_time.strftime('%Y%m%d')
        return amz_date, datestamp

    @staticmethod
    def get_hashed_payload(data, data_binary=True):
        return hashlib.sha256(data).hexdigest() if data_binary else hashlib.sha256(data.encode('UTF-8')).hexdigest()

    @staticmethod
    def hmac_sha256(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

class AWSS4RequestSigner:
    def __init__(self, data):
        self.__data = data

    def get_request_header(self, **kwargs):

        if (kwargs.get('access_key', None) is None or kwargs.get('secret_key', None) is None):
            raise Exception("Access Key and Secret Key are required")
        else:
            access_key = kwargs.get('access_key')
            secret_key = kwargs.get('secret_key')
            session_token = kwargs.get('session_token', None)

        host, canonical_uri = Utilities.parse_url(url=kwargs.get('url'))
        amz_date, datestamp = Utilities.get_time_fields()

        hashed_payload = Utilities.get_hashed_payload(data=self.__data, data_binary=kwargs.get('data_binary',True))
        print(f'hashed_payload - {hashed_payload}')
        canonical_request, signed_headers = self.create_canonical_request(host=host, amz_date=amz_date,
                                            method=kwargs.get('method'), hashed_payload=hashed_payload, session_token=session_token,
                                            canonical_querystring='', canonical_uri=canonical_uri)
        print(f'canonical_request - {canonical_request}, signed_headers - {signed_headers}')
        string_to_sign, scope = self.create_string_to_sign(amz_date=amz_date, datestamp=datestamp,
                                                                                  canonical_request=canonical_request,
                                                                                 region=kwargs.get('region_name'),
                                                                                  service=kwargs.get('service'))
        print(f'string_to_sign - {string_to_sign}, scope - {scope}')
        signature = self.create_signature(datestamp=datestamp, string_to_sign=string_to_sign,
                                          service = kwargs.get('service'), region=kwargs.get('region_name'), secret_key = secret_key)

        print(f'signature - {signature}')
        try:
            request_header = self.create_auth_headers_for_the_request(amz_date=amz_date, hashed_payload=hashed_payload,
                                                                  scope=scope, signed_headers=signed_headers,
                                                                  signature=signature, access_key=access_key, session_token=session_token)
        except Exception as ex:
            print(f'Reqest Header - {Exception}, {ex}')
        print(f'request_header - {request_header}')
        return request_header

    def create_canonical_request(self, host, amz_date, hashed_payload, session_token, method='POST', canonical_querystring='', canonical_uri='/'):

        canonical_headers = ('host:' + host.lower() + '\n' + 'x-amz-date:' + amz_date + '\n')
        signed_headers = 'host;x-amz-date'
        if session_token:
            canonical_headers += ('x-amz-security-token:' + session_token + '\n')
            signed_headers += ';x-amz-security-token'

        canonical_request = (method + '\n' + requests.utils.quote(canonical_uri) + '\n' + canonical_querystring + '\n' +
                             canonical_headers + '\n' + signed_headers + '\n' + hashed_payload)

        return canonical_request, signed_headers

    def create_string_to_sign(self, amz_date, datestamp, canonical_request, service, region, algorithm='AWS4-HMAC-SHA256'):

        scope = (datestamp + '/' + region + '/' + service + '/' + 'aws4_request')
        string_to_sign = algorithm + '\n' + amz_date + '\n' + scope + '\n' + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        return string_to_sign, scope

    def get_signature_key(self, secret_key, date_stamp, region_name, service_name):

        date_key = Utilities.hmac_sha256(('AWS4' + secret_key).encode('utf-8'), date_stamp)
        date_region_key = Utilities.hmac_sha256(date_key, region_name)
        date_region_service_key  = Utilities.hmac_sha256(date_region_key, service_name)
        signing_key = Utilities.hmac_sha256(date_region_service_key, 'aws4_request')
        return signing_key

    def create_signature(self, datestamp, string_to_sign, service, region, secret_key):

        signing_key = self.get_signature_key(secret_key, datestamp, region, service)
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature

    def create_auth_headers_for_the_request(self, amz_date, hashed_payload, scope, signed_headers
                                            , signature, access_key, session_token=None, algorithm='AWS4-HMAC-SHA256'):
        authorization_header = (
                algorithm + ' ' +
                'Credential=' + access_key + '/' + scope + ', ' +
                'SignedHeaders=' + signed_headers + ', ' +
                'Signature=' + signature
        )

        headers = {
            'Authorization': authorization_header,
            'x-amz-date': amz_date,
            'x-amz-content-sha256': hashed_payload
        }
        if session_token is not None:
            headers['x-amz-security-token'] = session_token
        return headers