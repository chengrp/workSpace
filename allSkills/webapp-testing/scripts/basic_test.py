#!/usr/bin/env python3
"""
Basic web application testing script.
Provides common testing utilities for web applications.
"""

import requests
import json
import time
from urllib.parse import urljoin

class WebAppTester:
    """Basic web application testing utility."""

    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []

    def test_endpoint(self, endpoint, method="GET", data=None, expected_status=200):
        """Test a single API endpoint."""
        url = urljoin(self.base_url, endpoint)

        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            elif method == "PUT":
                response = self.session.put(url, json=data)
            elif method == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            result = {
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": time.time()
            }

            if not success:
                result["error"] = f"Expected {expected_status}, got {response.status_code}"
                if response.text:
                    result["response_body"] = response.text[:500]  # Truncate long responses

            self.test_results.append(result)
            return result

        except Exception as e:
            error_result = {
                "endpoint": endpoint,
                "method": method,
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
            self.test_results.append(error_result)
            return error_result

    def test_form_submission(self, endpoint, form_data):
        """Test form submission (simplified version)."""
        return self.test_endpoint(endpoint, method="POST", data=form_data)

    def test_authentication(self, login_endpoint, credentials):
        """Test authentication flow."""
        # Test login
        login_result = self.test_endpoint(
            login_endpoint,
            method="POST",
            data=credentials,
            expected_status=200
        )

        if login_result.get("success"):
            # Store authentication token if present in response
            try:
                response_data = json.loads(self.session.get(login_endpoint).text)
                if "token" in response_data:
                    self.session.headers.update({
                        "Authorization": f"Bearer {response_data['token']}"
                    })
            except:
                pass

        return login_result

    def run_smoke_test(self, endpoints):
        """Run a basic smoke test on critical endpoints."""
        print("Running smoke tests...")
        for endpoint in endpoints:
            print(f"Testing {endpoint}...")
            result = self.test_endpoint(endpoint)
            status = "✓" if result.get("success") else "✗"
            print(f"  {status} {endpoint}: {result.get('status_code', 'error')}")

        return self.test_results

    def generate_report(self):
        """Generate a test report."""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r.get("success"))
        failed = total - passed

        report = {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "success_rate": (passed / total * 100) if total > 0 else 0
            },
            "details": self.test_results
        }

        return report

    def save_report(self, filename="test_report.json"):
        """Save test report to file."""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {filename}")
        return report

def main():
    """Example usage of the WebAppTester."""
    tester = WebAppTester("http://localhost:3000")

    # Define endpoints to test
    endpoints = [
        "/",
        "/api/health",
        "/api/users",
        "/api/products"
    ]

    # Run smoke tests
    tester.run_smoke_test(endpoints)

    # Example: Test authentication
    # credentials = {"username": "test", "password": "test123"}
    # tester.test_authentication("/api/login", credentials)

    # Generate and save report
    report = tester.save_report()

    print(f"\nTest Summary:")
    print(f"  Total tests: {report['summary']['total_tests']}")
    print(f"  Passed: {report['summary']['passed']}")
    print(f"  Failed: {report['summary']['failed']}")
    print(f"  Success rate: {report['summary']['success_rate']:.1f}%")

if __name__ == "__main__":
    main()