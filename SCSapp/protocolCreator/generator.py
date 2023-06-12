from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.fonts import addMapping
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph, Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT


def generate_pdf_table(competition, matches):
    font_path = "Arial.ttf"
    pdfmetrics.registerFont(TTFont('Arial', font_path))
    doc = SimpleDocTemplate("C:/Users/777/Downloads/team_stats.pdf", pagesize=landscape(A4), leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0)
    styles = getSampleStyleSheet()
    
    title_style = styles['Title']
    title_style.fontName = 'Arial'

    date_style = styles['Normal']
    date_style.fontName = 'Arial'
    date_style.fontSize = 15
    
    

    mas = []

    for i in range(1,len(competition['commands'])+1) :
        mas.append(i)


    data = [['№', 'Команда'] + mas + [ 'И', 'В',
             'П', 'Оч']]
    
    for i, team in enumerate(competition['commands'], start=1):

        teams_point = []

        for j, team1 in enumerate(competition['commands'], start=1):
            if i == j :
                teams_point.append("-")
            else:
                teams_point.append(teams_points(matches,team,team1))

        match_count = find_team_matches(matches, team)
        wins_count = calculate_wins_count(matches, team)
        losses_count = calculate_losses_count(matches, team)
        team_points = calculate_team_points(matches, team)
        data.append([i, team]+teams_point+[match_count, wins_count,
                     losses_count, team_points])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    
    for i, team in enumerate(competition['commands'], start=1):
        table.setStyle(TableStyle([('FONTNAME', (1, i), (1, i), 'Arial')]))  # Используем зарегистрированный шрифт только для названий команд

    elements = []

# Добавляем надпись с названием соревнования
    competition_title = "<b>{}</b>".format(competition['nameCompetition'])
    competition_title = Paragraph(competition_title, styles['Title'])
    elements.append(competition_title)

    # Добавляем надпись с "Протокол соревнования"
    title_style.fontSize = 15  # Установка размера шрифта
    competition_title = "<b>{}</b>".format("Протокол соревнования")
    competition_title = Paragraph(competition_title, styles['Title'])
    elements.append(competition_title)

    
    line_style = TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black)  # Линия под всей шириной первой строки
    ])
    line_data = [['']]  # Пустая таблица с одной ячейкой
    line_table = Table(line_data, colWidths=[doc.width-40])  # Ширина ячейки равна ширине страницы
    line_table.setStyle(line_style)
    elements.append(line_table)

# Добавляем пустой элемент для создания отступа
    spacer = Spacer(1, 0.5 * inch)
    elements.append(spacer)

    elements.append(table)

    spacer = Spacer(1, 0.5 * inch)
    elements.append(spacer)

     # Добавляем дату
    date_paragraph = Paragraph("Дата: ", date_style)
    date = Paragraph("{}".format(competition['date']), date_style)
    # Создаем таблицу с двумя ячейками для надписей
    table_data = [
        [date_paragraph,date]
    ]
    table = Table(table_data, colWidths=[600, 200])  # Установите ширину ячеек по вашему выбору

    # Настройка стиля таблицы
    table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Выравнивание текста в ячейках по левому краю
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Выравнивание текста по центру по вертикали
    ])
    table.setStyle(table_style)

    elements.append(table)  # Добавление таблицы в элементы документа

    spacer = Spacer(1, 0.3 * inch)
    elements.append(spacer)

    # Добавляем подпись
    signature_paragraph = Paragraph("Подпись организатора: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", date_style)
    signature = Paragraph("{} &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<u> &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</u>".format(competition['sponsor']), date_style)
    
    table_data = [
        [signature_paragraph,signature]
    ]
    table = Table(table_data, colWidths=[400, 400])  # Установите ширину ячеек по вашему выбору

    # Настройка стиля таблицы
    table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Выравнивание текста в ячейках по левому краю
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Выравнивание текста по центру по вертикали
    ])
    table.setStyle(table_style)
    elements.append(table)

    doc.build(elements)


def calculate_team_points(matches, team):
    team_points = 0
    for match in matches:
        if match['firstCommand'] == team:
            team_points += match['pointFirstCommand']
        elif match['secondCommand'] == team:
            team_points += match['pointSecondCommand']
    return team_points

def teams_points(matches, team1, team2):
    for match in matches:
        if match['firstCommand'] == team1 and match['secondCommand'] == team2:
           return str(match['pointFirstCommand']) + " : " + str(match['pointSecondCommand'])
        if match['firstCommand'] == team2 and match['secondCommand'] == team1:
           return str(match['pointSecondCommand']) + " : " + str(match['pointFirstCommand'])


def find_team_matches(matches, team):
    team_match_count = 0
    for match in matches:
        if match['firstCommand'] == team or match['secondCommand'] == team:
            team_match_count += 1
    return team_match_count


def calculate_wins_count(matches, team):
    wins_count = 0
    for match in matches:
        if match['firstCommand'] == team and match['pointFirstCommand'] > match['pointSecondCommand']:
            wins_count += 1
        elif match['secondCommand'] == team and match['pointSecondCommand'] > match['pointFirstCommand']:
            wins_count += 1
    return wins_count


def calculate_losses_count(matches, team):
    losses_count = 0
    for match in matches:
        if match['firstCommand'] == team and match['pointFirstCommand'] < match['pointSecondCommand']:
            losses_count += 1
        elif match['secondCommand'] == team and match['pointSecondCommand'] < match['pointFirstCommand']:
            losses_count += 1
    return losses_count


def main():
    competition = {'commands': ["ФСУ", "РТФ", "ФБ","ФВС"],
                   'nameCompetition' : "Межвузовские соревнования",
                   'sponsor' : "Иванов Иван Иванович",
                   'date':"09.06.2023",
                   'matches': [
                       {'firstCommand': "ФСУ", 'secondCommand': "РТФ",
              'pointFirstCommand': 3, 'pointSecondCommand': 0},
              {'firstCommand': "ФСУ", 'secondCommand': "ФБ",
              'pointFirstCommand': 3, 'pointSecondCommand': 0},
              {'firstCommand': "РТФ", 'secondCommand': "ФБ",
              'pointFirstCommand': 2, 'pointSecondCommand': 1},
              {'firstCommand': "ФСУ", 'secondCommand': "ФВС",
              'pointFirstCommand': 1, 'pointSecondCommand': 2},
              {'firstCommand': "РТФ", 'secondCommand': "ФВС",
              'pointFirstCommand': 2, 'pointSecondCommand': 1},
              {'firstCommand': "ФВС", 'secondCommand': "ФБ",
              'pointFirstCommand': 3, 'pointSecondCommand': 0}
                   ]}


    matches = competition['matches']  # Добавьте другие матчи, если нужно

    generate_pdf_table(competition, matches)
    print("PDF-файл с таблицей команд и их статистикой успешно создан.")

    

if __name__ == '__main__':
    main()
