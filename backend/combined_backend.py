"""
Combined FastAPI Backend for SurakshaSetu - Legal RAG System
Runs on port 3000 and includes testing functionality
Preserves all original RAG + LangGraph code without modifications
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
import os
import json
import time
import re
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Updated import - use google.genai instead of deprecated google.generativeai
try:
    import google.genai as genai
    from google.genai import types
    USING_NEW_SDK = True
except ImportError:
    import google.generativeai as genai
    USING_NEW_SDK = False
    print("⚠️ Using deprecated google.generativeai. Please upgrade to google-genai package")

# Configuration
class Config:
    """Configuration for the system"""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "INSERT API KEY HERE")
    GEMINI_MODEL = "gemini-2.0-flash-lite"  # Updated model name
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    MAX_RETRIES = 10
    RETRY_DELAY = 2
    JSON_DATA_PATH = None

# Global instances
app_state = {
    "embedder": None,
    "gemini_client": None,
    "graphrag_system": None
}

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    print("🚀 Starting Combined FastAPI server on port 3000...")
    print("🔧 Loading embedding model...")
    app_state["embedder"] = SentenceTransformer(Config.EMBEDDING_MODEL)
    print("✅ Embedding model loaded!")
    
    print("🔧 Setting up Gemini API...")
    if USING_NEW_SDK:
        app_state["gemini_client"] = genai.Client(api_key=Config.GEMINI_API_KEY)
    else:
        genai.configure(api_key=Config.GEMINI_API_KEY)
        app_state["gemini_client"] = genai.GenerativeModel(Config.GEMINI_MODEL)
    print("Gemini API configured!")
    print("Server ready on http://localhost:3000")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down server...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="SurakshaSetu Legal RAG API - Combined Backend",
    description="API for querying legal information using RAG + LangGraph (Running on port 3000)",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class QueryRequest(BaseModel):
    """Request model for querying the RAG system"""
    question: str
    k: int = 5

class QueryResponse(BaseModel):
    """Response model for query results"""
    answer: str
    sources: Optional[List[str]] = None
    query_type: Optional[str] = None
    chunks_retrieved: Optional[int] = None

class ConfigRequest(BaseModel):
    """Request model for setting JSON path"""
    json_path: str

class StatusResponse(BaseModel):
    """Response model for system status"""
    status: str
    message: str
    json_loaded: bool
    model_loaded: bool

# Helper Functions
def call_gemini_with_retry(client, prompt, max_retries=Config.MAX_RETRIES):
    """Call Gemini API with exponential backoff for rate limiting"""
    for attempt in range(max_retries):
        try:
            if USING_NEW_SDK:
                response = client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=prompt
                )
                return response.text.strip()
            else:
                response = client.generate_content(prompt)
                return response.text.strip()
        except Exception as e:
            error_msg = str(e).lower()
            
            if 'resource_exhausted' in error_msg or 'rate limit' in error_msg or '429' in error_msg:
                if attempt < max_retries - 1:
                    wait_time = Config.RETRY_DELAY * (2 ** attempt)
                    print(f"⚠️ Rate limit hit. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    return "Rate limit exceeded. Please wait a moment and try again."
            else:
                print(f"❌ Gemini API Error: {str(e)}")
                return f"Error: {str(e)}"
    
    return "Max retries reached. Please try again later."

# ImprovedGraphRAGSystem Class - PRESERVED WITHOUT MODIFICATION
class ImprovedGraphRAGSystem:
    """
    Improved GraphRAG with better chunking strategy
    Preserves all JSON fields and creates contextual chunks
    """
    
    def __init__(self, json_path: str, embedder, gemini_client):
        self.json_path = json_path
        self.chunks_with_meta = []
        self.faiss_index = None
        self.gemini_client = gemini_client
        self.embedder = embedder
        
        # Load and process JSON
        self._load_and_chunk_json()
        self._build_faiss_index()
    
    def _load_and_chunk_json(self):
        """Load JSON and create smart chunks with metadata"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        all_chunks = []
        
        for law in data.get("laws", []):
            law_name = law.get("name", "Unknown Law")
            law_desc = law.get("description", "")
            
            # Create law overview chunk
            overview_text = f"Law: {law_name}\n\nDescription: {law_desc}"
            all_chunks.append({
                "text": overview_text,
                "law": law_name,
                "type": "overview",
                "metadata": {}
            })
            
            # Process sections
            for section in law.get("sections", []):
                section_num = section.get("section_number", "")
                section_title = section.get("title", "")
                section_desc = section.get("description", "")
                
                section_text = f"Law: {law_name}\nSection {section_num}: {section_title}\n\n{section_desc}"
                
                all_chunks.append({
                    "text": section_text,
                    "law": law_name,
                    "type": "section",
                    "metadata": {
                        "section_number": section_num,
                        "section_title": section_title
                    }
                })
            
            # Process case studies
            for case in law.get("case_studies", []):
                case_name = case.get("case_name", "")
                facts = case.get("facts", "")
                outcome = case.get("outcome", "")
                significance = case.get("significance", "")
                
                case_text = f"""Law: {law_name}
Case Study: {case_name}

Facts: {facts}

Outcome: {outcome}

Significance: {significance}"""
                
                all_chunks.append({
                    "text": case_text,
                    "law": law_name,
                    "type": "case_study",
                    "metadata": {
                        "case_name": case_name
                    }
                })
            
            # Process penalties
            for penalty in law.get("penalties", []):
                offense = penalty.get("offense", "")
                penalty_desc = penalty.get("penalty", "")
                
                penalty_text = f"Law: {law_name}\nOffense: {offense}\nPenalty: {penalty_desc}"
                
                all_chunks.append({
                    "text": penalty_text,
                    "law": law_name,
                    "type": "penalty",
                    "metadata": {
                        "offense": offense
                    }
                })
            
            # Process procedures
            for proc in law.get("procedures", []):
                step = proc.get("step", "")
                action = proc.get("action", "")
                
                proc_text = f"Law: {law_name}\nProcedure Step {step}: {action}"
                
                all_chunks.append({
                    "text": proc_text,
                    "law": law_name,
                    "type": "procedure",
                    "metadata": {
                        "step": step
                    }
                })
        
        self.chunks_with_meta = all_chunks
        print(f"✅ Created {len(all_chunks)} contextual chunks")
    
    def _build_faiss_index(self):
        """Build FAISS index from chunks"""
        chunk_texts = [c['text'] for c in self.chunks_with_meta]
        embeddings = self.embedder.encode(chunk_texts, show_progress_bar=True)
        
        dimension = embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatIP(dimension)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.faiss_index.add(embeddings)
        
        print(f"✅ FAISS index built with {len(chunk_texts)} chunks")
    
    def _analyze_query(self, question: str) -> Dict[str, bool]:
        """Analyze what type of information the query needs"""
        q_lower = question.lower()
        
        comparison_keywords = ['difference', 'compare', 'vs', 'versus', 'between']
        needs_comparison = any(kw in q_lower for kw in comparison_keywords)
        
        procedure_keywords = ['how to', 'procedure', 'process', 'file', 'steps', 'complaint']
        needs_procedure = any(kw in q_lower for kw in procedure_keywords)
        
        case_keywords = ['example', 'case', 'instance', 'story', 'happened']
        needs_cases = any(kw in q_lower for kw in case_keywords)
        
        penalty_keywords = ['penalty', 'punishment', 'sentence', 'fine', 'imprisonment']
        needs_penalties = any(kw in q_lower for kw in penalty_keywords)
        
        situational_keywords = ['if i', 'what should i', 'can i', 'my situation', 'help me']
        is_situational = any(kw in q_lower for kw in situational_keywords)
        
        return {
            'needs_comparison': needs_comparison,
            'needs_procedure': needs_procedure,
            'needs_cases': needs_cases,
            'needs_penalties': needs_penalties,
            'is_situational': is_situational
        }
    
    def query(self, question: str, k: int = 5):
        """Query the system with smart retrieval based on query type"""
        try:
            # Analyze query
            query_info = self._analyze_query(question)
            
            # Encode question
            q_embedding = self.embedder.encode([question])
            faiss.normalize_L2(q_embedding)
            
            # Retrieve chunks
            scores, indices = self.faiss_index.search(q_embedding, k * 2)
            
            retrieved_chunks = []
            seen_laws = set()
            sources = set()
            
            # Smart filtering based on query type
            for idx in indices[0]:
                if idx >= len(self.chunks_with_meta):
                    continue
                
                chunk = self.chunks_with_meta[idx]
                chunk_type = chunk['type']
                law_name = chunk['law']
                
                # Type-based filtering
                if query_info['needs_procedure'] and chunk_type != 'procedure':
                    continue
                if query_info['needs_cases'] and chunk_type != 'case_study':
                    continue
                if query_info['needs_penalties'] and chunk_type != 'penalty':
                    continue
                
                retrieved_chunks.append(chunk)
                seen_laws.add(law_name)
                sources.add(law_name)
                
                if len(retrieved_chunks) >= k:
                    break
            
            # If we didn't get enough chunks, add more without filtering
            if len(retrieved_chunks) < k:
                for idx in indices[0]:
                    if idx >= len(self.chunks_with_meta):
                        continue
                    chunk = self.chunks_with_meta[idx]
                    if chunk not in retrieved_chunks:
                        retrieved_chunks.append(chunk)
                        sources.add(chunk['law'])
                        if len(retrieved_chunks) >= k:
                            break
            
            sources = sorted(list(sources))
            
            # Build context
            context_parts = []
            for chunk in retrieved_chunks:
                context_parts.append(f"[{chunk['type'].upper()}]\n{chunk['text']}")
            
            context = "\n\n" + "=" * 60 + "\n\n".join(context_parts)
            
            # Select prompt based on query type
            if query_info['needs_comparison']:
                system_instruction = """You are SurakshaSetu, a legal awareness assistant.

YOUR MISSION: Compare and contrast different laws clearly and accurately.

YOUR RESPONSE MUST:
1. Identify the laws being compared
2. Create a clear comparison with:
   - Purpose/Objective of each law
   - Who each law protects
   - Key differences
   - When to use which law
3. Use simple language
4. Use tables or bullet points for clarity

FORMAT:
📊 **Comparison**: [Law 1] vs [Law 2]

**[Law 1 Name]**:
- Purpose: [...]
- Protects: [...]
- Key Features: [...]

**[Law 2 Name]**:
- Purpose: [...]
- Protects: [...]
- Key Features: [...]

**Key Differences**:
| Aspect | [Law 1] | [Law 2] |
|--------|---------|---------|
| [...] | [...] | [...] |

**When to Use**:
- Use [Law 1] when: [...]
- Use [Law 2] when: [...]

CRITICAL RULES:
- Use ONLY information from the provided context
- Do NOT mix up different laws
- Be very clear about which information belongs to which law"""
            
            else:
                system_instruction = """You are SurakshaSetu, a legal awareness assistant for women and child protection laws.

YOUR MISSION:
- Explain laws in simple, clear language
- Make legal information accessible to everyone
- Provide practical information about rights and protections

YOUR RESPONSE MUST:
1. Identify the relevant law(s) from the context
2. Explain clearly:
   - What the law is about
   - Who it protects
   - Key provisions
   - How to use it (if relevant)
3. Include case examples if available in the context
4. Use simple language (10th grade reading level)

FORMAT:
📜 **Law**: [Law name]

**What It Is**: [Simple explanation]

**Who It Protects**: [...]

**Key Points**:
- [Point 1]
- [Point 2]
- [Point 3]

📖 **Example** (if available in context): [Case example]

💡 **Practical Information**: [How to use this law]

CRITICAL RULES:
- Use ONLY information from the provided context
- Use simple, clear language
- Break down legal jargon
- Do NOT give legal advice
- If context has case examples, USE THEM
- If asked for advice, say "consult a qualified lawyer" """
            
            # Create full prompt
            full_prompt = f"""{system_instruction}

{"="*80}
LEGAL CONTEXT FROM DATABASE:
{"="*80}

{context}

{"="*80}
USER QUESTION: {question}
{"="*80}

Provide a clear, helpful answer following ALL the rules above:"""
            
            # Call Gemini with retry handling
            answer = call_gemini_with_retry(self.gemini_client, full_prompt)
            
            # Add sources
            if sources and not answer.startswith("Error") and not answer.startswith("Rate limit"):
                answer += f"\n\n{'─'*60}\n📚 **Sources**: {', '.join(sources)}"
            
            return answer, sources, query_info, len(retrieved_chunks)
        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Error in query method:\n{error_details}")
            raise Exception(f"Error querying database: {str(e)}")

