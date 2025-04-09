import os
import requests
import logging
from requests.auth import HTTPBasicAuth
from typing import Optional


class NecmecAPI:
    def __init__(self, config_file: str, username: str, password: str, environment: str = 'production', log_file: Optional[str] = None):
        self.config = self.load_config(config_file)
        self.username = username
        self.password = password
        self.environment = environment
        self.base_url = self.config[environment]["base_url"]
        self.status_url = self.config[environment]["status_url"]
        self.xsd_url = self.config[environment]["xsd_url"]
        self.submit_url = self.config[environment]["submit_url"]
        self.upload_url = self.config[environment]["upload_url"]
        self.fileinfo_url = self.config[environment]["fileinfo_url"]
        self.finish_url = self.config[environment]["finish_url"]
        self.retract_url = self.config[environment]["retract_url"]

        self.logger = logging.getLogger(__name__)
        if log_file:
            logging.basicConfig(filename=log_file, level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.DEBUG)

    def load_config(self, config_file: str):
        """Load configuration from a JSON config file."""
        import json
        with open(config_file, 'r') as f:
            return json.load(f)

    def _make_request(self, method: str, endpoint: str, data: Optional[dict] = None, files: Optional[dict] = None):
        """Helper function to make API requests."""
        url = f"{self.base_url}{endpoint}"
        auth = HTTPBasicAuth(self.username, self.password)
        
        try:
            if method == 'GET':
                response = requests.get(url, auth=auth)
            elif method == 'POST':
                if files:
                    response = requests.post(url, auth=auth, data=data, files=files)
                else:
                    response = requests.post(url, auth=auth, json=data)
            else:
                self.logger.error(f"Unsupported HTTP method: {method}")
                return None

            response.raise_for_status()  # Raise an exception for HTTP error responses
            return response.json()

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None

    def get_status(self):
        """GET /status - Verify that the client can connect to and authenticate with the server."""
        return self._make_request('GET', self.status_url)

    def get_xsd(self):
        """GET /xsd - Download the latest XML schema definition."""
        return self._make_request('GET', self.xsd_url)

    def post_submit(self, xml_data: str):
        """POST /submit - Submit a report."""
        data = {'report': xml_data}
        return self._make_request('POST', self.submit_url, data=data)

    def post_upload(self, report_id: str, file_path: str):
        """POST /upload - Upload a file to a report."""
        files = {'file': open(file_path, 'rb')}
        data = {'report_id': report_id}
        return self._make_request('POST', self.upload_url, data=data, files=files)

    def post_fileinfo(self, report_id: str, file_id: str, fileinfo_xml: str):
        """POST /fileinfo - Provide additional details for an uploaded file."""
        data = {
            'report_id': report_id,
            'file_id': file_id,
            'file_info': fileinfo_xml
        }
        return self._make_request('POST', self.fileinfo_url, data=data)

    def post_finish(self, report_id: str):
        """POST /finish - Finish the report submission."""
        data = {'report_id': report_id}
        return self._make_request('POST', self.finish_url, data=data)

    def post_retract(self, report_id: str):
        """POST /retract - Cancel a report submission."""
        data = {'report_id': report_id}
        return self._make_request('POST', self.retract_url, data=data)
