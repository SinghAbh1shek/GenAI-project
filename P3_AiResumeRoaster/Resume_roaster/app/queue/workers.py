from ..db.collections.file import files_collection
from bson import ObjectId
from pdf2image import convert_from_path
import os
from dotenv import load_dotenv


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


import base64
from openai import OpenAI

client = OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def process_file(id: str, file_path: str):
    await files_collection.update_one({'_id': ObjectId(id)} , {
        '$set': {
            "status": "Processing..."
        }
    })
    await files_collection.update_one({'_id': ObjectId(id)} , {
        '$set': {
            "status": "Converting to images..."
        }
    })
    
    pages = convert_from_path(file_path)
    images = []

    for i, page in enumerate(pages):
        image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        page.save(image_save_path, 'JPEG')
        images.append(image_save_path)
        
    await files_collection.update_one({'_id': ObjectId(id)} , {
        '$set': {
            "status": "Converting to success!"
        }
    })
    
    
    images_base64 = [encode_image(img) for img in images]

    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Roast the resume below. Don't hold back. Start by addressing the person by name, like 'Hey [Name], let's roast your resume.' Use dark humour if you want, but do not use any abusive language. Avoid unnecessary chatbot-style headings. Provide professional advice at the end. Also, include an apology in case the roast hurts. Note: Do not use asterisks in the response.",
                },
                {
                "type": "image_url",
                "image_url": {
                    "url":  f"data:image/jpeg;base64,{images_base64[0]}"
                },
                },
            ],
            }
        ],
        )

    # print(response.choices[0].message.content)
    

    await files_collection.update_one({'_id': ObjectId(id)} , {
        '$set': {
            "status": "Processed!",
            "result": response.choices[0].message.content
        }
    })
