from datetime import datetime

class Url:
    """Model for URL documents in MongoDB."""
    
    def __init__(self, url, shortcode, created_at=None, updated_at=None, access_count=0):
        """
        Initialize a new URL object.
        
        Args:
            url (str): The original URL.
            shortcode (str): The generated shortcode.
            created_at (datetime, optional): Creation timestamp. Defaults to current time.
            updated_at (datetime, optional): Last update timestamp. Defaults to current time.
            access_count (int, optional): Number of times the URL has been accessed. Defaults to 0.
        """
        self.url = url
        self.shortcode = shortcode
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()
        self.access_count = access_count
    
    def to_dict(self):
        """
        Convert URL object to dictionary representation.
        
        Returns:
            dict: Dictionary representation of the URL object.
        """
        return {
            'url': self.url,
            'shortCode': self.shortcode,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at,
            'accessCount': self.access_count
        }
    
    @classmethod
    def from_dict(cls, data, include_id=True):
        """
        Create URL object from dictionary.
        
        Args:
            data (dict): Dictionary containing URL data.
            include_id (bool, optional): Whether to include the ID field. Defaults to True.
            
        Returns:
            Url: URL object.
        """
        url_obj = cls(
            url=data.get('url'),
            shortcode=data.get('shortCode'),
            created_at=data.get('createdAt'),
            updated_at=data.get('updatedAt'),
            access_count=data.get('accessCount', 0)
        )
        
        if include_id and '_id' in data:
            url_obj.id = str(data['_id'])
            
        return url_obj 