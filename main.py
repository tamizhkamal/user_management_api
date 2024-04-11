
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from database import get_db,engine
from user import models as user_models
from user.main import router as user_router
import uvicorn
from Auth.main import router as auth_router
import stripe

app = FastAPI()

origins = ['*']


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


user_models.Base.metadata.create_all(engine)

app.include_router(auth_router)
app.include_router(user_router)

# Set your Stripe secret key
# stripe.api_key = "sk_test_51P3KnESEX2FMsJ0t0qhk5R1x18pVZ5Kf7pIE3Cvs3OqsjdC8s4H5eqvjxYnXNKZisx9vyY0iRmdPubgqvw04mmow00oHLSiwZP"

# import httpx

# # Use httpx instead of requests
# @app.post("/charge")
# async with httpx.AsyncClient() as client:
#     charge = await client.post("https://api.stripe.com/v1/charges",data={"amount": amount,"currency": "usd","source": token,"description": "Example charge"},headers={"Authorization": f"Bearer {stripe.api_key}"}
#     )
#     charge.raise_for_status()  # Raise an error if the response is not successful
#     return {"status": "success", "charge": charge.json()}



# @app.post("/charge")
# async def charge(token: str, amount: int):
#     try:
#         # Create a charge using the Stripe API
#         charge = stripe.Charge.create(
#             amount=amount,
#             currency="int",
#             source=token,  # The token representing the card obtained from the client-side
#             description="Example charge"
#         )
#         return {"status": "success", "charge": charge}
#     except stripe.error.StripeError as e:
#         # Handle any errors that occur during the charge process
#         return {"status": "error", "message": str(e)}



if __name__=="__main__":
    uvicorn.run(app)
