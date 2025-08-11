# Name : Siarhei Hancharou
# Assignment #: 5
# Submission Date : 11/08/2020
#
# Program "President Candidate vs House Member Winners.":
# ("2000", 'Maryland') 4 republican, 4 democrat, house_dict.

from pathlib import Path
import A05ClassPrH


def _open_data(name: str):
  base = Path(__file__).resolve().parent
  path = base / name
  return path.open("r", encoding="utf-8", errors="ignore")

def main():
  print("-----------------------------------------------------------")
  print("To create a dictionary 'house_dict', \n"
        "call the function: house_dict = create_house_dict()")
  print("To create a dictionary 'president_dict',\n"
        "call the function: president_dict = create_president_dict()")
  print("-----------------------------------------------------------")
  print("The following functions are available for\n"
        "working with created dictionaries.")
  print("-----------------------------------------------------------")
  print("def process_president_data(president_dict)")
  print("def process_house_data(house_dict)")
  print("def state_breakdown(house_dict)")
  print("def compute_electoral_votes(house_dict)")
  print("def presidential_winner\n"
        "(president_dict, compute_electoral_votes(house_dict))")
  print("------------------------------------------------------------")
  house_dict = create_house_dict()
  president_dict = create_president_dict()
  w = process_president_data(president_dict)
  state_wins_by_party = state_breakdown(house_dict)

  while True:
    print("*********************************************")
    print("President Candidate vs House Member Winners.")
    print("**********************************************")
    print()
    print("To exit.....enter 'quit'.")
    # We make a set of years and States so that in the future,
    # if you enter the wrong year or state, you can tell the user the
    # available options.
    years = set()
    # We skip this key / value in the dictionary
    # and don't add it to hints.
    for i in president_dict:
      if i == tuple(["year", "state"]):
        continue
      years.add(i[0])

    print("Enter the election", end=" ")
    query_year = input("year:\n")
    if query_year == 'quit':
      break

    while query_year not in years:
      print(years)
      print("Select an electoral year.")
      print("Enter the election", end=" ")
      query_year = input("year:\n")
      if query_year in years:
        break

    if query_year == 'quit':
      break

    majority_dict = {}
    for i in state_wins_by_party:
      if i[0] == int(query_year):
        majority = 0
        majority_value_list = []
        for j in state_wins_by_party[i]:
          if state_wins_by_party[i][j] > majority:
            majority = state_wins_by_party[i][j]
            majority_value_list = [j]

        majority_dict.update({i: majority_value_list})

    election_results = {}
    for i in w:
      if i[0] == int(query_year):
        if i == tuple([int(query_year), 'District of Columbia']):
          continue
        # Comparing the parties.
        if w[i][1] != majority_dict[i][0].lower():
          election_results.update({i: [tuple([i[0]]) +
                                       w[i] +
                                       tuple([i[1]]) +
                                       tuple([majority_dict[i][
                                                0].lower()])]})

    print("*************************************************"
          "************************************************")
    print('{:5} {:19} {:19} {:15} {:30}'.
          format("Year", "Candidate", "Candidate Party",
                 "State", "Majority of Representatives Elected"))
    print("*************************************************"
          "************************************************")
    for i in election_results:
      for j in election_results[i]:
        print('{:5} {:20} {:19} {:15} {:15}'.
              format(j[0], j[1], j[2], j[5], j[6]))

    print("*************************************************"
          "************************************************")
    print()


