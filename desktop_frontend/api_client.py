import requests


class APIClient:
    """HTTP client for backend API communication"""
    
    def __init__(self, base_url='http://localhost:8000/api'):
        self.base_url = base_url
        self.token = None
    
    def set_token(self, token):
        """Set auth token"""
        self.token = token
    
    def _get_headers(self):
        """Get headers with auth token"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers
    
    def login(self, username, password):
        """User login"""
        url = f'{self.base_url}/auth/login/'
        data = {'username': username, 'password': password}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def register(self, username, email, password):
        """User registration"""
        url = f'{self.base_url}/auth/register/'
        data = {'username': username, 'email': email, 'password': password}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def upload_csv(self, file_path):
        """Upload CSV file"""
        url = f'{self.base_url}/upload/'
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, headers=headers)
        
        response.raise_for_status()
        return response.json()
    
    def get_datasets(self):
        """Get list of datasets"""
        url = f'{self.base_url}/datasets/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_dataset(self, dataset_id):
        """Get specific dataset"""
        url = f'{self.base_url}/datasets/{dataset_id}/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def download_pdf(self, dataset_id):
        """Download PDF report"""
        url = f'{self.base_url}/datasets/{dataset_id}/pdf/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.content

    def send_report_email(self, dataset_id, email):
        """Send dataset report via email"""
        url = f'{self.base_url}/datasets/{dataset_id}/send-email/'
        headers = self._get_headers()
        data = {'email': email}
        response = requests.post(url, json=data, headers=headers)
        # Don't raise for status here as we want to handle 500s manually if needed
        return response.json()

    def validate_dataset(self, dataset_id):
        """Get data quality validation report"""
        url = f'{self.base_url}/datasets/{dataset_id}/validate/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_alerts(self, dataset_id):
        """Get alerts for a dataset"""
        url = f'{self.base_url}/datasets/{dataset_id}/alerts/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def compare_datasets(self, dataset1_id, dataset2_id):
        """Compare two datasets"""
        url = f'{self.base_url}/compare/'
        data = {'dataset1_id': dataset1_id, 'dataset2_id': dataset2_id}
        response = requests.post(url, json=data, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_health_analysis(self, dataset_id):
        """Get health analysis for a dataset"""
        url = f'{self.base_url}/datasets/{dataset_id}/health_analysis/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_thresholds(self):
        """Get all alert thresholds"""
        url = f'{self.base_url}/thresholds/'
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def set_threshold(self, parameter, warning_threshold, critical_threshold):
        """Set alert threshold for a parameter"""
        url = f'{self.base_url}/thresholds/set/'
        data = {
            'parameter': parameter,
            'warning_threshold': warning_threshold,
            'critical_threshold': critical_threshold
        }
        response = requests.post(url, json=data, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def batch_upload_csv(self, file_paths):
        """Upload multiple CSV files"""
        url = f'{self.base_url}/upload/batch_upload/'
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        
        # Requests 'files' param for multiple files: [('files', file_obj1), ('files', file_obj2)...]
        files = []
        open_files = [] # To close them later
        try:
            for path in file_paths:
                f = open(path, 'rb')
                open_files.append(f)
                files.append(('files', f))
            
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            return response.json()
        finally:
            for f in open_files:
                f.close()

    def get_root_cause(self, params):
        """Get AI Root Cause Analysis"""
        url = f'{self.base_url}/datasets/root_cause/'
        response = requests.post(url, json=params, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
