import sys
import numpy as np
import math
import pandas as pd
import math


if __name__ == "__main__":
    global out1

    sample_file = sys.argv[1]
    actual_file = sys.argv[2]
    kt = int(sys.argv[3])
    n = int(sys.argv[4])
    p = float(sys.argv[5])

    #p = float(p/100)
    out1 = np.genfromtxt(sample_file, delimiter=',')
    out1 = np.asarray(out1)


    dis_mat = (np.sum((out1[None, :] - out1[:, None]) ** 2, -1) ** 0.5)

    copy_mat = dis_mat
    np.fill_diagonal(dis_mat, np.inf)

    i = len(out1)
    clusters = []
    for i in range(len(out1)):
        clusters.append([i])

    ind = []
    while i >= kt:
        dis_ind = np.argmin((dis_mat))
        dis_ind = np.unravel_index(dis_ind,dis_mat.shape)

        clusters[dis_ind[0]].extend( clusters[dis_ind[1]] )
        clusters.remove( clusters[dis_ind[1]] )

        dis_mat[:,dis_ind[0]] = np.minimum(dis_mat[:,dis_ind[0]], dis_mat[:,dis_ind[1]])
        dis_mat[dis_ind[0],:] =  (np.minimum(dis_mat[dis_ind[0],:], dis_mat[dis_ind[1],:]))

        dis_mat = np.delete(dis_mat, dis_ind[1], axis=0)
        dis_mat = np.delete(dis_mat, dis_ind[1], axis=1)

        np.fill_diagonal(dis_mat, np.inf)

        orig_ind = np.argmin((dis_mat))
        orig_ind = np.unravel_index(dis_ind,dis_mat.shape)
        #print dis_mat
        i-=1


centroid=[]
values = [[] for i in range(kt)]
val = []


for i in range(len(clusters)):
    for j in range(len(clusters[i])):
        val.append(out1[clusters[i][j]])
    values[i].extend(val)
    x = np.sum(val,axis=0)/len(clusters[i])
    centroid.append(x)


    val = []
#print values
print values


# print "Centroid"
# print centroid[0]
# print centroid[1]
# print centroid[2]

# print "Clusters"
# print clusters[0]
# print clusters[1]
# print clusters[2]


# print "Values"
# print values[0]
# print values[1]
# print values[2]



rep_points = []

for i in range(len(values)):
    x , y  = zip(*values[i])
    ind=np.argmin(x)
    rep_points.append(values[i][ind])
print rep_points


dist1 = []
max_distance = []
if n >1:
    for i in range(len(values)):
        dist1 = []
        x = values[i]
        for j in range(len(x)):
            dist1.append(math.sqrt((rep_points[i][0] - x[j][0]) ** 2 + (rep_points[i][1] - x[j][1]) ** 2))
        z = np.argmax(dist1)
        rep_points.append(x[z])
        #print rep_points

if n >=2:
    cl=len(clusters)
    pts=n-2
    for a in range(2,n):
        for i in range(len(values)):
            x = values[i]
        print x[1]
    print values
            #print x,"xxxxx"
#             dist2 = []
#             for k in range( 0, pts ):
#                 dist1 = []
#                 #print  rep_points[i+cl*k]
#                 #print i+cl*k
#                 #print len(x)
#
#                 for j in range( len( x ) ):
#
#
#                     dist1.append(math.sqrt((rep_points[i+cl*k][0] - x[j][0]) ** 2 + (rep_points[i+cl*k][1] - x[j][1]) ** 2))
#                 if k > 0:
#                     dist2 = np.minimum( dist1, dist2)
#                     #print dist2[0]
#                     q = np.argmax( dist2 )
#                 else:
#                     dist2 = dist1
#             rep_points.append( x[q] )
#             #print rep_points
#         pts +=1
#
# # for v in range(cl):
# #     print "Representative Points of Cluster",format(v)
# #     t=v
# #     for w in range(n):
# #         print rep_points[t]
# #         t = t + 3
# #
# # for v in range(cl):
# #     print "Cluster",format(v)
# #     t=v
# #     for w in range(n):
# #         b.append(rep_points[t])
# #         t = t + 3
# #     b = []
# #     c.append(b)
# # print c
#
#
# rep_points_1 = []
# j = 0
# cnt = 0
# final_rep_points = []
# for i in range(3):
#     j = i
#     #print centroid[i]
#     while cnt <= len(clusters):
#         m = (float)(centroid[i][0] - rep_points[j][0])
#         n = (float)(centroid[i][1] - rep_points[j][1])
#         rep_points_1.append([rep_points[j][0] + m*(p),rep_points[j][1] + n*(p)])
#         j = j+ len(clusters)
#         cnt +=1
#         #print j
#         #print "Outsie"
#     cnt = 0
#     j = i
#     final_rep_points.append(rep_points_1)
#
# #print final_rep_points
#
# out2 = np.genfromtxt(actual_file, delimiter=',')
# out2 = np.asarray(out2)
#
#
# j = 0
# cnt = 0
# final_pts = []
# minDist = 99999
# # for points in out2:
# #     for i in range(len(final_rep_points)):
#
#     #while( cnt < n ):
#         #dist = (math.sqrt((final_rep_points[i][0][0] - points[0]) ** 2 + (final_rep_points[i][0][1] - points[1]) ** 2))
#         #print dist
#     #     j+=1
#     #     cnt+=1
#     #     if dist < minDist:
#     #         minDist = dist
#     #         clustChoice = i
#     # cnt = 0
#     #final_pts.append([points,i])
# print final_pts
# clstr_point = []
# #ty = [[1,2],[34,45],[12,13]]
# minDist = 9999
# #print k
# # i =0
# # for points in out2:
# #     print points
# #     for w in range(len(rep_points_1)):
# #         #temp = rep_points_1[w]
# #         #x = final_rep_points[i]
# #         #print len(x)
# #         #print i
# #         #for j in temp:
# #            #print "z"
# #             #print "I"
# #             #print i
# #             #print j
# #             #print ty[j]
# #             #print j
# #         dist = (math.sqrt((rep_points_1[w][0] - points[0]) ** 2 + (rep_points[w][1] - points[1]) ** 2))
# #         print dist#     j+=1
# #         #     cnt+=1
# #         if dist < minDist:
# #             minDist = dist
# #             clustChoice = w  % n
# #             print clustChoice
# #         # i = i+1
# #     clstr_point.append([points,clustChoice])
# # print (clstr_point)
# #
#
# i =0
# ii=0
# x = final_rep_points[0]
# for points in out2:
#     i = 0
#     ii = 0
#     print points
#     while i < len(final_rep_points[0]):
#         for k in range(n):
#             z=k+i
#             dist = (math.sqrt((x[z][0] - points[0]) * 2 + (x[z][1] - points[1]) * 2))
#             if dist < minDist:
#                 minDist = dist
#                 clustChoice = ii
#         i = i+4
#         ii = ii +1
#     clstr_point.append([points,clustChoice])
# #print (clstr_point)
#
# #rep_points_1
# # for i in range(len(rep_points)):
# #     rep_points[i] = rep_points[i] + (centroid[j]-rep_points[i])*(p/100)