# The function opens the "house. tab" file, reads it,
# and returns a dictionary where the key is a tuple(year, state),
# and the value is a list of objects.
def create_house_dict():

  content_list_house_dirty = []
  with _open_data("house.tab") as f:
    content = f.readlines()

  # Read the content and divide it by tab.
  for i in content:
    content_list_house_dirty.append(i.split("\t"))

  # Clearing the list of special characters.
  content_list_house = []
  for i in content_list_house_dirty:
    n = []
    for j in i:
      n.append(j.rstrip())
    content_list_house.append(n)

  # Compare the list by the first two elements year and state.
  # Creating a list with nested lists of the same year.
  similar_unit_for_dic = []
  # Checking the last element.
  for ch in range(len(content_list_house)):
    if ch == len(content_list_house) - 1:
      if content_list_house[ch][:2] == \
        content_list_house[ch - 1][:2]:
        similar_unit_for_dic[-1] = similar_unit_for_dic[-1] + \
                                   [content_list_house[ch]]

    elif content_list_house[ch][:2] == \
      content_list_house[ch - 1][:2]:
      similar_unit_for_dic[-1] = similar_unit_for_dic[-1] + \
                                 [content_list_house[ch]]

    else:
      similar_unit_for_dic.append([content_list_house[ch]])

  # Creating a dictionary in which the tuple (year and state) is the key,
  # and the list with nested objects will be the value.
  house_dict = {}
  for i in similar_unit_for_dic:
    key = tuple([i[0][0], i[0][1]])
    value = []

    for ch in i:
      # Class attribute(year, state, state_po, state_fips,
      # state_cen, state_ic, office, district, stage,
      # special, runoff, candidate, party, writein, mode,
      # candidatevotes, totalvotes, unofficial, version)
      value.append(A05ClassPrH.House(ch[0], ch[1], ch[2],
                                     ch[3], ch[4], ch[5],
                                     ch[6], ch[7], ch[8],
                                     ch[9], ch[10], ch[11],
                                     ch[12], ch[13], ch[14],
                                     ch[15], ch[16], ch[17],
                                     ch[18]))

    # In the read house. tab, 8 lines were scattered, and this
    # cycle  was added to correctly collect all the data
    # for a certain year and state.
    if key in house_dict:
      house_dict[key] = house_dict[key] + value
      continue

    house_dict[key] = value

  return house_dict


# The function opens the "president.tab" file, reads it,
# and returns a dictionary where the key is a tuple(year, state),
# and the value is a list of objects.
def create_president_dict():

  content_list_president_dirty = []
  with _open_data("president.tab") as f: content = f.readlines()

  # Read the content and divide it by tab.
  for i in content:
    content_list_president_dirty.append(i.split("\t"))

  # Clearing the list of special characters.
  list_president = []
  for i in content_list_president_dirty:
    i.pop(-1)
    temp = []
    for j in i:
      temp.append(j.rstrip())
    list_president.append(temp)

  # Small changes in the data and too long names
  # of the candidates also had to shorten the name of the party.
  content_list_president = []
  for i in list_president:
    t_in = []
    for j in i:
      if len(i[8]) > 20:
        n = j[:20]
        t_in.append(n)
      # To better display the data for all empty spaces
      # in the list to be signed as there is "No data".
      # Rather, it was an attempt, but there were many such names.
      # I'll just display a cropped line.
      elif j == "":
        j = "No data"
        t_in.append(j)

      else:
        t_in.append(j)
    content_list_president.append(t_in)

  similar_unit_for_list = []

  for ch in range(len(content_list_president)):
    # Checking the last element.
    if ch == len(content_list_president) - 1:
      # if this object is equal to the previous one add
      # in previous list, if then different the new
      # dictionary object is different.
      if content_list_president[ch][:2] == \
        content_list_president[ch - 1][:2]:
        similar_unit_for_list[-1] = similar_unit_for_list[-1] + \
                                    [content_list_president[ch]]

    elif content_list_president[ch][:2] == \
      content_list_president[ch - 1][:2]:
      similar_unit_for_list[-1] = similar_unit_for_list[-1] + \
                                  [content_list_president[ch]]

    else:
      similar_unit_for_list.append([content_list_president[ch]])

  # Creating a dictionary in which the tuple (year and state) is the key,
  # and the list with nested objects will be the value.
  president_dict = {}
  for i in similar_unit_for_list:

    key = tuple([i[0][0], i[0][1]])
    value = []
    for ch in i:
      # Class attribute(year, state, state_po, state_fips, state_cen,
      # state_ic, office, candidate, party, writein, candidatevotes,
      # totalvotes, version, notes)
      value.append(A05ClassPrH.President(ch[0], ch[1], ch[2],
                                         ch[3], ch[4], ch[5],
                                         ch[6], ch[7], ch[8],
                                         ch[9], ch[10], ch[11],
                                         ch[12], ch[13]))

    # president_dict[key] = value
    # In the read house. tab, 8 lines were scattered, and this
    # cycle  was added to correctly collect all the data
    # for a certain year and state.
    if key in president_dict:
      president_dict[key] = president_dict[key] + value
      continue

    president_dict[key] = value

  return president_dict


