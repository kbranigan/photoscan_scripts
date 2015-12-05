#rotates model coordinate system in accordance of bounding box for active chunk
#scale is kept 
#compatibility: Agisoft PhotoScan Professional 1.1.0

import PhotoScan 
import math 

doc = PhotoScan.app.document
chunk = doc.chunk

R = chunk.region.rot		#Bounding box rotation matrix
C = chunk.region.center		#Bounding box center vector

if chunk.transform.matrix:
	T = chunk.transform.matrix
	s = math.sqrt(T[0,0] ** 2 + T[0,1] ** 2 + T[0,2] ** 2) 		#scaling
	S = PhotoScan.Matrix( [[s, 0, 0, 0], [0, s, 0, 0], [0, 0, s, 0], [0, 0, 0, 1]] ) #scale matrix
else:
	S = PhotoScan.Matrix( [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]] )

T = PhotoScan.Matrix( [[R[0,0], R[0,1], R[0,2], C[0]], [R[1,0], R[1,1], R[1,2], C[1]], [R[2,0], R[2,1], R[2,2], C[2]], [0, 0, 0, 1]])

chunk.transform.matrix = S * T.inv()		#resulting chunk transformation matrix