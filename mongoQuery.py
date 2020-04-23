from pymongo import MongoClient

# --------------------------------------------------------- #
#                     MongoDB connection                    #
# --------------------------------------------------------- #
# Get MongoDB instance
client = MongoClient('localhost', 27017)
# Get the target database 'bank'
bank = client.bank

# Get all collections
account = bank.account
client_set = bank.client_set  # 为了和上面的client = MongoClient('localhost', 27017)区分开
disp = bank.disp
district = bank.district
loan = bank.loan
trans = bank.trans
district_account_trans = bank.district_account_trans


# --------------------------------------------------------- #
#                         MongoDB APIs                      #
# --------------------------------------------------------- #
# Customer
# Customer Query 1 - Query the number of transaction of current account_id by trans_month and trans_year
def get_user_trans_amount_mongo(account_id, month, year):
    pipeline = [{"$match": {"trans_month": month, "trans_year": year, "account_id": account_id}},
                {"$group": {"_id": "$account_id", 'count': {'$sum': 1}}}]

    trans_amount = trans.aggregate(pipeline)

    trans_amount_list = list(trans_amount)

    return trans_amount_list[0]["count"]


# Customer Query 2 - Query all information of transactions of the current user by given month and year
def get_user_trans_info_mongo(account_id, month, year):
    trans_info = trans.find({"trans_month": month, "trans_year": year, "account_id": account_id},
                            {"_id": 0, "trans_id": 1, "amount": 1, "balance": 1, "type": 1, "date": 1})

    trans_info_list = list(trans_info)

    return trans_info_list


# Bank
# Bank Query 1 - Query the number of transactions by district_name and time(trans_month/trans_year)
def get_district_trans_amount_mongo(district_id, month, year):
    district_id = int(district_id)
    pipeline = [{"$match": {"trans_month": month, "trans_year": year, "district_id": district_id}},
                {"$group": {"_id": {"dist": "$district_name", "month": "$trans_month", "year": "$year"},
                            'count': {'$sum': 1}}}]

    trans_amount = district_account_trans.aggregate(pipeline)
    trans_amount_list = list(trans_amount)

    id_dict = trans_amount_list[0]['_id']
    count_dict = {'count': trans_amount_list[0]['count']}

    temp_dict = {}
    temp_dict.update(id_dict)
    temp_dict.update(count_dict)

    del temp_dict["month"]
    del temp_dict["year"]

    result = [temp_dict]

    return result


# Bank Query 2 - Query the number of transactions by account_id
def get_admin_trans_amount_mongo(account_id):
    pipeline = [{"$match": {"account_id": account_id}},
                {"$group": {"_id": "$account_id", 'count': {'$sum': 1}}}]

    trans_amount = district_account_trans.aggregate(pipeline)
    trans_amount_list = list(trans_amount)

    return trans_amount_list


# Bank Query 3 - Query the number of customers by different age range and loan status
def get_user_loan_info_mongo(age_range, loan_status):
    pipeline = [{"$lookup": {"from": "client_set",
                             "localField": "client_id",
                             "foreignField": "client_id",
                             "as": "client"}},
                {"$lookup": {"from": "loan",
                             "localField": "account_id",
                             "foreignField": "account_id",
                             "as": "loan"}},
                {"$unwind": "$client"},
                {"$addFields": {"age_range": "$client.age_range"}},
                {"$unwind": "$loan"},
                {"$addFields": {"status": "$loan.status"}},
                {"$match": {"age_range": age_range, "status": loan_status}},
                {"$group": {"_id": {"status": "$status", "age_range": "$age_range"}, 'count': {'$sum': 1}}}]

    user_loan_info = disp.aggregate(pipeline)
    user_loan_info_list = list(user_loan_info)
    return user_loan_info_list


# Bank Query 4 - Query the number of transactions by different region
def get_region_trans_amount_mongo(region):
    pipeline = [{"$match": {"region": region}},
                {"$group": {"_id": {"region": "$region"}, 'count': {'$sum': 1}}}]

    region_trans_amount = district_account_trans.aggregate(pipeline)
    region_trans_amount_list = list(region_trans_amount)

    id_dict = region_trans_amount_list[0]['_id']
    count_dict = {"count": region_trans_amount_list[0]['count']}

    temp_dict = {}
    temp_dict.update(id_dict)
    temp_dict.update(count_dict)
    result = [temp_dict]

    return result


# Bank Query 5 - Query the number of customers by different district and gender
def get_district_gender_amount_mongo(district_id, gender):
    pipeline5 = [{"$lookup": {"from": "district",
                              "localField": "district_id",
                              "foreignField": "district_id",
                              "as": "district"}},
                 {"$unwind": "$district"},
                 {"$addFields": {"district_name": "$district.district_name"}},
                 {"$unwind": "$district"},
                 {"$addFields": {"district_id": "$district.district_id"}},
                 {"$match": {"district_id": district_id, "gender": gender, }},
                 {"$group": {"_id": {"dist": "$district_name", "gender": "$gender"}, 'count': {'$sum': 1}}}]

    district_gender_amount = client_set.aggregate(pipeline5)
    district_gender_amount_list = list(district_gender_amount)

    id_dict = district_gender_amount_list[0]["_id"]
    count_dict = {"count": district_gender_amount_list[0]["count"]}

    result_dict = {}
    result_dict.update(id_dict)
    result_dict.update(count_dict)
    result = [result_dict]

    return result


# Bank Query 6 - Query the number of customers by different region
def get_user_region_amount_mongo(region):
    pipeline = [{"$lookup": {"from": "district",
                             "localField": "district_id",
                             "foreignField": "district_id",
                             "as": "district"}},
                {"$unwind": "$district"},
                {"$addFields": {"region": "$district.region"}},
                {"$match": {"region": region}},
                {"$group": {"_id": {"region": "$region"}, 'count': {'$sum': 1}}}]

    user_district_amount = client_set.aggregate (pipeline)
    user_district_amount_list = list (user_district_amount)

    return user_district_amount_list


# Get a list of districts with corresponding district_id
def get_district():
    dist = district.find({}, {"_id": 0, "district_id": 1, "district_name": 1})

    district_list = list(dist)

    for item in district_list:
        item['id'] = item['district_id'];
        item['name'] = item['district_name']

        del item['district_id']
        del item['district_name']

    return district_list


# Get a list of regions
def get_region():
    region = district.find({}, {"_id": 0, "region": 1}).distinct("region")

    region_list = []

    for item in region:  # item -> 'Prague'
        temp_dict = {"region": item}
        region_list.append(temp_dict)

    return region_list