import matplotlib.pyplot as plt
import pandas as pd
import impact_analysis_response_pb2

# Sort the queue impacts so the impacts where the new SLA is greater then the desired impact or increased from the previous SLA.
def CompareImpact(queue_impact):
    desired_delta = (queue_impact.desired_SLA_min - queue_impact.new_SLA_min) + (queue_impact.previous_SLA_min - queue_impact.new_SLA_min)
    return desired_delta


# This function takes a ImpactAnalysisResponse object and displays the Queues Impact Graph.
def GraphImpact(impact_analysis):
	data = {"Desired SLA": {}, "Previous SLA" : {}, "New SLA" : {}}
	queue_impact_list = impact_analysis.queue_Impact_analysis_list
	queue_impact_list.sort(key=CompareImpact)

	i = 0
	for queue_impact in queue_impact_list:
		# TODO(ballah): i variable used to insure the queue_id property is valid, and will be cleaned up later.
		i = i + 1
		id = queue_impact.queue_id or i
		data["Desired SLA"][id] = queue_impact.desired_SLA_min
		data["Previous SLA"][id] = queue_impact.previous_SLA_min
		data["New SLA"][id] = queue_impact.new_SLA_min

	df = pd.DataFrame(data)
	ax = df.plot(kind='bar')

	ax.set_ylabel('SLA (minutes)')
	ax.set_xlabel('Queue Id')
	ax.set_title('Queue Impact Analysis')

	plt.show()