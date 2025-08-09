#!/usr/bin/env python3
"""
Main Benchmarking Module for Legal AI
Parallel execution with config integration and enhanced evaluation
"""
import sys
import os
import json
import time
import csv
import torch
import numpy as np
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import Config
from legal_ai_core import LegalAI
from response_processor import ResponsePostProcessor
from enhanced_evaluator import EnhancedEvaluator
from prompts.prompts import PromptTemplates

class BenchmarkRunner:
    """Main benchmark runner with parallel execution"""
    
    def __init__(self):
        # Set fixed seeds for reproducibility
        torch.manual_seed(42)
        np.random.seed(42)
        
        # Initialize components
        self.legal_ai = LegalAI()
        self.post_processor = ResponsePostProcessor()
        self.evaluator = EnhancedEvaluator()
        self.prompt_templates = PromptTemplates()
        
        # Validate config before running
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration before benchmarking"""
        validation = Config.validate_config()
        if not validation['directories'] or not validation['memory']:
            raise RuntimeError(f"Configuration validation failed: {validation['errors']}")
        
        if validation['warnings']:
            print(f"⚠️ Configuration warnings: {validation['warnings']}")
    
    def run_single_benchmark(self, model: str, temperature: float, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single benchmark test"""
        
        try:
            # Apply temperature constraints
            if model == "gpt-oss:20b-q6" and temperature < Config.MIN_TEMP_GPT:
                temperature = Config.MIN_TEMP_GPT
            elif model == "llama3.1:8b" and temperature > Config.MAX_TEMP_LLAMA:
                temperature = Config.MAX_TEMP_LLAMA
            
            # Get context from database
            context = self.legal_ai.retrieve_context(scenario["question"])
            
            # Build enhanced prompt
            enhanced_prompt = self.prompt_templates.build_prompt(
                model, context, Config.PROMPT_MAX_TOKENS
            )
            
            # Generate response
            start_time = time.time()
            response = self.legal_ai.ollama_client.generate_response(
                prompt=scenario["question"],
                system_prompt=enhanced_prompt,
                model=model,
                temperature=temperature
            )
            response_time = time.time() - start_time
            
            # Post-process with retries
            final_content = self.post_processor.process_with_retries(
                response, max_retries=Config.RETRY_ATTEMPTS
            )
            
            # Evaluate response
            evaluation_result = self.evaluator.evaluate_benchmark_result(
                final_content, 
                scenario["question"], 
                scenario["category"], 
                context, 
                scenario["expected_aspects"], 
                response_time
            )
            
            return {
                'model': model,
                'temperature': temperature,
                'category': scenario["category"],
                'question': scenario["question"],
                'original_response': response,
                'final_content': final_content,
                'response_time': response_time,
                'context_length': len(context),
                'status': 'success',
                **evaluation_result
            }
            
        except Exception as e:
            return {
                'model': model,
                'temperature': temperature,
                'category': scenario["category"],
                'question': scenario["question"],
                'error': str(e),
                'status': 'error'
            }
    
    def run_parallel_benchmarks(self) -> Dict[str, Any]:
        """Run all benchmarks in parallel"""
        
        print("🚀 Starting Enhanced Legal AI Benchmarking")
        print("=" * 60)
        print(f"📊 Models: {Config.BENCHMARK_MODELS}")
        print(f"🌡️ Temperatures: {Config.BENCHMARK_TEMPERATURES}")
        print(f"📝 Scenarios: {len(Config.BENCHMARK_SCENARIOS)}")
        print(f"⚡ Parallel Threads: {Config.THREAD_POOL_SIZE}")
        print("=" * 60)
        
        # Get scenarios from config
        scenarios = Config.BENCHMARK_SCENARIOS
        
        # Prepare all benchmark tasks
        tasks = []
        for model in Config.BENCHMARK_MODELS:
            for temperature in Config.BENCHMARK_TEMPERATURES:
                for scenario in scenarios:
                    tasks.append((model, temperature, scenario))
        
        print(f"🔄 Running {len(tasks)} benchmark tests...")
        
        # Run benchmarks in parallel
        results = []
        with ThreadPoolExecutor(max_workers=Config.THREAD_POOL_SIZE) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self.run_single_benchmark, model, temp, scenario): (model, temp, scenario)
                for model, temp, scenario in tasks
            }
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(future_to_task):
                result = future.result()
                results.append(result)
                completed += 1
                
                # Progress update
                if completed % 4 == 0:
                    print(f"📈 Progress: {completed}/{len(tasks)} tests completed")
        
        # Generate summary
        summary = self._generate_summary(results)
        
        # Save results
        self._save_results(results, summary)
        
        return {
            'results': results,
            'summary': summary,
            'total_tests': len(tasks),
            'completed_tests': len([r for r in results if r['status'] == 'success']),
            'failed_tests': len([r for r in results if r['status'] == 'error'])
        }
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive summary of benchmark results"""
        
        successful_results = [r for r in results if r['status'] == 'success']
        
        if not successful_results:
            return {'error': 'No successful benchmark results'}
        
        # Calculate averages by model
        model_summaries = {}
        for model in Config.BENCHMARK_MODELS:
            model_results = [r for r in successful_results if r['model'] == model]
            if model_results:
                model_summaries[model] = self._calculate_model_summary(model_results)
        
        # Calculate overall averages
        overall_summary = self._calculate_overall_summary(successful_results)
        
        # Planning detection statistics
        planning_detected = sum(1 for r in successful_results if r.get('planning_detected', False))
        planning_rate = planning_detected / len(successful_results) if successful_results else 0
        
        return {
            'overall': overall_summary,
            'by_model': model_summaries,
            'planning_detection': {
                'total_detected': planning_detected,
                'detection_rate': planning_rate
            },
            'total_results': len(successful_results),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_model_summary(self, model_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary for a specific model"""
        
        scores = [r.get('comprehensive_score', 0) for r in model_results]
        response_times = [r.get('response_time', 0) for r in model_results]
        
        return {
            'avg_comprehensive_score': np.mean(scores),
            'avg_response_time': np.mean(response_times),
            'total_tests': len(model_results),
            'temperature_breakdown': self._get_temperature_breakdown(model_results)
        }
    
    def _calculate_overall_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall summary statistics"""
        
        scores = [r.get('comprehensive_score', 0) for r in results]
        response_times = [r.get('response_time', 0) for r in results]
        
        return {
            'avg_comprehensive_score': np.mean(scores),
            'avg_response_time': np.mean(response_times),
            'total_tests': len(results),
            'best_model': max(Config.BENCHMARK_MODELS, 
                            key=lambda m: np.mean([r.get('comprehensive_score', 0) 
                                                 for r in results if r['model'] == m]))
        }
    
    def _get_temperature_breakdown(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Get average scores by temperature"""
        temp_scores = {}
        for temp in Config.BENCHMARK_TEMPERATURES:
            temp_results = [r for r in results if r['temperature'] == temp]
            if temp_results:
                scores = [r.get('comprehensive_score', 0) for r in temp_results]
                temp_scores[f'temp_{temp}'] = np.mean(scores)
        return temp_scores
    
    def _save_results(self, results: List[Dict[str, Any]], summary: Dict[str, Any]):
        """Save results to files"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results as JSON
        results_file = Config.OUTPUTS_DIR / f"enhanced_benchmark_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump({
                'results': results,
                'summary': summary,
                'config': {
                    'models': Config.BENCHMARK_MODELS,
                    'temperatures': Config.BENCHMARK_TEMPERATURES,
                    'scenarios': len(Config.BENCHMARK_SCENARIOS)
                }
            }, f, indent=2)
        
        # Save summary as CSV
        csv_file = Config.OUTPUTS_DIR / f"enhanced_benchmark_summary_{timestamp}.csv"
        self._save_csv_summary(results, csv_file)
        
        # Save markdown table
        md_file = Config.OUTPUTS_DIR / f"enhanced_benchmark_table_{timestamp}.md"
        self._save_markdown_table(results, summary, md_file)
        
        print(f"💾 Results saved to:")
        print(f"   📄 JSON: {results_file}")
        print(f"   📊 CSV: {csv_file}")
        print(f"   📋 MD: {md_file}")
    
    def _save_csv_summary(self, results: List[Dict[str, Any]], filepath: Path):
        """Save results summary as CSV"""
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Model', 'Temperature', 'Category', 'Comprehensive_Score',
                'Response_Time', 'Word_Count', 'Citations', 'Planning_Detected'
            ])
            
            # Data
            for result in results:
                if result['status'] == 'success':
                    writer.writerow([
                        result['model'],
                        result['temperature'],
                        result['category'],
                        result.get('comprehensive_score', 0),
                        result.get('response_time', 0),
                        result.get('metrics', {}).get('word_count', 0),
                        result.get('metrics', {}).get('citation_count', 0),
                        result.get('planning_detected', False)
                    ])
    
    def _save_markdown_table(self, results: List[Dict[str, Any]], summary: Dict[str, Any], filepath: Path):
        """Save results as markdown table"""
        
        with open(filepath, 'w') as f:
            f.write("# Enhanced Legal AI Benchmark Results\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall summary
            f.write("## Overall Summary\n\n")
            f.write(f"- **Total Tests**: {summary['total_results']}\n")
            f.write(f"- **Average Score**: {summary['overall']['avg_comprehensive_score']:.2f}\n")
            f.write(f"- **Average Response Time**: {summary['overall']['avg_response_time']:.2f}s\n")
            f.write(f"- **Best Model**: {summary['overall']['best_model']}\n")
            f.write(f"- **Planning Detection Rate**: {summary['planning_detection']['detection_rate']:.1%}\n\n")
            
            # Model comparison table
            f.write("## Model Performance Comparison\n\n")
            f.write("| Model | Avg Score | Avg Response Time | Tests |\n")
            f.write("|-------|-----------|-------------------|-------|\n")
            
            for model, model_summary in summary['by_model'].items():
                f.write(f"| {model} | {model_summary['avg_comprehensive_score']:.2f} | "
                       f"{model_summary['avg_response_time']:.2f}s | {model_summary['total_tests']} |\n")
            
            f.write("\n## Detailed Results\n\n")
            f.write("| Model | Temp | Category | Score | Time | Words | Citations | Planning |\n")
            f.write("|-------|------|----------|-------|------|-------|-----------|----------|\n")
            
            for result in results:
                if result['status'] == 'success':
                    f.write(f"| {result['model']} | {result['temperature']} | {result['category']} | "
                           f"{result.get('comprehensive_score', 0):.2f} | "
                           f"{result.get('response_time', 0):.2f}s | "
                           f"{result.get('metrics', {}).get('word_count', 0)} | "
                           f"{result.get('metrics', {}).get('citation_count', 0)} | "
                           f"{'Yes' if result.get('planning_detected', False) else 'No'} |\n")

def main():
    """Main entry point for benchmarking"""
    
    try:
        runner = BenchmarkRunner()
        benchmark_results = runner.run_parallel_benchmarks()
        
        print("\n🎉 Benchmarking completed successfully!")
        print(f"✅ Completed: {benchmark_results['completed_tests']} tests")
        print(f"❌ Failed: {benchmark_results['failed_tests']} tests")
        print(f"📊 Overall Average Score: {benchmark_results['summary']['overall']['avg_comprehensive_score']:.2f}")
        
    except Exception as e:
        print(f"❌ Benchmarking failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
