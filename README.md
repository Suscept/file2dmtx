# file2dmtx
 A program for converting files to data matrix images for analog data storage.


Requirements
-

Python 3.10 https://www.python.org/downloads/release/python-3104

Pillow 9.0+ https://pillow.readthedocs.io/en/stable/

pylibdmtx 0.1.10 https://pypi.org/project/pylibdmtx/


Encoding structure
-

version!filename!partition!total!data

version: The version number of the data matrix

filename: The name and file extension of the encoded file

partition: Which partition of the file this perticular data matrix contains

total: The total amount of partitions used for the stored file

data: The actual encoded data using the encoding scheme defined by the version number for this partition
