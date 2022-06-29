import mysql.connector
import re
import requests
from bs4 import BeautifulSoup
import time 
def connect(mpage):
    car_y = list()
    car_m = list()
    all_car = list()
    page = 1
    req_tex = str()
    while page != int(mpage)+1:
        req_url ='https://www.truecar.com/used-cars-for-sale/listings/?page={}'.format(page)
        req = requests.get(req_url)
        print('page %i'%page)
        page += 1
        req_tex += '\n' + str(req.text)
    soup = BeautifulSoup( req_tex ,'html.parser')
    car_d = soup.find_all('a',{"data-test":"vehicleCardLink"})
    car_d_l = re.findall('for (\d+.+?)\"', str(car_d))
    car_mil = soup.find_all('div',{"data-test":"vehicleMileage"})
    car_mil_l = re.findall('svg>(.+?)\<',str(car_mil)) 
    car_p=soup.find_all("div",{'data-test':"vehicleCardPricingBlockPrice"})
    car_p_l = re.findall('(\$.+?)\<', str(car_p))
    
    
    car_pi_l = list()
    ni = 1
    for i in car_d_l:
        car_y.append(i[:4].strip())
        car_m.append(i[4:].strip())
    for i in car_p_l:
        car_pi = str(i)
        car_pi = car_pi.replace(',', '')
        car_pi = car_pi[1:]
        car_pi_l.append(car_pi)
    
    all_car = list()    
        
    for i in range(len(car_m)):
        all_car.append((car_m[i],car_y[i],car_mil_l[i],int(car_pi_l[i])))
    all_car=sorted(all_car,key =lambda x:x[3])
    
    return all_car

def in_db(h,u,p,d,info):
    tab = 'show tables;'
    sql ='''CREATE TABLE car(
        car_name CHAR(22) NOT NULL,
        years CHAR(20),
        mile CHAR(20),
        price INT )'''
    select = 'select *from car'
    drop = 'drop table car;'
    table = list()
    data  = list()
    db=mysql.connector.connect(host=h, user=u,password=p,database=d)
    cursor=db.cursor()

    cursor.execute(tab)
    for i in cursor:
        table.append(i[0])
    if 'car' not in table:
        cursor.execute(sql)
        for i in info:
            query = (f'INSERT INTO car VALUE(\'{i[0]}\',\'{i[1]}\',\'{i[2]}\',\'{i[-1]}\')' )
            cursor.execute(query)
            db.commit()        
    else:
        cursor.execute(select)
        for i in cursor:
            data.append(i)
        cursor.execute(drop)
        cursor.execute(sql)
        for i in info:
            data.append((i[0],i[1],i[2],i[3]))

        data = set(data)
        data = list(data)
        data = sorted(data,key= lambda x:x[3])
    
        for i in data:
            query = (f'INSERT INTO car VALUE(\'{i[0]}\',\'{i[1]}\',\'{i[2]}\',\'{i[-1]}\')' )
            cursor.execute(query)
            db.commit()
    return print('successful(database)')
   
def db_ser(h,u,p,d,low,high):
    tab = 'show tables;'
    select = 'select *from car'
    drop = 'drop table car;'
    serch_d= list()
    db=mysql.connector.connect(host=h, user=u,password=p,database=d)
    cursor=db.cursor()
    cursor.execute(select)
    for i in cursor:
        if i[-1] < high and i[-1] > low :
            serch_d.append(i)

    return serch_d

def db_all(h,u,p,d):
    db=mysql.connector.connect(host=h, user=u,password=p,database=d)
    cursor=db.cursor()
    cursor.execute('select *from car;')
    con = 1
    for i in cursor:
        print(f'{con} -> model : {i[0]}\nsale sakht : {i[1]}\tkarkard : {i[2]}\tgheymat : {i[3]}')
        print('_'*15)
        con += 1
    
def start():
    a = '''slm\ndr in code az site truecar etalt 
    mashin hara dar data base sbt kard va gable beroz resani ast
    az shoma etlati grfte mishvad bad az an 
    shoma mitvanid ba gheymate delkhah donbale mashin morde nazar begrdid '''
    print(a,'\n','_'*50)
    print('etlata database khod ra vard konid')
    time.sleep(1)
    h = input('host: ')
    u = input('user: ')
    p = input('password: ')
    d = input('database: ')    
    while True :
        if input('etlat dar database darid ya niyaz be stkhraj darid\n(y/n) :') == 'n':
            c = connect(int(input('chand safhe joste jo shvad?: ')))
            con = 1
            print('etlate zakhire shode: ')
            for i in c:
                print(f'{con} -> model : {i[0]}\nsale sakht : {i[1]}\tkarkard : {i[2]}\tgheymat : {i[3]}')
                print('_'*15)
                con += 1
            in_db(h,u,p,d,c)
            if input('braye khoroj (e) type konid braye edame (Enter): ') == 'e':
                break
        if input('etlat database neshan dade shvd?\n(y/n):  ') == 'y':
            db_all(h,u,p,d)
            
            if input('braye khoroj (e) type konid braye edame (Enter): ') == 'e':
                break
        if input('joste joye mashin?\n(y/n): ') == 'y':
            a =  db_ser(h,u,p,d,int(input('kafe gheymat: ')),int(input('sagfe gheymat: ')))
            con = 1
            for i in a :
                print(f'{con} -> model : {i[0]}\nsale sakht : {i[1]}\tkarkard : {i[2]}\tgheymat : {i[3]}')
                print('_'*15) 
                con += 1               
            if input('braye khoroj (e) type konid braye edame (Enter): ') == 'e':
                break
start()