#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Benchmarking Word Count ==="
echo ""

# Ensure Java files are compiled
echo "Compiling Java WordCount..."
cd ../003
nix develop --command bash -c 'javac WordCount.java' || true
cd ../004

echo ""
echo "Running WordCount benchmarks with hyperfine..."
echo ""

nix develop --command bash <<'EOF'
hyperfine \
    --warmup 1 \
    --runs 5 \
    --export-json wordcount_benchmark.json \
    --export-markdown wordcount_benchmark.md \
    --command-name "Java WordCount" "cd ../003 && nix develop --command bash -c 'java WordCount > /dev/null 2>&1'" \
    --command-name "JavaScript WordCount" "cd /home/nab/Niklas/ParallelComputing_Course_Tuebingen/004 && nix develop --command bash -c 'node word_count.js > /dev/null 2>&1'"
EOF

echo ""
echo "WordCount benchmark results:"
cat wordcount_benchmark.md

echo ""
echo ""
echo "=== Benchmarking Image Pipeline ==="
echo ""

# Ensure Java files are compiled
echo "Compiling Java ImagePipeline..."
cd ../003
nix develop --command bash -c 'javac ImagePipeline.java' || true
cd ../004

# Clean output directories
rm -rf out ../003/out
mkdir -p out ../003/out

echo ""
echo "Running ImagePipeline benchmarks with hyperfine..."
echo ""

nix develop --command bash <<'EOF'
hyperfine \
    --warmup 1 \
    --runs 5 \
    --export-json imagepipeline_benchmark.json \
    --export-markdown imagepipeline_benchmark.md \
    --command-name "Java ImagePipeline" "cd ../003 && rm -rf out && mkdir -p out && nix develop --command bash -c 'java ImagePipeline > /dev/null 2>&1'" \
    --command-name "JavaScript ImagePipeline" "cd /home/nab/Niklas/ParallelComputing_Course_Tuebingen/004 && rm -rf out && mkdir -p out && nix develop --command bash -c 'node image_pipeline.js > /dev/null 2>&1'"
EOF

echo ""
echo "ImagePipeline benchmark results:"
cat imagepipeline_benchmark.md

echo ""
echo ""
echo "=== All benchmarks completed ==="
echo "Results saved to:"
echo "  - wordcount_benchmark.json"
echo "  - wordcount_benchmark.md"
echo "  - imagepipeline_benchmark.json"
echo "  - imagepipeline_benchmark.md"

