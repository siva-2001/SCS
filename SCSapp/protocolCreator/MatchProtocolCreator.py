from fpdf import FPDF
import os
import configparser
from pathlib import Path

class PDFProtocolCreator():
    def __init__(self):
        self.pdf = FPDF('P', 'mm', 'A4')
        self.pdf.add_page()
        self.pdf.add_font('DejaVu', '', Path(__file__).parent.joinpath("DejaVuSansCondensed.ttf"), uni=True)
        self.pdf.set_font('DejaVu', size=10)

    def printProtocolTitle(self, competitionName):
        self.pdf.cell(0, 8, align='C', txt="ПРОТОКОЛ №", border=False)
        self.pdf.ln(8)
        self.pdf.cell(0, 8, align='C', txt=competitionName, border=False)
        self.pdf.ln(8)
        self.pdf.cell(0, 8, align='C', txt="Матча по воллейболу", border=False, ln=1)

    def printMatchData(self, place, time, date):
        self.pdf.cell(50, 8, txt="Место проведения:", border=False)
        self.pdf.cell(0, 8, txt=place, border='B', ln=1)
        self.pdf.cell(20, 8, txt="Время:", border=False)
        self.pdf.cell(60, 8, txt=time, border='B')
        self.pdf.cell(20, 8, txt="Дата:", border=False)
        self.pdf.cell(0, 8, txt=date, border='B')
        self.pdf.ln(12)
        self.pdf.cell(0, 8, txt="среди муж./жен./смеш. команд")
        self.pdf.ln(12)

    def printTeamTitle(self, firstTeam, secondTeam):
        self.pdf.cell(30, 8, txt="Команда А", border=False)
        self.pdf.cell(70, 8, txt=firstTeam, border='B')
        self.pdf.cell(30, 8, txt="Команда Б", border=False)
        self.pdf.cell(0, 8, txt=secondTeam, border='B')
        self.pdf.ln(12)
        self.pdf.cell(100, 8, txt="Состав команды (А)", border=False)
        self.pdf.cell(0, 8, txt="Состав команды (Б)", border=False)
        self.pdf.ln(12)

    def printListsOfPlayers(self, firstTeamPlayerList, secondTeamPlayerList):
        self.pdf.cell(20, 8, txt='№ п/п', border=1)
        self.pdf.cell(70, 8, txt='ФИО игрока', border=1)
        self.pdf.cell(10, 8, txt='', border=False)
        self.pdf.cell(20, 8, txt='№ п/п', border=1)
        self.pdf.cell(70, 8, txt='ФИО игрока', border=1)
        self.pdf.ln(8)

        for row in range(1, 13):
            self.pdf.cell(20, 8, txt=str(row), border=1)
            if (len(firstTeamPlayerList) > row-1):
                if (len(firstTeamPlayerList[row-1]) > 35):
                    self.pdf.set_font_size(5)
                self.pdf.cell(70, 8, txt=firstTeamPlayerList[row-1], border=1)
                self.pdf.set_font_size(10)
            else:
                self.pdf.cell(70, 8, txt="", border=1)

            self.pdf.cell(10, 8, txt='', border=False)
            self.pdf.cell(20, 8, txt=str(row), border=1)
            if (len(secondTeamPlayerList) > row - 1):
                if (len(secondTeamPlayerList[row-1]) > 35):
                    self.pdf.set_font_size(5)
                self.pdf.cell(70, 8, txt=secondTeamPlayerList[row-1], border=1)
                self.pdf.set_font_size(10)
            else:
                self.pdf.cell(70, 8, txt="", border=1)

            self.pdf.ln(8)

    def printRoundsScore(self, firstTeam, secondTeam):
        for i in range(len(firstTeam['roundsScore'])):
            self.pdf.cell(40, 8, txt="Счёт " + str(i+1) + " партии", border=False)
            self.pdf.cell(50, 8, txt=str(firstTeam["roundsScore"][i]) + ' : ' + str(secondTeam['roundsScore'][i]), border='B')
            self.pdf.cell(10, 8, txt='', border=False)
            if (i > 0 and i%2 == 0): self.pdf.ln(8)
        self.pdf.cell(40, 8, txt="Общий счет", border=False)
        self.pdf.cell(50, 8, txt=str(firstTeam['finalScore']) + " : " + str(secondTeam['finalScore']), border='B')

    def printTeamsLeaders(self, firstTeam, secondTeam):
        self.pdf.ln(8)
        self.pdf.cell(40, 8, txt="Капитан", border=False)
        if (len(firstTeam['players'][0]) > 28):
            self.pdf.set_font_size(5)
        self.pdf.cell(50, 8, txt=firstTeam['players'][0], border='B')
        self.pdf.set_font_size(10)
        self.pdf.cell(10, 8, txt='', border=False)
        self.pdf.cell(40, 8, txt="Капитан", border=False)
        if (len(secondTeam['players'][0]) > 28):
            self.pdf.set_font_size(5)
        self.pdf.cell(50, 8, txt=secondTeam['players'][0], border='B')
        self.pdf.set_font_size(10)
        self.pdf.ln(8)
        self.pdf.cell(40, 8, txt="Тренер", border=False)
        if (len(firstTeam['trainerFIO']) > 28):
            self.pdf.set_font_size(5)
        self.pdf.cell(50, 8, txt=firstTeam['trainerFIO'], border='B')
        self.pdf.set_font_size(10)
        self.pdf.cell(10, 8, txt='', border=False)
        self.pdf.cell(40, 8, txt="Тренер", border=False)
        if (len(secondTeam['trainerFIO']) > 28):
            self.pdf.set_font_size(5)
        self.pdf.cell(50, 8, txt=secondTeam['trainerFIO'], border='B')
        self.pdf.set_font_size(10)
        self.pdf.ln(16)

    def printJudges(self, firstJudgeFIO=None, secondJudgeFIO=None):
        self.pdf.ln(16)
        self.pdf.cell(40, 8, txt="Судья", border=False)
        if (len(firstJudgeFIO) > 28):
            self.pdf.set_font_size(5)
        self.pdf.cell(50, 8, txt=firstJudgeFIO, border='B')
        self.pdf.set_font_size(10)
        self.pdf.cell(10, 8, txt='', border=False)
        if secondJudgeFIO:
            self.pdf.cell(40, 8, txt="Судья 2", border=False)
            if (len(secondJudgeFIO) > 28):
                self.pdf.set_font_size(5)
                self.pdf.cell(50, 8, txt=d['secondJudgeFIO'], border='B')
        self.pdf.set_font_size(10)
        self.pdf.ln(8)
        self.pdf.cell(40, 8, txt="Секретарь", border=False)
        self.pdf.cell(50, 8, txt="", border='B')
        self.pdf.cell(10, 8, txt='', border=False)
        self.pdf.ln(16)
        self.pdf.cell(8, 8, txt='', border=0, align="C")
        self.pdf.ln(8)

    def printTimeouts(self, firstTeamTimeouts, secondTeamTimeouts):
        self.pdf.ln(8)
        self.pdf.cell(8, 8, txt='', border=0, align="C")
        self.pdf.cell(0, 8, txt="Перерывы", border=1, align='C')
        self.pdf.ln(8)
        for row in range(1, 3):
            self.pdf.cell(8, 8, txt=str(row), border=1, align="C")
            for column in range(1, 6):
                founded1 = find_index(firstTeamTimeouts, 'timeoutRound', column)
                founded2 = find_index(secondTeamTimeouts, 'timeoutRound', column)
                if (founded1 != -1):
                    self.pdf.cell(17, 8, txt=firstTeamTimeouts[founded1]['timeoutTime'], border=1, align="C")
                    firstTeamTimeouts[founded1]['timeoutRound'] = 0
                else:
                    self.pdf.cell(17, 8, txt=':', border=1, align="C")
                if (founded2 != -1):
                    self.pdf.cell(17, 8, txt=secondTeamTimeouts[founded2]['timeoutTime'], border=1, align="C")
                    secondTeamTimeouts[founded2]['timeoutRound'] = 0
                else:
                    self.pdf.cell(17, 8, txt=':', border=1, align="C")
                self.pdf.cell(3, 8, txt='', border=False)

            self.pdf.ln(8)
        self.pdf.ln(8)


    def volleyballMatchProtocol(self, d):
        self.printProtocolTitle(d.get('nameCompetition'))
        self.printMatchData(d.get('place'), d.get('time'), d.get('date'))
        self.printTeamTitle(d['firstCommand']["name"], d['secondCommand']["name"])
        self.printListsOfPlayers(d['firstCommand']['players'], d['secondCommand']['players'])
        self.printTeamsLeaders(d["firstCommand"], d["secondCommand"])
        self.printRoundsScore(d["firstCommand"], d["secondCommand"])
        self.printTimeouts(d['firstCommand']['timeouts'], d['secondCommand']['timeouts'])

        protocolName = "matchPr_" + str(d.get('competitionID')) + '.' + str(d.get('matchID')) + ".pdf"
        self.pdf.output(Path(__file__).parent.parent.parent.joinpath("media", "protocols", protocolName))






        # pdf.cell(8, 8, txt='', border=0, align="C")
        # pdf.cell(0, 8, txt="Замены", border=1, align='C', ln=1)
        #
        # for row in range(1, 7):
        #     pdf.cell(8, 8, txt=str(row), border=1, align="C")
        #     for column in range(1, 6):
        #         founded1 = find_index(d['firstCommand']['playerChanges'], 'changeRound', column)
        #         founded2 = find_index(d['secondCommand']['playerChanges'], 'changeRound', column)
        #         if (founded1 != -1):
        #             pdf.cell(17, 4, txt=d['firstCommand']['playerChanges'][founded1]['changedPlayer'] + ' / '
        #                                 + d['firstCommand']['playerChanges'][founded1]['playerOnChange'], border=1, align="C")
        #
        #         else: pdf.cell(17, 4, txt='/', border=1, align="C")
        #         if (founded2 != -1):
        #             pdf.cell(17, 4, txt=d['secondCommand']['playerChanges'][founded2]['changedPlayer'] + ' / '
        #                                 + d['secondCommand']['playerChanges'][founded2]['playerOnChange'], border=1,
        #                      align="C")
        #
        #         else:
        #             pdf.cell(17, 4, txt='/', border=1, align="C")
        #         pdf.cell(3, 8, txt='', border=False)
        #
        #     pdf.ln(4)
        #     pdf.cell(8, 4, txt='', border=0, align="C")
        #     for column in range(1, 6):
        #         founded1 = find_index(d['firstCommand']['playerChanges'], 'changeRound', column)
        #         founded2 = find_index(d['secondCommand']['playerChanges'], 'changeRound', column)
        #         if (founded1 != -1):
        #             pdf.cell(17, 4, txt=d['firstCommand']['playerChanges'][founded1]['changeTime'], border=1, align="C")
        #             d['firstCommand']['playerChanges'][founded1]['changeRound'] = 0
        #         else: pdf.cell(17, 4, txt=':', border=1, align="C")
        #         if (founded2 != -1):
        #             pdf.cell(17, 4, txt=d['secondCommand']['playerChanges'][founded2]['changeTime'], border=1, align="C")
        #             d['secondCommand']['playerChanges'][founded2]['changeRound'] = 0
        #         else:
        #             pdf.cell(17, 4, txt=':', border=1, align="C")
        #         pdf.cell(3, 8, txt='', border=False)
        #     pdf.ln(4)
        #
        # pdf.ln(8)
        # pdf.cell(8, 8, txt='', border=0, align="C")
        # pdf.cell(0, 8, txt="Расстановка", border=1, align='C', ln=1)
        # for row in range(1, 7):
        #     pdf.cell(8, 8, txt=str(row), border=1, align="C")
        #     for column in range(0, 5):
        #         pdf.cell(17, 8, txt='', border=1, align="C")
        #         pdf.cell(17, 8, txt='', border=1, align="C")
        #         pdf.cell(3, 8, txt='', border=False)
        #     pdf.ln(8)

    #
    #
    # def test(self):
    #     d = {
    #         'nameCompetition': 'Спортакиада',
    #         'competitionID' : 12,
    #         'matchID': 2,
    #         'place': 'ТУСУР',
    #         'time': '17:15',
    #         'date': '22.06.2023',
    #         'firstJudgeFIO': 'Павел Александрович Иванов',
    #
    #         'firstCommand': {
    #             'name': "ФСУ",
    #             'trainerFIO': "Чаймаа Даваа-Сурун Кенден-Дуржуевич",
    #             'roundsScore': [12, 13, 18, 22, 5],
    #             'finalScore': 5,
    #             'players': ['Толя', "Коля", "Петя", "Антон", "Влад", "Гоша", 'Тестовоя Длинная Строка'],
    #             'timeouts': [{
    #                 'timeoutRound': 3,
    #                 'timeoutTime': "12:21"
    #             },
    #                 {
    #                     'timeoutRound': 3,
    #                     'timeoutTime': "12:50"
    #                 }
    #             ],
    #         },
    #         'secondCommand': {
    #             'name': "РТФ",
    #             'trainerFIO': "Виктор Викторович Викторов",
    #             'roundsScore': [15, 18, 11, 23, 25],
    #             'finalScore': 5,
    #             'players': ['Толя', "Коля", "Петя", "Антон", "Влад", "Гоша", "Чаймаа Даваа-Сурун Кенден-Дуржуевич"],
    #             'timeouts': [{
    #                 'timeoutRound': 4,
    #                 'timeoutTime': "12:21"
    #             }],
    #         }
    #     }
    #
    #     self.volleyballMatchProtocol(d)


def find_index(li, key, value):
    return next((i for i, x in enumerate(li) if x[key] == value), -1)

