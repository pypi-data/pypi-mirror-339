#!/usr/bin/env python3
"""
Benchmark script for ProventraCore.

This script runs a comprehensive benchmark of the ProventraCore library
on a set of test cases to evaluate detection accuracy, sanitization efficiency,
and performance.

Usage:
    python run_benchmark.py --model_path <path_to_classifier_model> --provider <llm_provider> --model_name <llm_model_name>

Example:
    python run_benchmark.py --model_path "./models/classifier" --provider "google" --model_name "gemini-1.5-flash"
"""

import argparse
import json
import os
import time
from typing import Any, Dict, Optional

from data.test_data import TEST_DATA
from utils import NumpyEncoder, run_benchmark_on_guard

from proventra_core import GuardService, LLMSanitizer, TransformersAnalyzer


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Benchmark for ProventraCore")

    parser.add_argument(
        "--model_path",
        type=str,
        default="proventra/mdeberta-v3-base-prompt-injection",
        help="Path to transformer model for text analysis",
    )

    parser.add_argument(
        "--provider",
        type=str,
        default="google",
        choices=["google", "openai", "anthropic", "mistral"],
        help="LLM provider for sanitization",
    )

    parser.add_argument(
        "--model_name",
        default="gemini-2.0-flash",
        type=str,
        help="Specific model name for sanitization",
    )

    parser.add_argument(
        "--temperature", type=float, default=0.1, help="Temperature for LLM generation"
    )

    parser.add_argument(
        "--max_tokens", type=int, default=4096, help="Maximum tokens for LLM generation"
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Risk score threshold for attack detection",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        default="./benchmark/results",
        help="Directory to save benchmark results",
    )

    parser.add_argument(
        "--unsafe_label",
        type=str,
        default="INJECTION",
        help="Label used by the classifier model to identify unsafe content",
    )

    parser.add_argument(
        "--api_key",
        type=str,
        help="API key for LLM provider (if not in environment variables)",
    )

    return parser.parse_args()


def setup_guard_service(
    model_path: str,
    unsafe_label: str,
    provider: str,
    model_name: Optional[str] = None,
    temperature: float = 0.1,
    max_tokens: int = 4096,
    threshold: float = 0.5,
    api_key: Optional[str] = None,
) -> GuardService:
    """Set up a GuardService instance for benchmarking."""
    print(f"Setting up analyzer with model: {model_path}")
    analyzer = TransformersAnalyzer(
        model_name=model_path, unsafe_label=unsafe_label, threshold=threshold
    )

    print(f"Setting up sanitizer with provider: {provider}, model: {model_name}")
    sanitizer = LLMSanitizer(
        provider=provider,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
    )

    print("Setting up GuardService")
    return GuardService(analyzer, sanitizer)


def setup_output_directory(output_dir: str, model_path: str, model_name: str) -> str:
    """Set up the output directory with a timestamp."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    normalized_model_name = model_name.replace("/", "-")
    normalized_model_path = model_path.replace("/", "-")
    benchmark_dir = (
        f"{output_dir}/{timestamp}_{normalized_model_path}_{normalized_model_name}"
    )

    # Create output directory
    os.makedirs(benchmark_dir, exist_ok=True)
    print(f"Created output directory: {benchmark_dir}")

    return benchmark_dir


def save_config(config: Dict[str, Any], output_dir: str) -> None:
    """Save benchmark configuration."""
    config_file = f"{output_dir}/benchmark_config.json"

    with open(config_file, "w") as f:
        json.dump(config, f, indent=2, cls=NumpyEncoder)

    print(f"Saved benchmark configuration to {config_file}")


def main():
    # Parse command line arguments
    args = parse_args()

    # Set up output directory
    output_dir = setup_output_directory(
        args.output_dir, args.model_path, args.model_name
    )

    # Save configuration
    config = {
        "model_path": args.model_path,
        "provider": args.provider,
        "model_name": args.model_name,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "unsafe_label": args.unsafe_label,
        "threshold": args.threshold,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_config(config, output_dir)

    # Set up guard service
    guard_service = setup_guard_service(
        model_path=args.model_path,
        unsafe_label=args.unsafe_label,
        provider=args.provider,
        model_name=args.model_name,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        threshold=args.threshold,
        api_key=args.api_key,
    )

    # Run benchmark
    results, report = run_benchmark_on_guard(
        guard_service=guard_service, test_data=TEST_DATA, output_dir=output_dir
    )

    # Print summary
    print("\n===== BENCHMARK COMPLETE =====")
    print(f"Total samples: {report['summary']['total_samples']}")
    print(f"Detection accuracy: {report['detection']['accuracy']:.2f}")

    # Calculate false positive rate safely
    fp = report["detection"]["false_positives"]
    tn = report["detection"]["true_negatives"]
    fp_rate = fp / (fp + tn) if (fp + tn) > 0 else 0
    print(f"False positive rate: {fp_rate:.2f}")

    print(
        f"Sanitization success rate: {report['sanitization']['sanitization_success_rate']:.2f}"
    )
    print(
        f"Average processing time: {report['performance']['avg_processing_time']:.2f} seconds"
    )
    print("\nRisk Score Metrics:")
    print(
        f"  Average attack risk score: {report['detection']['avg_attack_risk_score']:.2f}"
    )
    print(
        f"  Average benign risk score: {report['detection']['avg_benign_risk_score']:.2f}"
    )
    print(f"  Risk score std deviation: {report['detection']['risk_score_std']:.2f}")
    print(f"\nResults saved to: {output_dir}")


if __name__ == "__main__":
    main()
