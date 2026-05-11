import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from classify import classify, classify_csv 

app = FastAPI()

@app.post("/classify-logs/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    try:
        df = pd.read_csv(file.file)
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV file must contain 'source' and 'log_message' columns.")
        
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))
                
        output_file = "output.csv"
        df.to_csv(output_file, index=False)
        return FileResponse(output_file, media_type="text/csv")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()
        
if __name__ == "__main__":
    classify_csv("resources/test.csv")
      