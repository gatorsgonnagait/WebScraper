from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


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
#rankings = 'http://gmbassett.nfshost.com/football/col_17wk01pred.html'
rankings = open('/home/gatorsgonnagait/PycharmProjects/WebScraper/testFile')
#rankings = open('/home/gatorsgonnagait/PycharmProjects/WebScraper/test', 'r')
def getRanking(link):

    #print(rankings.read())

    html = link.read()

    # with urllib.request.urlopen(rankings) as response:
    #    html = response.read()

    #print(html)
    soup = BeautifulSoup(html, "html.parser")

    #print(soup.get_text())

    team_ranks_df = pd.DataFrame(columns=[' Week', ' Favorite',' Favorite Rank', ' Underdog', ' Underdog Rank', ' Fav Expected Score', ' Dog Expected Score'])
    #date_df = pd.DataFrame(index=[], columns=[])
    #date = ''
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
                # elif strType(string) == 'str':
                #     date = date + ' ' + string
                elif string.isdigit() and int(string) < 20:
                    week = string
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

team_ranks_df = getRanking(rankings)
print(team_ranks_df)
team_ranks_df.to_excel('weekly_power_rankings.xlsx')