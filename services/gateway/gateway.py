"""
Simple API Gateway for local development
Routes requests to appropriate microservices
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="API Gateway")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service mapping
SERVICES = {
    "user": "http://localhost:8001",
    "product": "http://localhost:8002",
    "order": "http://localhost:8003",
    "supplier": "http://localhost:8004",
    "customer": "http://localhost:8005",
}

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request):
    """Route requests to appropriate service"""
    
    if service not in SERVICES:
        return {"error": f"Service '{service}' not found"}, 404
    
    # Build target URL
    target_url = f"{SERVICES[service]}/{path}"
    
    # Get request body
    body = await request.body()
    
    # Forward request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=dict(request.headers),
                content=body,
                params=dict(request.query_params),
                timeout=30.0
            )
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except Exception as e:
            return {"error": f"Failed to connect to {service} service: {str(e)}"}, 503

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "message": "Gateway is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