#  The function accepts  dictionary where the key is a tuple(year, state),
#  and the value is a list of objects, returns a dictionary with the
#  requested data where key tuple(year, state),  and the value is
#  a list  [candidate, party, candidatevotes, totalvotes]
def process_president_data(president_dict):
  # We make a set of years and States so that in the future,
  # if you enter the wrong year or state, you can tell
  # the user the available options.
  key = set()
  # We skip this key / value in the dictionary
  # and don't add it to hints.
  for i in president_dict:
    if i == tuple(["year", "state"]):
      continue
    key.add(i)

  # Making a dictionary that is returned by
  # the function according to the problem condition.
  president_dictionary_return_all = {}
  for i in key:
    max_votes = 0
    president_dictionary = {}
    president_dictionary_temp = {}
    for k in president_dict[i]:
      if int(k.get_candidatevotes()) > int(max_votes):
        max_votes = k.get_candidatevotes()
        president_dictionary[k] = str(max_votes)
        president_dictionary_temp[tuple([int(k.get_year()),
                                         k.get_state()])] = \
          (k.get_candidate(),
           k.get_party(),
           k.get_candidatevotes(),
           k.get_totalvotes())

    president_dictionary_return_all.update(president_dictionary_temp)

  return president_dictionary_return_all


# The function accepts a house_dict where the key is a tuple (year, state),
# and the value is a list of objects. The function returns dictionary that
# is returned by the function where the key is year, so and in it
# dictionaries in which the key is the winning district and the value of the
# winning candidate, his party and candidatevotes.
def process_house_data(house_dict):
  print()
  # Dictionary that is returned by function process_house_data(house_dict).
  house_dictionary_return_all = {}
  # We skip this key / value in the dictionary
  # and don't add it to hints.
  for keys in house_dict:
    if keys == tuple(["year", "state"]):
      continue

    district_temp = set()
    for key in house_dict[keys]:
      district_temp.add(key.get_district())

    # Run through the dictionary with the specified year and
    # state and create a new dictionary with the winners in each
    # district. Dictionary which the key will be the district number,
    # and the value will be a list with candidate, party, candidatevotes.
    district = 0

    house_dictionary_return = {}
    for i in range(len(district_temp) + 1):
      temp_votes = 0
      for key in house_dict[keys]:
        if int(key.get_district()) == district:
          if int(key.get_candidatevotes()) > temp_votes:
            temp_votes = int(key.get_candidatevotes())

            house_dictionary_return.update(
              {key.get_district(): [key.get_candidate(),
                                    key.get_party(),
                                    key.get_candidatevotes()]})

      district += 1

    keys = tuple([int(keys[0]), keys[1]])

    house_dictionary_return_all.update({keys: house_dictionary_return})

  # In the beginning, I made it so that the function returns
  # only the selected year and state. Then redid and returns
  # the dictionary with all the years.
  print("If you want to check the winner in \n"
        "a particular year and state .........enter 1.")
  print("If you skip this ....................enter 'any ch'")
  num = input("Enter num: \n")

  if num == '1':
    print()
    # We make a set of years and States so that in the future,
    # if you enter the wrong year or state, you can tell the user the
    # available options.
    years = set()
    states = set()
    # We skip this key / value in the dictionary
    # and don't add it to hints.
    for i in house_dict:
      if i == tuple(["year", "state"]):
        continue
      years.add(i[0])
      states.add(i[1])

    print("Enter the election ", end=" ")
    year = input("year:\n")

    if year not in years:
      while True:
        print(years)
        print("Enter the year starting from 1976 to 2016.")
        print("Enter the election ", end=" ")
        year = input("year:\n")
        if year in years:
          break

    print("Enter the ", end=" ")
    state = input("state:\n")
    if state not in states:
      while True:
        print(states)
        print("Enter one of the fifty States of America.")
        print("Enter the ", end=" ")
        state = input("state:\n")
        if state in states:
          break

    district_temp = set()
    for key in house_dict[tuple([year, state])]:
      district_temp.add(key.get_district())

    # Run through the dictionary with the specified year and
    # state and create a new dictionary with the winners in each
    # district. Dictionary which the key will be the district number,
    # and the value will be a list with candidate, party, candidatevotes.
    district = 0
    house_dictionary_return = {}
    for i in range(len(district_temp) + 1):
      temp_votes = 0
      for key in house_dict[tuple([year, state])]:
        if int(key.get_district()) == district:
          if int(key.get_candidatevotes()) > temp_votes:
            temp_votes = int(key.get_candidatevotes())
            house_dictionary_return.update({key.get_district(): [
              key.get_candidate(),
              key.get_party(),
              key.get_candidatevotes()]})

      district += 1

    # The user is offered two options for displaying
    # the processed information.
    print("To display data for all participants\n"
          "in each district...........................enter 1.")
    print("To display the winners in each district....enter 2.")
    num = int(input("Enter yours num: \n"))

    if num == 1:
      for key in house_dict[("year", "state")]:
        print(
          "---------------------------------------------------------"
          "-----")
        print("{:9} {:20} {:15} {:10}".format(key.get_district(),
                                              key.get_candidate()[:20],
                                              key.get_party(),
                                              key.get_candidatevotes()))
        print(
          "---------------------------------------------------------"
          "-----")
      for key in house_dict[tuple([year, state])]:
        print("{:9} {:20} {:15} {:10}".format(key.get_district(),
                                              key.get_candidate()[:20],
                                              key.get_party(),
                                              key.get_candidatevotes()))
      print("-----------------------------------------------------------"
            "---")

    if num == 2:
      for key in house_dict[("year", "state")]:
        print(
          "---------------------------------------------------------"
          "-----")
        print("{:9} {:20} {:15} {:10}".format(key.get_district(),
                                              key.get_candidate()[:20],
                                              key.get_party(),
                                              key.get_candidatevotes()))
        print(
          "---------------------------------------------------------"
          "-----")
      for key in house_dictionary_return:
        print("{:9} {:20} {:15} {:10}".
              format(key, house_dictionary_return[key][0][:20],
                     house_dictionary_return[key][1],
                     house_dictionary_return[key][2]))
      print("-----------------------------------------------------------"
            "---")

  return house_dictionary_return_all


