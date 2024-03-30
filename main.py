import httpx
from bs4 import BeautifulSoup as bs
from typing import Dict, Any
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def get_home():
    return {"error": "bad request"}


@app.post("/")
async def receive_payload(payload: dict):
    if len(payload) and payload["l"] != "" and payload["p"] != "":
        return await get(payload["l"], payload["p"])
    else:
        return {"error": "bad request"}


async def get(l: str, p: str) -> Dict[str, Any]:
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    }

    data = {
        '98login98': l,
        '11password11': p,
    }

    try:
        async with httpx.AsyncClient() as client:

            resp = await client.post('http://vpn.vimos.ru:36382/action.php', headers=headers, data=data,
                                     follow_redirects=True)

            resp.raise_for_status()  # Проверяем успешность запроса
            soup = bs(resp.text, "lxml")
            pas = soup.findAll("span", class_="accentuated")
            if len(pas) == 2:
                data_res = {
                    "l": pas[0].text,
                    "p": pas[1].text
                }
            else:
                data_res = {
                    "error": "bad answer"
                }

    except httpx.RequestError as e:
        data_res = {
            "error": "RequestError"
        }
    except (AttributeError, KeyError) as e:
        data_res = {
            "error": "AttributeError"
        }
    return data_res
