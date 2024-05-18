import httpx
from bs4 import BeautifulSoup as bs
from typing import Dict, Any
from fastapi import FastAPI
import html
from urllib.parse import quote, unquote

app = FastAPI()


@app.get("/")
async def get_home():
    return {"error": "bad request"}


@app.get("/{l}/{p}/")
async def receive_payload(l: str, p: str):
    print(p)
    if l != "" and p != "":
        try:
            decode_html_text = decode_html(l, p)
            print(decode_html_text)
            print(enecode_html("sdfsdf", "dsfsdf#dsgdsg"))
            return await get(decode_html_text["l"], decode_html_text["p"])
        except:
            return {"error": "bad request"}
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
        return data_res
    except httpx.RequestError as e:
        data_res = {
            "error": "RequestError"
        }
        return data_res
    except (AttributeError, KeyError) as e:
        data_res = {
            "error": "AttributeError"
        }
        return data_res



def decode_html(l_text: str, p_text: str) -> dict:
    decode_text = {"l": unquote(l_text), "p": unquote(p_text)}
    return decode_text


def enecode_html(l_text: str, p_text: str) -> dict:
    decode_text = {"l": quote(l_text), "p": quote(p_text)}
    return decode_text