# The function accepts a dictionary where the key is a tuple (year, state
# and the value is a list of objects. Returns a dictionary, the key is
# a tuple (year, state), and the value is a
# dictionary {'Republican': n, 'Democrat': n, 'Other': n}
# In addition, you can select and only see how much each party won
# over the years from 1979 to 2018, or only the selected year and state.
def state_breakdown(house_dict):
  print()
  # The main dictionary to which the processed data is
  # collected and returned by the function
  house_wins_by_party = {}
  # A sheet with keys that will be substituted in
  # the future in the loop to iterate through the elements.
  list_key = []
  for i in house_dict:
    if i == tuple(["year", "state"]):
      continue
    list_key.append(i)
  # I took the principle of searching for winners above,
  # but at the same time created a list of all years and
  # States (list_key), from which I took values and
  # substituted them into the loop.
  # Schematically, the dictionary will look like this
  # {("year", "state"): {"district": ('candidate', 'party', 'state',
  # 'candidatevotes'), "district2": ('candidate', 'party', 'state',
  # 'candidatevotes'}........{("year n", "state n"): {"district":
  # (candidate', 'party', 'state','candidatevotes'), ....."district n":
  # ('candidate', 'party', 'state', 'candidatevotes')}}

  # The temporary variable is reset to zero when moving
  # to the next item in the list.
  district = 0
  temp_max_votes = 0
  count_index = 0
  house_wins_by_party_temp = {}
  for i in range(len(list_key)):
    house_dictionary_with_wins = {}
    for j in house_dict[list_key[count_index]]:
      if int(j.get_district()) == int(district):
        if int(j.get_candidatevotes()) > int(temp_max_votes):
          temp_max_votes = int(j.get_candidatevotes())
          house_dictionary_with_wins. \
            update({j.get_district(): (j.get_candidate(),
                                       j.get_party(),
                                       j.get_state(),
                                       j.get_candidatevotes())})

      else:
        temp_max_votes = 0
        district = int(j.get_district())
        if int(j.get_district()) == district:
          if int(j.get_candidatevotes()) > int(temp_max_votes):
            temp_max_votes = int(j.get_candidatevotes())
            house_dictionary_with_wins. \
              update({j.get_district(): (j.get_candidate(),
                                         j.get_party(),
                                         j.get_state(),
                                         j.get_candidatevotes())})

    house_wins_by_party_temp.update({list_key[count_index]:
                                       house_dictionary_with_wins})
    count_index += 1
  # This loop iterates through the dictionary and counts the total
  # number of each party in a particular year and state
  for i in house_wins_by_party_temp:
    temp = {}
    democrat = 0
    republican = 0
    other = 0
    for j in house_wins_by_party_temp[i]:
      key = house_wins_by_party_temp[i][j][1]
      if key == "republican" or key == "re" or \
        key == "independent-republican":
        republican += 1

      elif key == "democrat" or key == "national democrat" or \
        key == "regular democracy" or key == "democratic-npl" or \
        key == "foglietta (democrat)":
        democrat += 1

      else:
        other += 1

    temp["Democrat"] = democrat
    temp["Republican"] = republican
    temp["Other"] = other
    # Changing the type of the null index in the key,
    # as specified in the task.
    i = tuple([int(i[0]), i[1]])

    house_wins_by_party.update({i: temp})

  # In the beginning, I made it so that the function only returned
  # the dictionary with the specified year and state, but in order
  # not to lose this, I added the function to view additional data
  # for the selected year or for all years.
  print("To display the total number of times\n"
        "each party won in the user's chosen\n"
        "year and state............................enter 1")
  print("To display the total number of wins\n"
        "each party won from 1979 to 2018..........enter 2")
  print("To skip ..................................enter 'any ch'.")
  num = input("Enter number:\n")

  if num == "1":
    house_win_year_state = {}
    # If user is selected num = 1 calculations are not performed
    # to speed up the function response.
    print()
    democrat = 0
    republican = 0
    other = 0

    # We make a set of years and States so that in the future,
    # if you enter the wrong year or state, you can tell the user the
    # available options.
    years = set()
    states = set()
    # We skip this key / value in the dictionary
    # and don't add it to hints.
    for i in house_dict:
      if i == tuple(["year", "state"]):
        continue
      years.add(i[0])
      states.add(i[1])

    print("Enter the election ", end=" ")
    year = input("year:\n")

    if year not in years:
      while True:
        print(years)
        print("Enter the year starting from 1976 to 2016.")
        print("Enter the election ", end=" ")
        year = input("year:\n")
        if year in years:
          break

    print("Enter the ", end=" ")
    state = input("state:\n")
    if state not in states:
      while True:
        print(states)
        print("Enter one of the fifty States of America.")
        print("Enter the ", end=" ")
        state = input("state:\n")
        if state in states:
          break

    district_temp = set()
    for key in house_dict[tuple([year, state])]:
      district_temp.add(key.get_district())
    # Dictionary house_dictionary_with_wings in which we add
    # dictionaries in which the key is the district,
    # the value of the winning party party
    house_dictionary_with_wins = {}
    for key in house_dict[tuple([year, state])]:
      district = 1
      for i in range(len(district_temp)):
        temp_votes = 0
        for key in house_dict[tuple([year, state])]:
          if int(key.get_district()) == district:
            if int(key.get_candidatevotes()) > temp_votes:
              temp_votes = int(key.get_candidatevotes())
              house_dictionary_with_wins. \
                update({key.get_district(): key.get_party()})

        district += 1
    # Running through the dictionary and count
    # the number of wins for each party.
    for key in house_dictionary_with_wins:
      if house_dictionary_with_wins[key] == "republican":
        republican += 1

      elif house_dictionary_with_wins[key] == "democrat":
        democrat += 1

      else:
        other += 1
    # A temporary dictionary that will then be the key
    # to the dictionary that is returned by the function.
    house_wins_by_party_temp = {}
    house_wins_by_party_temp["Republican"] = republican
    house_wins_by_party_temp["Democrat"] = democrat
    house_wins_by_party_temp["Other"] = other
    house_win_year_state[tuple([year, state])] = house_wins_by_party_temp

    for i in house_win_year_state:
      print(house_win_year_state[i])

  # Calculates party winners for all years.
  # I took the principle of searching for winners above,
  # but at the same time created a list of all years and States (list_key),
  # from which I took values and substituted them into the loop.
  if num == "2":
    print()
    list_key = []
    for i in house_dict:
      if i == tuple(["year", "state"]):
        continue
      list_key.append(i)
    # I took the principle of searching for winners above,
    # but at the same time created a list of all years and
    # States (list_key), from which I took values and
    # substituted them into the loop.
    # Schematically, the dictionary will look like this
    # {("year", "state"): {"district": ('candidate', 'party', 'state',
    # 'candidatevotes'), "district2": ('candidate', 'party', 'state',
    # 'candidatevotes'}........{("year n", "state n"): {"district":
    # (candidate', 'party', 'state','candidatevotes'), ....."district n":
    # ('candidate', 'party', 'state', 'candidatevotes')}}

    house_wins_by_party_all = {}
    district = 0
    temp_max_votes = 0
    count = 0
    for i in range(len(list_key)):
      house_dictionary_with_wins = {}
      for j in house_dict[list_key[count]]:
        if int(j.get_district()) == int(district):
          if int(j.get_candidatevotes()) > int(temp_max_votes):
            temp_max_votes = int(j.get_candidatevotes())
            house_dictionary_with_wins. \
              update({j.get_district(): (j.get_candidate(),
                                         j.get_party(),
                                         j.get_state(),
                                         j.get_candidatevotes())})

        else:
          temp_max_votes = 0
          district = int(j.get_district())
          if int(j.get_district()) == district:
            if int(j.get_candidatevotes()) > int(temp_max_votes):
              temp_max_votes = int(j.get_candidatevotes())
              house_dictionary_with_wins. \
                update({j.get_district(): (j.get_candidate(),
                                           j.get_party(),
                                           j.get_state(),
                                           j.get_candidatevotes())})

      house_wins_by_party_all.update({list_key[count]:
                                        house_dictionary_with_wins})
      count += 1

    total_all_years = {}
    democrat = 0
    republican = 0
    other = 0
    # We run through the dictionary and count the victories of each party.
    for i in house_wins_by_party_all:
      for j in (house_wins_by_party_all[i]):
        key = house_wins_by_party_all[i][j][1]
        if key == "republican" or key == "re" or \
          key == "independent-republican":
          republican += 1

        elif key == "democrat" or key == "national democrat" or \
          key == "regular democracy" or key == "democratic-npl" or \
          key == "foglietta (democrat)":
          democrat += 1
        else:
          other += 1

      total_all_years["Republican"] = republican
      total_all_years["Democrat"] = democrat
      total_all_years["Other"] = other

    print("In total, each party won from 1979 to 2018.")
    print(total_all_years)

  return house_wins_by_party


