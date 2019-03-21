import numpy as np# class Cluster:#    def __init__(self):#       pass#    def __repr__(self):#       return '(%s,%s)' % (self.left, self.right)#    def add(self, clusters, grid, lefti, righti):#       self.left = clusters[lefti]#       self.right = clusters[righti]#       # merge columns grid[row][righti] and row grid[righti] into corresponding lefti#       for r in grid:#          r[lefti] = min(r[lefti], r.pop(righti))#       grid[lefti] = map(min, zip(grid[lefti], grid.pop(righti)))#       clusters.pop(righti)#       return (clusters, grid)def add(clusters, grid, lefti, righti):  left = clusters[lefti]  right = clusters[righti]  # merge columns grid[row][righti] and row grid[righti] into corresponding lefti  for r in grid:     r[lefti] = min(r[lefti], r.pop(righti))  grid[lefti] = map(min, zip(grid[lefti], grid.pop(righti)))  clusters.pop(righti)  return (clusters, grid)def agglomerate(labels, grid):   """   given a list of labels and a 2-D grid of distances, iteratively agglomerate   hierarchical Cluster   """   clusters = labels   while len(clusters) > 1:      print clusters      # find 2 closest clusters      #print clusters      distances = [(1, 0, grid[1][0])]      #print grid[2:]      for i,row in enumerate(grid[2:]):         #print i,row         distances += [(i+2, j, c) for j,c in enumerate(row[:i+2])]         #print distances      j,i,_ = min(distances, key=lambda x:x[2])      print _      #print j,i      # merge i<-j      #c=[]      clusters, grid = add(clusters, grid, i, j)      clusters[i] = c      clus=clusters.pop()   return clusif __name__ == '__main__':   # Ref #1   out1 = np.genfromtxt('sam.txt', delimiter=',')   out1 = np.asarray(out1)   ItalyDistances = (np.sum((out1[None, :] - out1[:, None]) ** 2, -1) ** 0.5)   a = np.array(ItalyDistances).tolist()   #print type(ItalyDistances)   ItalyCities = list(range(0,4))   # ItalyDistances =[   #    [ 0,2.82,4.24,7.07],   #    [2.82,0,1.41,4,24],   #    [4.24,1.41,0,2.8],   #    [7.07,4.24,2.82,0]]   deee=agglomerate(ItalyCities, a)   print (deee[0])   """   (((BA,(NA,RM)),FI),(MI,TO))      |   |  |    |    |__|      |   |__|    |     |      |____|      |     |        |_________|     |             |__________|   """   # Ref 2   USACities = ['BOS','NY','DC','MIA','CHI','SEA','SF','LA','DEN']   USADistances = [      [   0,  206,  429, 1504,  963, 2976, 3095, 2979, 1949],      [ 206,    0,  233, 1308,  802, 2815, 2934, 2786, 1771],      [ 429,  233,    0, 1075,  671, 2684, 2799, 2631, 1616],      [1504, 1308, 1075,    0, 1329, 3273, 3053, 2687, 2037],      [ 963,  802,  671, 1329,    0, 2013, 2142, 2054,  996],      [2976, 2815, 2684, 3273, 2013,    0,  808, 1131, 1307],      [3095, 2934, 2799, 3053, 2142,  808,    0,  379, 1235],      [2979, 2786, 2631, 2687, 2054, 1131,  379,    0, 1059],      [1949, 1771, 1616, 2037,  996, 1307, 1235, 1059,    0]]   #print agglomerate(USACities, USADistances)   """   ((((((BOS,NY),DC),CHI),DEN),(SEA,(SF,LA))),MIA)               |__|   |    |    |     |   |  |      |                |_____|    |    |     |   |  |      |                   |       |    |     |   |__|      |                   |_______|    |     |    |        |                       |        |     |____|        |                       |________|       |           |                            |___________|           |                                  |_________________|   """