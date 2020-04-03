# epidemic-on-highschool-network
Analyzing the spread of an epidemic on a social interaction network, based on the yearbook of a high school class, where students could write a paragraph for their friends, giving a proxy for the social connections in that class.

# Structure
* `implementation_and_results.ipynb` for notebook that generates and shows most results. 
* `Simulation.py` contains the general model
* `Distribution.py` is a helper class that significantly speeds up random sampling by bulk sampling at runtime.
* `network_data.py` contains the networks edges and the (made-up) names.
* `names_vertexNr.xlsx` translates vertex number to the (made-up) names.
