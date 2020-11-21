import streamlit as st
import pandas as pd
import cv2
from PIL import Image,ImageEnhance
import requests
from bs4 import BeautifulSoup
import pytesseract
from win32com.client import Dispatch
a=[]
pytesseract.pytesseract.tesseract_cmd='C:\Program Files\Tesseract-OCR\\tesseract'
from apiclient.discovery import build
api_key='AIzaSyDlz1FvKYUmQIBznPFQnoD30ryDZSZyu2k'
resource = build("customsearch", 'v1', developerKey=api_key).cse()

# Security
# passlib,hashlib,bcrypt,scrypt
import hashlib
def speak(str):
    speak=Dispatch(('SAPI.Spvoice'))
    speak.Speak(str)


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB Management
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_medtable():
	c.execute('CREATE TABLE IF NOT EXISTS medtable(Salt TEXT)')
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
def add_meddata(Salt):
    c.execute('INSERT INTO medtable(Salt) VALUES (?)', (Salt))
    conn.commit()
def view_all_med():
    c.execute('SELECT * FROM medtable')
    data = c.fetchall()
    return data


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data
def main():
    """Built By Harshit Trehan"""

    html_temp = """
							<div style="background-color:#6666ff ;padding:20px">
							<h1 style="color:white;text-align:center;">The Med Assistant</h1>
							</div>
							"""
    st.markdown(html_temp, unsafe_allow_html=True)
    from PIL import Image
    img = Image.open("mede.jfif")

    st.image(img, width=698)

    html_temp = """
    							<div style="background-color:#6666ff ;padding:10px">
    							<h1 style="color:white;text-align:center;"></h1>
    							</div>
    							"""
    st.markdown(html_temp, unsafe_allow_html=True)


    menu = ["Home", "Why this app?", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)
    if st.sidebar.button("Side effects of high eye blinking?"):
        st.sidebar.text("high blood pressure,anxiety,depression etc")


    if st.sidebar.button('Check Eye Blinking Count'):
        i = 0
        cap = cv2.VideoCapture(0)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

        out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280, 720))

        ret, frame1 = cap.read()
        ret, frame2 = cap.read()
        print(frame1.shape)
        while cap.isOpened():
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)

                if cv2.contourArea(contour) < 900:
                    continue
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame1, "Eye Status: {} {}".format('Blinking', i), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)
                i = i + 1
            # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

            image = cv2.resize(frame1, (1280, 720))
            out.write(image)
            cv2.imshow("feed", frame1)
            frame1 = frame2
            ret, frame2 = cap.read()

            if cv2.waitKey(40) == 27:
                break

        cv2.destroyAllWindows()
        cap.release()

    if choice == "Home":
        # 6666ff
        st.text(" ")
        st.text(" ")
        st.text("Hey! I am here to assist you")
        st.markdown("![Alt Text](https://media.giphy.com/media/SKT4HdqZSSPbaobtPs/giphy.gif)")

        st.success("SIGN UP SO THAT YOU CAN ACCESS OUR APP")

    elif choice == "Why this app?":
        st.warning("VERSION 1.0")
        st.markdown("![Alt Text](https://media.giphy.com/media/SKT4HdqZSSPbaobtPs/giphy.gif)")

        st.success(
            "There are Lots of unused and left over medicine tablets. We all have with us and after some time we don't remember where and when to the use that medicine and we waste our money and go to the market to buy the medicine with same salt composition. This App is very user Friendly We Just Have To Upload or Click The Picture of the Medicine Box and it will give us all the details >>>*&  "
            "Added Support of Eye blinking Counter: Eye Blinking is a Serious Symptom of depression,anxiety etc ".upper())
        speak("There are Lots of unused and left over medicine tablets. We all have with us and after some time we don't remember where and when to the use that medicine and we waste our money and go to the market to buy the medicine with same salt composition. This App is very user Friendly We Just Have To Upload or Click The Picture of the Medicine Box and it will give us all the details >>>*&  "
            "Added Support of Eye blinking Counter: Eye Blinking is a Serious Symptom of depression,anxiety etc ")
    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                create_medtable()

                st.success("Logged In as {}".format(username))
                st.balloons()

                task = st.selectbox("Task", ["Upload", "Click", "Check Your Analytics"])
                if task == "Upload":

                    st.subheader("HEALTH PROBLEM DETECTION")

                    image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

                    if image_file is not None:
                        our_image = Image.open(image_file)
                        img = cv2.imread('check.jpg')
                        st.text("Original Image")
                            # st.write(type(our_image))
                        st.image(our_image)
                        if st.checkbox("CLICK HERE TO GET ALL THE DETAILS OF YOUR MEDICINE"):

                            text = pytesseract.image_to_string(img)
                            text.replace('\n', '')
                            a = [text.split('|')]
                            b = " ".join(text.split())
                            c = b.split('Tablets')
                            d = c[0].split()
                            res = requests.get('https://www.drugs.com/mtm/{}.html'.format(d[-1]))
                            page = res.content
                            soup = BeautifulSoup(page, 'html.parser')
                            k = 0
                            e = []
                            news_box = soup.find('div', {'class': 'contentBox'})
                            all_news = news_box.find_all('p')
                            for news in all_news:
                                links = news.find_all('a')
                                for link in links:
                                    if k < 3:
                                        k = k + 1
                                        pass
                                    elif k < 6:
                                        k = k + 1
                                        e.append(link.text)
                                    else:
                                        break
                            st.subheader('This Medicine Can Cure You From The Following Health Issues:')
                            st.markdown("![Alt Text](https://media.giphy.com/media/SKT4HdqZSSPbaobtPs/giphy.gif)")

                            speak('This Medicine Can Cure You From The Following Health Issues:')
                            for j in e:
                                st.success(j.upper())
                                speak(j)
                            st.text('MAIN SALT:')
                            st.warning(d[-1])

                            if st.checkbox('KNOW MORE DETAILS'):
                                resultof = resource.list(q=d[-1], cx='a827d0e4f76cba536').execute()
                                details = resultof['items'][0]['htmlSnippet']
                                st.text(details)
                elif task=="Click":
                    cam = cv2.VideoCapture(0)

                    cv2.namedWindow("test")

                    img_counter = 0

                    while True:
                        ret, frame = cam.read()
                        if not ret:
                            print("failed to grab frame")
                            break
                        cv2.imshow("test", frame)

                        k = cv2.waitKey(1)
                        if k % 256 == 27:
                            # ESC pressed
                            print("Escape hit, closing...")
                            break
                        elif k % 256 == 32:
                            # SPACE pressed
                            img_name = "opencv_frame_{}.png".format(img_counter)
                            cv2.imwrite(img_name, frame)
                            # need to run only once to load model into memory
                            text = pytesseract.image_to_string(img_name)
                            #print(result)
                            #print("{} written!".format(img_name))
                            img_counter += 1

                    cam.release()

                    cv2.destroyAllWindows()
                    if st.checkbox("CLICK HERE TO GET ALL THE DETAILS OF YOUR MEDICINE"):
                        text.replace('\n', '')
                        a = [text.split('|')]
                        b = " ".join(text.split())
                        c = b.split('Tablets')
                        d = c[0].split()
                        res = requests.get('https://www.drugs.com/mtm/{}.html'.format(d[-1]))
                        page = res.content
                        soup = BeautifulSoup(page, 'html.parser')
                        k = 0
                        e = []
                        news_box = soup.find('div', {'class': 'contentBox'})
                        all_news = news_box.find_all('p')
                        for news in all_news:
                            links = news.find_all('a')
                            for link in links:
                                if k < 3:
                                    k = k + 1
                                    pass
                                elif k < 6:
                                    k = k + 1
                                    e.append(link.text)
                                else:
                                    break
                        st.subheader('This Medicine Can Cure You From The Following Health Issues:')
                        for j in e:
                            st.success(j.upper())
                        st.text('MAIN SALT:')
                        st.warning(d[-1])


                        if st.checkbox('KNOW MORE DETAILS'):
                            resultof = resource.list(q=d[-1], cx='a827d0e4f76cba536').execute()
                            details = resultof['items'][0]['htmlSnippet']
                            st.text(details)

                elif task == "Check Your Analytics":
                    st.subheader("PAST SEARCHES")
                    user_result = view_all_med()
                    clean_db = pd.DataFrame(user_result, columns=["SALTS"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")





    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        st.selectbox("Your Gender", ["Male", "Female", "Others"])
        Age = st.text_input("Age")

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
            st.balloons()


if __name__ == '__main__':
    main()