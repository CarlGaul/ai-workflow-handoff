# FamilyBeginnings Legal AI - Context Report for New Cursor Window
## Comprehensive Project Status & Next Steps

**Date**: August 6, 2025  
**User**: Carl Gaul - Solo attorney, beginner coder, M4 Mac  
**Project**: FamilyBeginnings Legal AI - Non-profit legal assistance platform  
**Purpose**: Context for new Cursor window to continue development

---

## 🎯 **IMPORTANT: This is a CONTEXT DOCUMENT**

**Purpose**: This report provides comprehensive context for the new Cursor window to understand the current state of the FamilyBeginnings Legal AI project and continue development where we left off.

**Next Steps**: After reading this context, await additional instructions from Grok for specific implementation tasks.

---

## 📋 **Project Overview**

### **Mission**
FamilyBeginnings Legal AI is a non-profit legal assistance platform focused on helping parents with pregnancy discrimination cases. The system provides zero-hallucination legal analysis using a local database of real case law and statutes.

### **Technical Stack**
- **Hardware**: MacBook Air M4 with 24GB RAM, Metal acceleration
- **AI Models**: Ollama running locally (GPT-OSS 20B, Qwen 2.5 14B, Llama 3.1 8B)
- **Framework**: Streamlit app with database integration
- **Database**: ChromaDB with 1,071 legal documents
- **Language**: Python 3.13

### **Key Directories**
```
~/Desktop/AIProjects/LegalAI/          # Main project
~/Desktop/ai-workflow/                 # Code sharing with Grok
~/Desktop/AIProjects/quantized_models/ # AI models
~/Desktop/AIProjects/Pregnancy Discrimination Cases/ # Legal database
```

---

## 🔍 **Current Status & Recent Achievements**

### ✅ **Completed Successfully**

1. **GPT-OSS Model Quantization**
   - Successfully created `gpt-oss:20b-q6` model (13GB mxfp4 version)
   - Updated Modelfile with database-exclusive instructions
   - Model correctly refuses to hallucinate when no context provided
   - Integrated as default model in configuration

2. **Model Switching Capability**
   - Added model selector to Streamlit sidebar
   - Three models available: GPT-OSS 20B, Qwen 2.5 14B, Llama 3.1 8B
   - Real-time model switching without restarting app
   - Updated LegalAI and OllamaClient classes to support model switching

3. **Database Integration**
   - 1,071 legal documents in ChromaDB
   - Real citations from pregnancy discrimination cases
   - Zero-hallucination mode implemented
   - Context retrieval working properly

4. **Streamlit App Enhancement**
   - App running on http://localhost:8501
   - Model switching interface in sidebar
   - Benchmark page with enhanced save functionality
   - Error handling and debugging implemented

### ⚠️ **Critical Issues Identified**

1. **Save Functionality Broken**
   - Streamlit benchmark results not saving despite enhanced error handling
   - No recent files in `/Users/carlgaul/Desktop/AIProjects/LegalAI/src/benchmarks/`
   - Save button triggers but files don't appear
   - Error messages not showing in UI

2. **GPT-OSS Response Quality Poor**
   - Model providing minimal responses even with database context
   - Response quality significantly lower than expected for 20B parameter model
   - Prompts may be too restrictive, causing overly cautious behavior

3. **Prompt Inconsistency**
   - Different prompts used across models during benchmarking
   - Cannot accurately compare model performance
   - No standardized prompt template

4. **Missing Spreadsheet Integration**
   - No automated data collection for comprehensive analysis
   - Manual data collection required
   - User wants LibreOffice-compatible Excel export

5. **Model Output Storage**
   - Individual model responses not being saved
   - No detailed analysis of response quality
   - Cannot track model performance over time

---

## 🚀 **Immediate Next Steps Required**

### **Priority 1: Fix Save Functionality**
```python
# Enhanced save with better debugging needed in main.py
try:
    # Force session state persistence
    st.session_state['benchmark_results'] = results
    
    # Test file write permissions
    test_file = os.path.join(primary_dir, 'test_write.txt')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    
    # Ensure results are serializable
    serializable_results = []
    for result in results:
        serializable_result = {
            'category': result.get('category', ''),
            'question': result.get('question', ''),
            'response_time': float(result.get('response_time', 0)),
            'word_count': int(result.get('word_count', 0)),
            'citation_count': int(result.get('citation_count', 0)),
            'aspect_coverage': float(result.get('aspect_coverage', 0)),
            'response': str(result.get('response', '')),
            'status': result.get('status', 'unknown')
        }
        serializable_results.append(serializable_result)
    
    # Save with explicit error handling
    filepath = os.path.join(primary_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    st.success(f"✅ Results saved to {filepath}")
    
except Exception as e:
    st.error(f"❌ Save failed: {str(e)}")
    st.error(f"Debug: {len(results)} results, working dir: {os.getcwd()}")
    st.error(f"Primary dir exists: {os.path.exists(primary_dir)}")
    st.error(f"Primary dir writable: {os.access(primary_dir, os.W_OK)}")
```

