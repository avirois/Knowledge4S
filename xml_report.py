import xml.etree.ElementTree as ET
from mail_send import send_result

# Const defintion
UNIT_INDX = 0
INTEGRATION_INDX = 1
PATH_INDX = 0
TITLE_INDX = 1
FILES = [["out_report_unit.xml", "Unit Testing"],["out_report_integration.xml", "Integration Testing"]]

# Global variables
nTotalTests = 0
nTotalSuccess = 0
nTotalFailed = 0
nTotalError = 0
nTotalTime = 0.0

def measurements_calc(nTotal, nFailed, nError, nTime):
    # initialize result string
    res = ""

    # Calculate test success percentage
    successPercent = ((nTotal - nFailed - nError) / nTotal) * 100
    res += "Success Percentage - " + "{0:0.2f}".format(successPercent) + "%\n"

    # Save the running time of all tests
    res += "Total Test Running Time - " + str(nTime) + "s"

    return (res)

def test_report(xml_file):
    # Set global variables in function
    global nTotalTests, nTotalSuccess, nTotalFailed, nTotalError, nTotalTime

    # Parse the xml file as tree
    tree = ET.parse(xml_file[PATH_INDX])

    # Get root attribute of the tree
    root = tree.getroot()

    # Prepare results
    res = ""
    mail_res = '<p dir="ltr" style="text-align:left;">\n' + xml_file[TITLE_INDX] + " Report:<br>"
    lstErrors = []
    lstFailures = []

    # Run over the data of the test
    for child in root:
        dictTest = {}

        # Create dictionary with values of test
        for name, value in child.attrib.items():
            dictTest[name] = value

        for test in child:
            # Create dictionary for data of each test
            dictTestRes = {}

            # Create dictionary with values of test
            for name, value in test.attrib.items():
                dictTestRes[name] = value

            errors = test.findall("error")
            failures = test.findall("failure")

            # Check if error found
            if (errors):
                lstErrors.append([dictTestRes['name']] + errors)

            # Check if failure found
            if (failures):
                lstFailures.append([dictTestRes['name']] + failures)

    # Prepare report for mail
    mail_res += "Total Tests - " + dictTest['tests'] + "<br>Success Tests - " + str((int(dictTest['tests']) - int(dictTest['failures']) - int(dictTest['errors']))) + "<br>Failed Tests - " + dictTest['failures'] + "<br>Error Tests - " + dictTest['errors'] + "<br><br>Measurements:<br>"

    # Calculate the measurements
    res += measurements_calc(int(dictTest['tests']),  int(dictTest['failures']), int(dictTest['errors']), dictTest['time'])

    # Add the calculated measurements to the mail
    mail_res += "<br>".join(res.split("\n"))

    # Print results
    print(xml_file[TITLE_INDX] + " :\n" + res + "\n")

    # Append values of the current test to global
    nTotalTests += int(dictTest['tests'])
    nTotalSuccess += int(dictTest['tests']) - int(dictTest['failures']) - int(dictTest['errors'])
    nTotalError += int(dictTest['errors'])
    nTotalFailed += int(dictTest['failures'])
    nTotalTime += float(dictTest['time'])

    # Check if error exists
    if (lstErrors):
        # Add error section
        mail_res += "<br><br>Errors:<br>"

        # Prepare errors message
        error_res = ""
        nIndxError = 1

        # Run over errors
        for error in lstErrors:
            error_res += str(nIndxError) + ". " + error[0] + ":<br>" + "<br>".join(error[1].text.split("\n")) + "<br><br>"
            nIndxError += 1
        
        # Add errors
        mail_res += error_res

    # Check if failures exists
    if (lstFailures):
        # Add failures section
        mail_res += "<br><br>Failures:<br>"

        # Prepare errors message
        fail_res = ""
        nIndxFail = 1

        # Run over errors
        for fail in lstFailures:
            fail_res += str(nIndxFail) + ". " + fail[0] + ":<br>" + "<br>".join(fail[1].text.split("\n")) + "<br><br>"
            nIndxFail += 1

        # Add errors and failures to the mail report
        mail_res += fail_res

    # Close paragraph
    mail_res += "</p>"
    
    # Return the report of current test
    return (mail_res)

msgTotal = ""

# Run over the files
for file in FILES:
    msgTotal += test_report(file)
    msgTotal += "\n"

# Calculate measurements
measurements = measurements_calc(nTotalTests, nTotalFailed, nTotalError, nTotalTime)

# Prepare the total message
totalMeasure = "Total Report:\n" + measurements

# Print the total measurement
print(totalMeasure)

# Prepare the total message
testValues = "Total Tests - " + str(nTotalTests) + "\nSuccess Tests - " + str(nTotalSuccess) + "\nFailed Tests - " + str(nTotalFailed) + "\nError Tests - " + str(nTotalError) + "\n\nMeasurements:\n"
totalMeasure = "Total Report:\n" + testValues + "" + measurements

# Prepare the mail report
totalMail = '<p dir="ltr" style="text-align:left;"><b>' + '<br>'.join(totalMeasure.split("\n")) + '</b></p>' + msgTotal

# Send the results to all recipents in mail
send_result(totalMail)