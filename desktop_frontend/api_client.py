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
