monapi
==============

*Monapi is a set of REST services on top of a MongoDB built in Flask. For the moment, the functionality is limited and the return type is JSON. Suggestions are welcome.*

*Version: Beta 0.1*

*Requirements: flask, pymongo, json*

monapi.py
--------------

Just start the server on a machine with a MongoDB running server.

* GET '/'

Returns you the status of your Mongo server.

* GET '/<db>'

Make a get on your DB name and you will be returned some statistics about <db>.

