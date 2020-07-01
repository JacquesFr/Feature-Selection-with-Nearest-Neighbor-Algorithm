import math
import copy

"""
Written using python version 2.7
Jacques Fracchia
CS170 UCR
"""

def ForwardSelection(data, num_instances, num_features):
	final_set_of_features = []
	current_set_of_features = []
	final_accuracy = 0.0
	
	for i in range(num_features):
		feature_to_add_at_this_level = -1
		feature_to_add = -1
		best_so_far_accuracy = 0.0

		for j in range(1, num_features+1):
			if j not in current_set_of_features:
				temp_features = copy.deepcopy(current_set_of_features)
				temp_features.append(j)

				accuracy = leave_one_out_cross_validation(data, temp_features, num_instances)
				print "\tUsing feature(s) ", temp_features, " accuracy is ", accuracy, "%"

				if accuracy > final_accuracy:
					final_accuracy = accuracy
					feature_to_add_at_this_level = j

				if accuracy > best_so_far_accuracy:
					best_so_far_accuracy = accuracy
					feature_to_add = j

		if(feature_to_add_at_this_level >= 0):
			current_set_of_features.append(feature_to_add_at_this_level)
			final_set_of_features.append(feature_to_add_at_this_level)
			print "\n\nFeature set ", current_set_of_features, " was best, accuracy is ", final_accuracy, "%\n\n"

		else:
			print "\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)"			
			current_set_of_features.append(feature_to_add)
			print "Feature set ", current_set_of_features, " was best, accuracy is ", best_so_far_accuracy, "%\n\n"

	print "Finished search!! The best feature subset is", final_set_of_features, " which has an accuracy of accuracy: ", final_accuracy, "%"


def BackwardElimination(data, num_instances, num_features):
	current_set_of_features = []
	final_set_of_features = []
	final_accuracy = 0.0
	
	for i in range(1, num_features+1):
		current_set_of_features.append(i)
		final_set_of_features.append(i)

	for i in range(num_features):
		feature_to_remove_at_this_level = -1
		feature_to_remove = -1
		best_so_far_accuracy = 0.0

		for j in range(1, num_features + 1):
			if j in current_set_of_features:
				temp_subset = copy.deepcopy(current_set_of_features)
				temp_subset.remove(j)

				accuracy = leave_one_out_cross_validation(data, temp_subset, num_instances)
				print "\tUsing feature(s) ", temp_subset, " accuracy is ", accuracy, "%"

				if accuracy > final_accuracy:
					final_accuracy = accuracy
					feature_to_remove_at_this_level = j

				if accuracy > best_so_far_accuracy:
					best_so_far_accuracy = accuracy
					feature_to_remove = j

		if feature_to_remove_at_this_level >= 0:
			current_set_of_features.remove(feature_to_remove_at_this_level)
			final_set_of_features = current_set_of_features[:]
			print "\n\nFeature set ", current_set_of_features, " was best, accuracy is ", final_accuracy, "%\n\n"

		else:
			print "\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)"			
			current_set_of_features.remove(feature_to_remove)
			print "Feature set ", current_set_of_features, " was best, accuracy is ", best_so_far_accuracy, "%\n\n"


	print "Finished search!! The best feature subset is", final_set_of_features, " which has an accuracy of accuracy: ", final_accuracy, "%"


def Normalize(dataset, features_len, instances_len):
	std = []
	mean = []

	for i in range(features_len):
		mean.append((sum(row[i] for row in dataset))/instances_len)
		variance = sum( pow((row[i] - mean[i-1]), 2) for row in dataset)/instances_len
		std.append(math.sqrt(variance))

	for i in range(instances_len):
		for j in range (1, features_len + 1):
			x = dataset[i][j] - mean[j-1]
			dataset[i][j] = x / std[j-1]

	return dataset

def NearestNeighbor(dataset, position, features, instances_len):
	result = 0
	closest_path = float("inf")

	for i in range(instances_len):
		if position == i:
			pass

		else:
			length = 0
			for j in range(len(features)):
				x = dataset[i][features[j]] - dataset[position][features[j]]
				length = length + pow(x, 2)

			length = math.sqrt(length)
			if length < closest_path:
				closest_path = length
				result = i
				
	return result

def leave_one_out_cross_validation(dataset, features, instances_len):
	valid = 0.0
	for i in range(instances_len):
		position = i
		nearest_neighbor = NearestNeighbor(dataset, position, features, instances_len)

		if dataset[nearest_neighbor][0] == dataset[position][0]:
			valid = valid + 1

	accuracy = (valid / instances_len) * 100
	return accuracy


def main():
	print "Welcome to Jacques Fracchia\'s Feature Selection Algorithm."
	text = raw_input("Type in the name of the file to test: ")
	try:
		dataset = open(text, "r")
	except:
		raise IOError("Could not read: " + dataset)

	get_line = dataset.readline()
	instances_len = sum(1 for line in dataset)

	dataset.seek(0)

	instances = [[] for i in range (instances_len)]
	for i in range(instances_len):
		instances[i] = [float(x) for x in dataset.readline().split()]

	dataset.seek(0)

	features_len = len(get_line.split()) - 1
	features = []
	for i in range(0, features_len):
		features.append(i)

	dataset.seek(0)

	print "This dataset has " + str(features_len) + " features (not including the class attribute), with " + str(instances_len) + " instances."
	print "Please wait while I normalize the data... Done!"
	normalize_instances = Normalize(instances, features_len, instances_len)
	
	print "Type the number of the algorithm you want to run."
	print "1) Forward Selection"
	print "2) Backward Elimination"	
	selection = int(raw_input())
	accuracy = leave_one_out_cross_validation(normalize_instances, features, instances_len)
	
	print "Running nearest neighbor with all " + str(features_len) + " features, using \"leaving-one-out\" evaluation, I get an accuracy of " + str(accuracy) + "%."
	print "\nBeginning search.\n"
	if selection == 1:
		ForwardSelection(normalize_instances, instances_len, features_len)
	elif selection == 2:
		BackwardElimination(normalize_instances, instances_len, features_len)
	
if __name__ == "__main__":
	main()