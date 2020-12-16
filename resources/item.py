import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                    type=float,
                    required=True,
                    help="This field cannot be left blank!"
                )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

        #item = next(filter(lambda x: x['name'] == name, items), None)
        #return {'item': item}, 200 if item else 404
        #return {next(filter(lambda x: x['name'] == name, items), None)}


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exist.".format(name)}, 400
        #if next(filter(lambda x: x['name'] == name, items), None):
            #return {'message': "An item with name '{}' already exist.".format(name)}, 400

        data = Item.parser.parse_args()
        #data = request.get_json()
        ## item = {'name': name, 'price': data['price']}
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
            ##ItemModel.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500  # Internal Server Error
        return item.json(), 201



    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        ##connection = sqlite3.connect('data.db')
        ##cursor = connection.cursor()
        ##query = "DELETE FROM items WHERE name=?"
        ##cursor.execute(query, (name,))
        ##connection.commit()
        ##connection.close()

        #global items
        #items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()
        #data = request.get_json()
        #item = next(filter(lambda x: x['name'] == name, items), None)

        item = ItemModel.find_by_name(name)  # BU ZATEN VERİTABANINDAKİ OLAN İTEM, TAKİP EDİLİNCE DE "*" YAZAN YERE YAZILMASININ MANTIĞI YOK
        ##updated_item = {'name': name, 'price': data['price']}
        ###updated_item = ItemModel(name, data['price'])

        #DÜZENLENDİ
        if item is None:
            item = ItemModel(name, data['price'], data['store_id']) #Bunu Yazacağımıza şu şekilde de belirtebiliriz:
            #ItemMode(name, **data)  Daha kolay gösterim
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

# class ItemList(Resource):
#     def get(self):
#         return {"items": items}

class ItemList(Resource):
    def get(self):
        #return {'items': [item.json for item in ItemModel.query.all()]}  # ALT SATIR İLE AYNI DAHA BASİT HALİ
        return {'items': [x.json() for x in ItemModel.query.all()]}



        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name' : row[0], 'price' : row[1]})
        #
        # connection.close()
        # return {'items' : items}