# file2dmtx
[![CodeFactor](https://www.codefactor.io/repository/github/suscept/file2dmtx/badge)](https://www.codefactor.io/repository/github/suscept/file2dmtx)

 A program for converting files to [Data Matrix](https://en.wikipedia.org/wiki/Data_Matrix) images for analog data storage.


Requirements
-

Python 3.10 https://www.python.org/downloads/release/python-3104

Pillow 9.0+ https://pillow.readthedocs.io/en/stable/

pylibdmtx 0.1.10 https://pypi.org/project/pylibdmtx/

Limitations
-
Each Data Matrix only holds around 1.5kb of data, and due to a bug (#3) this is further reduced to around 1.2kb requiring many matrices to store even small files.

Encoding structure
-

version!filename!partition!total!data

version: The version number of the data matrix

filename: The name and file extension of the encoded file

partition: Which partition of the file this perticular data matrix contains

total: The total amount of partitions used for the stored file

data: The actual encoded data using the encoding scheme defined by the version number for this partition
