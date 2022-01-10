from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

web = webdriver.Chrome()
web.get('https://fd-tools.ncsa.illinois.edu/premiums')
web.implicitly_wait(20)
time.sleep(5)

###LIST OF STATES, COUNTIES, CROPS OF INTEREST     #Question: Does it even matter what state we are in?
alt_states = ['Michigan', 'Iowa']
alt_counties = {'Michigan': ['Ingham', 'Roscommon'],
                'Iowa': ['Polk', 'Story']}
states_list = ["Illinois", "Indiana", "Iowa", "Michigan", "Minnesota", "Missouri", "North Dakota", "Ohio", "South Dakota", "Wisconsin"]
counties_list = {   "Illinois": ["Cook", "DuPage", "Lake", "Will", "Kane", "McHenry", "Winnebago", "Madison", "St. Clair", "Champaign", "Sangamon", "Peoria", "McLean", "Rock Island", "Tazewell", "Kendall", "Kankakee", "LaSalle", "Macon", "DeKalb", "Vermilion", "Williamson", "Adams", "Jackson", "Whiteside", "Boone", "Coles", "Ogle", "Grundy", "Knox", "Henry", "Macoupin", "Stephenson", "Franklin", "Woodford", "Jefferson", "Marion", "Clinton", "Livingston", "Fulton", "Lee", "Morgan", "Monroe", "Effingham", "Bureau", "Christian", "Randolph", "McDonough", "Logan", "Montgomery", "Iroquois", "Saline", "Jersey", "Shelby", "Jo Daviess", "Fayette", "Perry", "Douglas", "Crawford", "Hancock", "Edgar", "Warren", "Union", "Bond", "Wayne", "Piatt", "Lawrence", "De Witt", "Richland", "Clark", "Pike", "Mercer", "Moultrie", "Carroll", "Massac", "Washington", "White", "Mason", "Clay", "Ford", "Greene", "Johnson", "Cass", "Menard", "Marshall", "Wabash", "Cumberland", "Jasper", "Hamilton", "Schuyler", "Henderson", "Brown", "Edwards", "Alexander", "Putnam", "Pulaski", "Stark", "Gallatin", "Scott", "Calhoun", "Pope", "Hardin"],
                    "Indiana": ["Marion", "Lake", "Allen", "Hamilton", "St. Joseph", "Elkhart", "Tippecanoe", "Vanderburgh", "Porter", "Hendricks", "Johnson", "Monroe", "Madison", "Clark", "Delaware", "LaPorte", "Vigo", "Bartholomew", "Howard", "Kosciusko", "Floyd", "Hancock", "Morgan", "Grant", "Wayne", "Boone", "Warrick", "Dearborn", "Henry", "Noble", "Marshall", "Lawrence", "Shelby", "Jackson", "DeKalb", "Dubois", "Harrison", "LaGrange", "Montgomery", "Cass", "Putnam", "Knox", "Huntington", "Miami", "Adams", "Steuben", "Whitley", "Gibson", "Jasper", "Daviess", "Clinton", "Jefferson", "Greene", "Wabash", "Ripley", "Wells", "Washington", "Jennings", "Decatur", "Clay", "Posey", "Randolph", "White", "Scott", "Fayette", "Starke", "Franklin", "Jay", "Owen", "Sullivan", "Spencer", "Fulton", "Carroll", "Orange", "Perry", "Parke", "Rush", "Fountain", "Vermillion", "Tipton", "Brown", "Newton", "Pulaski", "Pike", "Blackford", "Switzerland", "Crawford", "Martin", "Benton", "Warren", "Union", "Ohio"],
                    "Iowa": ["Polk","Linn","Scott","Johnson","Black Hawk","Woodbury","Dubuque","Story","Pottawattamie","Dallas","Warren","Clinton","Muscatine","Cerro Gordo","Marshall","Des Moines","Jasper","Webster","Wapello","Sioux","Lee","Marion","Boone","Benton","Plymouth","Bremer","Mahaska","Washington","Buchanan","Jones","Carroll","Winneshiek","Buena Vista","Henry","Fayette","Jackson","Cedar","Poweshiek","Jefferson","Clayton","Delaware","Dickinson","Hardin","Crawford","Tama","Clay","Iowa","Madison","Floyd","Page","Mills","Hamilton","Kossuth","Butler","Harrison","O'Brien","Allamakee","Cass","Wright","Appanoose","Union","Grundy","Chickasaw","Lyon","Shelby","Cherokee","Louisa","Hancock","Guthrie","Mitchell","Winnebago","Keokuk","Franklin","Montgomery","Sac","Calhoun","Humboldt","Emmet","Clarke","Howard","Palo Alto","Greene","Davis","Monona","Lucas","Decatur","Monroe","Worth","Van Buren","Adair","Fremont","Ida","Pocahontas","Wayne","Taylor","Osceola","Audubon","Ringgold","Adams"],
                    "Michigan": ["Wayne", "Oakland", "Macomb", "Kent", "Genesee", "Washtenaw", "Ingham", "Ottawa", "Kalamazoo", "Saginaw", "Livingston", "Muskegon", "St. Clair", "Jackson", "Berrien", "Monroe", "Calhoun", "Allegan", "Eaton", "Bay", "Lenawee", "Grand Traverse", "Lapeer", "Midland", "Clinton", "Van Buren", "Isabella", "Shiawassee", "Marquette", "Ionia", "Montcalm", "St. Joseph", "Barry", "Tuscola", "Cass", "Newaygo", "Hillsdale", "Branch", "Mecosta", "Sanilac", "Gratiot", "Houghton", "Delta", "Wexford", "Emmet", "Huron", "Clare", "Mason", "Alpena", "Oceana", "Charlevoix", "Dickinson", "Cheboygan", "Gladwin", "Iosco", "Otsego", "Manistee", "Roscommon", "Osceola", "Antrim", "Menominee", "Leelanau", "Ogemaw", "Benzie", "Kalkaska", "Arenac", "Gogebic", "Missaukee", "Crawford", "Presque Isle", "Lake", "Iron", "Mackinac", "Alcona", "Montmorency", "Alger", "Baraga", "Oscoda", "Schoolcraft", "Luce", "Ontonagon", "Keweenaw"],
                    "Minnesota": ["Hennepin", "Ramsey", "Dakota", "Anoka", "Washington", "St. Louis", "Stearns", "Olmsted", "Scott", "Wright", "Carver", "Sherburne", "Blue Earth", "Rice", "Crow Wing", "Clay", "Otter Tail", "Chisago", "Winona", "Beltrami", "Goodhue", "Itasca", "Kandiyohi", "Benton", "Mower", "Isanti", "Douglas", "Steele", "McLeod", "Carlton", "Becker", "Nicollet", "Morrison", "Polk", "Freeborn", "Cass", "Pine", "Le Sueur", "Mille Lacs", "Lyon", "Brown", "Todd", "Meeker", "Nobles", "Wabasha", "Hubbard", "Fillmore", "Dodge", "Martin", "Waseca", "Houston", "Kanabec", "Aitkin", "Roseau", "Redwood", "Sibley", "Renville", "Pennington", "Faribault", "Wadena", "Koochiching", "Chippewa", "Cottonwood", "Pope", "Watonwan", "Lake", "Jackson", "Yellow Medicine", "Stevens", "Rock", "Marshall", "Swift", "Pipestone", "Clearwater", "Murray", "Lac qui Parle", "Norman", "Wilkin", "Grant", "Lincoln", "Mahnomen", "Cook", "Big Stone", "Kittson", "Red Lake", "Lake of the Woods", "Traverse"],
                    "Missouri": ["St. Louis", "Jackson", "St. Charles", "St. Louis", "Greene", "Clay", "Jefferson", "Boone", "Jasper", "Cass", "Franklin", "Platte", "Buchanan", "Christian", "Cape Girardeau", "Cole", "St. Francois", "Newton", "Lincoln", "Taney", "Johnson", "Pulaski", "Camden", "Callaway", "Phelps", "Butler", "Pettis", "Howell", "Webster", "Scott", "Lawrence", "Laclede", "Barry", "Warren", "Lafayette", "Polk", "Stone", "Dunklin", "Stoddard", "Marion", "Audrain", "Texas", "Adair", "Miller", "Randolph", "Washington", "Crawford", "Saline", "Ray", "McDonald", "Nodaway", "Henry", "Vernon", "Clinton", "Morgan", "Perry", "Benton", "Pike", "Wright", "Ste. Genevieve", "Cooper", "New Madrid", "Andrew", "Pemiscot", "Dallas", "Bates", "Moniteau", "Dent", "Macon", "Livingston", "Gasconade", "Cedar", "Osage", "Mississippi", "Ripley", "Douglas", "Wayne", "DeKalb", "Bollinger", "Madison", "Linn", "Barton", "Montgomery", "Oregon", "Ralls", "Iron", "Howard", "Grundy", "Lewis", "Hickory", "St. Clair", "Ozark", "Caldwell", "Maries", "Carroll", "Monroe", "Harrison", "Daviess", "Shannon", "Dade", "Chariton", "Clark", "Gentry", "Reynolds", "Sullivan", "Carter", "Shelby", "Atchison", "Scotland", "Putnam", "Schuyler", "Holt", "Knox", "Mercer", "Worth"],
                    "North Dakota": ["Cass", "Burleigh", "Grand Forks", "Ward", "Williams", "Stark", "Morton", "Stutsman", "Richland", "Rolette", "McKenzie", "Ramsey", "Walsh", "Barnes", "Mountrail", "McLean", "Mercer", "Traill", "Pembina", "Benson", "Bottineau", "McHenry", "Ransom", "Dickey", "Dunn", "Sioux", "Pierce", "LaMoure", "Wells", "Sargent", "Cavalier", "Emmons", "Foster", "Bowman", "Nelson", "McIntosh", "Hettinger", "Kidder", "Renville", "Griggs", "Grant", "Divide", "Adams", "Eddy", "Towner", "Burke", "Logan", "Golden Valley", "Oliver", "Steele", "Sheridan", "Billings", "Slope"],
                    "Ohio": ["Franklin", "Cuyahoga", "Hamilton", "Summit", "Montgomery", "Lucas", "Butler", "Stark", "Lorain", "Mahoning", "Lake", "Warren", "Clermont", "Delaware", "Trumbull", "Medina", "Licking", "Greene", "Portage", "Fairfield", "Clark", "Wood", "Richland", "Wayne", "Miami", "Columbiana", "Allen", "Ashtabula", "Geauga", "Tuscarawas", "Muskingum", "Ross", "Scioto", "Hancock", "Erie", "Belmont", "Jefferson", "Athens", "Marion", "Knox", "Washington", "Lawrence", "Sandusky", "Huron", "Pickaway", "Union", "Seneca", "Ashland", "Darke", "Shelby", "Auglaize", "Logan", "Madison", "Holmes", "Brown", "Highland", "Fulton", "Clinton", "Crawford", "Preble", "Mercer", "Ottawa", "Guernsey", "Champaign", "Defiance", "Williams", "Coshocton", "Perry", "Morrow", "Putnam", "Jackson", "Hardin", "Gallia", "Fayette", "Hocking", "Van Wert", "Pike", "Adams", "Carroll", "Henry", "Meigs", "Wyandot", "Paulding", "Harrison", "Morgan", "Noble", "Monroe", "Vinton"],
                    "South Dakota": ["Minnehaha", "Pennington", "Lincoln", "Brown", "Brookings", "Codington", "Meade", "Lawrence", "Yankton", "Davison", "Beadle", "Hughes", "Union", "Oglala Lakota", "Clay", "Lake", "Roberts", "Butte", "Todd", "Charles Mix", "Custer", "Turner", "Hutchinson", "Grant", "Bon Homme", "Fall River", "Moody", "Spink", "Hamlin", "Dewey", "McCook", "Day", "Tripp", "Walworth", "Brule", "Kingsbury", "Marshall", "Deuel", "Gregory", "Corson", "Edmunds", "Lyman", "Clark", "Bennett", "Hanson", "Jackson", "Hand", "Stanley", "Douglas", "Perkins", "Ziebach", "Aurora", "Sanborn", "Potter", "Faulk", "McPherson", "Miner", "Mellette", "Buffalo", "Haakon", "Jerauld", "Campbell", "Hyde", "Harding", "Sully", "Jones"],
                    "Wisconsin": ["Milwaukee", "Dane", "Waukesha", "Brown", "Racine", "Outagamie", "Winnebago", "Kenosha", "Rock", "Marathon", "Washington", "La Crosse", "Sheboygan", "Eau Claire", "Walworth", "Fond du Lac", "St. Croix", "Ozaukee", "Dodge", "Jefferson", "Manitowoc", "Wood", "Portage", "Sauk", "Chippewa", "Columbia", "Grant", "Waupaca", "Calumet", "Monroe", "Barron", "Dunn", "Polk", "Douglas", "Pierce", "Shawano", "Marinette", "Oconto", "Green", "Oneida", "Clark", "Vernon", "Trempealeau", "Lincoln", "Door", "Juneau", "Waushara", "Iowa", "Vilas", "Jackson", "Kewaunee", "Taylor", "Adams", "Langlade", "Green Lake", "Richland", "Lafayette", "Sawyer", "Crawford", "Washburn", "Ashland", "Marquette", "Burnett", "Bayfield", "Rusk", "Price", "Buffalo", "Forest", "Pepin", "Iron", "Menominee", "Florence"]
}



