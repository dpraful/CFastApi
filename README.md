pyinstaller --clean --onefile --noconsole --name "GatewayAPI" ^
--hidden-import=pyodbc ^
--hidden-import=dotenv ^
--hidden-import=httpx ^
--hidden-import=httpcore ^
--hidden-import=h11 ^
--collect-all fastapi ^
--collect-all uvicorn ^
--collect-all pyodbc ^
--collect-all dotenv ^
--collect-all httpx ^
gateway.py

uvicorn getway:app --host 0.0.0.0 --port 8000

pyinstaller --clean --onefile --noconsole --name "CommonGetAPI" ^
--hidden-import=pyodbc ^
--hidden-import=dotenv ^
--collect-all fastapi ^
--collect-all uvicorn ^
--collect-all pyodbc ^
--collect-all dotenv ^
commonget.py

uvicorn commonget:app --host 0.0.0.0 --port 8001

pyinstaller --clean --onefile --noconsole --name "CommonPostAPI" ^
--hidden-import=pyodbc ^
--hidden-import=dotenv ^
--collect-all fastapi ^
--collect-all uvicorn ^
--collect-all pyodbc ^
--collect-all dotenv ^
commonpost.py

uvicorn commonpost:app --host 0.0.0.0 --port 8002

pyinstaller --clean --onefile --noconsole --name "CommonMGetAPI" ^
--hidden-import=dotenv ^
--hidden-import=fastapi.responses ^
--collect-all fastapi ^
--collect-all uvicorn ^
--collect-all dotenv ^
commonmget.py

uvicorn commonmget:app --host 0.0.0.0 --port 8003

pyinstaller --clean --onefile --noconsole --name "CommonMPostAPI" ^
--hidden-import=dotenv ^
--hidden-import=python_multipart ^
--hidden-import=fastapi.responses ^
--collect-all fastapi ^
--collect-all uvicorn ^
--collect-all dotenv ^
commonmpost.py

uvicorn commonmget:app --host 0.0.0.0 --port 8004