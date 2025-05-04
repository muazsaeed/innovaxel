from datetime import datetime
import validators
from bson.objectid import ObjectId
from pymongo import MongoClient

from config import current_config
from models.url import Url
from utils.shortcode_generator import generate_shortcode

class UrlService:
    """Service for URL shortening operations."""
    
    def __init__(self):
        """Initialize the URL service with MongoDB connection."""
        self.client = MongoClient(current_config.MONGO_URI)
        self.db = self.client[current_config.MONGO_DB]
        self.urls = self.db.urls
    
    def create_url(self, original_url):
        """
        Create a new shortened URL.
        
        Args:
            original_url (str): The original URL to shorten.
            
        Returns:
            dict: The created URL document with ID.
            
        Raises:
            ValueError: If the URL is invalid.
        """
        # Validate the URL
        if not validators.url(original_url):
            raise ValueError("Invalid URL")
        
        # Generate a unique shortcode
        while True:
            shortcode = generate_shortcode()
            # Check if shortcode already exists
            if not self.urls.find_one({"shortCode": shortcode}):
                break
        
        # Create timestamp (ISO format)
        now = datetime.utcnow().isoformat()
        
        # Create URL document
        url_obj = Url(
            url=original_url,
            shortcode=shortcode,
            created_at=now,
            updated_at=now,
            access_count=0
        )
        
        # Insert into database
        result = self.urls.insert_one(url_obj.to_dict())
        
        # Get the created document and add the ID
        created_url = url_obj.to_dict()
        created_url['id'] = str(result.inserted_id)
        
        return created_url
    
    def get_url_by_shortcode(self, shortcode):
        """
        Get a URL by its shortcode.
        
        Args:
            shortcode (str): The shortcode to look up.
            
        Returns:
            dict: The URL document or None if not found.
        """
        url_doc = self.urls.find_one({"shortCode": shortcode})
        
        if url_doc:
            url_doc['id'] = str(url_doc.pop('_id'))
            return url_doc
        
        return None
    
    def update_url_by_shortcode(self, shortcode, new_url):
        """
        Update a URL by its shortcode.
        
        Args:
            shortcode (str): The shortcode to update.
            new_url (str): The new URL.
            
        Returns:
            dict: The updated URL document or None if not found.
            
        Raises:
            ValueError: If the new URL is invalid.
        """
        # Validate the new URL
        if not validators.url(new_url):
            raise ValueError("Invalid URL")
        
        # Find the URL document
        url_doc = self.urls.find_one({"shortCode": shortcode})
        
        if not url_doc:
            return None
        
        # Update the URL and updated_at timestamp
        now = datetime.utcnow().isoformat()
        result = self.urls.update_one(
            {"shortCode": shortcode},
            {"$set": {"url": new_url, "updatedAt": now}}
        )
        
        # If update was successful, return the updated document
        if result.modified_count > 0:
            updated_doc = self.urls.find_one({"shortCode": shortcode})
            updated_doc['id'] = str(updated_doc.pop('_id'))
            return updated_doc
        
        return None
    
    def delete_url_by_shortcode(self, shortcode):
        """
        Delete a URL by its shortcode.
        
        Args:
            shortcode (str): The shortcode to delete.
            
        Returns:
            bool: True if the URL was deleted, False otherwise.
        """
        result = self.urls.delete_one({"shortCode": shortcode})
        return result.deleted_count > 0
    
    def increment_access_count(self, shortcode):
        """
        Increment the access count for a URL by its shortcode and return the original URL.
        
        Args:
            shortcode (str): The shortcode to increment access count for.
            
        Returns:
            str: The original URL or None if not found.
        """
        # Increment access count and get the document in a single operation
        result = self.urls.find_one_and_update(
            {"shortCode": shortcode},
            {"$inc": {"accessCount": 1}},
            return_document=True
        )
        
        if result:
            return result.get('url')
        
        return None
    
    def get_url_stats(self, shortcode):
        """
        Get statistics for a URL by its shortcode.
        
        Args:
            shortcode (str): The shortcode to get statistics for.
            
        Returns:
            dict: The URL document with statistics or None if not found.
        """
        url_doc = self.urls.find_one({"shortCode": shortcode})
        
        if url_doc:
            url_doc['id'] = str(url_doc.pop('_id'))
            return url_doc
        
        return None 