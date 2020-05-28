# output log directory.
Log_Directory = 'Build_Version'

#Name of the output log file.
File_Name = 'Site_Log.txt'

# browsercode takes a integer which represents a specific browser
#            ex: 0 for Chrome
#                1 for Firefox
#                other values open Internet Explorer
browsercode = '0'

# Path to the github 100 web sites list.
url_path = 'https://gist.githubusercontent.com/demersdesigns/4442cd84c1cc6c5ccda9b19eac1ba52b/raw/cf06109a805b661dd12133f9aa4473435e478569/craft-popular-urls'

# Variable to store 100 web url list.
web_url_list = []

# number of sites to open from 100 sites.
number_of_sites = 5

# variable to store randomly selected number_of_sites web sites from 100 site list.
selectList = []

# number of seconds to wait to close the btowser.
browser_close_time = 10
