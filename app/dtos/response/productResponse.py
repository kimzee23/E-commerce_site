
class productResponse:
    def __init__(self, id,name,description,price,category,image_url,stock,seller_id,created_at):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url
        self.stock = stock
        self.seller_id = seller_id
        self.created_at = created_at
    def to_dict(self):
        return self.__dict__