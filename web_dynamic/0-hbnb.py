#!/usr/bin/python3
"""
This module inits a Flask application server
"""

from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from flasgger import Swagger
from flask import Flask, abort
from flask import render_template, jsonify
from flask import Markup
import uuid


def get_name(name):
        """Get element by name"""
        return name[1]


def get_cities(city):
        """Get element by name"""
        return city.name


app = Flask(__name__)
swagger = Swagger(app)


@app.teardown_appcontext
def close_storage(uknown):
    """
    apply a close to the storage engine to reload
    """
    storage.close()


@app.route('/0-hbnb', strict_slashes=False)
def hbnb_filters():
    """
    List all Cities in db

    """
    try:
        states = storage.all(State)
        resp = []
        for state_id, state in states.items():
            resp.append([state_id.split('.')[1], state.name, state.cities])
        states = []
        for el in sorted(resp, key=get_name, reverse=False):
            cities = sorted(el[2], key=get_cities, reverse=False)
            cities = [{'name': citi.name, 'id': citi.id} for citi in cities]
            states.append((el[0], el[1], cities))
        storage.close()
        amenities = storage.all(Amenity)
        amens = []
        # try:
        #     for ameni in amenities.items():
        #         #print(ameni[1].name)
        #         amens.append(ameni[1].name)
        #     for st in states:
        #         print(st[1])
        #         for cit in st[2]:
        #             print('\t', cit['name'])
        #     for am in amens:
        #         print(am)
        # except Exception as e:
        #     print(e)
        # print('\n\n\t\tStates:\n', states, '\n\n\t\tAmenities', amenities)
        places = storage.all(Place)
        plas = []
        for place in places.items():
            user = storage.get_user(place[1].user_id)
            plas.append((place[1], user.first_name + ' ' + user.last_name))
        plas = sorted(plas, key=lambda x: x[0].name, reverse=False)
        # for pla in plas:
        # 	print(pla[0].name, pla[1])
        # print(plas[0].user_id)

        # users = storage.all(User)
        # for user in users.items():
        #     print(dir(user[1]))
        #     break
        # print(plas)
        template = render_template("0-hbnb.html", **{'states': states,
                                                     'amenities': amens,
                                                     'places': plas,
                                                     'cache_id': uuid.uuid4()})
        # print("Template is a: ", type(template))
        # with open('web_flask/test_2.html', 'w') as out:
        #    out.write(template)
        template = template.replace('&lt;BR /&gt;', '<br>')
        # with open('web_flask/test.html', 'w') as out:
        #    out.write(template)
        # print("\nTemplate:\n\t", dir(template), '\n')
        return template
    except Exception as e:
        print(e)
        return jsonify(e)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Routing the main path
    """
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5001")
