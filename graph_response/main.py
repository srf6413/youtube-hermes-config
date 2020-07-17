import matplotlib.pyplot as plt
import pandas as pd
import impact_analysis_response_pb2

def GraphImpact(impact_analysis):
	data = {"desired sla": {}, "old sla" : {}, "new sla" : {}}
	i = 0
	for queue_impact in impact_analysis.queue_Impact_analysis_list:
		i = i + 1
		id = queue_impact.queue_id or i
		data["desired sla"][id] = queue_impact.desired_SLA_min
		data["old sla"][id] = queue_impact.previous_SLA_min
		data["new sla"][id] = queue_impact.new_SLA_min

	df = pd.DataFrame(data)

	df.plot(kind='bar')

	plt.show()


impact_analysis = impact_analysis_response_pb2.ImpactAnalysisResponse()
f = open("/Users/isaiah/Dev/Google/youtube-hermes-config/response_results/impact.txt", "rb")
impact_analysis.ParseFromString(f.read())
f.close()

print(impact_analysis)
GraphImpact(impact_analysis)