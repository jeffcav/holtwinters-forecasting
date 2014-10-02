from estimator import *

class HoltWintersEstimator(Estimator):
    """ A class that implements the Holt-Winters model for estimation. 
    Attributes:
        periods: Number of periods in the time series. If you have 3 years of observations, with month by month data, periods=3.
        period_size: Indicates the period size. For example, if you have 3 years of observation, with month by month data, period_size=12, which is the number of months in a year.
        seasonal_factor: Indicates the seasonal factor of each observation on your data set.
        average_component: Indicates the average component in the Holt-Winters model.
        tendence_component: Indicates the tendence component in the Holt-Winters model.
        seasonal_component: Indicates the seasonal component in the Holt-Winters model.
    """

    def __init__(self, time_series, periods, period_size):
        """ Initializes a Holt-Winters estimator. """
        super(HoltWintersEstimator, self).setTimeSeries(time_series)
        self.periods = periods
        self.period_size = period_size
        self.seasonal_factor = []
        self.average_component = []
        self.tendence_component = []
        self.seasonal_component = []
        self.initializeComponents()
        print(self.seasonal_component)

    def estimate(self, t_base, t):
        """ Estimate the value when time is t, based on the t_base observation. Often t_base is t-1. """
        pass
    
    def periodMovingAverage(self, period):
        """ Returns the moving average of a period. """
        floor = (period - 1) * self.period_size
        ceil = period * self.period_size
        moving_average = 0.0

        for y in self.time_series[floor:ceil]:
            moving_average += y
        return moving_average/self.period_size

    def seasonalFactor(self, time, tendence_component):
        """ Calculates the seasonal factor for each historical data in the time series."""
        period = int((time / self.period_size) + 1)
        moving_average = self.periodMovingAverage(period)
        
        seasonal_correspondent = time % self.period_size #For example: All april's (4th month) correspondents in the historical data set.

        tendence = (((self.period_size + 1.0) / 2.0) - (seasonal_correspondent + 1)) * tendence_component
        seasonal_correspondents_average = moving_average - tendence
        return (self.time_series[time] / seasonal_correspondents_average)

    def initializeComponents(self):
        """ Initializes the components of the Holt-Winters model. """
        first_period_average = self.periodMovingAverage(1)
        last_period_average = self.periodMovingAverage(self.periods)

        #tendence component
        self.tendence_component.append((last_period_average - first_period_average) / ((self.periods - 1) * self.period_size))
        
        #average component
        self.average_component.append((first_period_average - (self.period_size / 2.0)) * self.tendence_component[0])

        #calculate all the seasonal factors
        for time in range(len(self.time_series)):
            self.seasonal_factor.append(self.seasonalFactor(time, self.tendence_component[0]))

        #calculate all seasonal averages by seasonal correspondent (eg. seasonal average of all april's correspondents) and sum them all
        seasonal_correspondent_averages = []
        seasonal_correspondent_averages_sum = 0.0

        for seasonal_correspondent_index in range(self.period_size):
            seasonal_correspondents_sum = 0.0
            for period in range(self.periods):
                seasonal_correspondents_sum += self.seasonal_factor[seasonal_correspondent_index + (period * self.period_size)]
            seasonal_correspondent_averages.append(seasonal_correspondents_sum * (1.0 / self.periods))
            seasonal_correspondent_averages_sum += seasonal_correspondent_averages[-1]
        
        #seasonal component
        self.seasonal_component.append([])
        for sn_average in seasonal_correspondent_averages:
            self.seasonal_component[0].append(sn_average * (self.period_size / seasonal_correspondent_averages_sum))



time_series_soda = [189, 229, 249, 289, 260, 431, 660, 777, 915, 613, 485, 
          277, 244, 296, 319, 370, 313, 556, 831, 960, 1152, 759, 
          607, 371, 298, 378, 373, 443, 374, 660, 1004, 1153, 1388, 
          904, 715, 441]
hwe = HoltWintersEstimator(time_series_soda, 3, 12)