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
        item = ItemModel(name, data['price'])

        try:
            item.insert()
            ##ItemModel.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500  # Internal Server Error
        return item.json(), 201



    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        #global items
        #items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()
        #data = request.get_json()
        #item = next(filter(lambda x: x['name'] == name, items), None)

        item = ItemModel.find_by_name(name)  # BU ZATEN VERİTABANINDAKİ OLAN İTEM, TAKİP EDİLİNCE DE "*" YAZAN YERE YAZILMASININ MANTIĞI YOK
        ##updated_item = {'name': name, 'price': data['price']}
        updated_item = ItemModel(name, data['price'])

        if item is None:
            #item = {'name': name, 'price': data['price']}
            #items.append(item)
            updated_item.insert()
            try:
                ItemModel.insert(updated_item)
            except:
                return {"message": "An error occured inserting the item."},500
        else:
            #item.update(data)
            try:
                #ItemModel.update(updated_item)
                updated_item.update() # "*"
            except:
                return {"message": "An error occured updating the item."}, 500
        #return updated_item
        return updated_item.json()

# class ItemList(Resource):
#     def get(self):
#         return {"items": items}

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name' : row[0], 'price' : row[1]})

        connection.close()
        return {'items' : items}