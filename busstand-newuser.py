from flask import Flask,render_template,request,url_for,redirect,abort,flash
import busstanddatabaseconnection as bsd
import allbusdatabase as abd
import newuserdb as ns
import time
from mysql.connector import pooling
import sampledb as sd
import random


app = Flask(__name__,static_folder='static')
app.secret_key = 'my_secret_key'

cnxpool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=32,
    host="localhost",
    user="root",
    password="",
    database="btsuserlogin"
)
   
#bsd.cur.execute("use busstand")
#bsd.cur.execute("create table new(name varchar(20))")
#print(bsd.cur.execute("show tables"))
global dbs 
dbs = ns.db
global ofs
ofs = 'newofficeuser'
global tb1,tb2,dbnm
tb1 = abd.db
tb2 = abd.db1
tb3 = abd.db2
dbnm = abd.dbname

# Root of the program 

@app.route("/")
def olduser():
    return render_template("projectinterface.html")


# office - office new user html file call

@app.route("/officenewuser",methods = ['post','get'])
def officenewuser():
  #  time.sleep(3)
    return render_template("officenewuser.html")
  #  @app.route("/newuserlogin",methods = ['post','get'])
   # def newuserlogin():
   #     return render_template("projectinterface.html")
    
@app.route("/newuserinuser",methods = ['post','get'])
def newuserinuser():
    return render_template("newuserinuser.html")


# user - user login after successful registration

@app.route("/userlogin",methods = ['post','get'])
def userlogin():
    return render_template("projectinterface.html")
    
  # Bus availability  

@app.route("/busavail",methods = ['post','get'])
def busavail():
    r = request.form.to_dict()
    busno = r['bus_no']
    busname = r['bus_name']
    rtfrom = r['route_from']
    rtto = r['route_to']
    bstime = r['bus_time']
    return busno

# dummy

