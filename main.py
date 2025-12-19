from fastapi import FastAPI
from pydantic import BaseModel
from orchestrator import handle_query

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    propertyId: str | None = None 

# forwards to orchestrator 

@app.post("/query")
def query_endpoint(req: QueryRequest):
    return handle_query(req.query, req.propertyId)

# done
