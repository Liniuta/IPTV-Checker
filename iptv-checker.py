try:    
    import sys
    import requests
    import re
    import os
    import shutil
    import time
    from datetime import datetime
except ModuleNotFoundError:
   print("One or more requierd modules are missing.")
   print("Please install requierd modules using this command:")
   print("pip install -r requirements.txt")
   print("or run install.bat from scripts folder.")
   input("Press ENTER to exit..")
   os._exit(1)

print("IPTV Checker v1.0")
print("github.com/Liniuta/IPTV-Checker")

m3u_file = input("Enter m3u file name: ")
timeout = input("Enter timeout: ")

try:
    shutil.copyfile(m3u_file, "playlist-backup.m3u")
    os.rename(m3u_file, "playlist_temp.txt")
    txt_file = "playlist_temp.txt"
    with open(txt_file) as f:
        text = f.read()
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        print("Number of streams loaded:", len(urls))
        working_urls = []
        for url in urls:
            try:
                r = requests.get(url)
                sc = r.status_code
                if sc == 200:
                    valid = 'Valid'
                else:
                    #valid = "Not valid"
                    pass
                now = datetime.now()
                date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")
                print(f'URL: {url}')
                #print(f'Status code: {sc}') 
                print(f'{valid}')
                print(f"Checked at {date_and_time}.")
                working_urls.append(url)
                time.sleep(int(timeout))
            except (requests.exceptions.RequestException, requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                now = datetime.now()
                date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")
                print(f'URL: {url}')
                print('Error while trying to check this URL, it may not working.')
                print(f"Checked at {date_and_time}.")
                time.sleep(int(timeout))
    os.rename("playlist_temp.txt", m3u_file)
    time.sleep(2)
    print('Generating checked playlist...')
    with open('playlist-checked.m3u', 'w') as file:
        file.write('#EXTM3U\n') 
        for url in working_urls:
            file.write('#EXTINF:-1,' + "Channel Name" + '\n')
            file.write(url + '\n')
    #print(working_urls)
    print("Done!")
    print("All streams checked!")
    input("Press ENTER to exit..")
    os._exit(1)
except FileNotFoundError:
    print(f"Can't find {m3u_file}!")
    print("Please check the file name!")
    input("Press ENTER to exit..")
    os._exit(1)
