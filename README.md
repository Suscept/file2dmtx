# file2dmtx
 A program for converting files to data matrix images for analog data storage.

Encoded structure
!version!filename!partition!total!data

version: The version number of the data matrix
filename: The name and file extension of the encoded file
partition: Which partition of the file this perticular data matrix contains
total: The total amount of partitions used for the stored file
data: The actual encoded data using the encoding scheme defined by the version number for this partition