### FUNCTION FOR INPUTTING PARAMETERS - THIS SENDKEYS INPUT AND READS OUTPUT FOR PARAMS
def input_parameters(state_name, county_name, crop_name):

    state_input = web.find_element(By.ID, 'react-select-2-input')
    state_displayed = web.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div/div[1]/div[1]')
    if state_displayed.text != state_name:                                      #does attribute 'text' always exist?
        state_input.send_keys(state_name)
        state_input.send_keys("\ue006")
        time.sleep(6)

    crop_input = web.find_element(By.ID, 'react-select-4-input')
    crop_displayed = web.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div/div/div/div[1]/div[1]')
    if crop_displayed.text != crop_name:
        crop_input.send_keys(crop_name)
        time.sleep(0.2)
        crop_input.send_keys("\ue006")


    county_input = web.find_element(By.ID, 'react-select-3-input')
    county_input.send_keys(county_name)                                                 #idk if this is necessary. Some nasty bugs possibly here
    county_input.send_keys("\ue006")
    time.sleep(2)
    button_input = web.find_element(By.CSS_SELECTOR, '.MuiButton-label')
    
    #web.execute_script('arguments[0].click();', button_input)
    

    table = 0
    button_input.click()
    
    table = web.find_elements(By.CSS_SELECTOR, ".MuiTable-root") #Changed from XPATH

    #Get autocompleted data, place in list , return as second element of tuple

    have_adjustment = web.find_element(By.ID, "useTaAdj").text
    ta_yield = web.find_element(By.ID, 'taYield').get_attribute('value')
    aph_yield = web.find_element(By.ID, 'aphYield').get_attribute('value')
    rate_yield = web.find_element(By.ID, 'rateYield').get_attribute('value')
    grain_type = web.find_element(By.ID, 'grainType').text
    practice = web.find_element(By.ID, 'practiceType').text
    risk_class = web.find_element(By.ID, 'riskClass').text
    pplanting = web.find_element(By.ID, 'preventedPlanting').text
    acres = web.find_element(By.ID, 'farmAcres').get_attribute('value')
    projected_price = web.find_element(By.ID, 'projectedPrice').get_attribute('value')
    volatility_factor = web.find_element(By.ID, 'volFactor').get_attribute('value')


    autocompleted = [have_adjustment, ta_yield, aph_yield, rate_yield, grain_type, practice, risk_class, pplanting, acres, projected_price, volatility_factor]
    return (table, autocompleted)

