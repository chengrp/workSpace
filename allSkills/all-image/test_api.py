#!/usr/bin/env python3
"""Test Google AI API without emoji"""
import os
import requests
import base64
from datetime import datetime

API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyAQlOh5gnPRNTKrnPXYlCuLHAqgnLHc_GY')
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

def test_api():
    """Test API connection"""
    try:
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": "A cute cat, simple style"}]
            }]
        }

        url = f"{API_URL}?key={API_KEY}"
        print(f"Sending request to Google AI API...")

        response = requests.post(url, headers=headers, json=data, timeout=60)

        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Response keys: {result.keys()}")

            # Try to extract image
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                print(f"Candidate keys: {candidate.keys()}")

                if 'content' in candidate:
                    content = candidate['content']
                    print(f"Content keys: {content.keys()}")

                    if 'parts' in content:
                        for i, part in enumerate(content['parts']):
                            print(f"Part {i} keys: {part.keys()}")
                            if 'inlineData' in part:
                                b64 = part['inlineData'].get('data')
                                if b64:
                                    # Save image
                                    output_path = f"test_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                                    with open(output_path, 'wb') as f:
                                        f.write(base64.b64decode(b64))
                                    print(f"SUCCESS! Image saved to: {output_path}")
                                    return True

            print("No image data found in response")
            print(f"Full response: {result}")
        else:
            print(f"API Error: {response.text}")

        return False

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
