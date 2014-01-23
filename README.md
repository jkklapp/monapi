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

* GET '/\<db\>'

Make a get on your DB name and you will be returned some statistics about \<db\>.

* GET '/_dbs'

Retrieves a list of db names available.

* GET '/\<db\>/\<coll\>'

Retrieves info from \<coll\> collection within \<db\> database.

* GET '/\<db\>/_colls'

Retrieves a list of collections inside \<db\>.

* GET '/\<db\>/\<coll\>/\<n\>'

Retrieves the nth document inside \<coll\> collection of \<db\> database.

* POST '/\<db\>/\<coll\>/_query'

Executes a query on \<coll\> collection contained in \<db\> database. The data posted must be a well-formed JSON to query documents.

* POST '/\<db\>/\<coll\>/_insert'

Inserts a well-formed JSON on \<coll\> collection inside \<db\> database.

* POST '/\<db\>/\<coll\>/_mr/\<output\>'

Executes a map-reduce job on \<coll\> collection within \<db\> database. Results are stored in \<output\> collection within \<db\> database. Mapper and reducer codes are provided in a JSON file like this:

{
    "mapper": "function(){  emit('A',1); }",
    "reducer": "function(key,values){ sum = 0; for (var i = 0; i \< values.length; i++) { sum+=values[i]; } return sum; }"
}

TODO
--------------
* Finish wiki
* Provide proper configuration capabilities

Author & License
--------------
Author: Jaakko Lappalainen, 2014. email: jkk.lapp@gmail.com

This program is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distri	buted in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

