import os
import sys
import uvicorn

backend_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
src_path = os.path.abspath(os.path.join(backend_path, 'src'))
api_path = os.path.abspath(os.path.join(src_path, 'api'))

if src_path not in sys.path:
    sys.path.append(src_path)
if api_path not in sys.path:
    sys.path.append(api_path)
    
from api import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
