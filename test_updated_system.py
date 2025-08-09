#!/usr/bin/env python3
"""
Test Script for Updated Legal AI Benchmarking System
Verifies components and simulates sample benchmark run
"""
import sys
import os
import time
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_config():
    """Test configuration loading and validation"""
    print("🔧 Testing Configuration...")
    
    try:
        from config import Config
        
        # Test config loading
        print(f"✅ Config loaded successfully")
        print(f"   - Default Model: {Config.DEFAULT_OLLAMA_MODEL}")
        print(f"   - Benchmark Models: {Config.BENCHMARK_MODELS}")
        print(f"   - Benchmark Temperatures: {Config.BENCHMARK_TEMPERATURES}")
        print(f"   - Scenarios: {len(Config.BENCHMARK_SCENARIOS)}")
        
        # Test validation
        validation = Config.validate_config()
        print(f"✅ Config validation: {validation}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_prompts():
    """Test prompt templates"""
    print("\n📝 Testing Prompt Templates...")
    
    try:
        from prompts.prompts import PromptTemplates
        
        # Test base prompt
        base_prompt = PromptTemplates.get_base_prompt()
        print(f"✅ Base prompt loaded ({len(base_prompt)} chars)")
        
        # Test model tweaks
        for model in ["gpt-oss:20b-q6", "qwen2.5:14b", "llama3.1:8b"]:
            tweak = PromptTemplates.get_model_tweak(model)
            print(f"✅ {model} tweak: {len(tweak)} chars")
        
        # Test truncation
        long_context = "This is a test context. " * 1000  # ~6000 chars
        truncated = PromptTemplates.truncate_context(long_context, 2000)
        print(f"✅ Truncation test: {len(long_context)} -> {len(truncated)} chars")
        
        # Test full prompt building
        test_context = "Test legal context with PDA and FMLA information."
        for model in ["gpt-oss:20b-q6"]:
            prompt = PromptTemplates.build_prompt(model, test_context)
            print(f"✅ Full prompt for {model}: {len(prompt)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Prompts test failed: {e}")
        return False

def test_response_processor():
    """Test response post-processing"""
    print("\n🔄 Testing Response Processor...")
    
    try:
        from src.response_processor import ResponsePostProcessor
        
        processor = ResponsePostProcessor()
        
        # Test planning detection
        test_responses = [
            "This is a normal legal memo without planning content.",
            "Let me craft a comprehensive legal memo for you...",
            "I'll produce an analysis of the PDA...",
            "Here's my analysis of the situation...",
            "We need to create a memo about this..."
        ]
        
        for i, response in enumerate(test_responses):
            detected = processor.detect_planning_content(response)
            print(f"✅ Test {i+1}: Planning detected = {detected}")
        
        # Test content extraction
        test_response = """
        Let me craft a comprehensive legal memo for you.
        
        <|start|>assistant<|message|>
        
        **To:** Partner
        **From:** Associate Attorney
        **Date:** [Current Date]
        **Subject:** Pregnancy Discrimination Act Analysis
        
        ### Introduction
        This memo analyzes the basic rights of pregnant employees under the PDA.
        
        ### Analysis
        The Pregnancy Discrimination Act provides important protections...
        """
        
        final_content = processor.extract_final_content(test_response)
        print(f"✅ Content extraction: {len(test_response)} -> {len(final_content)} chars")
        print(f"   Planning removed: {len(test_response) - len(final_content)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Response processor test failed: {e}")
        return False

def test_evaluator():
    """Test enhanced evaluator"""
    print("\n📊 Testing Enhanced Evaluator...")
    
    try:
        from src.enhanced_evaluator import EnhancedEvaluator
        
        evaluator = EnhancedEvaluator()
        
        # Test evaluation
        test_response = """
        **To:** Partner
        **From:** Associate Attorney
        **Date:** [Current Date]
        **Subject:** Pregnancy Discrimination Act Analysis
        
        ### Introduction
        This memo analyzes the basic rights of pregnant employees under the Pregnancy Discrimination Act (PDA).
        
        ### Analysis
        The PDA amends Title VII to prohibit employment discrimination against individuals because of their pregnancy, childbirth, or related medical conditions (42 U.S.C. § 2000e(k)).
        
        ### Conclusion
        Pregnant employees are entitled to comprehensive protections under federal law.
        """
        
        # Test individual metrics
        completeness = evaluator.evaluate_response_completeness(test_response)
        alignment = evaluator.evaluate_alignment_to_question(test_response, "PDA analysis", "PDA Memo")
        zero_hallucination = evaluator.evaluate_zero_hallucination_compliance(test_response, "test context")
        accuracy = evaluator.evaluate_accuracy(test_response, "PDA analysis")
        citations = evaluator.evaluate_citations(test_response)
        clarity = evaluator.evaluate_clarity(test_response)
        explaining = evaluator.evaluate_explaining(test_response)
        
        print(f"✅ Completeness: {completeness:.2f}/10")
        print(f"✅ Alignment: {alignment:.2f}/10")
        print(f"✅ Zero-Hallucination: {zero_hallucination:.2f}/10")
        print(f"✅ Accuracy: {accuracy:.2f}/10")
        print(f"✅ Citations: {citations:.2f}/10")
        print(f"✅ Clarity: {clarity:.2f}/10")
        print(f"✅ Explaining: {explaining:.2f}/10")
        
        # Test comprehensive evaluation
        expected_aspects = ["PDA coverage", "equal treatment", "reasonable accommodations"]
        evaluation = evaluator.evaluate_benchmark_result(
            test_response, "PDA analysis", "PDA Memo", "test context", 
            expected_aspects, 2.5
        )
        
        comprehensive_score = evaluation['comprehensive_score']
        print(f"✅ Comprehensive Score: {comprehensive_score:.2f}/10")
        
        return True
        
    except Exception as e:
        print(f"❌ Evaluator test failed: {e}")
        return False

def test_benchmark_enhancements():
    """Test benchmark enhancements integration"""
    print("\n🚀 Testing Benchmark Enhancements...")
    
    try:
        from src.benchmark_enhancements import BenchmarkEnhancements
        
        enhancements = BenchmarkEnhancements()
        
        # Test enhanced prompt generation
        test_context = "Test legal context with PDA and FMLA information."
        for model in ["gpt-oss:20b-q6"]:
            prompt = enhancements.get_enhanced_prompt(model, 0.7, test_context)
            print(f"✅ Enhanced prompt for {model}: {len(prompt)} chars")
        
        # Test response processing
        test_response = """
        Let me craft a comprehensive legal memo for you.
        
        **To:** Partner
        **From:** Associate Attorney
        **Subject:** Test Memo
        
        This is a test legal memo.
        """
        
        processed = enhancements.process_benchmark_response(
            test_response, "Test question", "Test Category", "test context", 1.5
        )
        
        print(f"✅ Response processing: Planning detected = {processed['planning_detected']}")
        print(f"✅ Final content length: {len(processed['final_content'])} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Benchmark enhancements test failed: {e}")
        return False

def simulate_sample_run():
    """Simulate a sample benchmark run"""
    print("\n🎯 Simulating Sample Benchmark Run...")
    
    try:
        from config import Config
        from src.benchmark_enhancements import BenchmarkEnhancements
        
        enhancements = BenchmarkEnhancements()
        
        # Simulate one scenario with all models/temps
        scenario = Config.BENCHMARK_SCENARIOS[0]  # PDA Memo
        models = ["llama3.1:8b", "gpt-oss:20b-q6", "qwen2.5:14b"]
        temps = [0.3, 0.5, 0.7, 1.0]
        
        print(f"📝 Scenario: {scenario['category']}")
        print(f"🤖 Models: {len(models)}")
        print(f"🌡️ Temperatures: {len(temps)}")
        print(f"📊 Total tests: {len(models) * len(temps)}")
        
        # Simulate processing (without actual Ollama calls)
        results = []
        start_time = time.time()
        
        for model in models:
            for temp in temps:
                # Apply temperature constraints
                if model == "gpt-oss:20b-q6" and temp < Config.MIN_TEMP_GPT:
                    temp = Config.MIN_TEMP_GPT
                elif model == "llama3.1:8b" and temp > Config.MAX_TEMP_LLAMA:
                    temp = Config.MAX_TEMP_LLAMA
                
                # Simulate response
                simulated_response = f"""
                **To:** Partner
                **From:** Associate Attorney
                **Subject:** {scenario['category']}
                
                This is a simulated response for {model} at temperature {temp}.
                The Pregnancy Discrimination Act (42 U.S.C. § 2000e(k)) provides important protections.
                """
                
                # Process response
                processed = enhancements.process_benchmark_response(
                    simulated_response, 
                    scenario['question'], 
                    scenario['category'], 
                    "simulated context", 
                    2.0
                )
                
                results.append({
                    'model': model,
                    'temperature': temp,
                    'comprehensive_score': processed['comprehensive_score'],
                    'planning_detected': processed['planning_detected']
                })
        
        end_time = time.time()
        
        # Display results
        print(f"\n📊 Sample Run Results:")
        print(f"⏱️ Total time: {end_time - start_time:.2f}s")
        print(f"✅ Completed: {len(results)} tests")
        
        # Calculate averages
        avg_score = sum(r['comprehensive_score'] for r in results) / len(results)
        planning_detected = sum(1 for r in results if r['planning_detected'])
        
        print(f"📈 Average Score: {avg_score:.2f}/10")
        print(f"🔄 Planning Detected: {planning_detected}/{len(results)}")
        
        # Model performance
        for model in models:
            model_results = [r for r in results if r['model'] == model]
            model_avg = sum(r['comprehensive_score'] for r in model_results) / len(model_results)
            print(f"   {model}: {model_avg:.2f}/10")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample run simulation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Legal AI Benchmarking System - Component Tests")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_config),
        ("Prompt Templates", test_prompts),
        ("Response Processor", test_response_processor),
        ("Enhanced Evaluator", test_evaluator),
        ("Benchmark Enhancements", test_benchmark_enhancements),
        ("Sample Run Simulation", simulate_sample_run)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for benchmarking.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()

