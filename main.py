from fastapi import FastAPI, UploadFile, File, Form
from payment import Payment
import shutil

app = FastAPI()

# Initialize the Payment object
payment_checker = Payment()

@app.post("/pay")
async def pay(image: UploadFile = File(...), price: float = Form(...)):
    try:
        # Save the uploaded image
        with open(f"/tmp/{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Check payment using the saved image path
        image_path = f"/tmp/{image.filename}"
        is_paid = payment_checker.pay(image_path, price)

        return {"success": is_paid}
    except Exception as e:
        return {"error": str(e)}
