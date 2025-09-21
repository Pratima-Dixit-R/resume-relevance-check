# Resume Relevance Check Application
# Main package initialization

__version__ = \"1.0.0\"
__author__ = \"Pratima Dixit R\"
__email__ = \"pratimadixit2305@gmail.com\"

# Configure Python path for relative imports
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Add src directory to path
src_path = project_root / \"src\"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)