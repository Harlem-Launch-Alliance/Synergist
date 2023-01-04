import csv

header = ['time, altitude']
input = [[1, 0],[2, 20],[3, 100],[4,120]]

def datalog(input):
    # open the file in the write mode
    with open('altitude.csv', 'w', newline='') as csvfile:
        # create the csv writer
        writer = csv.writer(csvfile)
        #write the header
        writer.writerow(header)
        # write the data
        writer.writerow(input)



        # fieldnames = ['time', 'altitude']
        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        # while(writer.length >1):
        #     writer.writerow({'Time': time, 'Altitude': altitude})
        #     value = input.pop(0)
        # for i in range(len(dataArray)):
        #     writer.writerow({'Time': currentTime, 'Altitude': altitude})