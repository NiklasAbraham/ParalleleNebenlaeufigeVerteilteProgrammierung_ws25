#!/usr/bin/env bash
set -euo pipefail

# Get into nix environment and run tests
cd "$(dirname "$0")"

echo "=== Testing Java Compilation and Execution ==="
echo ""

# Compile all Java files
echo "1. Compiling Java files..."
nix develop --command bash <<'EOF'
javac Mergesort.java WordCount.java ImagePipeline.java 2>&1
echo "Compilation exit code: $?"
ls -1 *.class 2>&1 | head -10
EOF

echo ""
echo "2. Testing Mergesort (small test with timeout)..."
nix develop --command bash <<'EOF'
timeout 60 java Mergesort 2>&1 | head -30 || echo "Test completed or timed out"
EOF

echo ""
echo "3. Testing WordCount (will download books, may take time)..."
nix develop --command bash <<'EOF'
timeout 180 java WordCount 2>&1 | tail -20 || echo "Test completed or timed out"
EOF

echo ""
echo "4. Testing ImagePipeline (will download images)..."
nix develop --command bash <<'EOF'
timeout 120 java ImagePipeline 2>&1 | tail -20 || echo "Test completed or timed out"
ls -1 out/*.png 2>&1 | head -5 || echo "No output images found"
EOF

echo ""
echo "=== All tests completed ==="

