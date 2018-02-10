from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re

def strType(var):
    try:
        if int(var) == float(var):
            return 'int'
    except:
        try:
            float(var)
            return 'float'
        except:
            return 'str'

def getRanking(link):

    #print(rankings.read())

    #html2 = link.read()

    with urllib.request.urlopen(link) as response:
       html2 = response.read()

    #print(html)
    soup = BeautifulSoup(html2, "html.parser")

    #print(soup.get_text())

    team_ranks_df = pd.DataFrame(columns=[' Week', ' Favorite',' Favorite Rank', ' Underdog', ' Underdog Rank', ' Fav Expected Score', ' Dog Expected Score'])
    #date_df = pd.DataFrame(index=[], columns=[])
    year = ''
    week = ''
    line_num = 0
    for line in soup.get_text().split("\n"):

        #print(line)
        #game_line = pd.Series()
        game_line = []

        if line_num == 2:
            # get date somehow
            # 2017-08-26
            # should be in this format or say week 1

            print(line)

            for string in line.split(' '):
                if string.isdigit() and int(string) > 20:
                    year = string

                elif string.isdigit() and int(string) < 20:
                    week = string
                    print(week)
                    break
                elif string == 'Bowl' or string == 'FBS':
                    week = link[46:48]
                    break



            #date_df = pd.DataFrame({' Date' : date}, index=[0])
            #team_ranks_df = team_ranks_df.append(date_df)
        if line_num > 10:
            team_1 = ''
            team_2 = ''
            team_1_rank = ''
            team_2_rank = ''

            found_team_1 = True
            found_team_2 = False

            expected_score = []
            for string in line.split(' '):

                #print(string)
                if string.isdigit() and found_team_1:

                    game_line.append(string)
                    found_team_1 = True
                    team_1_rank = string

                    #print(team_1_rank)
                                                                                # checks if string is not empty
                elif not string.isdigit() and found_team_1 and string != 'over' and string:

                    team_1 = team_1 +' '+ string
                    #print(team_1)

                elif string == 'over':
                    found_team_1 = False
                    found_team_2 = True

                elif string.isdigit() and found_team_2:
                    team_2_rank = string
                    #print(team_2_rank)

                elif not string.isdigit() and found_team_2 and strType(string) != 'float' and string and string != 'to':
                    team_2 = team_2 +' '+ string
                    #print(team_2)

                elif strType(string) == 'float':
                    #print(string)
                    expected_score.append(string)

            # checks if data is valid
            if len(expected_score) == 2:
                #game_list=[[team_1[1:],team_1_rank, team_2[1:], team_2_rank, expected_score[0], expected_score[1] ]]
                game_frame = pd.DataFrame({' Week': week, ' Favorite' : team_1[1:], ' Favorite Rank' : team_1_rank, ' Underdog': team_2[1:],
                        ' Underdog Rank': team_2_rank, ' Fav Expected Score' : expected_score[0], ' Dog Expected Score' : expected_score[1]}, index=[year])

                #print(game_frame)
                #game_frame = pd.concat([date_df, game_frame], axis=1)
                team_ranks_df = team_ranks_df.append(game_frame)[list(team_ranks_df)]
                print()
                print(team_1[1:])
                print(team_1_rank)

                print(team_2[1:])

                print(team_2_rank)
                print(expected_score)

                print()
                print()

        line_num += 1


    return team_ranks_df


webPage = open('/home/gatorsgonnagait/PycharmProjects/WebScraper/homePage')

html = webPage.read()

soup = BeautifulSoup(html, "html.parser")
# print(soup.find_all('li'))

links_2017 = []
links_seasons = []
season_2017_df = pd.DataFrame()

for line in soup.find_all('a', attrs={'href' : re.compile('col')}):
    #print(line.get('href'))
    link = line.get('href')
    #print(link[10:14])
    if link[10:14] == 'pred':
        #print(link)
        links_2017.append(link)
    elif len(link) == 11:
        #print(link)
        links_seasons.append(link)


for link in links_2017:
    print(link)
    link2 = 'http://gmbassett.nfshost.com/football/'+link
    week_df = getRanking(link2)
    season_df = season_2017_df.append(week_df)

season_2017_df.to_excel('2017_power_rankings.xlsx')



# reverses list and starts at 2006

for season in reversed(links_seasons[:11]):
    print(season)
    link = 'http://gmbassett.nfshost.com/football/' + season
    with urllib.request.urlopen(link) as response:
       html2 = response.read()

    soup = BeautifulSoup(html2, "html.parser")

    links_weekly = []

    for line in soup.find_all('a', attrs={'href': re.compile('col')}):
        # print(line.get('href'))
        link = line.get('href')
        # print(link[10:14])
        if link[10:14] == 'pred':
            # print(link)
            links_weekly.append(link)

    season_current_df = pd.DataFrame()
    year = links_weekly[0][4:6]
    print(year)
    for link in links_weekly:
        link2 = 'http://gmbassett.nfshost.com/football/' + link
        week_df = getRanking(link2)
        season_current_df = season_current_df.append(week_df)

    print(season_current_df)
    season_current_df.to_excel('20'+year+'_power_rankings.xlsx')