import xml.etree.ElementTree as ET
from mail_send import send_result

tree = ET.parse('out_report.xml')
root = tree.getroot()
res = ""
mail_res = '<p dir="ltr" style="text-align:left;">\n'
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
mail_res += "Testing Report:<br>Total Tests - " + dictTest['tests'] + "<br>Success Tests - " + str((int(dictTest['tests']) - int(dictTest['failures']) - int(dictTest['errors']))) + "<br>Failed Tests - " + dictTest['failures'] + "<br>Error Tests - " + dictTest['errors'] + "<br><br>Measurements:<br>"

# Calculate test success percentage
successPercent = ((int(dictTest['tests']) - int(dictTest['failures'])) / int(dictTest['tests'])) * 100
res += "Success Percentage - " + "{0:0.2f}".format(successPercent) + "%\n"

# Save the running time of all tests
time = dictTest['time']
res += "Total Test Running Time - " + str(time) + "s"

# Add the calculated measurements to the mail
mail_res += "<br>".join(res.split("\n"))

# Print results
print(res)

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

# Send the results to all recipents in mail
send_result(mail_res)
