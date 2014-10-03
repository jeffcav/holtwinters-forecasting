from estimator import *

class HoltWintersEstimator(Estimator):
    """ A class that implements the Holt-Winters model for estimation. 
    Attributes:
        number_of_seasons: Number of seasons in the time series. If you have 3 years of observations, with month by month data, number_of_seasons=3.
        season_size: Indicates the number of observations in each season. For example, if you have 3 years of observation, with month by month data, season_size=12, which is the number of months in a year.
        seasonal_factor: Indicates the seasonal factor of each observation on your data set.
        average_component: Indicates the average component in the Holt-Winters model.
        tendence_component: Indicates the tendence component in the Holt-Winters model.
        seasonal_component: Indicates the seasonal component in the Holt-Winters model.
    """

    def __init__(self, time_series, number_of_seasons, season_size):
        """ Initializes a Holt-Winters estimator. """
        super(HoltWintersEstimator, self).setTimeSeries(time_series)
        self.number_of_seasons = number_of_seasons
        self.season_size = season_size
        self.seasonal_factor = []
        self.average_component = []
        self.tendence_component = []
        self.seasonal_component = []
        self.initializeComponents()
        print(self.seasonal_component)

    def seasonOfTime(self, time):
        """ Returns the season which holds the data at a given time. """
        return int((time / self.season_size) + 1)

    def seasonalIndexOfTime(self, time):
        """ Returns the seasonal correspondence of time. For example, if 24 month-by-month observations were made and time=13, it corresponds to the first element of the season it belongs to. """
        return time % self.season_size

    def estimate(self, time, base_time):
        """ Estimate the value of the function on time, based on the base_time observation. Often base_time is time-1. """
        season = self.seasonOfTime(time)
        seasonal_index = self.seasonalIndexOfTime(time)
        estimation = (self.average_component[base_time] + self.tendence_component[base_time] * time) * self.seasonal_component[season-1][seasonal_index-1]
        return estimation
    
    def seasonMovingAverage(self, season):
        """ Returns the moving average of a season. """
        floor = (season - 1) * self.season_size
        ceil = season * self.season_size
        moving_average = 0.0

        for y in self.time_series[floor:ceil]:
            moving_average += y
        return moving_average/self.season_size

    def seasonalFactor(self, time, tendence_component):
        """ Calculates the seasonal factor for each historical data in the time series."""
        season = self.seasonOfTime(time)
        moving_average = self.seasonMovingAverage(season)
        
        seasonal_correspondent = self.seasonalIndexOfTime(time) #For example: All april's (4th month) correspondents in the historical data set.
        #TODO retirar o comentario acima

        tendence = (((self.season_size + 1.0) / 2.0) - (seasonal_correspondent + 1)) * tendence_component
        seasonal_correspondents_average = moving_average - tendence
        return (self.time_series[time] / seasonal_correspondents_average)

    def initializeComponents(self):
        """ Initializes the components of the Holt-Winters model. """
        first_season_average = self.seasonMovingAverage(1)
        last_season_average = self.seasonMovingAverage(self.number_of_seasons)

        #tendence component
        self.tendence_component.append((last_season_average - first_season_average) / ((self.number_of_seasons - 1) * self.season_size))
        
        #average component
        self.average_component.append( first_season_average - ((self.season_size / 2.0) * self.tendence_component[0]))

        #calculate all the seasonal factors
        for time in range(len(self.time_series)):
            self.seasonal_factor.append(self.seasonalFactor(time, self.tendence_component[0]))

        #calculate all seasonal averages by seasonal correspondent (eg. seasonal average of all april's correspondents) and sum them all
        seasonal_correspondent_averages = []
        seasonal_correspondent_averages_sum = 0.0

        for seasonal_correspondent_index in range(self.season_size):
            seasonal_correspondents_sum = 0.0
            for season in range(self.number_of_seasons):
                seasonal_correspondents_sum += self.seasonal_factor[seasonal_correspondent_index + (season * self.season_size)]
            seasonal_correspondent_averages.append(seasonal_correspondents_sum * (1.0 / self.number_of_seasons))
            seasonal_correspondent_averages_sum += seasonal_correspondent_averages[-1]
        
        #seasonal component
        self.seasonal_component.append([])
        for sn_average in seasonal_correspondent_averages:
            self.seasonal_component[0].append(sn_average * (self.season_size / seasonal_correspondent_averages_sum))


time_series_soda = [189, 229, 249, 289, 260, 431, 660, 777, 915, 613, 485, 
          277, 244, 296, 319, 370, 313, 556, 831, 960, 1152, 759, 
          607, 371, 298, 378, 373, 443, 374, 660, 1004, 1153, 1388, 
          904, 715, 441]
hwe = HoltWintersEstimator(time_series_soda, 3, 12)
print(hwe.estimate(1, 0))