from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
import mysql.connector
from fastapi.responses import JSONResponse

app = FastAPI()
db = mysql.connector.connect(
    user='test',
    password='test',
    host='localhost',
    database='blogapplication'
)
cursor = db.cursor()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class FormData(BaseModel):
    id: int
    name: str
    age: int

@app.post("/submit")
async def handle_form_submission(data: FormData):
    try:
        id =data.id
        name = data.name
        age = data.age
        sql="insert into students(id,name,age) values(%s,%s,%s)"
        cursor.execute(sql,(id,name,age))
        db.commit()
        print(f"Received ID:{id}, Name: {name}, Age: {age}")
        return {"message": "Data received successfully", "ID":id, "name": name, "age": age}
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get('/student')
def getstudent():
   return "Hi"
@app.get('/student/{id}')
def getstudent(id):
    cursor.execute(f"select * from students where id={id}")
    result=cursor.fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return [{'id': row[0], 'name': row[1], 'age': row[2]} for row in result]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")

