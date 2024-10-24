
# code source: https://jon.glass/blog/attempts-to-parse-webcachev01-dat/

import pyesedb
file_object = open("WebCacheV01.dat", "rb")
esedb_file = pyesedb.file()
esedb_file.open_file_object(file_object)
ContainersTable = esedb_file.get_table_by_name("Containers")
WebHistoryTables = []
for i in range(0,ContainersTable.get_number_of_records()-1):
	Container_Record = ContainersTable.get_record(i)
	ContainerID = Container_Record.get_value_data_as_integer(0)
	Container_Name = Container_Record.get_value_data_as_string(8)
	Container_Directory = Container_Record.get_value_data_as_string(10)
	if Container_Name == "History" and "History.IE5" in Container_Directory:
		WebHistoryTables += [ContainerID]
 
for i in WebHistoryTables:
	WebHistoryTable = esedb_file.get_table_by_name("Container_"+ str(i))
	for j in range(0,WebHistoryTable.get_number_of_records()-1):
		WebHistoryRecord = WebHistoryTable.get_record(j)
		
		URL = WebHistoryRecord.get_value_data_as_string(17)
		print (URL)
 
esedb_file.close()