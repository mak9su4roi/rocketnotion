import dropbox
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dropbox import Dropbox
from fastapi.encoders import jsonable_encoder
from inscription_recognizer import predict
from notion_script import embed
from notion.client import NotionClient



DROPBOX_TOKEN = 'PLACE_HOLDER'



app = FastAPI()
data = {"folder": None,
        "token": None,
        "notebooks": []}
dbx = Dropbox(DROPBOX_TOKEN)


def exist_dbx(path):
    try:
        dbx.files_get_metadata(path)
        return True
    except:
        return False



@app.get("/", response_class=HTMLResponse)
async def read_items(folder: str = None,
                     token: str = None,
                     ADDNotebook: str = None,
                     RMNotebook: str = None):
    if token:
        try:
            tkn = NotionClient(token_v2=token)
            del tkn
            data["token"] = token
        except:
            pass

    if folder:
        if exist_dbx(f'/{folder}'):
            data["folder"] = folder

    if ADDNotebook and not any([nb for nb in data["notebooks"] if nb["link"] == ADDNotebook]):
        if data["token"]:
            try:
                client = NotionClient(token_v2=data["token"])
                page = client.get_block(ADDNotebook)
                title = page.title
                data["notebooks"].append({"link": ADDNotebook, "title": title})
                del client
            except:
                pass

    if RMNotebook and any([nb for nb in data["notebooks"] if nb["title"] == RMNotebook]):
        data["notebooks"] = list(filter(lambda x: x["title"] != RMNotebook, data["notebooks"]))
    return f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
        <div style="background:#876C9D;color:white;padding:1vh;height:97vh">
            <div style="margin-left:40%">
            <form>
                  <label for="dsf">Dropbox folder:</label><br>
                  <input type="text" id="folder" name="folder">
                  <input type="submit" value="Submit">
            </form>
            <br>
            <br>
            <form>
                  <label for="nt">Notion Token:</label><br>
                  <input type="text" id="token" name="token">
                  <input type="submit" value="Submit">
            </form>
            <br>
            <br>
            <form>
                  <label for="dsf">Add Notebook:</label><br>
                  <input type="text" id="folder" name="ADDNotebook">
                  <input type="submit" value="Submit">
            </form>
            <br>
            <br>
            <form>
                  <label for="dsf">Remove Notebook:</label><br>
                  <input type="text" id="folder" name="RMNotebook">
                  <input type="submit" value="Submit">
            </form>
            <br>
            <br>
            <p> Dropbox folder: <span style='color:{"#62BAAC"*bool(data['folder']) or "red" }'> {data['folder'] or  "Not specified"}</span> <p>
            <p> Notion token:   <span style='color:{"#62BAAC"*bool(data['token']) or "red" }'> {"+"*bool(data['token']) or  "Not specified"}</span> <p>
            <p> Notebooks: 
            <ul>
              {" ".join([f'<li>{nb["title"]}: <span style="color:#62BAAC"> {ind} </span> </li>' for ind, nb in enumerate(data["notebooks"])])}
            </ul>
            </p>
            <br>
            <br>
            {'<a style="padding:2px;text-decoration:none;color:#876C9D;background-color:cyan;border:80% solid #876C9D" href="/dashboard">  choose photos </a>' if data['token'] and data['folder'] and data['notebooks'] else
            '<p> You need to specify: token, folder and at least one notebook </p>'}
            </div>
            </div>
        </body>
    </html>
    """


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
        <div style="background:#5F249F;padding:1vh;height:97vh">
            <div style="margin-left:40%">
                <form action="" method="post">
                    {" ".join([f'<input type="checkbox" id="{entry.name}" name="{entry.name}" value="+">' +
                               f'<label style="color:white" for="{entry.name}"> {entry.name} </label><br><br>'
                               for entry in dbx.files_list_folder(f"/{data['folder']}").entries if entry.name.endswith(".jpg")])}
                    <button name="btn" value="upvote"> Recognise and Insert </button>
                </form>
            </div>
        </div>
        </body>
    </html>
    """


def get_link(folder, file):
    link = dbx.sharing_create_shared_link(f"/{folder}/{file}").url.replace("dl=0", "raw=1")
    return link


@app.post("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    da = await request.form()
    da = jsonable_encoder(da)
    files = [{"name": key, "path": f"/{data['folder']}/{key}", "link": get_link(data['folder'], key),
              "inscription": None}
             for key, item in da.items() if key != "btn"]
    if not files:
        return "nothing"
    for elm in files:
        with open(f"files/{elm['name']}", "wb") as file:
            metadata, res = dbx.files_download(path=elm["path"])
            file.write(res.content)

    for elm in files:
        prd = predict(f"files/{elm['name']}")
        elm["inscription"] = int("".join(map(str, reversed(prd))), 2)
        if elm["inscription"] < len(data['notebooks']):
            embed(data["token"],
                  data["notebooks"][elm["inscription"]]["link"],
                  elm["link"])

    return f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
        <div style="background:#B1A8B9;color:white;text-align:center">
            {" ".join([f"<div class='img-with-text'> <img style='margin-top:10px;margin-bottom:10px' src='{file['link']}' "
                       f"height='500'/> <p> Notebook: {file['inscription']} ({'inserted'*(file['inscription'] < len(data['notebooks'])) or 'wrong inscription'}) </p> </div>" 
                       for file in files])}
        </div>
        </body>
    </html>
    """

