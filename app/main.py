from fastapi import FastAPI

import os
import platform 

app_name = os.getenv("APP_NAME","Python REST API ")
app_version = os.getenv("APP_VERSION","1.0.0")
app = FastAPI(title=app_name, version=app_version)

@app.get('/')
def home():

    return {"Welcome":"Application",
            "application":app_name,
            "current_version":app_version}


@app.get('/health')
def status():

    return {"status": "healthy"}

@app.get('/api/info')
def info():
    return {"application":app_name,"version":app_version,
            "python version":platform.python_version(),
            "runtime":platform.python_implementation(),
            
            }


@app.get("/api/demo")
def demo():
    return {
        "message": "Hello from FastAPI!",
        "environment": "production",
        "version": "1.0.0",
        "deployment": "CI/CD successful"
    }