# ============================================================================
# API ENDPOINTS - ORIGINAL FUNCTIONALITY PRESERVED
# ============================================================================

@app.get("/", response_model=StatusResponse)
async def root():
    """Root endpoint - check API status"""
    return {
        "status": "online",
        "message": "SurakshaSetu Legal RAG API is running on port 3000",
        "json_loaded": app_state["graphrag_system"] is not None,
        "model_loaded": app_state["embedder"] is not None and app_state["gemini_client"] is not None
    }

@app.post("/set-json-path", response_model=StatusResponse)
async def set_json_path(config: ConfigRequest):
    """Set the path to the legal JSON database"""
    try:
        if not os.path.exists(config.json_path):
            raise HTTPException(status_code=404, detail=f"JSON file not found at: {config.json_path}")
        
        Config.JSON_DATA_PATH = config.json_path
        app_state["graphrag_system"] = ImprovedGraphRAGSystem(
            config.json_path,
            app_state["embedder"],
            app_state["gemini_client"]
        )
        
        return {
            "status": "success",
            "message": f"Legal database loaded successfully from {config.json_path}",
            "json_loaded": True,
            "model_loaded": True
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading JSON: {str(e)}")

@app.post("/upload-json")
async def upload_json(file: UploadFile = File(...)):
    """Upload a JSON file and load it into the system"""
    try:
        # Save uploaded file
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Load into GraphRAG system
        Config.JSON_DATA_PATH = file_path
        app_state["graphrag_system"] = ImprovedGraphRAGSystem(
            file_path,
            app_state["embedder"],
            app_state["gemini_client"]
        )
        
        return {
            "status": "success",
            "message": f"JSON file '{file.filename}' uploaded and loaded successfully",
            "json_loaded": True,
            "model_loaded": True,
            "file_path": file_path
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading JSON: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_legal_database(request: QueryRequest):
    """Query the legal database with a question"""
    if app_state["graphrag_system"] is None:
        raise HTTPException(
            status_code=400,
            detail="Legal database not loaded. Please set JSON path or upload JSON file first."
        )
    
    try:
        answer, sources, query_info, chunks_retrieved = app_state["graphrag_system"].query(
            request.question,
            k=request.k
        )
        
        query_type = "general"
        if query_info.get('is_situational'):
            query_type = "situational"
        elif query_info.get('needs_comparison'):
            query_type = "comparison"
        elif query_info.get('needs_procedure'):
            query_type = "procedure"
        elif query_info.get('needs_cases'):
            query_type = "case_based"
        
        return {
            "answer": answer,
            "sources": sources,
            "query_type": query_type,
            "chunks_retrieved": chunks_retrieved
        }
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Error processing query:\n{error_details}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get current system status"""
    return {
        "status": "online",
        "message": "System operational",
        "json_loaded": app_state["graphrag_system"] is not None,
        "model_loaded": app_state["embedder"] is not None and app_state["gemini_client"] is not None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "port": 3000}

# ============================================================================
# ADDITIONAL TEST ENDPOINTS (from testing_file.py functionality)
# ============================================================================

@app.get("/test/all-endpoints")
async def test_all_endpoints():
    """
    Test all API endpoints and return comprehensive diagnostics
    This endpoint provides the same functionality as the test mode in testing_file.py
    """
    results = {
        "timestamp": time.time(),
        "tests": []
    }
    
    # Test 1: Health Check
    try:
        health = await health_check()
        results["tests"].append({
            "name": "Health Check",
            "status": "passed",
            "result": health
        })
    except Exception as e:
        results["tests"].append({
            "name": "Health Check",
            "status": "failed",
            "error": str(e)
        })
    
    # Test 2: Root Status
    try:
        status = await root()
        results["tests"].append({
            "name": "Root Status",
            "status": "passed",
            "result": status.dict()
        })
    except Exception as e:
        results["tests"].append({
            "name": "Root Status",
            "status": "failed",
            "error": str(e)
        })
    
    # Test 3: System Status
    try:
        sys_status = await get_status()
        results["tests"].append({
            "name": "System Status",
            "status": "passed",
            "result": sys_status.dict()
        })
    except Exception as e:
        results["tests"].append({
            "name": "System Status",
            "status": "failed",
            "error": str(e)
        })
    
    # Summary
    passed = sum(1 for t in results["tests"] if t["status"] == "passed")
    total = len(results["tests"])
    results["summary"] = {
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "success_rate": f"{(passed/total)*100:.1f}%"
    }
    
    return results

@app.get("/test/sample-queries")
async def get_sample_queries():
    """
    Return sample queries for testing the RAG system
    Helps users understand what questions they can ask
    """
    return {
        "sample_queries": [
            {
                "category": "General Information",
                "questions": [
                    "What is POSH Act?",
                    "What is POCSO Act?",
                    "Tell me about Section 498A IPC"
                ]
            },
            {
                "category": "Penalties",
                "questions": [
                    "What are the penalties under POCSO?",
                    "What is the punishment for domestic violence?"
                ]
            },
            {
                "category": "Procedures",
                "questions": [
                    "How do I file a complaint for domestic violence?",
                    "What is the procedure to file a POSH complaint?"
                ]
            },
            {
                "category": "Comparisons",
                "questions": [
                    "What is the difference between POSH and POCSO?",
                    "Compare IPC 498A and Domestic Violence Act"
                ]
            }
        ],
        "usage_tip": "Use the /query endpoint with POST request containing: {\"question\": \"your question\", \"k\": 5}"
    }

@app.get("/info")
async def get_server_info():
    """
    Get detailed server information
    Provides information about the running server, loaded models, and configuration
    """
    return {
        "server": {
            "title": "SurakshaSetu Legal RAG API - Combined Backend",
            "version": "2.0.0",
            "port": 3000,
            "host": "localhost"
        },
        "models": {
            "embedding_model": Config.EMBEDDING_MODEL,
            "llm_model": Config.GEMINI_MODEL,
            "sdk_version": "new" if USING_NEW_SDK else "legacy"
        },
        "state": {
            "embedder_loaded": app_state["embedder"] is not None,
            "gemini_loaded": app_state["gemini_client"] is not None,
            "database_loaded": app_state["graphrag_system"] is not None,
            "database_path": Config.JSON_DATA_PATH
        },
        "endpoints": {
            "main": {
                "GET /": "Check API status",
                "GET /health": "Health check",
                "GET /status": "System status"
            },
            "data_management": {
                "POST /set-json-path": "Set JSON database path",
                "POST /upload-json": "Upload JSON database file"
            },
            "query": {
                "POST /query": "Query the legal database"
            },
            "testing": {
                "GET /test/all-endpoints": "Test all endpoints",
                "GET /test/sample-queries": "Get sample queries",
                "GET /info": "Get server information"
            }
        },
        "instructions": {
            "setup": [
                "1. Upload or set path to legal JSON database using /upload-json or /set-json-path",
                "2. Verify database is loaded using /status endpoint",
                "3. Start querying using /query endpoint"
            ],
            "query_example": {
                "endpoint": "POST /query",
                "body": {
                    "question": "What is POSH Act?",
                    "k": 5
                }
            }
        }
    }

# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("🚀 Starting SurakshaSetu Legal RAG API on port 3000")
    print("="*80)
    print("\n📋 Available endpoints:")
    print("   • http://localhost:3000/          - API Status")
    print("   • http://localhost:3000/health    - Health Check")
    print("   • http://localhost:3000/status    - System Status")
    print("   • http://localhost:3000/info      - Server Info")
    print("   • http://localhost:3000/docs      - API Documentation (Swagger)")
    print("\n🧪 Testing endpoints:")
    print("   • http://localhost:3000/test/all-endpoints  - Run all tests")
    print("   • http://localhost:3000/test/sample-queries - Get sample queries")
    print("\n💬 Query endpoint:")
    print("   • POST http://localhost:3000/query - Ask legal questions")
    print("\n" + "="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=3000)
