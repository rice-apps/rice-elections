"""
Finger util for name lookup.
"""

__author__ = 'Matthew Schurr <Matthew.A.Schurr@rice.edu>'

from socket import 

def finger(host, args):
    FINGER_PORT = 79
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, FINGER_PORT))
    s.send(args + "\r\n")
    result = "";
    while 1:
        buf = s.recv(1024)
        result += buf;
        if not buf: break
    return result;

def json_finger(host,args):
    # Query FINGER PROTOCOL
    res = finger(host,args);
    json = [];

    # Check If Result Exists
    if "0 RESULTS:" in res:
        return [];

    # Explode On "------------------------------------------------------------"
    segments = res.split("------------------------------------------------------------")

    for seg in segments:
        # Check: Segment Is A Record
        if "name:" not in seg:
            continue;

        record = {};

        # Explode On Lines
        lines = seg.split("\n");

        for line in lines:
            # Verify Key-Value Tuple
            if ":" not in line:
                continue;

            # Explode on :
            idx = line.find(":")
            key = line[:idx];
            val = line[idx+1:];
            key = key.strip(" ").replace(" ","_");
            val = val.strip(" ")
            record[key] = val;

        # Append to Result
        json.append(record);

    return json;

print json_finger("rice.edu","mas20");