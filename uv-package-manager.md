To start a **FastAPI** project with **uv**, follow these steps:  

---

### **1. Install `uv` (if not already installed)**
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Or, using `pipx`:
```sh
pipx install uv
```

---

### **2. Create a New FastAPI Project**
```sh
mkdir my_fastapi_project && cd my_fastapi_project
```

---

### **3. Initialize a Virtual Environment**
```sh
uv init
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

---

### **4. Install FastAPI and Uvicorn**
```sh
uv add fastapi "uvicorn[standard]"
```

---

### **5. Create `main.py`**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with uv!"}
```

---

### **6. Run FastAPI**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Your API will be live at:  
- 🌍 `http://127.0.0.1:8000/`
- 📜 Swagger UI: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- 📖 Redoc UI: [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)

 

That's it! 🎉 Your FastAPI project is up and running with **uv**. 🚀 Let me know if you need any modifications! 😊

**********************************************

Create and Activate Virtual Environment
- uv venv
- .\.venv\Scripts\activate   (for windows)
- uv sync

**********************************************


### Here are some **`uv`** commands that you can use for managing your FastAPI project:  

### **1. Project Initialization & Setup**
- **Initialize a new project** (creates `pyproject.toml`)  
  ```sh
  uv init
  ```
- **Add dependencies**  
  ```sh
  uv add fastapi uvicorn sqlalchemy
  ```
- **Add dev dependencies** (e.g., for testing & formatting)  
  ```sh
  uv add --dev pytest black isort
  ```

### **2. Installing & Managing Dependencies**
- **Install all dependencies (from `uv.lock`)**  
  ```sh
  uv install
  ```
- **Remove a dependency**  
  ```sh
  uv remove fastapi
  ```
- **Upgrade all dependencies**  
  ```sh
  uv upgrade
  ```
- **Upgrade a specific dependency**  
  ```sh
  uv upgrade fastapi
  ```

### **3. Running & Checking Dependencies**
- **List all installed dependencies**  
  ```sh
  uv list
  ```
- **Check for dependency updates**  
  ```sh
  uv outdated
  ```

### **4. Running Your FastAPI App**
- **Run the FastAPI server with Uvicorn**  
  ```sh
  uvicorn main:app --reload
  ```

### **5. Virtual Environment & Shell**
- **Start a shell in the project environment**  
  ```sh
  uv venv
  ```
- **Run a command inside the virtual environment**  
  ```sh
  uv run python script.py
  ```

### **6. Lock File Management**
- **Regenerate `uv.lock`**  
  ```sh
  uv sync
  ```
- **Check if dependencies are consistent**  
  ```sh
  uv doctor
  ```

### **7. Clean Up & Uninstall**
- **Remove all installed dependencies**  
  ```sh
  uv pip freeze | xargs uv remove
  ```
- **Remove all unused dependencies**  
  ```sh
  uv prune
  ```

Would you like me to suggest a `pyproject.toml` template for your FastAPI project? 🚀



