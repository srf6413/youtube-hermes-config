# import matplotlib.pyplot as plt
# import pandas as pd
import impact_analysis_response_pb2
# import matplotlib.patches as mpatches

# # plt.gca().set_prop_cycle('color', ["#4285f4", "#ea4335"])

# # Sort the queue impacts so the impacts where the new SLA is greater then the desired impact or increased from the previous SLA
# def CompareImpact(queue_impact):
#     desired_delta = (queue_impact.desired_SLA_min - queue_impact.new_SLA_min) + (queue_impact.previous_SLA_min - queue_impact.new_SLA_min)
#     return desired_delta


# def GraphImpact(impact_analysis):
# 	# data = {"Desired SLA": {}, "Previous SLA" : {}, "New SLA" : {}}
# 	data = {"Previous SLA" : {}, "New SLA" : {}}
# 	i = 0
# 	queue_impact_list = impact_analysis.queue_Impact_analysis_list
# 	queue_impact_list.sort(key=CompareImpact)
# 	y_min = queue_impact_list[0].previous_SLA_min # find the lowest y value for desired/new/prev SLA
# 	for queue_impact in queue_impact_list:
# 		i = i + 1
# 		id = queue_impact.queue_id or i
# 		data["Previous SLA"][id] = queue_impact.previous_SLA_min
# 		data["New SLA"][id] = queue_impact.new_SLA_min
# 		if queue_impact.previous_SLA_min < y_min:
# 			y_min = queue_impact.previous_SLA_min
# 		if queue_impact.new_SLA_min < y_min:
# 			y_min = queue_impact.new_SLA_min
# 		if queue_impact.desired_SLA_min < y_min:
# 			y_min = queue_impact.desired_SLA_min

# 	df = pd.DataFrame(data)
# 	# ax = df.plot(kind='bar', color=["#4285f4", "#fbbc05"]) //cf2415 red, yellow e49e09, blue 4285f4
# 	ax = df.plot(kind='bar', color=["#e49e09", "#2e9048"])
# 	# ax = df.plot(kind='bar', color=["#4285f4", "#ea4335"])

# 	# Set the y axis label
# 	ax.set_ylabel('SLA (minutes)')

# 	# Set the x axis label
# 	ax.set_xlabel('Queue Id')

# 	# Set the chart's title
# 	ax.set_title('Queue Impact Analysis')
# 	i = 0
# 	for queue_impact in queue_impact_list:
# 		i = i + 1
# 		id = queue_impact.queue_id or i
# 		# Plot the desired SLA lines and add one label to the legend
# 		plt.hlines(y = queue_impact.desired_SLA_min, xmin = i-1.4, xmax = i-.6, label = (i == 1) and "Desired SLA" or None)

# 	# Get labels for data that has been plotted to ax
# 	handles, labels = ax.get_legend_handles_labels()

# 	# plot the legend
# 	plt.legend(handles=handles, loc=(1.05, .5))
# 	plt.tight_layout()
# 	plt.ylim(ymin=y_min/2)
# 	plt.show()


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
    the desired impact or increased from the previous SLA

		Args:
				queue_impact : the list of queue impacts

		Returns:
				str: the desired delta SLA
		"""
		desired_delta = (queue_impact.desired_SLA_min - queue_impact.new_SLA_min) + \
    (queue_impact.previous_SLA_min - queue_impact.new_SLA_min)
		return desired_delta


	def graph_impact(self, impact_analysis):
		"""Creates the impact analysis .png and saves it to the project directory.

		Args:
				impact_analysis (ImpactAnalsisResponse): the ImpactAnalysisResponse Protobuf object

		Returns:
				str: the path to the graph impact analysis .png file
		"""
		data = {"Previous SLA" : {}, "New SLA" : {}}
		queue_impact_list = impact_analysis.queue_Impact_analysis_list
		i = 0
		for queue_impact in queue_impact_list:
			i += 1
			queue_impact.queue_id = queue_impact.queue_id or str(i)

		queue_impact_list.sort(key=self.compare_impact)
		matplotlib.use('tkagg')
		y_min = queue_impact_list[0].previous_SLA_min # find the lowest y value for desired/new/prev SLA
		i = 0
		for queue_impact in queue_impact_list:
			i += 1
			id = queue_impact.queue_id or i
			data["Previous SLA"][id] = queue_impact.previous_SLA_min
			data["New SLA"][id] = queue_impact.new_SLA_min
			if queue_impact.previous_SLA_min < y_min:
				y_min = queue_impact.previous_SLA_min
			if queue_impact.new_SLA_min < y_min:
				y_min = queue_impact.new_SLA_min
			if queue_impact.desired_SLA_min < y_min:
				y_min = queue_impact.desired_SLA_min

		# for queue_impact in queue_impact_list:
		# 	i += 1
		# 	queue_id = queue_impact.queue_id or i
		# 	data["Desired SLA"][queue_id] = queue_impact.desired_SLA_min
		# 	data["Previous SLA"][queue_id] = queue_impact.previous_SLA_min
		# 	data["New SLA"][queue_id] = queue_impact.new_SLA_min

		data_frame = pd.DataFrame(data)
		a_x = data_frame.plot(kind='bar', color=["#e49e09", "#2e9048"])

		# Set the y axis label
		a_x.set_ylabel('SLA (minutes)')

		# Set the x axis label
		a_x.set_xlabel('Queue Id')

		# Set the chart's title
		a_x.set_title('Queue Impact Analysis')
		i = 0
		for queue_impact in queue_impact_list:
			i = i + 1
			id = queue_impact.queue_id or i
			# Plot the desired SLA lines and add one label to the legend
			plt.hlines(y = queue_impact.desired_SLA_min, xmin = i-1.4, xmax = i-.6, label = (i == 1) and "Desired SLA" or None)

		# Get labels for data that has been plotted to ax
		handles, labels = a_x.get_legend_handles_labels()

		# plot the legend
		plt.legend(handles=handles, loc=(1.05, .5))
		plt.tight_layout()
		plt.ylim(ymin=y_min/2)
		plt.xticks(rotation=0)

		path = os.getcwd() + "/impact.png"

		plt.savefig(path)

		return path
		
impact_analysis = impact_analysis_response_pb2.ImpactAnalysisResponse()
f = open("/Users/isaiah/Dev/Google/youtube-hermes-config/graph_response/impact.txt", "rb")
impact_analysis.ParseFromString(f.read())
f.close()

# GraphImpact(impact_analysis)
print(GraphAnalysis().graph_impact(impact_analysis))
# print(impact_analysis)