from datetime import datetime, UTC
from app.extensions import mongo

db = mongo.cx.get_database()
class URL:
    @staticmethod
    def create(url, short_code=None):
        """Create a new URL entry"""
        if not short_code:
            short_code = URL.generate_short_code()

        url_data = {
            'url': url,
            'short_code': short_code,
            'created_at': datetime.now(UTC),
            'updated_at': datetime.now(UTC),
            'access_count': 0
        }

        result = mongo.db.urls.insert_one(url_data)
        url_data['id'] = str(result.inserted_id)
        return url_data

    @staticmethod
    def get_by_short_code(short_code):
        """Get URL by short code"""
        url = mongo.db.urls.find_one({'short_code': short_code})
        if url:
            url['id'] = str(url['_id'])
            return url
        return None

    @staticmethod
    def update(short_code, new_url):
        """Update URL"""
        result = mongo.db.urls.update_one(
            {'short_code': short_code},
            {
                '$set': {
                    'url': new_url,
                    'updated_at': datetime.now(UTC)
                }
            }
        )
        return result.modified_count > 0

    @staticmethod
    def delete(short_code):
        """Delete URL"""
        result = mongo.db.urls.delete_one({'short_code': short_code})
        return result.deleted_count > 0

    @staticmethod
    def increment_access_count(short_code):
        """Increment access count"""
        mongo.db.urls.update_one(
            {'short_code': short_code},
            {'$inc': {'access_count': 1}}
        )

    @staticmethod
    def generate_short_code(length=6):
        """Generate a random short code"""
        import shortuuid
        return shortuuid.ShortUUID().random(length=length)

    @staticmethod
    def get_all():
        """Retrieve all URL documents"""
        return list(mongo.db.urls.find())
