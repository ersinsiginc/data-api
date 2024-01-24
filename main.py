# uvicorn main:app --reload
# http://127.0.0.1:8000/?tableName=NOTIFICATIONS

from fastapi import FastAPI
import os
import pandas as pd
import json

app = FastAPI()


@app.get("/")
def read_root(tableName: str):
    data_dir = 'extracktedData'
    data = []
    file_path = os.path.join(data_dir, tableName + '.csv')

    if not os.path.exists(file_path):
        return {"error": "Belirtilen tablo bulunamadı."}
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip', sep=';')
        if len(df) > 1000:
            df = df.tail(1000)
        result = df.to_json(orient="index")
        parsed = json.loads(result)
        data.append(parsed)
        return {tableName: data}
    except pd.errors.ParserError as e:
        return {"error": f"Tablo okunurken bir hata oluştu: {str(e)}"}
