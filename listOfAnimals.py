import requests
from bs4 import BeautifulSoup


url = 'https://en.wikipedia.org/wiki/List_of_animal_names'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find and scrape tables from wikipedia
tables = soup.findAll('table', {'class': 'wikitable'})
table = tables[1] # Choose the big table

clean_data = [] # Will be filled with list of rows 

# Loop through each row in the table
for row in table.find_all('tr'):
    cells = row.find_all('td') # Get cells
    cell_contents = [cell.get_text(strip=False) for cell in cells] # Get cell contents

    # Workaround for multiple words in a cell become one word (e.g. cell that contains "hippotigrine" and "zebrine" become "hippotigrinezebrine")
    word_lists = [] # List of words per cell
    # Iterate cells
    for cell in cells:
        words = [word.strip() for word in cell.stripped_strings]
        word_lists.append(words)

    # Add clean data to list 
    clean_data.append(word_lists)

AnimalsDict = {} # Dictionary for collaterals and the animals belonging to it

for row in clean_data: # Iterate through clean data and add the animal to the relevant collaterls
    if len(row) > 5: 
            collaterals = row[5] # The collaterals
            name = row[0][0] # The animle name
            if len(collaterals) > 0 and collaterals[0] != '?':  # Validate collateral exist and its not '?'
                for collateral in collaterals: # Iterate through collaterals
                    if collateral not in AnimalsDict: # Create the collateral key in the  dict if not exist
                        AnimalsDict[collateral] = [] # Create empty list per collateral - will be inserted with animals names
                    AnimalsDict[collateral].append(name) # Append the relevant list with animal name


# Start html structure
html_data = """
<style>
table,th,td,tr {border: 1px solid black; border-collapse: collapse;text-align: center;}
</style>
<table>
  <tr>
    <th>Collateral</th>
    <th>Animals</th>
  </tr>
"""
# Iterate dict and  build html
for key in AnimalsDict:
    html_data+="<tr><td>"+key+"</td><td>" 
    html_data+=','.join(AnimalsDict[key])+"</td></tr>"
html_data+="</table>"

# Write html data to file
file = open("web.html", "w")
file.write(html_data)
file.close()



    