# The function accepts a dictionary where the key is a tuple (year, state),
# and the value is a list of objects. Returns a dictionary in which the
# key is tuple (year, state), and the value is the number of electoral
# votes. Additionally, you can display all electoral votes every (year, state)
# and their electoral_votes.
def compute_electoral_votes(house_dict):
  electoral_votes = {}
  for i in house_dict:
    if i == tuple(['year', 'state']):
      continue
    # We run through the dictionary with key tuple (year, state)
    # collect all the districts and put them in the set and then
    # take len (district) + 2 senators
    district = set()
    for key in house_dict[i]:
      district.add(key.get_district())
      i = tuple([int(i[0]), i[1]])
    electoral_votes[i] = len(district) + 2
    electoral_votes[i[0], "District of Columbia"] = 3

  print("Check the number of electors for\n"
        "a particular state....................enter 1.\n"
        "To display all electors in each\n"
        "year and state........................enter 2.\n"
        "To skip...............................enter 'any ch'.")

  num = input("Enter num: ")
  # Displaying data for the selected year
  if num == "1":
    print("Enter an electoral year and state.")
    # We make a set of years and States so that in the future,
    # if you enter the wrong year or state, you can tell the user the
    # available options.
    years = set()
    states = set()
    # We skip this key / value in the dictionary
    # and don't add it to hints.
    for i in house_dict:
      if i == tuple(["year", "state"]):
        continue
      years.add(i[0])
      states.add(i[1])

    print("Enter the election ", end=" ")
    year = input("year:\n")

    if year not in years:
      while True:
        print(years)
        print("Enter the year starting from 1976 to 2016.")
        print("Enter the election ", end=" ")
        year = input("year:\n")
        if year in years:
          break

    print("Enter the ", end=" ")
    state = input("state:\n")
    if state == "District of Columbia":
      print("****Note****")
      print("     Under the 23rd Amendment of the Constitution,\n"
            "the District of Columbia is allocated three\n"
            "electors and treated like a State for purposes\n"
            "of the Electoral College.")

    if state not in states:
      while True:
        print(states)
        print("Enter one of the fifty States of America.")
        print("Enter the ", end=" ")
        state = input("state:\n")
        if state in states:
          break

    # We run through the dictionary with key tuple (year, state)
    # collect all the districts and put them in the set and then
    # take len (district) + 2 senators
    district = set()
    electoral_votes_y_s = {}
    for key in house_dict[tuple([year, state])]:
      district.add(key.get_district())

    electoral_votes_y_s[tuple([year, state])] = len(district) + 2
    for i in electoral_votes_y_s:
      print(electoral_votes_y_s[i])

  # Displaying data from the entire dictionary to the user.
  if num == "2":
    for i in electoral_votes:
      print(i, electoral_votes[i])

  return electoral_votes


