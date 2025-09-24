import requests
import json

# Test data
test_data = {
    "question_text": "Build Your Custom Chocolate Pack - Test",
    "short_text": "Custom Chocolate Pack",
    "solutions_metadata": [
        {
            "code_details": [
                {
                    "default_code": True,
                    "code_data": """<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
    <h1>Test HTML</h1>
    <input type="text" id="test-input">
    <button id="calculate">Calculate</button>
    <span id="result">0</span>
</body>
</html>""",
                    "language": "HTML"
                },
                {
                    "default_code": True,
                    "code_data": "body { font-family: Arial; background: #f0f0f0; }",
                    "language": "CSS"
                },
                {
                    "default_code": True,
                    "code_data": "document.getElementById('calculate').addEventListener('click', function() { document.getElementById('result').textContent = 'Clicked'; });",
                    "language": "JAVASCRIPT"
                }
            ]
        }
    ],
    "test_cases": [
        {
            "id": "test-1",
            "display_text": "When the Calculate button is clicked, it should show result",
            "criteria": "document.getElementById('calculate').click(); const result = document.getElementById('result').textContent; assert(result === 'Clicked');",
            "evaluation_type": "CLIENT_SIDE_EVALUATION",
            "order": 1,
            "reason_for_failure": None,
            "weightage": 10
        },
        {
            "id": "test-2", 
            "display_text": "Input field should exist",
            "criteria": "const input = document.getElementById('test-input'); assert(input !== null);",
            "evaluation_type": "CLIENT_SIDE_EVALUATION",
            "order": 2,
            "reason_for_failure": None,
            "weightage": 10
        }
    ],
    "tag_names": [
        "SUB_TOPIC_CSS_FLEXBOX",
        "COURSE_Modern_Responsive_Web_Design", 
        "MODULE_Introduction_to_CSS_Flexbox",
        "UNIT_Introduction_to_CSS_Flexbox"
    ],
    "replica_type": "webcoding",
    "num_replicas": 2
}

def test_api():
    url = "http://127.0.0.1:5000/api/generate-replicas"
    headers = {"Content-Type": "application/json"}
    
    try:
        print("Testing API endpoint...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data, headers=headers, timeout=60)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS!")
            print(f"Generated {len(result.get('replicas', {}))} replicas")
            
            # Print first replica details
            if result.get('replicas'):
                first_replica_key = list(result['replicas'].keys())[0]
                first_replica = result['replicas'][first_replica_key]
                
                print(f"\nFirst Replica ({first_replica_key}):")
                print(f"- Short Text: {first_replica.get('short_text', 'N/A')}")
                print(f"- Question Length: {len(first_replica.get('question_text', ''))}")
                print(f"- HTML Length: {len(first_replica.get('html_code', ''))}")
                print(f"- CSS Length: {len(first_replica.get('css_code', ''))}")
                print(f"- JS Length: {len(first_replica.get('js_code', ''))}")
                print(f"- Test Cases: {len(first_replica.get('test_cases', []))} structured test cases")
                
                # Show test case structure
                if first_replica.get('test_cases'):
                    print("\nTest Case Structure:")
                    for i, tc in enumerate(first_replica['test_cases'][:2]):  # Show first 2
                        print(f"  Test {i+1}:")
                        print(f"    ID: {tc.get('id')}")
                        print(f"    Order: {tc.get('order')}")
                        print(f"    Display Text: {tc.get('display_text', '')[:100]}...")
                        print(f"    Weightage: {tc.get('weightage')}")
                
            # Show token usage
            session_usage = result.get('session_usage', {})
            print(f"\nToken Usage:")
            print(f"- Session: {session_usage.get('session_tokens', 0)}")
            print(f"- Total: {session_usage.get('total_tokens', 0)}")
            
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ REQUEST ERROR: {e}")
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON DECODE ERROR: {e}")
        print(f"Response text: {response.text}")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    test_api()