@app.route("/newofficeuserentry",methods = ['post','get'])
def newofficeuserentry():
    r = request.form.to_dict()
    distr  = r['dis']
    dname = r['dpname']
    name = r['nam']
    jb = r['jbr']
    id = r['idno']
    ads = r['addr']
    pn = r['pno']
    ps = r['ps2']
    pds = r['ps3']

    if ps == pds:
       # bsd.cur.execute(f"create database {name}")
        bsd.cur.execute(f"use {dbs}")
        bsd.cur.execute(f"insert into {ofs}(dist,dpname,name,jbrle,idno,addr,pno,ps1,cps) value(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(distr,dname,name,jb,id,ads,pn,ps,pds))
        bsd.mydb.commit()
    else:
        return render_template("newpassvalidate.html")
    return render_template("login1.html")

# office user validation 
@app.route('/officevalidation', methods = ['get','post'])
def officevalidation():
    r = request.form.to_dict()
    usname1 = r['us1']
    pswd1 = r['ps']
    
    def execute_query(usname, pswd):
    # Get a connection from the pool
        cnx = cnxpool.get_connection()

    # Get a cursor to interact with the database
        cursor = cnx.cursor()

    # Define the query to retrieve the user's data
        cursor.execute(f'use {dbs} ')
        cursor.execute(f'select name,ps1 from newofficeuser where name = %s && ps1 = %s',(usname,pswd))
        result = cursor.fetchone()

        if result is not None:
            return  render_template('busavailall.html',usname=usname) 
        else:
            mes = 'CHECK YOUR USERNAME AND PASSWORD '
            return render_template('projectinterface.html',mes=mes)
        

    return execute_query(usname1,pswd1)
# staff validation 

@app.route('/staffvalidation', methods = ['get','post'])
def staffvalidation():
    r = request.form.to_dict()
    sfname = r['sfname']
    pno = r['pno']
    
    def execute_query(usname, pswd):
    # Get a connection from the pool
        cnx = cnxpool.get_connection()

    # Get a cursor to interact with the databases
        cursor = cnx.cursor()

    # Define the query to retrieve the user's data
        cursor.execute(f'use {dbnm} ')        
        cursor.execute(f'select Name,pno from newemreg where Name = %s && pno = %s',(usname,pswd))
        result = cursor.fetchone()
        cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        res = cursor.fetchall()
        cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        jbs = cursor.fetchone()[2]
        cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        res = cursor.fetchall()
        cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        idn = cursor.fetchone()[3]
        cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        res = cursor.fetchall()
        cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        dn = cursor.fetchone()[4]
        cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        res = cursor.fetchall()
        cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        ds = cursor.fetchone()[7]
        # cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        # res = cursor.fetchall()
        # cursor.execute(f'select * from newemreg where pno = "{pswd}"')
        # rs = cursor.fetchone()[2]

        if result is not None:
            return  render_template('staffreason.html',usname=usname,jbs=jbs,idn=idn,dn=dn,ds=ds) 
        else:
            mes = 'CHECK YOUR USERNAME AND PHONE NUMBER '
            return render_template('projectinterface.html',mes=mes)
        

    return execute_query(sfname,pno)



@app.route("/newregemp",methods = ['post','get'])
def newregemp():
    r = request.form.to_dict()
    uname = r['nme']
    email = r['emal']
    jbrs = r['jbr']
    id = r['idno']
    dpn = r['dpname']
    pno = r['p_no']
    addr = r['adrs']
    dst = r['dst']
    tlk = r['tlk']
    vil = r['vlg']
    pcdee = r['pcde']
    ns.cur.execute(f'use {dbnm} ')
    ns.cur.execute(f"insert into {tb1}(Name,e_id,jb,ino,dname,pno,addr,dstr,taluk,vil,pcde) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(uname,email,jbrs,id,dpn,pno,addr,dst,tlk,vil,pcdee))
    ns.mydb.commit()
    return render_template("newemregsuccess.html")
    


@app.route("/busreg",methods = ['post','get'])
def busreg():
    r = request.form.to_dict()
    dst = r['dist']
    t_lk = r['tkl']
    dpn = r['dpname']
    bno = r['busno']
    bsname = r['busname']
    bsfrm = r['busfrom']
    bsto = r['busto']
    bskms = r['bskm']
    btps = r['btp']
    ns.cur.execute(f'use {dbnm} ')
    ns.cur.execute(f"insert into {tb2}(distr,taluk,dpname,bsno,bsname,f_rom,t_o,bskilo,bstype) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(dst,t_lk,dpn,bno,bsname,bsfrm,bsto,bskms,btps))
    ns.mydb.commit()
    return render_template("newemregsuccess.html")


# allotment section 
@app.route('/alotdetail',methods = ['get','post'])
def alotdetail():
    r = request.form.to_dict()
    bnno = r['bno']
    def execute_query(bnno):
    # Get a connection from the pool
        cnx = cnxpool.get_connection()

    # Get a cursor to interact with the database
        cursor = cnx.cursor()

    # Define the query to retrieve the user's data
        cursor.execute(f'use {dbnm} ')
        cursor.execute(f'select * from busreg where bsno = "{bnno}"')
        res = cursor.fetchone()
        

        if res is not None:
            val = res[0]
            val1 = res[2]
            return  render_template('showallotedbus.html',val = val,val1=val1) 
        else:
            return "check user name and password......................"
        

    return execute_query(bnno)
@app.route('/alotmentdetail',methods = ['get','post'])
def alotmentdetail():
    r = request.form.to_dict()
    bsnum = r['bns']
    drnam = r['drn']
    drid = r['drid']
    crnam = r['crn']
    crid = r['crid']
    abd.cur.execute('use allbusinformation')
    abd.cur.execute(f'insert into busalot values(%s,%s,%s,%s,%s)',(bsnum,drnam,drid,crnam,crid))
    abd.mydb.commit()
    return "success added....."

    



@app.route('/busav', methods = ['get','post'])
def busav():
    return render_template('busavailall.html')

# user - new user entry get data from newuserinuser.html

@app.route('/newuserentry', methods = ['get','post'])
def newuserentry():
    r = request.form.to_dict()
    uname = r['nme']
    email = r['emal']
    pno = r['p_no']
    addr = r['adrs']
    dst = r['dst']
    tlk = r['tlk']
    vil = r['vlg']
    pcdee = r['pcde']
    ps = r['pwd1']
    cps = r['pwd2']
    if ps == cps :
        ns.cur.execute(f'use {dbs} ')
        ns.cur.execute(f"insert into {dbs}(Name,email_id,pno,addrs,district,taluk,village,pincode,ps1,cps1) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(uname,email,pno,addr,dst,tlk,vil,pcdee,ps,cps))
        ns.mydb.commit()
    else:
        return render_template("newpassvalidate.html")
    
        
    return render_template('newuserreg.html')

# user - username and password validation and enter into user interface 

@app.route('/uservalidation', methods = ['get','post'])
def uservalidation():
    r = request.form.to_dict()
    usname1 = r['us1']
    pswd1 = r['ps']
    def execute_query(usname, pswd):
    # Get a connection from the pool
        cnx = cnxpool.get_connection()

    # Get a cursor to interact with the database
        cursor = cnx.cursor()

    # Define the query to retrieve the user's data
        cursor.execute(f'use {dbs} ')
        cursor.execute(f'select Name,ps1 from btsuserlogin where Name = %s && ps1 = %s',(usname,pswd))
        result = cursor.fetchone()

        if result is not None:
            return render_template("userinterface.html") 
        else:
            return "check user name and password......................"

    # Close the cursor and connection
        cursor.close()
        cnx.close()

    return execute_query(usname1, pswd1)

@app.route("/update",methods = ['post','get'])
def update():
    dbn6 = 'allbusinformation'
    r = request.form.to_dict()
    dst = r['dis']
    dname = r['dipname']
    blns = r['bolno']
    bno = r['busno']
    bname = r['busname']
    drname = r['busdriname']
    drno = r['busdrino']
    conname = r['busconname']
    bcono  = r['busconno']
    
    abd.cur.execute('use allbusinformation')
    abd.cur.execute(f'select * from busreg where bno ="{blns}"')
    res = abd.cur.fetchall()

    if res is not None:
        abd.cur.execute('use allbusinformation')
        abd.cur.execute(f'update  busreg set distr = "{dst}",dname = "{dname}",bno = "{bno}",bname="{bname}",drname="{drname}",drno="{drno}",crname="{conname}",crno="{bcono}" where bno = "{blns}"')
        abd.mydb.commit()
        return "perfect solved...."
        
    else:
        return "BUS NUMBER NOT AVAILABLE"
        

    

@app.route("/delete",methods = ['post','get'])
def delete():
    r = request.form.to_dict()
    bnno = r['bn']
    abd.cur.execute('use allbusinformation')
    abd.cur.execute(f'delete from busreg where bno ="{bnno}"')
    abd.mydb.commit()
    return "deleted.... successfully..."

@app.route("/empoverview",methods = ['post','get'])
def empoverview():
    r = request.form.to_dict()
    bnno = r['emid']
    def execute_query(bnno):
    # Get a connection from the pool
        cnx = cnxpool.get_connection()

    # Get a cursor to interact with the database
        cursor = cnx.cursor()

    # Define the query to retrieve the user's data
        cursor.execute(f'use {dbnm} ')
        cursor.execute(f'select * from newemreg where ino = "{bnno}"')
        res = cursor.fetchall()

        if res is not None:
            return  render_template('showempdetails.html',res=res) 
        else:
            return "not showing emp details"
        

    return execute_query(bnno)



@app.route("/busoverview",methods = ['post','get'])
def busoverview():
    r = request.form.to_dict()
    bnno = r['bsnos']
    def execute_query(bnno):
    # Get a connection from the pool
        cnx = cnxpool.get_connection()

    # Get a cursor to interact with the database
        cursor = cnx.cursor()

    # Define the query to retrieve the user's data
        cursor.execute('use allbusinformation')
        cursor.execute(f'select * from busreg where bno = "{bnno}"')
        res = cursor.fetchall()
        cursor.execute(f'select * from busreg where bno = "{bnno}"')
        rs = cursor.fetchone()[5]
        cursor.execute(f'select*from newemreg where ino = "{rs}"')
        ng = cursor.fetchall()
        cursor.execute(f'select * from busreg where bno = "{bnno}"')
        rs = cursor.fetchone()[7]
        cursor.execute(f'select*from newemreg where ino = "{rs}"')
        ns = cursor.fetchall()


        if res and ng is not None:
            return  render_template('showbusdetails.html',res=res,ng=ng,ns=ns) 
        else:
            return "not showing emp details"
        

    return execute_query(bnno)


@app.route("/userview",methods = ['post','get'])
def userview():
    r = request.form.to_dict()
    bnno = r['bsn']
    def execute_query(bnno):
    # Get a connection from the pool
        cnx = cnxpool.get_connection()

    # Get a cursor to interact with the database
        cursor = cnx.cursor()

    # Define the query to retrieve the user's data
        cursor.execute('use allbusinformation')
        cursor.execute(f'select * from busreg where bsno = "{bnno}"')
        res = cursor.fetchall()
        
        def choose_random_string(strings):
            if not strings:
                return None
            return random.choice(strings)
        string_list = ["THENDRAL NAGAR", "EB OFFICE", "COLLECTOR OFFICE", "HOSPITAL BYEPASS","MALLAVADI","KONDAM","NAYUDUMANGALAM","KALASAPAKKAM","VASUR","POLUR"]
        random_string = choose_random_string(string_list)

        if res  is not None:
            return  render_template('showuserdetails.html',res=res,random_string = random_string ) 
        else:
            return "not showing emp details"
        

    return execute_query(bnno)

@app.route("/staffreason",methods = ['post','get'])
def staffreason():
    if request.method == 'POST':
        r = request.form.to_dict()
        bsnos = r['bsno']
        res1 = r['accdnt']
       
        if res1 :
            abd.cur.execute('use allbusinformation')
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            drname = abd.cur.fetchone()[1]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            drid= abd.cur.fetchone()[2]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            crname = abd.cur.fetchone()[3]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            crid = abd.cur.fetchone()[4]
            abd.cur.execute(f'insert into busreason values(%s,%s,%s,%s,%s,%s)',(bsnos,drname,drid,crname,crid,res1))
            abd.mydb.commit()

        return "reason  validated...."
    else:
        return render_template('busfaredetails.html')
    


@app.route("/staffreason1",methods = ['post','get'])
def staffreason1():
    if request.method == 'POST':
        r = request.form.to_dict()
        bsnos = r['bsno']
        res1 = r['brkdn']
        
        if res1 :
            abd.cur.execute('use allbusinformation')
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            drname = abd.cur.fetchone()[1]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            drid= abd.cur.fetchone()[2]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            crname = abd.cur.fetchone()[3]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            crid = abd.cur.fetchone()[4]
            abd.cur.execute(f'insert into busreason values(%s,%s,%s,%s,%s,%s)',(bsnos,drname,drid,crname,crid,res1))
            abd.mydb.commit()

        return "reason  validated...."
    else:
        return render_template('busfaredetails.html')
    
@app.route("/staffreason2",methods = ['post','get'])
def staffreason2():
    if request.method == 'POST':
        r = request.form.to_dict()
        bsnos = r['bsno']
        
        res1 = r['cm_iss']
        
        if res1 :
            abd.cur.execute('use allbusinformation')
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            drname = abd.cur.fetchone()[1]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            drid= abd.cur.fetchone()[2]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            crname = abd.cur.fetchone()[3]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            crid = abd.cur.fetchone()[4]
            abd.cur.execute(f'insert into busreason values(%s,%s,%s,%s,%s,%s)',(bsnos,drname,drid,crname,crid,res1))
            abd.mydb.commit()

        return "reason  validated...."
    else:
        return render_template('busfaredetails.html')
    
@app.route("/staffreason3",methods = ['post','get'])
def staffreason3():
    if request.method == 'POST':
        r = request.form.to_dict()
        bsnos = r['bsno']
       
        res1 = r['others']
        if res1 :
            abd.cur.execute('use allbusinformation')
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            drname = abd.cur.fetchone()[1]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            drid= abd.cur.fetchone()[2]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            crname = abd.cur.fetchone()[3]
            abd.cur.execute(f'select*from busalot where busno="{bsnos}"')
            ms = abd.cur.fetchall()
            abd.cur.execute(f'select * from busalot where busno = "{bsnos}"')
            crid = abd.cur.fetchone()[4]
            abd.cur.execute(f'insert into busreason values(%s,%s,%s,%s,%s,%s)',(bsnos,drname,drid,crname,crid,res1))
            abd.mydb.commit()

        return "reason  validated...."
    else:
        return render_template('busfaredetails.html')
        

lst = 0
@app.route('/busfare',methods = ['post','get'])
def  busfare():
    if request.method == 'POST':
        r = request.form.to_dict()
        li = r['f_m']
        ot = r['t_o']
        bsf = r['bf']
        sd.cur.execute('use sample')
        sd.cur.execute(f'insert into faredetails values(%s,%s,%s)',(li,ot,bsf))
        sd.db.commit()
        sd.cur.execute(f'select*from faredetails where f_rom="{li}"')
        ms = sd.cur.fetchall()

        return render_template('showallotedbus.html',ms=ms)
    else:
        return render_template('busfaredetails.html')


if __name__ == "__main__":
    app.run(debug=True)     
