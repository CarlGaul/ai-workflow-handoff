import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import psutil

# Load environment variables
load_dotenv()

class Config:
    """Enhanced configuration management for Legal AI system with benchmarking"""
    
    # ========================================
    # CORE DIRECTORIES
    # ========================================
    DATABASE_DIR = Path(os.getenv("DATABASE_DIR", "database"))
    CACHE_DIR = Path(os.getenv("CACHE_DIR", "cache"))
    VECTOR_DATABASE_DIR = Path(os.getenv("VECTOR_DATABASE_DIR", "vector_database"))
    TEMP_DIR = Path(os.getenv("TEMP_DIR", "temp"))
    LOGS_DIR = Path(os.getenv("LOGS_DIR", "logs"))
    OUTPUTS_DIR = Path(os.getenv("OUTPUTS_DIR", "outputs"))
    
    # Legacy support for vector DB
    VECTOR_DB_DIR = str(VECTOR_DATABASE_DIR)
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    AUTHORITY_LEVELS = {"supreme_court": 10, "court_of_appeals": 5, "appellate_division": 8, "civil_court": 12}
    
    # ========================================
    # OLLAMA CONFIGURATION
    # ========================================
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    DEFAULT_OLLAMA_MODEL = os.getenv("DEFAULT_OLLAMA_MODEL", "gpt-oss:20b-q6")
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))
    OLLAMA_ENABLE_METAL = os.getenv("OLLAMA_ENABLE_METAL", "true").lower() == "true"
    
    # Legacy support
    GPU_ENABLED = True
    AUTO_LOAD_MODEL = True
    FALLBACK_MODELS = ["gpt-oss:20b-q6", "qwen2.5:14b"]
    
    # ========================================
    # MEMORY MANAGEMENT
    # ========================================
    MAX_MEMORY_USAGE_PERCENT = int(os.getenv("MAX_MEMORY_USAGE_PERCENT", "75"))
    MEMORY_WARNING_THRESHOLD = int(os.getenv("MEMORY_WARNING_THRESHOLD", "8"))  # GB
    ENABLE_MEMORY_MONITORING = os.getenv("ENABLE_MEMORY_MONITORING", "true").lower() == "true"
    GARBAGE_COLLECTION_INTERVAL = int(os.getenv("GARBAGE_COLLECTION_INTERVAL", "300"))
    AUTO_MEMORY_CLEANUP = os.getenv("AUTO_MEMORY_CLEANUP", "true").lower() == "true"
    
    # ========================================
    # PERFORMANCE OPTIMIZATION
    # ========================================
    ENABLE_METAL_ACCELERATION = os.getenv("ENABLE_METAL_ACCELERATION", "true").lower() == "true"
    ENABLE_COREML_ACCELERATION = os.getenv("ENABLE_COREML_ACCELERATION", "true").lower() == "true"
    THREAD_POOL_SIZE = int(os.getenv("THREAD_POOL_SIZE", "4"))
    MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "2"))
    
    # ========================================
    # LEGAL RESEARCH CONFIGURATION
    # ========================================
    MAX_CASES_PER_QUERY = int(os.getenv("MAX_CASES_PER_QUERY", "8"))
    CASE_SUMMARY_MAX_LENGTH = int(os.getenv("CASE_SUMMARY_MAX_LENGTH", "4"))
    ENABLE_CASE_CACHING = os.getenv("ENABLE_CASE_CACHING", "true").lower() == "true"
    LEGAL_RESEARCH_MODE = os.getenv("LEGAL_RESEARCH_MODE", "direct")  # direct|vector|hybrid
    
    # ========================================
    # LEGAL-BERT CONFIGURATION
    # ========================================
    LEGAL_BERT_MODEL = os.getenv("LEGAL_BERT_MODEL", "nlpaueb/legal-bert-base-uncased")
    ENABLE_LEGAL_BERT = os.getenv("ENABLE_LEGAL_BERT", "true").lower() == "true"
    LEGAL_BERT_CONFIDENCE_THRESHOLD = float(os.getenv("LEGAL_BERT_CONFIDENCE_THRESHOLD", "0.75"))
    ENABLE_COREML_LEGAL_BERT = os.getenv("ENABLE_COREML_LEGAL_BERT", "true").lower() == "true"
    
    # ========================================
    # SYSTEM PROMPT CONFIGURATION
    # ========================================
    ENABLE_ZERO_HALLUCINATION_MODE = os.getenv("ENABLE_ZERO_HALLUCINATION_MODE", "true").lower() == "true"
    ENFORCE_DOCUMENT_CITATIONS = os.getenv("ENFORCE_DOCUMENT_CITATIONS", "true").lower() == "true"
    REQUIRE_BLUEBOOK_CITATIONS = os.getenv("REQUIRE_BLUEBOOK_CITATIONS", "true").lower() == "true"
    MAX_RESPONSE_LENGTH = int(os.getenv("MAX_RESPONSE_LENGTH", "4000"))
    
    # Standardized system prompt for all models
    SYSTEM_PROMPT = """You are a hyper-competent associate attorney specializing in pregnancy discrimination and employment law, taking instructions from a partner. Rely EXCLUSIVELY on the local legal database for authority—citations to statutes, cases, policy documents, and case law therein. Zero hallucination: ONLY cite/quote from provided DB context. If not in context, say 'No relevant DB info—general principle only.'

Always provide legal authority for assertions of law. Always explain elements of legal claims at issue (e.g., for retaliation: protected activity, adverse action, causal nexus).

Structure responses as professional memos with To/From/Date/Subject, Introduction, Analysis, Conclusion."""
    
    # ========================================
    # BENCHMARKING CONFIGURATION
    # ========================================
    # Benchmark scenarios (reduced to 4 for speed)
    BENCHMARK_SCENARIOS = [
        {
            "category": "PDA Memo",
            "question": "Draft a legal memo analyzing the basic rights of pregnant employees under the Pregnancy Discrimination Act. Include specific citations to relevant cases and statutes from the database.",
            "expected_aspects": ["PDA coverage", "equal treatment", "reasonable accommodations", "bluebook citations"]
        },
        {
            "category": "FMLA Accommodations", 
            "question": "Analyze the legal requirements for reasonable accommodations for pregnant employees under FMLA. Cite specific cases and regulations from the database that establish these requirements.",
            "expected_aspects": ["FMLA rights", "reasonable accommodation", "light duty", "job protection"]
        },
        {
            "category": "NY Law",
            "question": "Analyze how New York State law protects pregnant employees beyond federal law. Cite specific NY statutes and cases from the database.",
            "expected_aspects": ["NY protections", "state statutes", "local laws", "enhanced rights"]
        },
        {
            "category": "Remedies",
            "question": "Draft a brief on legal remedies available for pregnancy discrimination victims. Include specific citations to cases and statutes establishing these remedies.",
            "expected_aspects": ["damages", "injunctive relief", "attorney fees", "back pay"]
        }
    ]
    
    # Benchmark models and temperatures
    BENCHMARK_MODELS = ["llama3.1:8b", "gpt-oss:20b-q6", "qwen2.5:14b"]
    BENCHMARK_TEMPERATURES = [0.3, 0.5, 0.7, 1.0]
    
    # Processing flags
    PARALLEL_THREADS = int(os.getenv("PARALLEL_THREADS", "4"))
    PROMPT_MAX_TOKENS = int(os.getenv("PROMPT_MAX_TOKENS", "2000"))
    MIN_TEMP_GPT = float(os.getenv("MIN_TEMP_GPT", "0.7"))
    MAX_TEMP_LLAMA = float(os.getenv("MAX_TEMP_LLAMA", "0.7"))
    RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "2"))
    
    # Metric weights for evaluation
    METRIC_WEIGHTS = {
        'completeness': 0.25,
        'alignment': 0.15,
        'zero_hallucination': 0.20,
        'accuracy': 0.15,
        'citations': 0.10,
        'clarity': 0.10,
        'aspect_coverage': 0.05
    }
    
    # ========================================
    # DEVELOPMENT & DEBUGGING
    # ========================================
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
    ENABLE_PERFORMANCE_LOGGING = os.getenv("ENABLE_PERFORMANCE_LOGGING", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    BENCHMARK_MODE = os.getenv("BENCHMARK_MODE", "false").lower() == "true"
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and system readiness"""
        validation_results = {
            'directories': True,
            'memory': True,
            'ollama': True,
            'performance': True,
            'warnings': [],
            'errors': []
        }
        
        # Validate directories
        try:
            for dir_attr in ['DATABASE_DIR', 'CACHE_DIR', 'VECTOR_DATABASE_DIR', 'TEMP_DIR', 'LOGS_DIR', 'OUTPUTS_DIR']:
                dir_path = getattr(cls, dir_attr)
                dir_path.mkdir(parents=True, exist_ok=True)
                if not dir_path.exists():
                    validation_results['directories'] = False
                    validation_results['errors'].append(f"Cannot create directory: {dir_path}")
        except Exception as e:
            validation_results['directories'] = False
            validation_results['errors'].append(f"Directory validation error: {e}")
        
        # Validate memory
        try:
            mem = psutil.virtual_memory()
            available_gb = mem.available / (1024**3)
            
            if available_gb < cls.MEMORY_WARNING_THRESHOLD:
                validation_results['warnings'].append(
                    f"Low memory: {available_gb:.1f}GB available (threshold: {cls.MEMORY_WARNING_THRESHOLD}GB)"
                )
            
            if mem.percent > cls.MAX_MEMORY_USAGE_PERCENT:
                validation_results['warnings'].append(
                    f"High memory usage: {mem.percent:.1f}% (max: {cls.MAX_MEMORY_USAGE_PERCENT}%)"
                )
                
        except Exception as e:
            validation_results['memory'] = False
            validation_results['errors'].append(f"Memory validation error: {e}")
        
        return validation_results
    
    @classmethod
    def setup_logging(cls):
        """Setup logging configuration"""
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cls.LOGS_DIR / 'legal_ai.log'),
                logging.StreamHandler() if cls.DEBUG_MODE else logging.NullHandler()
            ]
        )
        
        return logging.getLogger('LegalAI')
    
    @classmethod
    def get_system_info(cls) -> Dict[str, Any]:
        """Get current system information"""
        mem = psutil.virtual_memory()
        
        return {
            'memory': {
                'total_gb': mem.total / (1024**3),
                'available_gb': mem.available / (1024**3),
                'used_percent': mem.percent,
            },
            'config': {
                'metal_acceleration': cls.ENABLE_METAL_ACCELERATION,
                'thread_pool_size': cls.THREAD_POOL_SIZE,
                'parallel_threads': cls.PARALLEL_THREADS,
                'prompt_max_tokens': cls.PROMPT_MAX_TOKENS,
                'retry_attempts': cls.RETRY_ATTEMPTS
            },
            'benchmarking': {
                'models': cls.BENCHMARK_MODELS,
                'temperatures': cls.BENCHMARK_TEMPERATURES,
                'scenarios': len(cls.BENCHMARK_SCENARIOS)
            }
        }
    
    @classmethod
    def print_config_summary(cls):
        """Print configuration summary"""
        print("🔧 Legal AI Configuration Summary")
        print("=" * 50)
        print(f"📁 Database: {cls.DATABASE_DIR}")
        print(f"📁 Outputs: {cls.OUTPUTS_DIR}")
        print(f"🤖 Default Model: {cls.DEFAULT_OLLAMA_MODEL}")
        print(f"⚡ Metal Acceleration: {cls.ENABLE_METAL_ACCELERATION}")
        print(f"🧵 Thread Pool Size: {cls.THREAD_POOL_SIZE}")
        print(f"📊 Benchmark Models: {len(cls.BENCHMARK_MODELS)}")
        print(f"🌡️ Benchmark Temperatures: {len(cls.BENCHMARK_TEMPERATURES)}")
        print(f"📝 Benchmark Scenarios: {len(cls.BENCHMARK_SCENARIOS)}")
        print(f"🔄 Retry Attempts: {cls.RETRY_ATTEMPTS}")
        print(f"📏 Prompt Max Tokens: {cls.PROMPT_MAX_TOKENS}")
        print("=" * 50)

# Initialize logging
logger = Config.setup_logging()
