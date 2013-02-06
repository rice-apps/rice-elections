"""
Python Network Finger Utility
@author Matthew Schurr <mschurr@rice.edu>

You can use this program to retrieve information about students/faculty at Rice 
using a search query.

The search returns a list of dictionaries structured similar to the examples 
below (note that more than one result can be returned).
A search with no results returns an empty list.

Example Usage:
    res = finger("mas20"); # Search by NetID

    [{
            "mailto": "mailto:mschurr@rice.edu",
            "major": "Computer Science",
            "name": "Schurr, Matthew Alexander",
            "email": "mschurr@rice.edu",
            "college": "Duncan College",
            "matric_term": "Fall 2012",
            "address": "Duncan College MS-715, 1601 Rice Blvd, , TX 77005-4401",
            "class": "sophomore student"
        }]

    res = finger("Devika"); # Search by Name

    [{
            "mailto": "mailto:devika@rice.edu",
            "name": "Subramanian, Dr Devika",
            "office": "3094 Duncan Hall",
            "title": "Professor; Professor, ECE",
            "mailstop": "Computer Science MS132",
            "email": "devika@rice.edu",
            "phone": "713-348-5661",
            "department": "Computer Science",
            "homepage": "http://www.cs.rice.edu/~devika/",
            "class": "faculty"
        }]
"""

__author__ = 'Matthew Schurr <Matthew.A.Schurr@rice.edu>'

from socket import *

def finger(query):
    """
    Searches the FINGER server at rice.edu 
    (see http://tools.ietf.org/html/rfc1288) for information related to a 
    search query.

    Args:
        query {String}: the lookup query

    Returns:
        Returns a list of dictionaries.
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("rice.edu", 79))
    s.send(query + "\r\n")
    res = "";
    while 1:
        buf = s.recv(1024)
        res += buf;
        if not buf:
            break

    json = [];

    if "0 RESULTS:" in res:
        return [];

    segments = res.split("------------------------------------------------------------")

    for seg in segments:
        if "name:" not in seg:
            continue;

        record = {};
        lines = seg.split("\n");

        for line in lines:
            if ":" not in line:
                continue;

            idx = line.find(":");
            key = line[:idx].strip(" ").replace(" ","_");
            val = line[idx+1:].strip(" ");
            record[key] = val;

        json.append(record);

    return json;