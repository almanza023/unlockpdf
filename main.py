from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pikepdf
import io
import base64
import getpass

app = FastAPI()

@app.post("/remove-password/")
async def remove_password_from_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        password = ""
        with pikepdf.open(io.BytesIO(content), password=password) as pdf:
            output = io.BytesIO()
            pdf.save(output)
            output.seek(0)
            pdf_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
        return JSONResponse(content={"pdf": pdf_base64})
    except pikepdf.PasswordError:
        return JSONResponse(content={"error": "Incorrect password"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


  