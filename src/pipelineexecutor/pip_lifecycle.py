import os, json
import tempfile
import csv

''' Running status of pipeline video 
#
	0: NOT PICKED FOR PROCESSING,
	1: RUNNING, 
	2: PICKED AND FAILED, 
	3: PICKED AND UPLOADED SUCCESSFULLY
#
'''
PIPELINE_VIDEO_PROCESSING_STATUS = [0,1,2,3]


'''
#
	Write-Replace pattern has been used here, the idea is to write updated contents 
	into a temporary file and replace it with the original file.
#
'''
def DumpContentsIntoFile(contents, path_to_status_file):
	with tempfile.NamedTemporaryFile('wb', dir=os.path.dirname(path_to_status_file), delete=False) as tf:
		json.dump(contents, tf)
		tempname = tf.name
	os.rename(tempname, path_to_status_file)



def GetAllKeyValues(path_to_content):
	contents = {}
	with open(path_to_content) as f:
		for line in csv.reader(f, dialect="excel-tab"):
			contents[line[0]] = line[1]
	return contents


def StartExecution(key, path_to_status_file):
	#Load the status to RUNNING(1) state
	contents = json.load(open(path_to_status_file))
	if key in contents:
		status = int(contents[key])
		if status>2:
			return (False, "Video with key " + key + " has been already processed/uploaded so skipping..")
	else:
		contents[key] = str(PIPELINE_VIDEO_PROCESSING_STATUS[1])

	#Update the status
	DumpContentsIntoFile(contents, path_to_status_file)
	return True, ""


def EndExecution(key, path_to_status_file):	
	#Update the status to SUCCESS(3)
	contents = json.load(open(path_to_status_file))
	contents[key] = str(PIPELINE_VIDEO_PROCESSING_STATUS[3])

	#Update the status
	DumpContentsIntoFile(contents, path_to_status_file)



