from abc import ABCMeta, abstractmethod
class Estimator(object):
	"""" A base class for implementing estimators.

	Attributes:
		time_series: The historical data set.
	"""
	__metaclass__ = ABCMeta

	def setTimeSeries(self, time_series):
		""" Set the time series data set. """
		self.time_series = time_series

	@abstractmethod
	def estimate(self, t_base, t):
		""" Abstract method. Must be implemented by Estimator's subclasses to run the implemented estimation algorithm."""
		pass