# Accepts the dictionary president_dict and returned by the compute_electoral_
# votes(house_dict) function. Returns the dictionary. in which the key is
# the year, the value of the candidate's name, party, and the number of votes.
def presidential_winner(president_dict, electoral_votes):
  list_key = []
  for i in president_dict:
    if i == tuple(["year", "state"]):
      continue
    list_key.append(i)

  president_dictionary_with_wins = {}
  count = 0
  for i in range(len(list_key)):
    temp_max_votes = 0
    for j in president_dict[list_key[i]]:
      if tuple(list_key[i]) == tuple([j.get_year(), j.get_state()]):
        if int(j.get_candidatevotes()) > int(temp_max_votes):
          count += 1
          temp_max_votes = int(j.get_candidatevotes())
          president_dictionary_with_wins.update({
            tuple([int(j.get_year()), j.get_state()]): [
              j.get_year(),
              j.get_candidate(),
              j.get_party(),
              j.get_state(),
              j.get_candidatevotes()]})

  for i in president_dictionary_with_wins:
    president_dictionary_with_wins[i].append(electoral_votes[i])

  electoral_votes_of_winner_temp = {}
  electoral_votes_of_winner = {}
  count = 0

  years = set()
  for i in president_dictionary_with_wins:
    years.add(i[0])

  for year in years:
    democrat_votes = 0
    republican_votes = 0
    candidate_a = ""
    candidate_b = ""
    for i in president_dictionary_with_wins:
      if i[0] == year:
        count += 1
        if president_dictionary_with_wins[i][2] == "democrat":
          candidate_a = president_dictionary_with_wins[i][1]
          democrat_votes += president_dictionary_with_wins[i][-1]

        if president_dictionary_with_wins[i][2] == "republican":
          candidate_b = president_dictionary_with_wins[i][1]
          republican_votes += president_dictionary_with_wins[i][-1]

        if president_dictionary_with_wins[i][1] == candidate_a:
          if democrat_votes > republican_votes and democrat_votes >= 270:
            electoral_votes_of_winner_temp.update({int(i[0]): [
              president_dictionary_with_wins[i][1],
              president_dictionary_with_wins[i][2],
              democrat_votes]})

        if president_dictionary_with_wins[i][1] == candidate_b:
          if republican_votes > democrat_votes and republican_votes >= 270:
            electoral_votes_of_winner_temp.update({int(i[0]): [
              president_dictionary_with_wins[i][1],
              president_dictionary_with_wins[i][2],
              republican_votes]})

    electoral_votes_of_winner.update(electoral_votes_of_winner_temp)

  return electoral_votes_of_winner


main()
