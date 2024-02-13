import os.path
from contextlib import asynccontextmanager
from base.oracle import OracleClientUtil
from oracle.outbound import get_data
import glob, re, json, asyncio
from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists(public_json_dir):
        refresh_json()
    asyncio.create_task(timer(refresh_time))
    yield


app = FastAPI(lifespan=lifespan)
app.setup()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
public_json_dir = "./static/data.json"
refresh_time = 10 # 设定刷新时间, 单位分钟


def main():
    files = glob.glob("./configs/*.conf")
    response = {}
    response["code"] = 0
    response["OracleCloud"] = []
    for file_name in files:
        with open(file_name, "r", encoding="utf-8") as f:
            profile_name = f.readline()
            profile_name = re.sub("[\n\[\]]", "", profile_name)
            f.close()
        ocu = OracleClientUtil(file_name, profile_name)
        response["OracleCloud"].append(get_data(ocu, profile_name))
    response["code"] = 200
    return response


def refresh_json():
    response_json = main()
    with open(public_json_dir, "w", encoding="utf-8") as f:
        json.dump(response_json, f)
        f.close()


async def timer(separate_time):
    while True:
        refresh_json()
        await asyncio.sleep(separate_time * 60)


@app.get("/")
async def index():
    return FileResponse("./static/index.html")

# 想不到其他解决办法, 太菜, 能用就行
@app.get("/assets/{filename:path}")
async def assets(filename: str):
    if '.js' in filename:
        return FileResponse(f"./static/assets/{filename}", media_type="application/javascript")
    if '.css' in filename:
        return FileResponse(f"./static/assets/{filename}", media_type="text/css")


@app.get("/data")
@app.post("/data")
async def web():
    with open(public_json_dir, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000)
