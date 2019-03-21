import sys
import numpy as np
import csv
import math
from scipy.sparse import csr_matrix


csv_file=sys.argv[1]

n = int(sys.argv[2])
m = int(sys.argv[3])
f = int(sys.argv[4])
k = int(sys.argv[5])

U = np.ones(shape=(n, f))
V = np.ones(shape=(f, m))



def calculate_rmse(mat):
        m_dash_output = np.matmul(U,V)
        sub= np.subtract(mat,m_dash_output)
        rmsmean_o= np.sqrt(np.nanmean(np.square(sub)))
        print "%0.4f" % rmsmean_o



if __name__ == "__main__":
        data=[]
        dta=[]
        raw_data = open(csv_file, 'r')
        reader = csv.reader(raw_data,delimiter=',')
        next(reader, None)
        for row in reader:
            data.append(row)

        data = np.asarray(data)
        for x in data:
            dta.append(map(float,x))

        dta = np.asarray(dta)
        dta = dta[:,0:-1]
        rows, row_pos = np.unique(dta[:, 0], return_inverse=True)
        cols, col_pos = np.unique(dta[:, 1], return_inverse=True)

        pivot_table = np.empty(shape=(len(rows), len(cols)))*np.nan
        pivot_table[row_pos, col_pos] = dta[:, 2]


        for z in range(k):
            for r in range(n):
                Mtemp = np.array(pivot_table[r, :])
                for s in range(f):

                    tmpsum = 0.0
                    tmpd = 0.0
                    Vtemp = np.array(V[s,:])
                    Vtemp[np.isnan(Mtemp)] = np.nan
                    tmpd = np.nansum(np.square(Vtemp))
                    tmpsum = np.nansum(V[s,:] * (Mtemp-np.matmul(U[r,:],V)+ U[r][s]*V[s,:]))
                    if tmpd==0:
                        U[r][s]
                    else:
                        U[r][s] = tmpsum/tmpd


            for s in range(m):
                Mtemp = np.array(pivot_table[:,s])
                for r in range(f):
                    tmpsum = 0.0
                    tmpd = 0.0
                    Utemp = np.array(U[:,r])
                    Utemp[np.isnan(Mtemp)] = np.nan
                    tmpd = np.nansum(np.square(Utemp))
                    tmpsum = np.nansum(U[:,r] * (Mtemp - np.matmul(U, V[:,s]) + U[:,r]*V[r, s]))
                    if tmpd==0:
                        V[r][s]
                    else:
                        V[r][s] = tmpsum/tmpd




            calculate_rmse(pivot_table)
