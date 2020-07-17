import matplotlib.pyplot as plt
import pandas as pd
import impact_analysis_response_pb2

# Sort the queue impacts so the impacts where the new SLA is greater then the desired impact or increased from the previous SLA
def CompareImpact(queue_impact):
    desired_delta = (queue_impact.desired_SLA_min - queue_impact.new_SLA_min) + (queue_impact.previous_SLA_min - queue_impact.new_SLA_min)
    return desired_delta


def GraphImpact(impact_analysis):
	data = {"Desired SLA": {}, "Previous SLA" : {}, "New SLA" : {}}
	i = 0
	queue_impact_list = impact_analysis.queue_Impact_analysis_list
	queue_impact_list.sort(key=CompareImpact)
	for queue_impact in queue_impact_list:
		i = i + 1
		id = queue_impact.queue_id or i
		data["Desired SLA"][id] = queue_impact.desired_SLA_min
		data["Previous SLA"][id] = queue_impact.previous_SLA_min
		data["New SLA"][id] = queue_impact.new_SLA_min

	df = pd.DataFrame(data)
	ax = df.plot(kind='bar')

	# Set the y axis label
	ax.set_ylabel('SLA (minutes)')

	# Set the x axis label
	ax.set_xlabel('Queue Id')

	# Set the chart's title
	ax.set_title('Queue Impact Analysis')

	plt.show()


impact_analysis = impact_analysis_response_pb2.ImpactAnalysisResponse()
f = open("/Users/isaiah/Dev/Google/youtube-hermes-config/graph_response/impact.txt", "rb")
impact_analysis.ParseFromString(f.read())
f.close()

print(impact_analysis)
GraphImpact(impact_analysis)