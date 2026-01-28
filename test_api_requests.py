"""
Sample API Test Requests for Flask Authentication System
Run this file to test all API endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

class TestRunner:
    def __init__(self):
        self.session = requests.Session()
        self.user_data = {
            'username': 'testuser123',
            'email': 'testuser@example.com',
            'password': 'SecurePassword123!',
            'new_password': 'NewPassword456!'
        }
    
    def print_response(self, title, response):
        """Pretty print response"""
        print(f"\n{'='*60}")
        print(f"TEST: {title}")
        print(f"{'='*60}")
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
    
    def test_register(self):
        """Test user registration"""
        url = f"{BASE_URL}/register"
        payload = {
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.session.post(url, json=payload)
        self.print_response("User Registration", response)
        return response.status_code == 201
    
    def test_register_duplicate(self):
        """Test duplicate username registration"""
        url = f"{BASE_URL}/register"
        payload = {
            'username': self.user_data['username'],
            'email': 'different@example.com',
            'password': self.user_data['password']
        }
        response = self.session.post(url, json=payload)
        self.print_response("Duplicate Username Registration (Should Fail)", response)
        return response.status_code == 400
    
    def test_register_missing_fields(self):
        """Test registration with missing fields"""
        url = f"{BASE_URL}/register"
        payload = {'username': self.user_data['username']}
        response = self.session.post(url, json=payload)
        self.print_response("Registration with Missing Fields (Should Fail)", response)
        return response.status_code == 400
    
    def test_login_before_verification(self):
        """Test login before email verification"""
        url = f"{BASE_URL}/login"
        payload = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.session.post(url, json=payload)
        self.print_response("Login Before Email Verification (Should Fail)", response)
        return response.status_code == 401
    
    def test_forgot_password(self):
        """Test forgot password request"""
        url = f"{BASE_URL}/forgot-password"
        payload = {'email': self.user_data['email']}
        response = self.session.post(url, json=payload)
        self.print_response("Forgot Password Request", response)
        return response.status_code == 200
    
    def test_resend_verification(self):
        """Test resend verification email"""
        url = f"{BASE_URL}/resend-verification"
        payload = {'email': self.user_data['email']}
        response = self.session.post(url, json=payload)
        self.print_response("Resend Verification Email", response)
        return response.status_code == 200
    
    def test_index(self):
        """Test home endpoint"""
        url = f"{BASE_URL}/"
        response = self.session.get(url)
        self.print_response("Home Endpoint", response)
        return response.status_code == 200
    
    def test_profile_without_auth(self):
        """Test profile access without authentication"""
        url = f"{BASE_URL}/profile"
        response = self.session.get(url)
        self.print_response("Profile Access Without Auth (Should Fail)", response)
        # Should redirect or return 401
        return response.status_code in [301, 302, 401]
    
    def run_all_tests(self):
        """Run all test cases"""
        print("\n" + "="*60)
        print("FLASK AUTHENTICATION SYSTEM - API TEST SUITE")
        print("="*60)
        
        tests = [
            ("Index/Home Endpoint", self.test_index),
            ("User Registration", self.test_register),
            ("Duplicate Username Registration", self.test_register_duplicate),
            ("Registration with Missing Fields", self.test_register_missing_fields),
            ("Login Before Email Verification", self.test_login_before_verification),
            ("Forgot Password Request", self.test_forgot_password),
            ("Resend Verification Email", self.test_resend_verification),
            ("Profile Access Without Auth", self.test_profile_without_auth),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                passed = test_func()
                results.append((test_name, "✓ PASSED" if passed else "✗ FAILED"))
            except Exception as e:
                results.append((test_name, f"✗ ERROR: {str(e)}"))
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        for test_name, result in results:
            print(f"{test_name}: {result}")
        
        passed_count = sum(1 for _, result in results if "PASSED" in result)
        total_count = len(results)
        print(f"\nTotal: {passed_count}/{total_count} tests passed")

if __name__ == "__main__":
    runner = TestRunner()
    runner.run_all_tests()
