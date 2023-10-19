import requests
from bs4 import BeautifulSoup
import schedule
import time
import vonage

#I've removed my vonage API key, vonage secret and phone number from the code
#because I don't want to share that information on github
key = "add your vonage API key here, otherwise code won't work"
secret = "add your vonage secret here, otherwise code won't work"
number = "add the phone number you want the alert to be sent to here as a string"

#uses the vonage api to send a text message 
def send_message(message):
    client = vonage.Client(key=key, secret=secret)
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": number,
            "text": message,
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")


def scan_lulu():
    new_list = []
    #file stores the previous colours of the skirt
    #opens it and stores them in a list
    f = open("lulu_list", "r")
    prev_list = f.read()
    prev_list = prev_list.split("\n")
    #removes the empty string at the end
    prev_list.pop()
    print(prev_list)
    f.close()
    #uses the beatuiful soup and requests libraries to scrape the HTML off of lulu
    URL = "https://shop.lululemon.com/p/skirts-and-dresses-skirts/Pace-Rival-Skirt/_/prod3770004?color=0001"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    swatch_elements = soup.find_all(attrs={"data-testid": "swatch"})
    # f = open("lulu_list", "a")
    # Iterates through the elements with the skirt colour tag 
    #stores the colours in a list
    for element in swatch_elements:
        aria_label = element.get("aria-label")
        # print(aria_label)
        new_list.append(aria_label)
        
        # f.write(aria_label)
        # f.write("\n")
    
    #if there has been a new skirt added
    if new_list != prev_list:
        print("OMG A CHANGE NEW SKIRT!")
        new_colour = "something was removed, not added :("
        #identifies the new colour 
        for item in new_list:
            if item not in prev_list:
                new_colour = item
        #uses send message function above to text the new colour
        send_message("OMG THERE'S A NEW SKIRT! THE COLOUR IS : " + new_colour)
        #clears the file with the old colours
        with open("lulu_list", 'w') as file:
            pass
        #adds the new colours to a file
        f = open("lulu_list", "a")
        for colour in new_list:
            f.write(colour)
            f.write("\n")
        
        f.close()
        #the lists are the same aka no new skirt added
    else:
        print("no changes :(")

   
scan_lulu()

#uses the python scheduler to run the code every 30 min 
#so the website is checked every 30 min if new colours have been added
schedule.every(30).minutes.do(scan_lulu)
while True:
 
    # Checks whether a scheduled task 
    # is pending to run or not
    schedule.run_pending()
    time.sleep(10000)