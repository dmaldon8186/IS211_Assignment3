import requests
import csv
import argparse
import re

def image_format_func(text):
    search_result = bool(re.search("^.*\.(jpg|jpeg|gif|png|JPG|JPEG|GIF|PNG)$", text))
    if search_result == True:
        return True
    else:
        return False

def browser_func(text):
    search_result = re.search("Firefox|Chrome|MSIE|Safari", text)
    if bool(search_result) == True:
        return search_result.group(0)
    else:
        return False

def downloadData(url):
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        data = list(cr)
    return data

def processData(data):
    data_count = 0
    image_count = 0
    browser_dict = {'Firefox':0, 'Chrome':0, 'MSIE':0, 'Safari':0}
    for x in data:
        data_count += 1
        img_result = image_format_func(x[0])
        if img_result == True:
            image_count += 1
        browser_result = browser_func(x[2])
        if browser_result != False:
            browser_dict[browser_result] += 1
    print("Images found: " + str(image_count))
    print("Image requests account for " + str(image_count/data_count*100) + "% of all requests.")
    print(browser_dict)
    print(str(max(browser_dict, key=browser_dict.get)) + " is the most popular browser.")

def main():
    downloaded_data=None
    parser=argparse.ArgumentParser()
    parser.add_argument ("--url", required=True, help="Provide the CSV file's URL.")
    args=parser.parse_args()
    try:
        downloaded_data=downloadData(args.url)
    except:
        print("Error occured while downloading the file!!!")
    processData(downloaded_data)   

if __name__=="__main__":
    main()