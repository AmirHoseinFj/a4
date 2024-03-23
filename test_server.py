# Amirhossein Ghaffarzadeh 
# 120734223
# 2024-03-22

import http.client
import json
import threading
import unittest
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler

class MyServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host_port = ('localhost', 8000)
        cls.test_server = HTTPServer(cls.host_port, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.test_server.serve_forever)
        cls.server_thread.setDaemon(True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.test_server.shutdown()
        cls.test_server.server_close()
        cls.server_thread.join()

    def test_get_request(self):
        # Establish a connection and issue a GET request
        conn = http.client.HTTPConnection(*self.host_port)
        conn.request('GET', '/')
        resp = conn.getresponse()

        # Retrieve and decode the server's response
        resp_body = resp.read().decode()
        conn.close()

        # Validate the response status, reason, and content type
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.reason, 'OK')
        self.assertEqual(resp.getheader('Content-Type'), 'application/json')

        # Confirm the response body matches expected JSON content
        expected_data = {'message': 'This is a GET request response'}
        self.assertEqual(json.loads(resp_body), expected_data)

    def test_post_request(self):
        # Payload for POST request
        test_payload = json.dumps({'sampleKey': 'sampleValue'})

        # Initiate connection and send POST request with JSON payload
        conn = http.client.HTTPConnection(*self.host_port)
        headers = {'Content-Type': 'application/json'}
        conn.request('POST', '/', body=test_payload, headers=headers)
        resp = conn.getresponse()

        # Read and decode the response
        resp_body = resp.read().decode()
        conn.close()

        # Ensure response status, reason, and content type are as expected
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.reason, 'OK')
        self.assertEqual(resp.getheader('Content-Type'), 'application/json')

        # Verify the response content matches the expected JSON structure
        expected_resp_content = {'received': {'sampleKey': 'sampleValue'}}
        self.assertEqual(json.loads(resp_body), expected_resp_content)

if __name__ == '__main__':
    unittest.main()
