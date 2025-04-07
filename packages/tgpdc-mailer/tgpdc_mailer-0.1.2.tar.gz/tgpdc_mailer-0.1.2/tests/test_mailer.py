# tests/test_mailer.py

import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import requests
from src.tgpdc_mailer.mailer import Mailer

class TestMailer(unittest.TestCase):
    
    def setUp(self):
        """Set up test cases"""
        # Define test credentials that will be used across all tests
        self.test_credentials = {
            'tenant_id': 'test_tenant',
            'client_id': 'test_client',
            'client_secret': 'test_secret',
            'sender_email': 'sender@test.com'
        }
        
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'TENANT_ID': 'env_tenant',
            'CLIENT_ID': 'env_client',
            'CLIENT_SECRET': 'env_secret',
            'SENDER_EMAIL': 'env_sender@test.com'
        })
        self.env_patcher.start()

    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
        
    @patch('requests.post')
    def test_ensure_valid_token_refresh(self, mock_post):
        """Test that token gets refreshed when expired"""
        # Mock initial token response
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 0  # Token immediately expires
        }
        mock_token_response.status_code = 200
        
        # Mock second token response
        mock_token_response2 = MagicMock()
        mock_token_response2.json.return_value = {
            'access_token': 'new_test_token',
            'expires_in': 3600
        }
        mock_token_response2.status_code = 200
        
        mock_post.side_effect = [mock_token_response, mock_token_response2]
        
        mailer = Mailer(**self.test_credentials)
        mailer._refresh_token()
        self.assertEqual(mailer.token, 'test_token')
        
        mailer._ensure_valid_token()
        self.assertEqual(mailer.token, 'new_test_token')
        self.assertEqual(mock_post.call_count, 2)

    def test_template_context_replacement(self):
        """Test template variable replacement"""
        template_content = """
        <html>
            <body>
                <h1>Hello {{ name }}!</h1>
                <p>Your order #{{ order_id }} total is ${{ amount }}</p>
            </body>
        </html>
        """
        
        expected_content = """
        <html>
            <body>
                <h1>Hello John!</h1>
                <p>Your order #12345 total is $99.99</p>
            </body>
        </html>
        """
        
        template_context = {
            'name': 'John',
            'order_id': '12345',
            'amount': '99.99'
        }
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            mailer = Mailer(**self.test_credentials)
            with patch.object(mailer, '_ensure_valid_token'):
                with patch('requests.post') as mock_post:
                    mock_response = MagicMock()
                    mock_response.status_code = 202
                    mock_post.return_value = mock_response
                    
                    mailer.send_email(
                        to_emails="test@example.com",
                        subject="Test",
                        template_path="test.html",
                        template_context=template_context
                    )
                    
                    # Get the email_data from the API call
                    called_data = mock_post.call_args[1]['json']
                    actual_content = called_data['message']['body']['content']
                    
                    self.assertEqual(actual_content.strip(), expected_content.strip())

    @patch('requests.post')
    def test_email_timeout(self, mock_post):
        """Test handling of request timeout"""
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        
        template_content = "<html><body>Test</body></html>"
        with patch('builtins.open', mock_open(read_data=template_content)):
            mailer = Mailer(**self.test_credentials)
            result = mailer.send_email(
                to_emails="test@example.com",
                subject="Test Subject",
                template_path="template.html",
                template_context={}
            )
        
        self.assertFalse(result['success'])
        self.assertIn('Request timed out', result['message'])

    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()

    def test_initialization_with_direct_credentials(self):
        """Test initialization with directly provided credentials"""
        mailer = Mailer(**self.test_credentials)
        
        self.assertEqual(mailer.tenant_id, 'test_tenant')
        self.assertEqual(mailer.client_id, 'test_client')
        self.assertEqual(mailer.client_secret, 'test_secret')
        self.assertEqual(mailer.sender_email, 'sender@test.com')

    def test_initialization_with_env_variables(self):
        """Test initialization using environment variables"""
        mailer = Mailer()
        
        self.assertEqual(mailer.tenant_id, 'env_tenant')
        self.assertEqual(mailer.client_id, 'env_client')
        self.assertEqual(mailer.client_secret, 'env_secret')
        self.assertEqual(mailer.sender_email, 'env_sender@test.com')

        
    @patch('requests.post')
    def test_token_refresh(self, mock_post):
        """Test token refresh mechanism"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        mailer = Mailer(**self.test_credentials)
        mailer._refresh_token()

        self.assertEqual(mailer.token, 'test_token')
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_token_refresh_failure(self, mock_post):
        """Test token refresh failure handling"""
        mock_post.side_effect = Exception("Token refresh failed")

        mailer = Mailer(**self.test_credentials)
        with self.assertRaises(Exception):
            mailer._refresh_token()

    @patch('requests.post')
    def test_send_email_success(self, mock_post):
        """Test successful template email sending"""
        # Mock token refresh
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_token_response.status_code = 200

        # Mock email send
        mock_email_response = MagicMock()
        mock_email_response.status_code = 202

        mock_post.side_effect = [mock_token_response, mock_email_response]

        template_content = "<html><body>Hello {{ name }}!</body></html>"
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            mailer = Mailer(**self.test_credentials)
            result = mailer.send_email(
                to_emails="test@example.com",
                subject="Test Subject",
                template_path="fake_template.html",
                template_context={"name": "John"}
            )

        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Email sent successfully')

    @patch('requests.post')
    def test_send_email_multiple_recipients(self, mock_post):
        """Test sending email to multiple recipients"""
        # Mock responses
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_token_response.status_code = 200

        mock_email_response = MagicMock()
        mock_email_response.status_code = 202

        mock_post.side_effect = [mock_token_response, mock_email_response]

        template_content = "<html><body>Test</body></html>"
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            mailer = Mailer(**self.test_credentials)
            result = mailer.send_email(
                to_emails=["test1@example.com", "test2@example.com"],
                subject="Test Subject",
                template_path="fake_template.html",
                template_context={},
                cc_emails=["cc@example.com"],
                bcc_emails=["bcc@example.com"]
            )

        self.assertTrue(result['success'])

    def test_template_not_found(self):
        """Test handling of non-existent template file"""
        mailer = Mailer(**self.test_credentials)
        result = mailer.send_email(
            to_emails="test@example.com",
            subject="Test Subject",
            template_path="nonexistent_template.html",
            template_context={}
        )

        self.assertFalse(result['success'])
        self.assertIn('Error', result['message'])

    @patch('requests.post')
    def test_send_email_api_failure(self, mock_post):
        """Test handling of API failure"""
        # Mock token refresh success
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_token_response.status_code = 200

        # Mock email send failure
        mock_email_response = MagicMock()
        mock_email_response.status_code = 400
        mock_email_response.text = "Bad Request"

        mock_post.side_effect = [mock_token_response, mock_email_response]

        template_content = "<html><body>Test</body></html>"
        
        with patch('builtins.open', mock_open(read_data=template_content)):
            mailer = Mailer(**self.test_credentials)
            result = mailer.send_email(
                to_emails="test@example.com",
                subject="Test Subject",
                template_path="fake_template.html",
                template_context={}
            )

        self.assertFalse(result['success'])
        self.assertIn('Failed to send email', result['message'])

if __name__ == '__main__':
    unittest.main()