#output_table = input_parameters(current_state, current_county, current_crop)


#CREATE HEADER ROW
param_titles = ["State", "County", "Crop"]
autocomplete_titles = ["TA/YE Adjustment Used", "TA Yield (bu/acre)", "APH Yield (bu/acre)", "Rate Yield (bu/acre)", "Type", "Practice", "Risk Class", "Prevented Planting", "Acres", "Projected Price ($)", "Volatility Factor"]
rows_list_1_1 = ["Revenue Protection", "Revenue Protection With Harvest Price Exclusion", "Yield Protection"]
rows_list_1_2 = ["Enterprise", "Basic", "Optional", "Min. Revenue Guarantee", "Enterprise", "Basic", "Optional", "Revenue Guarantee", "Enterprise", "Basic", "Optional", "Yield Guarantee (bu/acre)"]
rows_list_2_1 = ["Coverage Level"]
rows_list_2_2 = ["50%", "55%", "60%", "65%", "70%", "75%", "80%", "85%"]                                            #I thought this list went to 100% for some reason?
rows_list_1 = [rows_list_1_1[i//4] +": "+ rows_list_1_2[i] for i in range(len(rows_list_1_2))]
rows_list_2 = [rows_list_2_1[0] + ": " + rows_list_2_2[i] for i in range(len(rows_list_2_2))]
newlength = (len(rows_list_1))*(len(rows_list_2))
columns_list = param_titles + autocomplete_titles + [rows_list_1[i%len(rows_list_1)] + ", " + rows_list_2[i//len(rows_list_1)] for i in range(newlength)]





#LOOP OVER DATA AND WRITE TO CSV FILE

with open('CORN_INDIVIDUAL_FARMLEVEL_PREMIUMS.csv', 'w', newline = '') as csvfile:
    wr = csv.writer(csvfile)
    wr.writerow(columns_list)


    #LOOP NOW CONFIG FOR IOWA ONLY
    for state in states_list:
        for county in counties_list[state]:   
            output_table = input_parameters(state, county, "Soybeans")
            if output_table[0]:
                wr.writerow([state, county, "Soybeans"] + output_table[1] + [d.text for d in output_table[0][0].find_elements(By.CSS_SELECTOR, 'td') if (d.text[len(d.text)-1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])])

    
    #for row in output_table.find_elements(By.CSS_SELECTOR, 'tr'):
        #wr.writerow([d.text for d in row.find_elements(By.CSS_SELECTOR, 'td')])


