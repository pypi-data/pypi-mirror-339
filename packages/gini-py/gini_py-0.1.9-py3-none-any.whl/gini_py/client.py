import json
from typing import List, Optional
from .crypto.encryption import Encryptor
from .models import Attachment, GiniResponse
import socket
import ast
import base64

class GiniClient:
    def __init__(self, api_key: str, port: int, host: str = "localhost"):
        """Initialize the Gini SDK client.
        
        Args:
            api_key: The API key for authentication
            host: The host address of the server
            port: The port number of the server
        """
        self.api_key = api_key
        self.host = host
        self.port = port
        self.encryptor = Encryptor(api_key)

    def execute_gini(self, input : str, attachments: Optional[List[Attachment]] = None, gini_id: Optional[str] = None) -> GiniResponse:
        """Execute a Gini request.
        
        Args:
            gini_id: The ID of the Gini to execute
            input: The input to the Gini
            attachments: List of file attachments
            
        Returns:
            GiniResponse object containing status and response
            
        Raises:
            ConnectionError: If unable to connect to the server
            Exception: If the server returns an error
        """
        data = {
            "giniID": gini_id,
            "value": input,
            "attachments": [att.model_dump() for att in attachments] if attachments else []
        }
        
        # Base64 encode just the data portion
        encoded_data = base64.b64encode(json.dumps(data).encode()).decode()
        
        request_data = {
            "action": "EXECUTE_GINI",
            "data": encoded_data
        }
        
        # Encrypt the request
        encrypted_payload = self.encryptor.encrypt_message(json.dumps(request_data))
        
        # Create a raw socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
            sock.sendall(encrypted_payload.encode())
            
            # Receive response
            response = sock.recv(4096).decode()
            decrypted_response = self.encryptor.decrypt_message(response)
            raw_response = json.loads(decrypted_response)
            
            if "error" in raw_response:
                raise Exception(raw_response["error"])
            
            # Decode the base64 response value
            response_content = base64.b64decode(raw_response.get("response")).decode()
            try: 
                response_content = json.loads(response_content)  # Try to parse as JSON
            except Exception:
                pass
            
            return GiniResponse(
                response=response_content
            )
        
        finally:
            sock.close()