from sanic import Sanic
from sanic.response import text, json
from pathlib import Path
import aiosqlite
import datetime

app = Sanic("MyHelloWorldApp")

@app.get("/")
async def hello_world(request):
	return text("Hello, world.")
    
@app.get("/despedida")
async def bye_world(request):
	return text("Good bye, world!.")

@app.post("/entrada")
async def entrada(request):
	## Se activa cuando no hay json
	if not request.json:
		return json({"R":False})
	jo = request.json
	# reviso si existe voltaje
	if not 'voltaje' in jo:
		return json({"R":False})
	# reviso si existe region
	if not 'region' in jo:
		return json({"R":False})
	# reviso si existe esp
	if not 'esp' in jo:
		return json({"R":False})
	### conexion a base de datos
	## Existe la base de datos?
	Fdb = Path('.') / 'basedatos.db'
	if not Fdb.resolve().exists():
		return json({"R":False})
		
	db = await aiosqlite.connect(str(Fdb.resolve()))
	SQL = "insert into Registro values(?,?,?,?)"
	ahora = datetime.datetime.now()
	cursor = await db.execute(SQL,[
		jo['esp'],
		jo['region'], # reg
		jo['voltaje'], # valor
		ahora.isoformat()
	])
	await db.commit()
	await db.close()
	return json({"R":True})
