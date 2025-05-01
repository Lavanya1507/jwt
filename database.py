from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://admin:f6J!UpeuS_Zkxtn@userlogindetails.24tdohu.mongodb.net/?retryWrites=true&w=majority&appName=UserLoginDetails"

client = AsyncIOMotorClient(MONGO_URL)
db = client["UserLoginDetails"]  # your database name