### **Priority 2: Improve GPT-OSS Prompts**
```python
# Enhanced system prompt needed in gpt-oss-q6.Modelfile
SYSTEM """You are an associate attorney specializing in pregnancy discrimination and employment law. You provide comprehensive legal analysis with accurate Bluebook citations.

INSTRUCTIONS:
- Use the provided legal database context as your primary source
- When database context is available, provide detailed analysis with specific citations
- Use Bluebook citation format for all legal references
- Write in professional legal memo format with clear headings
- If database context is limited, provide general legal principles and acknowledge limitations
- Be thorough and analytical in your responses
- Include relevant statutes, case law, and regulatory guidance when available
- Structure responses as: Question Presented, Short Answer, Discussion, Conclusion"""
```

### **Priority 3: Standardize Benchmark Prompts**
```python
# Standardized benchmark prompts needed
STANDARD_BENCHMARK_PROMPTS = {
    "pregnancy_termination": {
        "question": "Draft a legal memo on pregnancy discrimination under Title VII for an employee terminated after announcing pregnancy.",
        "expected_aspects": ["Title VII", "termination", "pregnancy", "discrimination"],
        "system_prompt": "You are an associate attorney. Provide comprehensive legal analysis with Bluebook citations from the database context."
    },
    "accommodation_denial": {
        "question": "Analyze potential claims for a pregnant worker denied reasonable accommodations, citing relevant EEOC guidance.",
        "expected_aspects": ["accommodations", "EEOC", "reasonable", "pregnancy"],
        "system_prompt": "You are an associate attorney. Provide comprehensive legal analysis with Bluebook citations from the database context."
    },
    "ny_retaliation": {
        "question": "Prepare a complaint outline for a pregnancy-related retaliation case in NY Supreme Court.",
        "expected_aspects": ["retaliation", "NY", "complaint", "court"],
        "system_prompt": "You are an associate attorney. Provide comprehensive legal analysis with Bluebook citations from the database context."
    }
}
```

### **Priority 4: Spreadsheet Integration**
```python
# Spreadsheet integration module needed
import pandas as pd
import openpyxl
from datetime import datetime

class BenchmarkSpreadsheet:
    def __init__(self, output_path="/Users/carlgaul/Desktop/ai-workflow/outputs/benchmark_results.xlsx"):
        self.output_path = output_path
        self.results_df = pd.DataFrame(columns=[
            'timestamp', 'model', 'question_category', 'response_time', 
            'word_count', 'citation_count', 'aspect_coverage', 'response_text',
            'benchmark_source', 'temperature', 'status'
        ])
    
    def add_result(self, result_data):
        """Add a single benchmark result to the spreadsheet"""
        new_row = {
            'timestamp': datetime.now().isoformat(),
            'model': result_data.get('model'),
            'question_category': result_data.get('category'),
            'response_time': result_data.get('response_time'),
            'word_count': result_data.get('word_count'),
            'citation_count': result_data.get('citation_count'),
            'aspect_coverage': result_data.get('aspect_coverage'),
            'response_text': result_data.get('response'),
            'benchmark_source': result_data.get('source', 'streamlit'),
            'temperature': result_data.get('temperature'),
            'status': result_data.get('status', 'success')
        }
        self.results_df = pd.concat([self.results_df, pd.DataFrame([new_row])], ignore_index=True)
    
    def save_spreadsheet(self):
        """Save results to Excel file compatible with LibreOffice"""
        with pd.ExcelWriter(self.output_path, engine='openpyxl') as writer:
            # Main results sheet
            self.results_df.to_excel(writer, sheet_name='Benchmark_Results', index=False)
            
            # Summary statistics sheet
            summary_stats = self.results_df.groupby('model').agg({
                'response_time': ['mean', 'std'],
                'word_count': ['mean', 'std'],
                'citation_count': ['mean', 'std'],
                'aspect_coverage': ['mean', 'std']
            }).round(2)
            summary_stats.to_excel(writer, sheet_name='Summary_Statistics')
            
            # Model comparison sheet
            model_comparison = self.results_df.groupby('model').agg({
                'response_time': 'mean',
                'word_count': 'mean',
                'citation_count': 'mean',
                'aspect_coverage': 'mean'
            }).round(2)
            model_comparison.to_excel(writer, sheet_name='Model_Comparison')
```

---

## 📊 **Technical Architecture**

