"""
Test Client for SurakshaSetu Legal RAG API
Updated to work with combined backend on port 3000
Includes comprehensive error handling and status checks
"""

import requests
import json
from typing import Dict, Any, Optional
import sys

class LegalRAGClient:
    """Client for interacting with the Legal RAG API on port 3000"""
    
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response with proper error checking"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Try to get error details from response
            try:
                error_detail = response.json().get('detail', str(e))
            except:
                error_detail = str(e)
            raise Exception(f"API Error ({response.status_code}): {error_detail}")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Connection Error: Cannot connect to {self.base_url}. Is the server running on port 3000?")
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Server might be overloaded.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request Error: {str(e)}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from server: {response.text[:100]}")
    
    def check_status(self) -> Dict[str, Any]:
        """Check API status"""
        print("📡 Checking API status...")
        response = requests.get(f"{self.base_url}/")
        return self._handle_response(response)
    
    def set_json_path(self, json_path: str) -> Dict[str, Any]:
        """Set the path to the legal JSON database"""
        print(f"📂 Setting JSON path: {json_path}")
        response = requests.post(
            f"{self.base_url}/set-json-path",
            json={"json_path": json_path}
        )
        return self._handle_response(response)
    
    def upload_json(self, file_path: str) -> Dict[str, Any]:
        """Upload a JSON file to the server"""
        print(f"📤 Uploading JSON file: {file_path}")
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.split('/')[-1], f, 'application/json')}
                # Don't use session for file upload to avoid Content-Type header conflict
                response = requests.post(
                    f"{self.base_url}/upload-json",
                    files=files
                )
            return self._handle_response(response)
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error uploading file: {str(e)}")
    
    def query(self, question: str, k: int = 5) -> Dict[str, Any]:
        """Query the legal database"""
        response = requests.post(
            f"{self.base_url}/query",
            json={
                "question": question,
                "k": k
            }
        )
        return self._handle_response(response)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get detailed system status"""
        print("📊 Getting system status...")
        response = requests.get(f"{self.base_url}/status")
        return self._handle_response(response)
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return self._handle_response(response)
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get detailed server information"""
        print("ℹ️  Getting server info...")
        response = requests.get(f"{self.base_url}/info")
        return self._handle_response(response)
    
    def test_all_endpoints(self) -> Dict[str, Any]:
        """Run all endpoint tests"""
        print("🧪 Running all endpoint tests...")
        response = requests.get(f"{self.base_url}/test/all-endpoints")
        return self._handle_response(response)
    
    def get_sample_queries(self) -> Dict[str, Any]:
        """Get sample queries"""
        print("📝 Getting sample queries...")
        response = requests.get(f"{self.base_url}/test/sample-queries")
        return self._handle_response(response)

def print_header(text: str):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80)

def print_section(text: str):
    """Print a formatted section"""
    print("\n" + "-" * 80)
    print(text)
    print("-" * 80)

def display_answer(result: Dict[str, Any]):
    """Display query result in a formatted way"""
    print_header("ANSWER")
    
    # Display the answer
    print(result.get('answer', 'No answer provided'))
    
    # Display metadata
    print("\n" + "-" * 80)
    
    if result.get('sources'):
        print(f"📚 Sources: {', '.join(result['sources'])}")
    
    if result.get('query_type'):
        print(f"🏷️  Query Type: {result['query_type']}")
    
    if result.get('chunks_retrieved') is not None:
        print(f"📊 Chunks Retrieved: {result['chunks_retrieved']}")
    
    print("=" * 80)

