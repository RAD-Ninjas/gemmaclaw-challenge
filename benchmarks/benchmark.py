#!/usr/bin/env python3
"""
GemmaClaw Benchmark — Measure Gemma 4 performance on your hardware.
Runs 3 standardized prompts and reports timing.
"""

import requests
import time
import platform
import os

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = os.environ.get("GEMMACLAW_MODEL", "gemma4:e2b")

PROMPTS = [
    {
        "name": "Short (haiku)",
        "message": "Write a haiku about a robot.",
        "expected_tokens": 20
    },
    {
        "name": "Medium (explanation)",
        "message": "Explain how a CPU cache works in 3 sentences.",
        "expected_tokens": 80
    },
    {
        "name": "Long (story)",
        "message": "Write a short story (150 words) about an AI that lives on a tiny computer.",
        "expected_tokens": 200
    }
]


def get_system_info():
    """Gather basic system info for the report."""
    info = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or "unknown",
    }
    # Try to get RAM
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    info["ram_gb"] = round(kb / 1024 / 1024, 1)
                    break
    except FileNotFoundError:
        # macOS
        try:
            import subprocess
            result = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True)
            info["ram_gb"] = round(int(result.stdout.strip()) / (1024**3), 1)
        except Exception:
            info["ram_gb"] = "unknown"
    return info


def run_prompt(prompt_info):
    """Run a single prompt and measure performance."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt_info["message"]}],
        "stream": False
    }

    start = time.time()
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Error: Ollama not running. Start with: ollama serve")
        return None

    elapsed = time.time() - start
    result = response.json()

    # Ollama includes eval metrics in response
    eval_count = result.get("eval_count", 0)
    eval_duration = result.get("eval_duration", 0)  # nanoseconds

    if eval_duration > 0:
        tok_per_sec = eval_count / (eval_duration / 1e9)
    elif elapsed > 0 and eval_count > 0:
        tok_per_sec = eval_count / elapsed
    else:
        tok_per_sec = 0

    return {
        "name": prompt_info["name"],
        "tokens": eval_count,
        "elapsed_sec": round(elapsed, 2),
        "tok_per_sec": round(tok_per_sec, 1),
        "response_preview": result["message"]["content"][:80]
    }


def main():
    print("=" * 55)
    print("  GemmaClaw Benchmark")
    print("=" * 55)
    print()

    sys_info = get_system_info()
    print(f"System:  {sys_info['platform']}")
    print(f"Arch:    {sys_info['machine']}")
    print(f"RAM:     {sys_info.get('ram_gb', '?')} GB")
    print(f"Model:   {MODEL}")
    print()

    results = []
    for i, prompt in enumerate(PROMPTS):
        print(f"[{i+1}/{len(PROMPTS)}] Running: {prompt['name']}...")
        result = run_prompt(prompt)
        if result is None:
            return
        results.append(result)
        print(f"  {result['tokens']} tokens in {result['elapsed_sec']}s = {result['tok_per_sec']} tok/s")
        print(f"  Preview: {result['response_preview']}...")
        print()

    print("-" * 55)
    print("RESULTS SUMMARY")
    print("-" * 55)
    print(f"{'Test':<20} {'Tokens':<8} {'Time':<8} {'Tok/s':<8}")
    print("-" * 55)
    for r in results:
        print(f"{r['name']:<20} {r['tokens']:<8} {r['elapsed_sec']:<8} {r['tok_per_sec']:<8}")

    avg_tps = sum(r["tok_per_sec"] for r in results) / len(results)
    print("-" * 55)
    print(f"{'Average':<20} {'':<8} {'':<8} {round(avg_tps, 1):<8}")
    print()
    print("Share these results at the showcase or add them to benchmarks/README.md!")


if __name__ == "__main__":
    main()
