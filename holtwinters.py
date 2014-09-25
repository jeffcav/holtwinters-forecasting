

time_series_soda = [189, 229, 249, 289, 260, 431, 660, 777, 915, 613, 485, 
          277, 244, 296, 319, 370, 313, 556, 831, 960, 1152, 759, 
          607, 371, 298, 378, 373, 443, 374, 660, 1004, 1153, 1388, 
          904, 715, 441]

    
def calculateMovingAverage(time_series, period_size, period):
    current_moving_average = 0.0
    
    for y in time_series[ (period - 1) * period_size : period * period_size ]:
        current_moving_average = current_moving_average + y
    return current_moving_average/period_size
    
    
def calculateS(time_series, t, period_size, tendence_component):
    period = (t/period_size) + 1
    corresponding_moving_average = calculateMovingAverage(time_series, period_size, period)
    j = t % period_size
    
    yj_av = corresponding_moving_average - ( ( ( (period_size + 1.0) / 2.0) - (j+1) ) * tendence_component )
    return time_series[t] / yj_av

def calculateSazonalComponents(sazonal_averages, L, sazonal_averages_sum):
    sazonal_components = []
    for average_sn_t in sazonal_averages:
        sazonal_components.append( average_sn_t * ( L / sazonal_averages_sum) )
    return sazonal_components

    
def hwm(time_series, m, L):
    a0 = []
    b1 = []
    snt = []
    sazonal_averages_sum = 0.0
    S = []
    Sn = []
    sazonal_averages = []
    sazonal_components = []
    sazonal_components_t = []

    first_period_average = calculateMovingAverage(time_series, L, 1)
    last_period_average = calculateMovingAverage(time_series, L, m)
        
    b1.append( ( last_period_average - first_period_average ) / ( (m - 1) * L ) )
    a0.append( first_period_average - ( (L/2) * b1[0] ) )
    
    for t in range(len(time_series)):
        S.append(calculateS(time_series, t, L, b1[0]))
    
    for t in range(L):
        s_somat = 0.0
        for k in range(m):
            s_somat = s_somat + S[t + (k * L)]
        sazonal_averages.append((1.0 / m) * s_somat)
        sazonal_averages_sum = sazonal_averages_sum + ( (1.0 / m) * s_somat )

    sazonal_components.append( calculateSazonalComponents(sazonal_averages, L, sazonal_averages_sum) )
    #Agora ja temos a0(0), b1(0) e Sn_t(0)

    

def main():
    m=3
    L=12
    
    hwm(time_series_soda, m, L)
    
main()

