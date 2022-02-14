import argparse
import urllib.request
import logging
import datetime
import sys
#This section of the code contains a function to download the data provided in class. A parameter was set with the
#url link(by using the console), and urllib.request was used to open the url.
def downloadData(url):
    """Downloads the data"""
    with urllib.request.urlopen(url) as response:
        web_data = response.read().decode('utf-8')

    return web_data

#This section of the code contains a function named processData which takes the content files as a parameter. Then
#the split function was used to so the file can be processed line by line. Then birtday was converted into a datetime
#object with the format dd/mm/yy.
def processData(file_content):
    person_dict = {}
    for data_line in file_content.split("\n"):
        if len(data_line) == 0:
            continue

        identifier, name, birthday = data_line.split(",")
        if identifier == "id":
            continue

        id_int = int(identifier)
        try:
            real_birthday = datetime.datetime.strptime(birthday, "%d/%m/%Y")
            person_dict[id_int] = (name, real_birthday)
        except ValueError as e:
            print(f"error parsing {birthday}")

    return person_dict


#This section of the code contains a function with two parameters(id, personData). It then contains a if statement
#to print a person's name and birthday if it is found in the database and to produced a message if the person is not
#found
def displayPerson(id, personData):

    if id in personData:
        personName = personData[id][0]
        birthday = personData[id][1]
        personDOB = birthday.strftime('%Y-%m-%d')
        print("Person #" + str(id) + " is " + personName + " with a birthday of " + personDOB)
    else:
        print("No user found with that id")



#In this section of the code, I created a while loop in which the user is asked to input a person's id and the
#program keeps doing so until an input of 0 or less is provided.
def main(url):

    print(f"Running main with URL = {url}...")
    data = downloadData(url)
    personData = processData(data)

    while(True):
        id = input("What's the person id: ")
        if int(id) <= 0:
            sys.exit()
        elif int(id) > 0:
            displayPerson(int(id), personData)

        logging.basicConfig(filename='error.log', level=logging.ERROR, encoding='utf-8', filemode='w')
        Assignment2 = logging.getLogger()




if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
