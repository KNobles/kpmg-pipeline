from fastapi import FastAPI, status
from algolia import get_CLA_by_id, get_CLA_by_name, get_CLAs, initialize_database, get_CLAs_by_keyword, get_comparison

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    initialize_database() 

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return "Alive"


@app.get("/cla", status_code=status.HTTP_200_OK)
async def cla_get():
    CLA_list = get_CLAs()

    return CLA_list

@app.get("/cla/{id}", status_code=status.HTTP_200_OK)
async def cla_by_id_get(id: str):
    CLA = get_CLA_by_id(id)

    return CLA

@app.get("/cla", status_code=status.HTTP_200_OK)
async def cla_by_name_get(name: str):
    CLA = get_CLA_by_name(name)

    return CLA


@app.get("/search", status_code=status.HTTP_200_OK, response_model=list[dict])
async def search_get(keyword: str):
    CLA_list = get_CLAs_by_keyword(keyword)

    return CLA_list

@app.get("/comparison/{id}", status_code=status.HTTP_200_OK)
async def comparison_get(id: str):
    comparison = get_comparison(id)

    return comparison
