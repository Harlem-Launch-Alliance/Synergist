import csv

header = ['time', 'altitude']
values = [[1, 0],[2, 20],[3, 100],[4,120]]

def datalog(title, inputs):
    # open the file in the write mode
    with open('altitude.csv', 'w', newline='') as csvfile:
        # create the csv writer
        writer = csv.writer(csvfile)
        #write the header
        writer.writerow(title)
        # write the data
        writer.writerows(inputs)
        for i in range(len(inputs),0,-1):
            inputs.pop(i-1)


datalog(header, values)
print(values)



        # fieldnames = ['time', 'altitude']
        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        # while(writer.length >1):
        #     writer.writerow({'Time': time, 'Altitude': altitude})
        #     value = input.pop(0)
        # for i in range(len(dataArray)):
        #     writer.writerow({'Time': currentTime, 'Altitude': altitude})