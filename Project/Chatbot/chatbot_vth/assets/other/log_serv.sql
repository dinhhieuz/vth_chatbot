exec sp_execute_external_script 
@language =N'Python',
@script=N'OutputDataSet = InputDataSet
print("Input data is {0}".format(InputDataSet))
', 
@input_data_1 = N'SELECT 1 as col'