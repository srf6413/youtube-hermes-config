"""This module holds the GraphAnalysis class which is responsible for
generating a impact analysis graph png from an Impact Analysis Response
protobuf object.
"""
import os
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

class GraphAnalysis():
	"""Responsible for generating an impact analysis graph .png image
  from an Impact Analysis Response protobuf object.
	"""

	def compare_impact(self, queue_impact):
		"""Sorts the queue impacts so the impacts where the new SLA is greater then
    the desired impact or increased from the previous SLA.

		Args:
				queue_impact : the list of queue impacts

		Returns:
				str: the desired delta SLA
		"""
		desired_delta = (queue_impact.desired_SLA_min - queue_impact.new_SLA_min) + \
    (queue_impact.previous_SLA_min - queue_impact.new_SLA_min)
		return desired_delta


	def graph_impact(self, impact_analysis):
		"""Creates the impact analysis png and saves it to the project directory.

		Args:
				impact_analysis (ImpactAnalsisResponse): the ImpactAnalysisResponse Protobuf object

		Returns:
				str: the path to the graph impact analysis .png file
		"""
		data = {"Desired SLA": {}, "Previous SLA" : {}, "New SLA" : {}}
		i = 0
		queue_impact_list = impact_analysis.queue_Impact_analysis_list
		queue_impact_list.sort(key=self.compare_impact)
		matplotlib.use('tkagg')

		for queue_impact in queue_impact_list:
			i += 1 # TODO(ballah): i variable used to insure the queue_id property is valid,
        #  and will be cleaned up later.
			queue_id = queue_impact.queue_id or i
			data["Desired SLA"][queue_id] = queue_impact.desired_SLA_min
			data["Previous SLA"][queue_id] = queue_impact.previous_SLA_min
			data["New SLA"][queue_id] = queue_impact.new_SLA_min

		data_frame = pd.DataFrame(data)
		a_x = data_frame.plot(kind='bar')

		a_x.set_ylabel('SLA (minutes)')
		a_x.set_xlabel('Queue Id')
		a_x.set_title('Queue Impact Analysis')

		plt.xticks(rotation=0)
		path = os.getcwd() + "/impact.png"
		plt.savefig(path)

		return path
