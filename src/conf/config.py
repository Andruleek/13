import cloudinary
import cloudinary.uploader
import cloudinary.config

class Config:
    DB_URL = "postgresql+asyncpg://postgres:150209@localhost:5432/contacts"


config = Config


CONTACT_LIMIT = 5

CORS_RESOURCES = {
    r"/*": {
        "origins": ["*"],
        "allow_headers": [
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Credentials",
        ],
        "expose_headers": [
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Credentials",
        ],
        "supports_credentials": True,
    }
}

cloudinary.config(
    cloud_name="your_cloud_name",
    api_key="your_api_key",
    api_secret="your_api_secret"
)