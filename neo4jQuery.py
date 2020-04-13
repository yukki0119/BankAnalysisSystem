import sys

from neo4j import GraphDatabase

driver = GraphDatabase.driver ("bolt://localhost:7687", auth=("neo4j", "neo4j123456"))


def customer_query(year, month, search_type, account_id):
    # print('in customer_query function')
    if search_type == 1:
        with driver.session () as session:
            return session.read_transaction (search_num_of_trans, month, year, account_id)
    if search_type == 2:
        with driver.session () as session:
            return session.read_transaction (search_trans_info, month, year, account_id)


def search_num_of_trans(tx, month, year, account_id):
    # print('in search_num_of_trans function')
    month_larger = month + 1
    year_larger = year
    if month == 12:
        month_larger = 1
        year_larger = year + 1
    # print('year_larger', year_larger, 'month_larger :', month_larger)
    # print(account_id)
    result = tx.run ("Match (a:account)-[r:made]->(t:trans) where t.date >= date({year:{year}, month:{month}}) and "
                     "t.date < date({year:{year_larger}, month:{month_larger}}) and a.account_id={acc} return count("
                     "t)", year=year, month=month, year_larger=year_larger, month_larger=month_larger, acc=account_id)
    count = [record["count(t)"] for record in result]
    return count[0]


def search_trans_info(tx, month, year, account_id):
    month_larger = month + 1
    year_larger = year
    if month == 12:
        month_larger = 1
        year_larger = year + 1
    result = tx.run ("Match (a:account)-[r:made]->(t:trans) where t.date >= date({year:{year}, month:{month}}) and "
                     "t.date < date({year:{year_larger}, month:{month_larger}}) and a.account_id={acc} return "
                     "t.trans_id as trans_id, t.amount as amount, t.balance as balance, t.type as type, t.date as date "
                     , year=year, month=month, year_larger=year_larger, month_larger=month_larger, acc=account_id)
    data = result.data ()
    return data


def admin_query(req):
    query_id = int (req.get ('queryID'))
    res = None
    print ('request in admin query :', req)
    if query_id == 1:
        with driver.session () as session:
            return session.read_transaction (query1, req)
    if query_id == 2:
        with driver.session () as session:
            return session.read_transaction (query2, req)
    if query_id == 3:
        with driver.session () as session:
            return session.read_transaction (query3, req)
    if query_id == 4:
        with driver.session () as session:
            return session.read_transaction (query4, req)
    if query_id == 5:
        with driver.session () as session:
            return session.read_transaction (query5, req)


# Query the number of transactions by district and time: MATCH (t:trans), (a:account)-[:made]->(t:trans),
# (a)-[:BelongTo]->(d:district {district_id:"71"}), (d)-[:Belongto]->(r:region {name:"north Moravia"}) RETURN COUNT (*)
def query1(tx, req):
    print(req)
    district_id = req['dist']
    year = int (req['year'])
    month = int (req['month'])
    month_larger = month + 1
    year_larger = year
    if month == 12:
        month_larger = 1
        year_larger = year + 1
    result = tx.run ("Match (a:account)-[r:made]->(t:trans), (a)-[:BelongTo]->(d:district) where t.date >= date({"
                     "year:{year}, month:{month}}) and t.date < date({year:{year_larger}, month:{month_larger}}) and "
                     "d.district_id={dist} return count(t) as count, d.district_name as dist", year=year, month=month,
                     year_larger=year_larger,
                     month_larger=month_larger, dist=district_id)
    res = result.data ()
    print (res)
    return res


# 2.Query the number of transactions by account_id
# MATCH (m:account {account_id:"576"}),(m)-[:made]->(t:trans) RETURN COUNT(*)
def query2(tx, req):
    account_id = req.get ('account_id')
    result = tx.run ("Match (a:account)-[r:made]->(t:trans) where a.account_id={acc} return count(t) as count", acc=account_id)
    res = result.data ()
    print (res)
    return res


# 3.Query the number of customers by different age_range and loan ability: MATCH (a:account), (a)-[:apply]->(l:loan {
# status:"A"}), (c:client)-[:hold {type:"OWNER"}]->(a) WHERE 0 < c.age AND c.age<= 25 RETURN COUNT (*)
def query3(tx, req):
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
    print(age_left, age_right, status)
    result = tx.run("MATCH (a:account)-[:made]->(l:loan), (c:client)-[h:hold]->(a) WHERE l.status={status} and "
                    "h.type=\"OWNER\" and c.age >= {age_left} AND c.age <= {age_right} RETURN COUNT (c) as count", status=status, age_left=age_left, age_right=age_right)
    res = result.data()
    print(res)
    return res


# 4.Query the number of transactions by different region:
# MATCH (t:trans), (a:account)-[:made]->(t:trans), (a)-[:BelongTo]->(d:district),
# (d)-[:BelongTo]->(r:region {region:"north Moravia"}) RETURN COUNT (*)
def query4(tx, req):
    region = req['region']
    result = tx.run("MATCH (a:account)-[:made]->(t:trans), (a)-[:BelongTo]->(d:district),"
                    "(d)-[:BelongTo]->(r:region) where r.region={region} RETURN COUNT(t) as count", region=region)
    res = result.data()
    print(res)
    return res


# match (n:client{gender:"M"}),(n)-[:BelongTo]->(d:district {district_id:"2"}) RETURN COUNT (*)
def query5(tx, req):
    dist_id = req['dist']
    gender = req['gender']
    result = tx.run("MATCH (n:client)- [:BelongTo] -> (d:district) where n.gender={gender} and d.district_id={dist} "
                    "RETURN COUNT(n) as count, d.district_name as dist", gender=gender, dist=dist_id)
    res = result.data()
    print(res)
    return res


def get_district():
    with driver.session () as session:
        return session.read_transaction (get_district_helper)


def get_district_helper(tx):
    result = tx.run ("Match (d:district) return d.district_id as id, d.district_name as name")
    return result.data ()


def get_region():
    with driver.session () as session:
        return session.read_transaction (get_region_helper)


def get_region_helper(tx):
    result = tx.run ("Match (r:region) return r.region as region")
    return result.data ()
