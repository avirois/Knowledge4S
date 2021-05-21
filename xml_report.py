import xml.etree.ElementTree as ET

tree = ET.parse('out_report.xml')
root = tree.getroot()

# Run over the data of the test
for child in root:
    dictTest = {}

    # Create dictionary with values of test
    for name, value in child.attrib.items():
        dictTest[name] = value

# Calculate test success percentage
successPercent = ((int(dictTest['tests']) - int(dictTest['failures'])) / int(dictTest['tests'])) * 100
print("Success Percentage - " + str(successPercent) + "%")

# Save the running time of all tests
time = dictTest['time']
print("Total Test Running Time - " + str(time) + "s")