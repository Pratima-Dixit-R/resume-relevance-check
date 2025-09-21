#!/usr/bin/env python3
\"\"\"
Dependency Test Script for Resume Relevance Check Application
Tests all installed packages and their functionality
\"\"\"

import sys
import os
from pathlib import Path
import importlib
import traceback
import subprocess
from typing import List, Tuple

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / \"src\"))

def test_package_import(package_name: str, test_function=None) -> Tuple[bool, str]:
    \"\"\"
    Test if a package can be imported and optionally run a test function
    \"\"\"
    try:
        module = importlib.import_module(package_name)
        if test_function:
            test_function(module)
        return True, f\"✅ {package_name} - OK\"
    except ImportError as e:
        return False, f\"❌ {package_name} - ImportError: {e}\"
    except Exception as e:
        return False, f\"⚠️ {package_name} - Error: {e}\"

def test_transformers(module):
    \"\"\"Test transformers functionality\"\"\"
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(\"bert-base-uncased\")
    tokens = tokenizer(\"Hello world\")
    assert len(tokens['input_ids']) > 0

def test_sentence_transformers(module):
    \"\"\"Test sentence transformers functionality\"\"\"
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([\"This is a test sentence\"])
    assert embeddings.shape[0] == 1

def test_fastapi(module):
    \"\"\"Test FastAPI functionality\"\"\"
    from fastapi import FastAPI
    app = FastAPI()
    assert app is not None

def test_streamlit(module):
    \"\"\"Test Streamlit functionality\"\"\"
    import streamlit as st
    # Basic import test
    assert hasattr(st, 'write')

def test_plotly(module):
    \"\"\"Test Plotly functionality\"\"\"
    import plotly.graph_objects as go
    fig = go.Figure(data=go.Bar(x=[1, 2, 3], y=[1, 3, 2]))
    assert fig is not None

def test_sklearn(module):
    \"\"\"Test scikit-learn functionality\"\"\"
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([\"hello world\", \"hello universe\"])
    assert matrix.shape[0] == 2

def test_pypdf2(module):
    \"\"\"Test PyPDF2 functionality\"\"\"
    from PyPDF2 import PdfReader
    # Just test import
    assert PdfReader is not None

def test_docx(module):
    \"\"\"Test python-docx functionality\"\"\"
    import docx
    # Just test import
    assert docx is not None

def test_sqlalchemy(module):
    \"\"\"Test SQLAlchemy functionality\"\"\"
    from sqlalchemy import create_engine, text
    engine = create_engine(\"sqlite:///:memory:\")
    with engine.connect() as conn:
        result = conn.execute(text(\"SELECT 1\"))
        assert result.fetchone()[0] == 1

def test_custom_modules():
    \"\"\"Test custom application modules\"\"\"
    results = []
    
    # Test custom modules
    custom_tests = [
        (\"parsing.resume_parser\", None),
        (\"parsing.jd_parser\", None),
        (\"scoring.hard_match\", None),
        (\"scoring.semantic_match\", None),
        (\"scoring.verdict\", None),
        (\"storage.database\", None),
        (\"utils.text_extraction\", None),
        (\"utils.embeddings\", None),
    ]
    
    for module_name, test_func in custom_tests:
        success, message = test_package_import(module_name, test_func)
        results.append((success, message))
    
    return results

def main():
    print(\"🧪 Resume Relevance Check - Dependency Test Suite\")
    print(\"=\" * 60)
    
    # Core dependencies to test
    dependencies = [
        (\"fastapi\", test_fastapi),
        (\"uvicorn\", None),
        (\"streamlit\", test_streamlit),
        (\"plotly\", test_plotly),
        (\"sqlalchemy\", test_sqlalchemy),
        (\"transformers\", test_transformers),
        (\"sentence_transformers\", test_sentence_transformers),
        (\"torch\", None),
        (\"sklearn\", test_sklearn),
        (\"numpy\", None),
        (\"pandas\", None),
        (\"PyPDF2\", test_pypdf2),
        (\"docx\", test_docx),
        (\"requests\", None),
        (\"aiofiles\", None),
        (\"python_dotenv\", None),
    ]
    
    print(\"\n📦 Testing Core Dependencies:\")
    print(\"-\" * 40)
    
    all_success = True
    failed_packages = []
    
    for package_name, test_func in dependencies:
        success, message = test_package_import(package_name, test_func)
        print(message)
        if not success:
            all_success = False
            failed_packages.append(package_name)
    
    print(\"\n🔧 Testing Custom Modules:\")
    print(\"-\" * 40)
    
    custom_results = test_custom_modules()
    for success, message in custom_results:
        print(message)
        if not success:
            all_success = False
    
    print(\"\n🐍 Python Environment Info:\")
    print(\"-\" * 40)
    print(f\"Python Version: {sys.version}\")
    print(f\"Python Path: {sys.executable}\")
    print(f\"Project Root: {project_root}\")
    
    print(\"\n📊 Test Summary:\")
    print(\"-\" * 40)
    
    if all_success:
        print(\"🎉 All tests passed! Your environment is ready.\")
        print(\"\n🚀 Ready to start the application:\")
        print(\"   • FastAPI: python -m uvicorn src.api.main:app --reload\")
        print(\"   • Streamlit: python -m streamlit run src/dashboard/streamlit_app.py\")
    else:
        print(f\"❌ {len(failed_packages)} package(s) failed to import.\")
        print(\"\n📥 To install missing packages:\")
        print(\"   pip install -r requirements.txt\")
        
        if failed_packages:
            print(\"\n🔧 Failed packages:\")
            for pkg in failed_packages:
                print(f\"   • {pkg}\")
    
    print(\"\n\" + \"=\" * 60)
    return all_success

if __name__ == \"__main__\":
    success = main()
    sys.exit(0 if success else 1)