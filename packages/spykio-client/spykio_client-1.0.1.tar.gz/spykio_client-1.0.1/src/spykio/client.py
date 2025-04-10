import requests

class SpykioClient:
    def __init__(self, api_key=None, base_url="https://api.spyk.io"):
        self.api_key = api_key
        self.base_url = base_url
        self.query = self._create_query()
        self.files = self._create_files()
    
    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'spykio-client-python',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def _create_query(self):
        class Query:
            def __init__(self, client):
                self.client = client
            
            def search(self, index, user_query, accurate_match=False, get_relevant_info=False):
                """Search for information in a specific index."""
                options = {
                    'index': index,
                    'userQuery': user_query,
                    'accurateMatch': accurate_match,
                    'getRelevantInfo': get_relevant_info
                }
                
                response = requests.post(
                    f"{self.client.base_url}/query",
                    headers=self.client._get_headers(),
                    json=options
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                # Filter unwanted fields
                if 'metrics' in response_data and 'tokenUsage' in response_data['metrics']:
                    del response_data['metrics']['tokenUsage']
                
                if 'documents' in response_data and isinstance(response_data['documents'], list):
                    filtered_docs = []
                    for doc in response_data['documents']:
                        filtered_docs.append({
                            'id': doc.get('id'),
                            'content': doc.get('content'),
                            'summary': doc.get('summary'),
                            'created_at': doc.get('created_at')
                        })
                    response_data['documents'] = filtered_docs
                
                return response_data
        
        return Query(self)
    
    def _create_files(self):
        class Files:
            def __init__(self, client):
                self.client = client
            
            def upload(self, index, mime_type=None, base64_string=None, content=None):
                """Upload a file or content to a specific index."""
                request_body = {'index': index}
                
                if content is not None:
                    request_body['content'] = content
                else:
                    request_body['mimeType'] = mime_type
                    request_body['base64String'] = base64_string
                
                response = requests.post(
                    f"{self.client.base_url}/uploadFile",
                    headers=self.client._get_headers(),
                    json=request_body
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                # Filter out unwanted fields
                if 'categorization' in response_data:
                    del response_data['categorization']
                
                if 'metrics' in response_data:
                    del response_data['metrics']
                
                return response_data
        
        return Files(self)
