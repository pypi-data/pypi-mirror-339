import requests
import os
import time
import json
from typing import List, Dict, Union, Optional
from dotenv import load_dotenv

class Mailer:
    """A class for sending templated emails using Microsoft Graph API."""
    
    def __init__(self, tenant_id: str = None, client_id: str = None, 
                 client_secret: str = None, sender_email: str = None):
        """
        Initialize the TemplateMailer.
        
        Args:
            tenant_id: Microsoft tenant ID
            client_id: Microsoft client ID
            client_secret: Microsoft client secret
            sender_email: Sender email address
        """
        load_dotenv()
        
        self.tenant_id = tenant_id or os.getenv("TENANT_ID")
        self.client_id = client_id or os.getenv("CLIENT_ID")
        self.client_secret = client_secret or os.getenv("CLIENT_SECRET")
        self.sender_email = sender_email or os.getenv("SENDER_EMAIL")
        
        if not all([self.tenant_id, self.client_id, self.client_secret, self.sender_email]):
            raise ValueError("Missing required credentials")
            
        self.token = None
        self.token_expires = 0

    def _refresh_token(self) -> None:
        """Refresh the access token."""
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.token = token_data['access_token']
            self.token_expires = time.time() + token_data.get('expires_in', 3600) - 300
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get token: {str(e)}")

    def _ensure_valid_token(self) -> None:
        """Ensure we have a valid token."""
        if not self.token or time.time() >= self.token_expires:
            self._refresh_token()

    def send_email(
        self,
        to_emails: Union[str, List[str]],
        subject: str,
        template_path: str,
        template_context: Dict,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> Dict[str, Union[bool, str]]:
        """
        Send email using an HTML template.

        Args:
            to_emails: Single email address or list of email addresses
            subject: Email subject
            template_path: Path to HTML template file
            template_context: Dictionary of template variables
            cc_emails: Optional list of CC recipients
            bcc_emails: Optional list of BCC recipients

        Returns:
            Dictionary containing success status and message
        """
        try:
            self._ensure_valid_token()

            # Normalize email lists
            if isinstance(to_emails, str):
                to_emails = [to_emails]
            cc_emails = cc_emails or []
            bcc_emails = bcc_emails or []

            # Read and process template
            with open(template_path, 'r', encoding='utf-8') as file:
                template_content = file.read()

            # Replace template variables
            for key, value in template_context.items():
                placeholder = f"{{{{ {key} }}}}"
                template_content = template_content.replace(placeholder, str(value))

            # Prepare email data
            email_data = {
                'message': {
                    'subject': subject,
                    'body': {
                        'contentType': 'HTML',
                        'content': template_content
                    },
                    'toRecipients': [
                        {'emailAddress': {'address': email}} 
                        for email in to_emails
                    ],
                    'ccRecipients': [
                        {'emailAddress': {'address': email}}
                        for email in cc_emails
                    ],
                    'bccRecipients': [
                        {'emailAddress': {'address': email}}
                        for email in bcc_emails
                    ]
                },
                'saveToSentItems': 'true'
            }

            # Send email
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }

            url = f'https://graph.microsoft.com/v1.0/users/{self.sender_email}/sendMail'
            
            response = requests.post(
                url,
                headers=headers,
                json=email_data,
                timeout=30
            )

            if response.status_code == 202:
                return {'success': True, 'message': 'Email sent successfully'}
            else:
                return {'success': False, 'message': f'Failed to send email: {response.text}'}

        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}