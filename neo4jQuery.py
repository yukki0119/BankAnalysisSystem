from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j123456"))


def customer_query(year, month, search_type, account_id):
    # print('in customer_query function')
    if search_type == 1:
        with driver.session() as session:
            return session.read_transaction(search_num_of_trans, month, year, account_id)
    if search_type == 2:
        with driver.session() as session:
            return session.read_transaction(search_trans_info, month, year, account_id)


def search_num_of_trans(tx, month, year, account_id):
    # print('in search_num_of_trans function')
    month_larger = month + 1
    year_larger = year
    if month == 12:
        month_larger = 1
        year_larger = year + 1
    # print('year_larger', year_larger, 'month_larger :', month_larger)
    # print(account_id)
    result = tx.run("Match (a:account)-[r:made]->(t:trans) where t.date >= date({year:{year}, month:{month}}) and "
                    "t.date < date({year:{year_larger}, month:{month_larger}}) and a.account_id={acc} return count("
                    "t)", year=year, month=month, year_larger=year_larger, month_larger=month_larger,acc=account_id)
    count = [record["count(t)"] for record in result]
    return count[0]


def search_trans_info(tx, month, year, account_id):
    month_larger = month + 1
    year_larger = year
    if month == 12:
        month_larger = 1
        year_larger = year + 1
    result = tx.run("Match (a:account)-[r:made]->(t:trans) where t.date >= date({year:{year}, month:{month}}) and "
                    "t.date < date({year:{year_larger}, month:{month_larger}}) and a.account_id={acc} return t.trans_id, t.amount, t.balance, t.type, t.date"
                    , year=year, month=month, year_larger=year_larger, month_larger=month_larger,acc=account_id)
    # print([record["t.trans_id"], record["t.amount"], record["t.balance"], record["t.type"], record["t.date"] for record in result])
    data = result.data()
    return data