 
from fpdf import FPDF

class PDFProtocolCreator():

    def volleybalMatchProtocol(self, d):

        pdf = FPDF('P', 'mm', 'A4')

        pdf.add_page()
        pdf.add_font('DejaVu', '', 'Arial.ttf', uni=True)
        pdf.set_font('DejaVu', size=10)

        pdf.cell(0, 8, align='C', txt="ПРОТОКОЛ №", border=False)
        pdf.ln(16)
        pdf.cell(0, 8, align='C', txt="соревнований по воллейболу", border=False, ln=1)
        pdf.cell(50, 8, txt="Место проведения:", border=False)
        pdf.cell(0, 8, txt=d.get('place'), border='B', ln=1)
        pdf.cell(20, 8, txt="Время:", border=False)
        pdf.cell(60, 8, txt=d.get('datetime'), border='B')
        pdf.cell(20, 8, txt="Дата:", border=False)
        pdf.cell(0, 8, txt="                ", border='B')
        pdf.ln(12)
        pdf.cell(0, 8, txt="среди муж./жен./смеш. команд")
        pdf.ln(12)
        pdf.cell(30, 8, txt="Команда А", border=False)
        pdf.cell(70, 8, txt=d['firstCommand']["name"], border='B')
        pdf.cell(30, 8, txt="Команда Б", border=False)
        pdf.cell(0, 8, txt=d['secondCommand']["name"], border='B')
        pdf.ln(12)
        pdf.cell(100, 8, txt="Состав команды (А)", border=False)
        pdf.cell(0, 8, txt="Состав команды (Б)", border=False)
        pdf.ln(12)

        pdf.cell(20, 8, txt='№ п/п', border=1)
        pdf.cell(70, 8, txt='ФИО игрока', border=1)
        pdf.cell(10, 8, txt='', border=False)
        pdf.cell(20, 8, txt='№ п/п', border=1)
        pdf.cell(70, 8, txt='ФИО игрока', border=1)
        pdf.ln(8)

        for row in range(1, 13):
            pdf.cell(20, 8, txt=str(row), border=1)
            if (len(d['firstCommand']['players']) > row-1):
                if (len(d['firstCommand']['players'][row-1]) > 35):
                    pdf.set_font_size(5)
                pdf.cell(70, 8, txt=d['firstCommand']['players'][row-1], border=1)
                pdf.set_font_size(10)
            else:
                pdf.cell(70, 8, txt="", border=1)

            pdf.cell(10, 8, txt='', border=False)
            pdf.cell(20, 8, txt=str(row), border=1)
            if (len(d['secondCommand']['players']) > row - 1):
                if (len(d['secondCommand']['players'][row-1]) > 35):
                    pdf.set_font_size(5)
                pdf.cell(70, 8, txt=d['secondCommand']['players'][row-1], border=1)
                pdf.set_font_size(10)
            else:
                pdf.cell(70, 8, txt="", border=1)

            pdf.ln(8)

        pdf.ln(8)
        pdf.cell(40, 8, txt="Капитан", border=False)
        if (len(d['firstCommand']['players'][0]) > 28):
            pdf.set_font_size(5)
        pdf.cell(50, 8, txt=d["firstCommand"]['players'][0], border='B')
        pdf.set_font_size(10)
        pdf.cell(10, 8, txt='', border=False)
        pdf.cell(40, 8, txt="Капитан", border=False)
        if (len(d['secondCommand']['players'][0]) > 28):
            pdf.set_font_size(5)
        pdf.cell(50, 8, txt=d["secondCommand"]['players'][0], border='B')
        pdf.set_font_size(10)
        pdf.ln(8)
        pdf.cell(40, 8, txt="Тренер", border=False)
        if (len(d['firstCommand']['trainerFIO']) > 28):
            pdf.set_font_size(5)
        pdf.cell(50, 8, txt=d["firstCommand"]['trainerFIO'], border='B')
        pdf.set_font_size(10)
        pdf.cell(10, 8, txt='', border=False)
        pdf.cell(40, 8, txt="Тренер", border=False)
        if (len(d['secondCommand']['trainerFIO']) > 28):
            pdf.set_font_size(5)
        pdf.cell(50, 8, txt=d["secondCommand"]['trainerFIO'], border='B')
        pdf.set_font_size(10)

        pdf.ln(16)
        pdf.cell(40, 8, txt="Счёт 1 партии", border=False)
        pdf.cell(50, 8, txt=str(d["firstCommand"]['roundsScore'][0]) + ' : ' + str(d["secondCommand"]['roundsScore'][0]), border='B')
        pdf.cell(10, 8, txt='', border=False)
        pdf.cell(40, 8, txt="Счёт 2 партии", border=False)
        if (len(d["firstCommand"]['roundsScore']) > 2):
            pdf.cell(50, 8, txt=str(d["firstCommand"]['roundsScore'][1]) + ' : ' + str(d["secondCommand"]['roundsScore'][1]), border='B')
        else:
            pdf.cell(50, 8, txt='', border='B')
        pdf.ln(8)
        pdf.cell(40, 8, txt="Счёт 3 партии", border=False)
        if (len(d["firstCommand"]['roundsScore']) > 2):
            pdf.cell(50, 8, txt=str(d["firstCommand"]['roundsScore'][2]) + ' : ' + str(d["secondCommand"]['roundsScore'][2]), border='B')
        else:
            pdf.cell(50, 8, txt='', border='B')
        pdf.cell(10, 8, txt='', border=False)
        pdf.cell(40, 8, txt="Счёт 4 партии", border=False)
        if (len(d["firstCommand"]['roundsScore']) > 3):
            pdf.cell(50, 8, txt=str(d["firstCommand"]['roundsScore'][3]) + ' : ' + str(d["secondCommand"]['roundsScore'][3]), border='B')
        else:
            pdf.cell(50, 8, txt='', border='B')
        pdf.ln(8)
        pdf.cell(40, 8, txt="Счёт 5 партии", border=False)
        if (len(d["firstCommand"]['roundsScore']) > 4):
            pdf.cell(50, 8, txt=str(d["firstCommand"]['roundsScore'][4]) + ' : ' + str(d["secondCommand"]['roundsScore'][4]), border='B')
        else:
            pdf.cell(50, 8, txt='', border='B')
        pdf.cell(10, 8, txt='', border=False)
        pdf.cell(40, 8, txt="Общий счет", border=False)
        pdf.cell(50, 8, txt=str(d["firstCommand"]['finalScore']) + " : " + str(d["secondCommand"]['finalScore']), border='B')

        pdf.ln(16)
        pdf.cell(40, 8, txt="Судья 1", border=False)
        if (len(d['firstJudgeFIO']) > 28):
            pdf.set_font_size(5)
        pdf.cell(50, 8, txt=d['firstJudgeFIO'], border='B')
        pdf.set_font_size(10)
        pdf.cell(10, 8, txt='', border=False)
        pdf.cell(40, 8, txt="Судья 2", border=False)
        if (len(d['secondJudgeFIO']) > 28):
            pdf.set_font_size(5)
        pdf.cell(50, 8, txt=d['secondJudeFIO'], border='B')
        pdf.set_font_size(10)
        pdf.ln(8)
        pdf.cell(40, 8, txt="Секретарь", border=False)
        pdf.cell(50, 8, txt="", border='B')
        pdf.cell(10, 8, txt='', border=False)
        # pdf.cell(40, 8, txt="Представитель (Б)", border=False)
        # pdf.cell(50, 8, txt="", border='B')

        pdf.ln(16)
        pdf.cell(8, 8, txt='', border=0, align="C")
       # pdf.cell(0, 8, txt="Счет игры по пратиям", border=1, align='C')
        pdf.ln(8)

        pdf.cell(8, 8, txt='', border=0, align="C")
        pdf.cell(34, 8, txt="1 партия", border=1, align="C")
        pdf.cell(3, 8, txt='', border=False)
        pdf.cell(34, 8, txt="2 партия", border=1, align="C")
        pdf.cell(3, 8, txt='', border=False)
        pdf.cell(34, 8, txt="3 партия", border=1, align="C")
        pdf.cell(3, 8, txt='', border=False)
        pdf.cell(34, 8, txt="4 партия", border=1, align="C")
        pdf.cell(3, 8, txt='', border=False)
        pdf.cell(34, 8, txt="5 партия", border=1, align="C")
        pdf.ln(8)

        pdf.cell(8, 8, txt='', border=0, align="C")
        pdf.cell(17, 8, txt="А", border=1, align="C")
        pdf.cell(17, 8, txt="Б", border=1, align="C")
        pdf.cell(3, 8, txt='', border=False)
        pdf.cell(17, 8, txt="А", border=1, align="C")
        pdf.cell(17, 8, txt="Б", border=1, align="C")
        pdf.cell(3, 8, txt='', border=False)
        pdf.cell(17, 8, txt="А", border=1, align="C")
        pdf.cell(17, 8, txt="Б", border=1, align="C")
        pdf.cell(3, 8, txt='', border=False)
        pdf.cell(17, 8, txt="А", border=1, align="C")
        pdf.cell(17, 8, txt="Б", border=1, align="C")
        pdf.cell(3, 8, txt='', border=False)
        pdf.cell(17, 8, txt="А", border=1, align="C")
        pdf.cell(17, 8, txt="Б", border=1, align="C")
        pdf.ln(8)

        # for row in range(1, 31):
        #     pdf.cell(8, 8, txt='', border=0, align="C")
        #     if(row <= d['firstCommand']['roundsScore'][0]):
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     if (row <= d['secondCommand']['roundsScore'][0]):
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     pdf.cell(3, 8, txt='', border=False)
        #     if (row <= d['firstCommand']['roundsScore'][1]):
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     if (row <= d['secondCommand']['roundsScore'][1]):
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     pdf.cell(3, 8, txt='', border=False)
        #     if (row <= d['firstCommand']['roundsScore'][2]):
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     if ((row <= d['secondCommand']['roundsScore'][2])):
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     pdf.cell(3, 8, txt='', border=False)
        #     if (len(d['firstCommand']['roundsScore']) > 3):
        #         if (row <= d['firstCommand']['roundsScore'][3]):
        #             pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #         else:
        #             pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     if (len(d['secondCommand']['roundsScore']) > 3):
        #         if ((row <= d['secondCommand']['roundsScore'][3])):
        #             pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #         else:
        #             pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     pdf.cell(3, 8, txt='', border=False)
        #     if (len(d['firstCommand']['roundsScore']) > 4):
        #         if (row <= d['firstCommand']['roundsScore'][4]):
        #             pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #         else:
        #             pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     if (len(d['secondCommand']['roundsScore']) > 4):
        #         if ((row <= d['secondCommand']['roundsScore'][4])):
        #             pdf.cell(17, 8, txt=str(row), border=1, align="C")
        #         else:
        #             pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     else:
        #         pdf.cell(17, 8, txt=str(row), border=1, align="C", fill=True)
        #     pdf.ln(8)

        pdf.ln(8)
        pdf.cell(8, 8, txt='', border=0, align="C")
        pdf.cell(0, 8, txt="Перерывы", border=1, align='C')
        pdf.ln(8)
        for row in range(1, 3):
            pdf.cell(8, 8, txt=str(row), border=1, align="C")
            for column in range(1, 6):
                founded1 = find_index(d['firstCommand']['timeouts'], 'timeoutRound', column)
                founded2 = find_index(d['secondCommand']['timeouts'], 'timeoutRound', column)
                if (founded1 != -1):
                    pdf.cell(17, 8, txt=d['firstCommand']['timeouts'][founded1]['timeoutTime'], border=1, align="C")
                    d['firstCommand']['timeouts'][founded1]['timeoutRound'] = 0
                else:
                    pdf.cell(17, 8, txt=':', border=1, align="C")
                if (founded2 != -1):
                    pdf.cell(17, 8, txt=d['secondCommand']['timeouts'][founded2]['timeoutTime'], border=1, align="C")
                    d['secondCommand']['timeouts'][founded2]['timeoutRound'] = 0
                else:
                    pdf.cell(17, 8, txt=':', border=1, align="C")
                pdf.cell(3, 8, txt='', border=False)

            pdf.ln(8)



        pdf.ln(8)
        pdf.cell(8, 8, txt='', border=0, align="C")
        pdf.cell(0, 8, txt="Замены", border=1, align='C', ln=1)

        for row in range(1, 7):
            pdf.cell(8, 8, txt=str(row), border=1, align="C")
            for column in range(1, 6):
                founded1 = find_index(d['firstCommand']['playerChanges'], 'changeRound', column)
                founded2 = find_index(d['secondCommand']['playerChanges'], 'changeRound', column)
                if (founded1 != -1):
                    pdf.cell(17, 4, txt=d['firstCommand']['playerChanges'][founded1]['changedPlayer'] + ' / '
                                        + d['firstCommand']['playerChanges'][founded1]['playerOnChange'], border=1, align="C")

                else: pdf.cell(17, 4, txt='/', border=1, align="C")
                if (founded2 != -1):
                    pdf.cell(17, 4, txt=d['secondCommand']['playerChanges'][founded2]['changedPlayer'] + ' / '
                                        + d['secondCommand']['playerChanges'][founded2]['playerOnChange'], border=1,
                             align="C")

                else:
                    pdf.cell(17, 4, txt='/', border=1, align="C")
                pdf.cell(3, 8, txt='', border=False)

            pdf.ln(4)
            pdf.cell(8, 4, txt='', border=0, align="C")
            for column in range(1, 6):
                founded1 = find_index(d['firstCommand']['playerChanges'], 'changeRound', column)
                founded2 = find_index(d['secondCommand']['playerChanges'], 'changeRound', column)
                if (founded1 != -1):
                    pdf.cell(17, 4, txt=d['firstCommand']['playerChanges'][founded1]['changeTime'], border=1, align="C")
                    d['firstCommand']['playerChanges'][founded1]['changeRound'] = 0
                else: pdf.cell(17, 4, txt=':', border=1, align="C")
                if (founded2 != -1):
                    pdf.cell(17, 4, txt=d['secondCommand']['playerChanges'][founded2]['changeTime'], border=1, align="C")
                    d['secondCommand']['playerChanges'][founded2]['changeRound'] = 0
                else:
                    pdf.cell(17, 4, txt=':', border=1, align="C")
                pdf.cell(3, 8, txt='', border=False)
            pdf.ln(4)

        pdf.ln(8)
        pdf.cell(8, 8, txt='', border=0, align="C")
        pdf.cell(0, 8, txt="Расстановка", border=1, align='C', ln=1)
        for row in range(1, 7):
            pdf.cell(8, 8, txt=str(row), border=1, align="C")
            for column in range(0, 5):
                pdf.cell(17, 8, txt='', border=1, align="C")
                pdf.cell(17, 8, txt='', border=1, align="C")
                pdf.cell(3, 8, txt='', border=False)
            pdf.ln(8)

        pdf.output('test.pdf')

def find_index(li, key, value):
    return next((i for i, x in enumerate(li) if x[key] == value), -1)

