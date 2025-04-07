from django.shortcuts import get_object_or_404
from django.db.models import Q

class StockManager:
    """Simple utility class for stock management operations."""

    @staticmethod
    def list_items(model, search_term=''):
        """
        List stock items with optional search filtering.
        
        Args:
            model: The Django model class (e.g., Product)
            search_term: String to filter items by name
        
        Returns:
            QuerySet: Filtered or all items
        """
        if search_term:
            return model.objects.filter(product_name__icontains=search_term)
        return model.objects.all()

    @staticmethod
    def sell_item(model, item_id):
        """
        Sell one unit of a stock item if available.
        
        Args:
            model: The Django model class (e.g., Product)
            item_id: The ID of the item to sell
        
        Returns:
            bool: True if sold, False if not possible
        """
        try:
            item = get_object_or_404(model, id=item_id)
            if item.total_quantity > 0:
                item.total_quantity -= 1
                item.quantity_sold += 1
                item.save()
                return True
            return False
        except:
            return False

    @staticmethod
    def delete_item(model, item_id):
        """
        Delete a stock item from the database.
        
        Args:
            model: The Django model class (e.g., Product)
            item_id: The ID of the item to delete
        
        Returns:
            bool: True if deleted, False if not found or not deleted
        """
        try:
            item = get_object_or_404(model, id=item_id)
            item.delete()
            return True
        except:
            return False