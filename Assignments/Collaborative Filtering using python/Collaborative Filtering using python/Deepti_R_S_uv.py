import sys
import numpy as np
import csv

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

        M = np.empty(shape=(len(rows), len(cols)))*np.nan
        M[row_pos, col_pos] = dta[:, 2]


        for z in range(0,k):
            for r in range(0,n):
                M_temp = np.array(M[r, :])
                for s in range(0,f):

                    temp_sum = 0.0
                    tmpd = 0.0
                    Vtemp = np.array(V[s,:])
                    Vtemp[np.isnan(M_temp)] = np.nan
                    tmpd= np.square(Vtemp)
                    tmpd = np.nansum(tmpd)
                    temp_sum = np.nansum(V[s,:] * (M_temp-np.matmul(U[r,:],V)+ U[r][s]*V[s,:]))
                    U[r][s] = temp_sum / tmpd


            for s in range(m):
                Mtemp = np.array(M[:,s])
                for r in range(f):
                    tmpsum = 0.0
                    tmpd = 0.0

                    Utemp = np.array(U[:,r])
                    Utemp[np.isnan(Mtemp)] = np.nan
                    tmpd=np.square(Utemp)
                    tmpd = np.nansum(tmpd)
                    tmpsum = np.nansum(U[:,r] * (Mtemp - np.matmul(U, V[:,s]) + U[:,r]*V[r, s]))
                    V[r][s] = tmpsum / tmpd



            calculate_rmse(M)


