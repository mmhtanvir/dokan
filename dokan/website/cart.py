from .models import Cart

def get_cart_count(user):
    if user.is_authenticated:
        items = Cart.query.filter_by(buyer_id=user.id).all()
        return len(items)
    return 0