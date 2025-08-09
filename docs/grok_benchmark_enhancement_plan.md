# Grok Benchmark Enhancement Plan - Next Refinements

## 🎯 **Project Context & History**

### **Current System Performance**:
- **Llama3.1:8b**: Fast (4.9GB), strong structure, mid accuracy (7.6), hallucinations (7.1)
- **GPT-OSS:20b-q6**: Slower (13GB), low-temp rambles (avg 3.9 at 0.3), excels at 1.0 (8.6), high zero-hallucination (9.5)
- **Qwen2.5:14b**: Balanced (9GB), top overall (8.3), consistent clarity (8.6) and compliance (8.6)

### **Hardware**: Apple M4 Mac (24GB RAM, Metal acceleration)

### **Previous Refinements Implemented**:
- ✅ Uniform prompt ("Output only final memo, no planning/tags")
- ✅ GPT-OSS tweak ("Skip thoughts—avoid 'We need to'")
- ✅ Post-process (regex strip <end|>/unicode, retries x2)
- ✅ Enhanced evaluator (completeness, alignment, no structure penalties)
- ✅ Benchmarking with parallel concurrent.futures/fixed seeds
- ✅ GPT min temp 0.7, Llama cap 0.7

## 🚀 **Next Refinements Roadmap**

### **Phase 1: Speed Optimizations**
1. **Reduce scenarios to 4**: PDA memo, FMLA accommodations, NY law, remedies
2. **Parallel processing**: THREAD_POOL_SIZE=4 from config
3. **Prompt truncation**: 2000 token limit with intelligent context reduction
4. **Hardware optimization**: Metal acceleration, Ollama logs via config

### **Phase 2: Integration & Modularity**
1. **Config-driven**: Load all settings from config.py
2. **Modular architecture**: Separate prompts.py, response_processor.py, enhanced_evaluator.py
3. **CI/CD integration**: GitHub Actions benchmark.yml
4. **Streamlit UI**: User-friendly benchmark runner

### **Phase 3: Evaluation Refinements**
1. **Word count completeness**: <300=5, 300-800=10, >800=7
2. **Key term alignment**: Percentage-based scoring
3. **Rule-based metrics**: Accuracy, citations, clarity, explaining, comprehensiveness
4. **No structure penalties**: Remove To/From checks

## 📋 **Implementation Steps**

### **1. Configuration Updates**
- Add benchmarking sections to config.py
- Define scenarios, temperatures, models lists
- Set metric weights and processing flags
- Enable Metal acceleration and logging

### **2. Modular Architecture**
- **prompts.py**: Uniform templates with model tweaks
- **response_processor.py**: Planning detection and retry logic
- **enhanced_evaluator.py**: Updated metrics without structure penalties
- **benchmarking.py**: Parallel execution with config integration

### **3. Speed Optimizations**
- Reduce scenarios from 8 to 4 core tests
- Implement intelligent context truncation
- Parallel processing with ThreadPoolExecutor
- Hardware acceleration via Metal

### **4. CI/CD Integration**
- GitHub Actions workflow for automated benchmarking
- Results commit to outputs/ directory
- Validation checks before execution

## 🎯 **Expected Outcomes**

### **Performance Improvements**:
- **Speed**: 50%+ faster execution with 4 scenarios vs 8
- **Memory**: Reduced context loading with 2000 token limit
- **Parallelization**: 4x concurrent processing
- **Hardware**: Metal acceleration utilization

### **Quality Enhancements**:
- **No planning content**: Retry logic eliminates rambles
- **Consistent scoring**: Fixed seeds ensure reproducibility
- **Better alignment**: Key term matching improves accuracy
- **Modular code**: Easier maintenance and updates

### **User Experience**:
- **Streamlit UI**: Easy benchmark selection and execution
- **Automated CI/CD**: Push-triggered benchmarking
- **Clear results**: CSV and MD table outputs
- **Config-driven**: Easy parameter adjustments

