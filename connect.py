from dotenv import load_dotenv
import os

load_dotenv()

CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")

print(CANVAS_TOKEN)