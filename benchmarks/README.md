# Benchmarks

Measure and share your hardware's performance with Gemma 4.

## Quick Benchmark

```bash
# Simple speed test — time a known prompt
time ollama run gemma4:e2b "Write a haiku about a robot learning to cook" --verbose
```

The `--verbose` flag shows tokens/second at the end.

## Structured Benchmark

Use the benchmark script to run a standardized set of prompts and record results:

```bash
python3 benchmark.py
```

This runs 3 prompts of increasing complexity and reports:
- Tokens per second (generation speed)
- Time to first token (latency)
- Total generation time

## Share Your Results

Add your results to the table below via PR or share at the showcase!

| Hardware | RAM | Model | Quantization | Tok/s | Notes |
|----------|-----|-------|-------------|-------|-------|
| Raspberry Pi 5 | 8GB | E2B | Q4_K_M | 2-5 | Default setup |
| Mac M1 | 8GB | E2B | Q4_K_M | 30-45 | |
| Mac M1 | 16GB | E4B | Q4_K_M | 25-35 | |
| Jetson Orin Nano | 8GB | E2B | Q4_K_M | 20-30 | GPU accelerated |
| Pixel 8 | 8GB | E2B | Q4_K_M | ~48 | Via Termux |

*These are approximate — your results may vary.*