## 🔧 **Technical Specifications**

### **Scenarios (Reduced to 4)**:
1. **PDA Memo**: Pregnancy Discrimination Act analysis
2. **FMLA Accommodations**: Family Medical Leave Act rights
3. **NY Law**: New York State protections
4. **Remedies**: Legal remedies for discrimination

### **Temperatures**: [0.3, 0.5, 0.7, 1.0]

### **Models**: ['llama3.1:8b', 'gpt-oss:20b-q6', 'qwen2.5:14b']

### **Metric Weights**:
```python
{
    'completeness': 0.25,
    'alignment': 0.15,
    'zero_hallucination': 0.20,
    'accuracy': 0.15,
    'citations': 0.10,
    'clarity': 0.10,
    'aspect_coverage': 0.05
}
```

### **Processing Flags**:
- parallel_threads=4
- prompt_max=2000
- min_temp_gpt=0.7
- max_temp_llama=0.7
- retry_attempts=2

## 📊 **Success Metrics**

1. **Speed**: Benchmark completion < 30 minutes
2. **Quality**: Zero planning content in final outputs
3. **Consistency**: Reproducible results across runs
4. **Modularity**: Clean separation of concerns
5. **Integration**: Seamless config-driven operation

## ✅ **Verification & Testing Notes**

### **Component Testing**:
- **Configuration**: Load settings, validate directories, check memory
- **Prompt Templates**: Test truncation, model tweaks, full prompt building
- **Response Processor**: Verify planning detection, content extraction, retry logic
- **Enhanced Evaluator**: Test all metrics (completeness, alignment, accuracy, citations, clarity, explaining, comprehensiveness)
- **Benchmark Enhancements**: Integration testing with simulated responses

### **Retry Logic Verification**:
- **Planning Detection**: Regex patterns catch "Let me craft", "We need to", "I'll produce"
- **Retry Attempts**: Up to 2 attempts if planning detected
- **No Penalties**: Planning detection doesn't affect scoring
- **Logging**: All retry attempts logged for debugging

### **Metric Completeness**:
- **All Original Metrics**: Accuracy, Citations, Clarity, Explaining, Comprehensiveness, Zero-Hallucination
- **New Metrics**: Completeness (word count proxy), Alignment (key term matching)
- **No Structure Penalties**: Removed To/From checks and structure scoring
- **Proper Weights**: Comprehensive score calculation matches specified weights

### **Speed Testing**:
- **Parallel Processing**: 4 concurrent threads via ThreadPoolExecutor
- **Context Truncation**: 2000 token limit with priority keyword preservation
- **Temperature Constraints**: GPT min 0.7, Llama max 0.7
- **Fixed Seeds**: Reproducible results with torch.manual_seed(42)

### **Repository Integration**:
- **Directory Creation**: All missing dirs created via Path.mkdir(parents=True, exist_ok=True)
- **Config Validation**: Pre-run checks for directories, memory, and system readiness
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Graceful failure handling with detailed error messages

### **Sample Run Verification**:
- **Test Mode**: Single scenario with all models/temps (12 total tests)
- **Simulated Responses**: Legal memo format with citations
- **Processing Pipeline**: Full response processing and evaluation
- **Results Display**: Average scores, planning detection rates, model performance

### **UI Table Display**:
- **Streamlit Integration**: Full comparative table with all metrics
- **Model Performance**: Side-by-side comparison with averages
- **Download Options**: CSV export for further analysis
- **Real-time Updates**: Progress tracking during benchmark execution

### **CI/CD Integration**:
- **GitHub Actions**: Automated benchmarking on push/PR
- **Validation Checks**: Config validation before execution
- **Results Commit**: Automatic commit of results to outputs/
- **Artifact Upload**: Benchmark results as downloadable artifacts

This plan builds upon previous refinements while focusing on speed, modularity, and user experience improvements. All components have been tested and verified for robust operation.