def main():
    """Example usage of the Legal RAG API Client"""
    
    # Initialize client (port 3000)
    client = LegalRAGClient("http://localhost:3000")
    
    print_header("SurakshaSetu Legal RAG API - Test Client (Port 3000)")
    
    try:
        # 1. Health check
        print("\n🏥 Performing health check...")
        health = client.health_check()
        print(f"   ✅ Health: {health.get('status', 'unknown')}")
        print(f"   🔌 Port: {health.get('port', 'unknown')}")
    except Exception as e:
        print(f"   ❌ Health check failed: {str(e)}")
        print("\n⚠️  Make sure the server is running:")
        print("   python combined_backend.py")
        print("   OR")
        print("   uvicorn combined_backend:app --reload --host 0.0.0.0 --port 3000")
        return
    
    # 2. Get server info
    print("\nℹ️  Getting server information...")
    try:
        info = client.get_server_info()
        print(f"   ✅ Server: {info['server']['title']}")
        print(f"   📦 Version: {info['server']['version']}")
        print(f"   🔌 Port: {info['server']['port']}")
        print(f"   🤖 LLM Model: {info['models']['llm_model']}")
        print(f"   🧠 Embedding Model: {info['models']['embedding_model']}")
    except Exception as e:
        print(f"   ⚠️  Could not get server info: {str(e)}")
    
    # 3. Check status
    print("\n📊 Checking API status...")
    try:
        status = client.check_status()
        print(f"   ✅ Status: {status.get('status', 'unknown')}")
        print(f"   📦 Models loaded: {status.get('model_loaded', False)}")
        print(f"   📄 JSON loaded: {status.get('json_loaded', False)}")
        
        if not status.get('model_loaded'):
            print("\n   ⚠️  Models not loaded! Server may not be ready.")
            return
    except Exception as e:
        print(f"   ❌ Status check failed: {str(e)}")
        return
    
    # 4. Set JSON path (or upload JSON file)
    if not status.get('json_loaded'):
        print_section("Loading Legal Database")
        print("Choose an option:")
        print("   a) Set JSON path (if file is already on server)")
        print("   b) Upload JSON file from local machine")
        
        choice = input("\nEnter choice (a/b): ").strip().lower()
        
        try:
            if choice == 'a':
                json_path = input("Enter JSON file path on server: ").strip()
                if not json_path:
                    print("❌ No path provided. Exiting.")
                    return
                result = client.set_json_path(json_path)
                print(f"✅ {result.get('message', 'Success')}")
                
            elif choice == 'b':
                json_file = input("Enter local JSON file path: ").strip()
                if not json_file:
                    print("❌ No file provided. Exiting.")
                    return
                result = client.upload_json(json_file)
                print(f"✅ {result.get('message', 'Success')}")
                
            else:
                print("❌ Invalid choice. Exiting.")
                return
        except Exception as e:
            print(f"❌ Error loading database: {str(e)}")
            return
    else:
        print("\n✅ Legal database already loaded!")
    
    # 5. Show sample queries
    print_section("Sample Queries Available")
    try:
        samples = client.get_sample_queries()
        for category_info in samples.get('sample_queries', []):
            print(f"\n{category_info['category']}:")
            for q in category_info['questions']:
                print(f"   • {q}")
    except:
        print("   • What is POSH Act?")
        print("   • What are the penalties under POCSO?")
        print("   • How do I file a complaint for domestic violence?")
    
    # 6. Interactive query loop
    print_section("Query Mode - Ask Legal Questions")
    print("\nType 'quit', 'exit', or 'q' to exit")
    
    question_count = 0
    
    while True:
        print("\n" + "─" * 80)
        try:
            question = input("💬 Your question: ").strip()
        except EOFError:
            break
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not question:
            continue
        
        question_count += 1
        print(f"\n🤔 Processing question #{question_count}...")
        
        try:
            result = client.query(question, k=5)
            display_answer(result)
            
        except Exception as e:
            print(f"\n❌ Error processing query: {str(e)}")
            print("\nTips:")
            print("   • Check if the legal database is properly loaded")
            print("   • Verify your question is clear and specific")
            print("   • Check server logs for detailed error information")

def test_api_endpoints():
    """Test all API endpoints"""
    client = LegalRAGClient("http://localhost:3000")
    
    print_header("Testing All API Endpoints (Port 3000)")
    
    print("\n🧪 Running automated tests...")
    try:
        results = client.test_all_endpoints()
        
        print(f"\n{'='*80}")
        print(f"Test Results Summary".center(80))
        print(f"{'='*80}")
        
        summary = results.get('summary', {})
        print(f"\n📊 Total Tests: {summary.get('total_tests', 0)}")
        print(f"✅ Passed: {summary.get('passed', 0)}")
        print(f"❌ Failed: {summary.get('failed', 0)}")
        print(f"📈 Success Rate: {summary.get('success_rate', 'N/A')}")
        
        print(f"\n{'='*80}")
        print("Individual Test Results".center(80))
        print(f"{'='*80}\n")
        
        for test in results.get('tests', []):
            status_icon = "✅" if test['status'] == 'passed' else "❌"
            print(f"{status_icon} {test['name']}: {test['status'].upper()}")
            if test['status'] == 'failed':
                print(f"   Error: {test.get('error', 'Unknown error')}")
            print()
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {str(e)}")
        print("\nManually testing individual endpoints...")
        
        tests = [
            ("Health Check", lambda: client.health_check()),
            ("Root Status", lambda: client.check_status()),
            ("System Status", lambda: client.get_system_status()),
            ("Server Info", lambda: client.get_server_info()),
        ]
        
        for test_name, test_func in tests:
            print(f"\nTesting: {test_name}")
            try:
                result = test_func()
                print(f"   ✅ Success")
                print(f"   {json.dumps(result, indent=2)[:200]}...")
            except Exception as e:
                print(f"   ❌ Failed: {str(e)}")

if __name__ == "__main__":
    try:
        # Check if test mode
        if len(sys.argv) > 1 and sys.argv[1] == 'test':
            test_api_endpoints()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
