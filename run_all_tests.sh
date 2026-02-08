#!/bin/bash

# Run All Tests Script
# Runs all tests in sequence to verify the RAG system

echo ""
echo "======================================================================"
echo "🧪 RUNNING ALL RAG SYSTEM TESTS"
echo "======================================================================"
echo ""
echo "This will run 3 tests in sequence:"
echo "  1️⃣  Basic Retrieval (no LLM)"
echo "  2️⃣  Real Documents (no LLM)"  
echo "  3️⃣  Full RAG Pipeline (with LLM)"
echo ""
echo "⚠️  Make sure Ollama is running: ollama serve"
echo ""
read -p "Press Enter to continue..."

echo ""
echo "======================================================================"
echo "TEST 1: Basic Retrieval"
echo "======================================================================"
python tests/test_retrieval.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Test 1 failed! Fix errors before continuing."
    exit 1
fi

echo ""
read -p "✅ Test 1 passed! Press Enter to continue to Test 2..."

echo ""
echo "======================================================================"
echo "TEST 2: Real Documents"
echo "======================================================================"
python tests/test_real_docs.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Test 2 failed! Fix errors before continuing."
    exit 1
fi

echo ""
read -p "✅ Test 2 passed! Press Enter to continue to Test 3..."

echo ""
echo "======================================================================"
echo "TEST 3: Full RAG Pipeline"
echo "======================================================================"
python tests/test_rag_pipeline.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Test 3 failed! Check if Ollama is running."
    exit 1
fi

echo ""
echo "======================================================================"
echo "🎉 ALL TESTS PASSED!"
echo "======================================================================"
echo ""
echo "✅ Your RAG system is working perfectly!"
echo ""
echo "📝 Next steps:"
echo "   • Try the interactive CLI: python -m discord_rag_bot.cli.interactive"
echo "   • Set up Discord bot: See SETUP_GUIDE.md Step 5"
echo ""