### **Current File Structure**
```
~/Desktop/AIProjects/LegalAI/
├── src/
│   ├── main.py (Streamlit app with model switching)
│   ├── legal_ai_core.py (LegalAI class with model support)
│   ├── ollama_client.py (OllamaClient with model_name parameter)
│   ├── config.py (Configuration with gpt-oss:20b-q6 as default)
│   ├── gpt-oss-q6.Modelfile (Updated prompts)
│   └── benchmark_spreadsheet.py (NEEDS TO BE CREATED)
├── benchmarks/ (Save location for benchmark results)
├── database/ (Legal documents)
└── ai-workflow/outputs/ (Backup save location)
```

### **Key Configuration**
```python
# .env file updated
DEFAULT_OLLAMA_MODEL=gpt-oss:20b-q6

# config.py updated
DEFAULT_OLLAMA_MODEL = os.getenv("DEFAULT_OLLAMA_MODEL", "gpt-oss:20b-q6")
FALLBACK_MODELS = ["gpt-oss:20b-q6", "qwen2.5:14b"]
```

### **Available Models**
- `gpt-oss:20b-q6` (13GB, quantized, default)
- `qwen2.5:14b` (fallback)
- `llama3.1:8b` (lightweight)

---

## 🎯 **User Requirements & Preferences**

### **User Profile**
- Solo attorney, beginner coder
- M4 Mac with 24GB RAM
- Prefers LibreOffice for spreadsheets
- Values zero-hallucination responses
- Needs comprehensive legal analysis

### **Specific Requirements**
1. **Save Functionality**: Must work reliably for data collection
2. **Response Quality**: GPT-OSS must provide comprehensive analysis
3. **Prompt Consistency**: Essential for fair model comparison
4. **Spreadsheet Integration**: Automated data collection with LibreOffice compatibility
5. **Model Output Storage**: Individual responses must be preserved for analysis

### **8-Benchmark Matrix Goal**
Compare performance across:
- Streamlit vs Terminal
- Different models (GPT-OSS, Qwen, Llama)
- Response quality metrics
- Memory usage tracking

---

## 🔧 **Development Commands**

### **Current Working Directory**
```bash
cd ~/Desktop/AIProjects/LegalAI
```

### **Streamlit App**
```bash
streamlit run src/main.py
# Running on http://localhost:8501
```

### **Model Testing**
```bash
# Test GPT-OSS model
ollama run gpt-oss:20b-q6 "Test pregnancy discrimination memo." --verbose

# Test database integration
python3 -c "from src.legal_ai_core import LegalAI; print('✅ DB ready:', LegalAI().collection.count())"
```

### **File Locations**
- **Benchmarks**: `/Users/carlgaul/Desktop/AIProjects/LegalAI/src/benchmarks/`
- **Outputs**: `/Users/carlgaul/Desktop/ai-workflow/outputs/`
- **Models**: `/Users/carlgaul/Desktop/AIProjects/quantized_models/`

---

## 📝 **Recent Issues & Solutions**

### **Import Issues Fixed**
- Added proper error handling for LegalAI import
- Defined `LegalAI = None` when imports fail
- Added checks before using LegalAI

### **Model Switching Implemented**
- Updated LegalAI class to accept `model_name` parameter
- Updated OllamaClient to store and use model names
- Added model selector to Streamlit sidebar

### **Database Integration Working**
- 1,071 documents in ChromaDB
- Real citations from pregnancy discrimination cases
- Context retrieval functioning properly

---

## 🚨 **Critical Issues to Address**

1. **Save Functionality**: Primary blocker for data collection
2. **GPT-OSS Response Quality**: Model not providing comprehensive analysis
3. **Prompt Standardization**: Needed for fair benchmarking
4. **Spreadsheet Integration**: Missing automated data collection
5. **Model Output Storage**: Individual responses not being saved

---

## 📋 **Next Steps for New Cursor Window**

1. **Read this context document thoroughly**
2. **Await specific instructions from Grok**
3. **Implement fixes in priority order**
4. **Test each fix before moving to next**
5. **Maintain beginner-friendly approach**
6. **Focus on user experience and reliability**

---

## 🎯 **Success Criteria**

### **Immediate Goals**
- [ ] Save functionality working reliably in Streamlit
- [ ] GPT-OSS providing comprehensive legal responses
- [ ] Consistent prompts across all models
- [ ] Basic spreadsheet export working

### **Short-term Goals**
- [ ] Complete 8-benchmark matrix implementation
- [ ] Automated data collection from both Streamlit and terminal
- [ ] Detailed response storage and analysis
- [ ] LibreOffice-compatible spreadsheet generation

---

**This context document provides comprehensive understanding of the FamilyBeginnings Legal AI project status. The new Cursor window should use this information to continue development where we left off, awaiting specific implementation instructions from Grok.**

**Contact**: Carl Gaul - Solo attorney, beginner coder, M4 Mac user  
**Project**: FamilyBeginnings Legal AI - Non-profit legal assistance platform  
**Mission**: Helping parents with pregnancy discrimination cases through AI-powered legal research 