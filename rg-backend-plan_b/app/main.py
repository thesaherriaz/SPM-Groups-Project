from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import ResearchGapRequest, ResearchGapResponse
from app.services.gemini_service import get_research_gaps, is_relevant_query

app = FastAPI(title="Research Genie Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Research Genie API"}


@app.post("/research-gaps", response_model=ResearchGapResponse)
def get_research_gaps_endpoint(request: ResearchGapRequest):
    check = is_relevant_query(request.query)
    if not check["relevant"] or not check["safe"]:
        raise HTTPException(status_code=400, detail=check["message"])

    research_gap = get_research_gaps(request.query)
    gaps_list = research_gap.get("gaps", [])
    return ResearchGapResponse(gaps=gaps_list)


@app.get("/researchgap", response_model=ResearchGapResponse)
def get_research_gaps_get_endpoint(query: str):
    check = is_relevant_query(query)
    if not check["relevant"] or not check["safe"]:
        raise HTTPException(status_code=400, detail=check["message"])

    research_gap = get_research_gaps(query)
    gaps_list = research_gap.get("gaps", [])
    return ResearchGapResponse(gaps=gaps_list)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend running successfully"}
