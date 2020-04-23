import sys

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL


# app._static_folder = './static'
#

def sqlcustomer_query1(year1, month1, search_type, account, mysql):
    cur = mysql.connection.cursor()
    year1 = str(year1)[2:]
    print(month1, year1)
    query = """select count(t.trans_id) as count from transaction t where t.trans_month= %s and t.trans_year = %s and account_id =%s"""
    param = (int(month1),int(year1), int(account))
    cur.execute(query, param)
    result = cur.fetchall()
    cur.close()
    result = list(result)[0]['count']
    print('res is :', result)
    return result

def sqlcustomer_query2(year1, month1, search_type, account,mysql):
    cur = mysql.connection.cursor()
    year1 = str(year1)[2:]
    query2 = "select t.trans_id, t.amount, t.balance, t.type, t.date from transaction t where t.trans_month= %s && t.trans_year = %s && account_id =%s"
    param = (int(month1), int(year1), int(account))
    cur.execute(query2, param)
    result = cur.fetchall()
    cur.close()
    print('res is :', result)
    print(type(result))
    result = list(result)
    print(result)
    return result


def sqladmin_query(req,mysql):
    query_id = int(req.get('queryID'))
    res = None
    if query_id == 1:
        print ('request in admin query :', req)
        return sqladmin_query1(req,mysql)
    if query_id == 2:
        print('request in admin query :', req)
        return sqladmin_query2(req,mysql)
    if query_id == 3:
        print('request in admin query :', req)
        return sqladmin_query3(req,mysql)
    if query_id == 4:
        print('request in admin query :', req)
        return sqladmin_query4(req,mysql)
    if query_id == 5:
        print('request in admin query :', req)
        return sqladmin_query5(req,mysql)
    if query_id == 6:
        print('request in admin query :', req)
        return sqladmin_query6(req,mysql)
#
#Query the number of transactions by district and time 对的
def sqladmin_query1(req,mysql):
    print(req)
    cur = mysql.connection.cursor()
    year = int(req['year'])
    year1 = str(year)[2:]
    month = int(req['month'])
    district_id = req['dist']
    adminquery1 = """select d.district_name as dist, count(d.district_id) as count, t.trans_month, t.trans_year from account a, transaction t, district d where a.account_id = t.account_id and t.trans_month = %s and t.trans_year = %s and a.district_id = d.district_id group by d.district_id, t.trans_year, t.trans_month, d.district_name having d.district_id = %s"""
    param = (int(month), int(year1),int(district_id))
    cur.execute(adminquery1, param)
    result = cur.fetchall()
    cur.close()
    print('res is :', result)
    print(type(result))
    result = list(result)
    print(result)
    return result

# 2.Query the number of transactions by account_id
def sqladmin_query2(req,mysql):
    print('admin query 2 req is: ',req)
    cur = mysql.connection.cursor()
    account_id = req.get('account_id')
    adminquery2 = """select count(t.trans_id)as count from transaction t where t.account_id =%s"""
    param = (int(account_id),)
    print(type(account_id))
    cur.execute(adminquery2, param)
    result = cur.fetchall()
    cur.close()
    print('admin query2 res is :', result)
    print(type(result))
    result = list(result)
    print(result)
    return result
#
# 3.Query the number of customers by different age_range and loan ability
def sqladmin_query3(req,mysql):
    print(req)
    cur = mysql.connection.cursor()
    status = req['status']
    age_range = int(req['age_range'])
    age_left = 0
    age_right = 0
    if age_range == 1:
        age_left = 0
        age_right = 25
    if age_range == 2:
        age_left = 26
        age_right = 50
    if age_range == 3:
        age_left = 51
        age_right = 75
    if age_range == 4:
        age_left = 76
        age_right = sys.maxsize
    adminquery3 = "select count(f.client_id ) as count from fact_table f where f.status= %s && f.age >= %s && f.age <= %s"
    param = (status, age_left, age_right)
    cur.execute(adminquery3, param)
    result = cur.fetchall()
    cur.close()
    print('res is :', result)
    print(type(result))
    result = list(result)
    print(result)
    return result

# 4.Query the number of transactions by different region:
# MySQLdb._exceptions.ProgrammingError: not all arguments converted during bytes formatting
def sqladmin_query4(req,mysql):
    cur = mysql.connection.cursor()
    region = req['region']
    adminquery4 = "select count(t.trans_id)as count from transaction t, district d, account a where d.region = %s and t.account_id = a.account_id and a.district_id = d.district_id"
    param = (region,)
    cur.execute(adminquery4, param)
    result = cur.fetchall()
    cur.close()
    print('res is :', result)
    print(type(result))
    result = list(result)
    print(result)
    return result

#5.Query the number of customers by different district and gender
def sqladmin_query5(req,mysql):
    cur = mysql.connection.cursor()
    gender = req['gender']
    district_id = req['dist']
    adminquery5 = "select d.district_name as dist, count(f.client_id )as count from fact_table f ,district d where f.gender= %s && d.district_id =%s group by 1"
    param = (gender, int(district_id))
    cur.execute(adminquery5, param)
    result = cur.fetchall()
    cur.close()
    print('res is :', result)
    print(type(result))
    result = list(result)
    print(result)
    return result


# 6.Query the number of customers by different region
# MySQLdb._exceptions.ProgrammingError: not all arguments converted during bytes formatting
def sqladmin_query6(req,mysql):
    cur = mysql.connection.cursor()
    region = req['region']
    adminquery6 = "select count(c.client_id)as count from client c, district d where c.district_id = d.district_id && d.region = %s"
    param = (region,)
    cur.execute(adminquery6, param)
    result = cur.fetchall()
    cur.close()
    print('res is :', result)
    print(type(result))
    result = list(result)
    print(result)
    return result


def get_district(mysql):
    cur = mysql.connection.cursor()
    cur.execute("select d.district_id as id, d.district_name as name from district d ")
    result = cur.fetchall()
    cur.close()
    print('res is :', result)
    return list(result)

def get_region(mysql):
    cur = mysql.connection.cursor()
    cur.execute("select distinct (d.region) as region from district d ")
    result = cur.fetchall()
    cur.close()
    print('res is :', result)
    return list(result)




