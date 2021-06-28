from app import db
from .model import CartModel
from app.infra.db.base_dao import BaseDao


class CartDao(BaseDao):

    def __init__(self):
        super().__init__('Cart', CartModel)

    def getCurrentUserCart(self, userId):
        query = 'SELECT * FROM Cart WHERE Cart.id_User = %(userId)s AND Cart.id NOT IN (SELECT Command.id_Cart FROM Command)'
        result = db.find(query, {'userId': userId})
        return self._mapper.from_tuple(result)

    def save(self, cartModel):
        if not isinstance(cartModel, CartModel):
            raise ValueError("cartModel should be of type cartModel")
        query = 'INSERT INTO Cart (id, id_User, totalCost) VALUES (%s, %s, %s)'
        cartId = db.create(query, self._mapper.to_tuple(cartModel))

        if cartId:
            return self.getById(cartId)
        else:
            raise Exception("Could not save cart")