### User [user.py](/models/user.py)

* email: string 
* password: string 
* first_name: string 
* last_name: string 
* places: relationship
* reviews: relationship

## State [state.py](/models/state.py)

* name: string
* cities: Cities related with State

## City [city.py](/models/city.py)

* state_id: string
* name: string
* places: relationship

## Amenity [amenity.py](/models/amenity.py)

* name: string

## Place [place.py](/models/place.py)

* city_id: string
* user_id: string
* name: string
* description: string
* number_rooms: integer
* number_bathrooms: integer
* max_guest: integer
* price_by_night: integer
* latitude: float
* longitude: float
* amenities: replationship


## Review [review.py](/models/review.py)

* place_id: string
* user_id: string
* text: string