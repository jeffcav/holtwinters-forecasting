

time_series_soda = [189, 229, 249, 289, 260, 431, 660, 777, 915, 613, 485, 
          277, 244, 296, 319, 370, 313, 556, 831, 960, 1152, 759, 
          607, 371, 298, 378, 373, 443, 374, 660, 1004, 1153, 1388, 
          904, 715, 441]

    
def moving_average(time_series, period_size, period):
    current_moving_average = 0.0
    
    for y in time_series[ (period - 1) * period_size : period * period_size ]:
        current_moving_average = current_moving_average + y
    return current_moving_average/period_size
    
    
def S(time_series, t, period_size, b1):
    period = (t/period_size) + 1
    corresponding_moving_average = moving_average(time_series, period_size, period)
    j = t % period_size
    
    yj_av = corresponding_moving_average - ( ( ( (period_size + 1.0) / 2.0) - (j+1) ) * b1 )
    return time_series[t] / yj_av

def hwm(time_series, m, L):
    a0 = []
    b1 = []
    snt = []
    sn_average = []
    sn_somat = 0.0
    St = []
    Sn = []

    first_period_average = moving_average(time_series, L, 1)
    last_period_average = moving_average(time_series, L, m)
        
    b1.append( ( last_period_average - first_period_average ) / ( (m - 1) * L ) )
    a0.append( first_period_average - ( (L/2) * b1[0] ) )
    
    #TODO refatorar daqui para baixo. Os calculos iniciais ja estao ok. 
    
    for t in range(len(time_series)):
        St.append(S(time_series, t, L, b1[0]))
    
    for t in range(L):
        s_somat = 0.0
        for k in range(m):
            s_somat = s_somat + St[t + (k * L)]
        sn_average.append((1.0 / m) * s_somat)
        sn_somat = sn_somat + ( (1.0 / m) * s_somat )
    
    for i in range(L):
        Sn.append( sn_average[i] * ( L / sn_somat) )
    print Sn
    #current_sn_average = 0.0
    #for i in range(m-1):
    #    current_sn_average = current_sn_average + S(i)
    

def main():
    m=3
    L=12
    
    hwm(time_series_soda, m, L)
    
main()

