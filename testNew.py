import telebot
from playwright.sync_api import sync_playwright


key = '5956180389:AAFDaE7LiFvlRyXCHdvCM4lT6EW41jEtO7I'

bot = telebot.TeleBot(key)

@bot.message_handler(commands=['start'])
def start(message):
    name = message.chat.first_name
    #bot.send_message(message.chat.id,"")
    bot.send_message(message.chat.id, "hello " + name)
    bot.send_message(message.chat.id,"Select /start or select /Vtu_No")


@bot.message_handler(commands=['Vtu_No'])
def start(message):
    msg = bot.send_message(message.chat.id,"Enter your vtu no.")
    bot.register_next_step_handler(msg, pincode_step)

def pincode_step(message):
    pin = message.text
    law = []
    bot.send_message(message.chat.id, "Estimated Waiting Time: 50 secs")
   
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto("http://exams.veltech.edu.in/studentlogin/stulogin.aspx")
        page.fill('input#txtUserName', pin)
        page.fill('input#txtPassword', pin)
        page.click('input[type=image]')
        CGPA = 0
        CGPA1 = 0
        AB = []
        NE = []
        for x in range(1, 9):
            page.goto('http://exams.veltech.edu.in/Studentlogin/UserPages/StudentUniversityResultsBySem.aspx')
            html1 = page.content()

            page.select_option('select#ContentPlaceHolder1_ddlSemester', label=str(x))
            Name = page.inner_text('#ContentPlaceHolder1_lblNameTxt')
            RegNo = page.inner_text('#ContentPlaceHolder1_lblRegNoTxt')
            Degree = page.inner_text('#ContentPlaceHolder1_lblDegTxt')
            Branch = page.inner_text('#ContentPlaceHolder1_lblBranchTxt')
            if x == 1:
                law.append(f'Name: {Name} ')
                law.append(f'RegNo: {RegNo}')
                law.append(f'Degree: {Degree}')
                law.append(f'Branch: {Branch}')
            column_code = page.locator("//table[@id='ContentPlaceHolder1_gvExamResult2013']//tr/td[3]")
            if column_code.all_inner_texts() == []:
                break
            else:
                column_headers = page.locator("table#ContentPlaceHolder1_gvExamResult2013 th")
                column_code = page.locator("//table[@id='ContentPlaceHolder1_gvExamResult2013']//tr/td[3]")
                column_name = page.locator("//table[@id='ContentPlaceHolder1_gvExamResult2013']//tr/td[4]")
                column_grade = page.locator("//table[@id='ContentPlaceHolder1_gvExamResult2013']//tr/td[5]")
                column_result = page.locator("//table[@id='ContentPlaceHolder1_gvExamResult2013']//tr/td[6]")
                ######################### CREATING EMPTY LIST FOR DTORING VALUES ##############################
                CODE11 = []
                for i in range(len(column_code.all_inner_texts())):
                    CODE11.append(column_code.all_inner_texts()[i])
                NAME11 = []
                for i in column_name.all_inner_texts():
                    NAME11.append(i)
                GRADE11 = []
                for i in column_grade.all_inner_texts():
                    GRADE11.append(i)

                #########################  CREDITS GENRATION  #################################

                page.goto('http://exams.veltech.edu.in/Studentlogin/UserPages/StudentCreditsPoint.aspx')
                html2 = page.content()
                column1_headers = page.locator("table#ContentPlaceHolder1_gvCredits  th")

                column_type = page.locator("//table[@id='ContentPlaceHolder1_gvCredits']//th")

                column1_Code = page.locator("//table[@id='ContentPlaceHolder1_gvCredits']//tr/td[1]")
                column1_Name = page.locator("//table[@id='ContentPlaceHolder1_gvCredits']//tr/td[2]")
                column1_CreditsRegistered = page.locator("//table[@id='ContentPlaceHolder1_gvCredits']//tr/td[3]")
                column_EarnedCredits = page.locator("//table[@id='ContentPlaceHolder1_gvCredits']//tr/td[4]")

                ###################################################################################
                Course_Code_NotFiltered = column1_Code.all_inner_texts()
                Course_Code_Filtered = []
                Course_Code_Filtered1 = []

                for i in Course_Code_NotFiltered:
                    if i == "\xa0\xa0Foundation Courses (60 Credits)" or i == "\xa0\xa0Programme Core Courses (" \
                                                                              "60 Credits)" or i == \
                            "\xa0\xa0Programme Electives (18 Credits)" or i == "\xa0\xa0Programme Electives (18 Credits)" or i == \
                            "\xa0\xa0Allied Electives (6 Credits)" or i == "\xa0\xa0Institute Electives (10 Credits)" or i == \
                            "\xa0\xa0Value Education Electives (4 Credits)" or i == "\xa0\xa0(b) Seminar (2 Credits)" or i == \
                            "\xa0\xa0(c) Minor project (4 Credits)" or i == "\xa0\xa0(d) Major project (12 Credits)" or i == \
                            "\xa0\xa0(d) Major project (12 Credits)" or i == "\xa0\xa0Industry/Higher Institute Learning " \
                                                                             "Interaction (2 Credits)" or i == "\xa0\xa0Independent Learning (20 Credits) : (a) Self- Learning " \
                                                                                                               "Course (2 Credits)":
                        Course_Code_Filtered.append(i)
                    else:
                        Course_Code_Filtered1.append(i)

                ########################Creating Dictionary####################################
                DictMain = dict(zip(Course_Code_Filtered1, column1_CreditsRegistered.all_inner_texts()))
                ######################### CREATING LIST #######################################
                Credits_finals = []
                for k, v in DictMain.items():
                    for j in CODE11:
                        if k == j:
                            Credits_finals.append(v)
                GRADE_POINTS = []

                for i in range(len(CODE11)):
                    if GRADE11[i] == 'S':
                        GRADE_POINTS.append(10)
                    elif GRADE11[i] == 'A':
                        GRADE_POINTS.append(9)
                    elif GRADE11[i] == 'B':
                        GRADE_POINTS.append(8)
                    elif GRADE11[i] == 'C':
                        GRADE_POINTS.append(7)
                    elif GRADE11[i] == 'D':
                        GRADE_POINTS.append(6)
                    elif GRADE11[i] == 'E':
                        GRADE_POINTS.append(5)
                    elif GRADE11[i] == 'NE':
                        NE.append(NAME11[i])
                    elif GRADE11[i] == 'AB':
                        GRADE_POINTS.append(0)
                        AB.append(NAME11[i])

                Total_Credits = 0
                Total_Grade_Points = 0
                for i in range(len(Credits_finals)):
                    Total_Credits += int(Credits_finals[i])
                    Total_Grade_Points += int(GRADE_POINTS[i]) * int(Credits_finals[i])
                GPA = Total_Grade_Points / Total_Credits
                law.append(f"Gpa of Semester {x} : {round(GPA, 2)} ")
                CGPA += GPA
                CGPA1 = round((CGPA / x), 2)
                law.append(f"Cgpa after Semester {x} : {round((CGPA / x), 2)} ")
        law.append("\n")
        law.append(f" Total Cgpa: {CGPA1}")
        #print(end="\n")
        if AB != []:
            law.append(f"\n")
            law.append("Absent Exam List:")
            #print("Absent Exam List:")
            for i in range(len(AB)):
                law.append(f"{str(i+1)}. {AB[i]}")
                #print(str(i + 1) + '.', AB[i])
       # print(end="\n")
        if NE != []:
            law.append(f"\n")
            law.append("Not Eligible Exam List:")
            #print("Not Eligible Exam List:")
            for i in range(len(NE)):
                law.append(f"{str(i+1)}. {NE[i]} ")
             #   print(str(i + 1) + '.', NE[i])

   # raw = []
    #raw.append(law)
    #for i in raw:
     #   for j in i:
      #      bot.send_message(message.chat.id, j)


    #for j in law:
        #bot.send_message(message.chat.id, j)

    f = open("west.txt", "w")
    for i in range(len(law)):
        f.writelines(law[i])
        f.writelines(" \n ")
    f.close()
    f = open("west.txt", "r+")
    a = f.read()

    bot.send_message(message.chat.id, f"{a}")


print("Telegram Bot started..!")
bot.polling()

