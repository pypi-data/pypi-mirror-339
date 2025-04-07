import re
import json
import random
import string
import datetime

def test_regex(pattern, test_string):
    try:
        regex = re.compile(pattern)
        matches = regex.findall(test_string)
        
        if not matches and regex.search(test_string):
            # If no groups but there is a match
            matches = [regex.search(test_string).group(0)]
            
        return matches
    except re.error as e:
        raise Exception(f"Invalid regex pattern: {str(e)}")

def generate_db_data(data_type="users", count=10, output_format="json"):
    generators = {
        "users": generate_user_data,
        "products": generate_product_data,
        "orders": generate_order_data
    }
    
    if data_type not in generators:
        raise Exception(f"Unknown data type: {data_type}. Available types: {', '.join(generators.keys())}")
    
    data = generators[data_type](count)
    
    formatters = {
        "json": format_as_json,
        "sql": format_as_sql,
        "csv": format_as_csv
    }
    
    if output_format not in formatters:
        raise Exception(f"Unknown output format: {output_format}. Available formats: {', '.join(formatters.keys())}")
    
    return formatters[output_format](data, data_type)

def generate_user_data(count):
    users = []
    domains = ["example.com", "test.org", "domain.net", "mail.com"]
    
    for i in range(1, count + 1):
        first_name = random.choice(["John", "Jane", "Bob", "Alice", "Sam", "Emma", "Tom", "Lisa", "Mike", "Sarah"])
        last_name = random.choice(["Smith", "Jones", "Brown", "Johnson", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson"])
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        
        users.append({
            "id": i,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "age": random.randint(18, 65),
            "created_at": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        })
    
    return users

def generate_product_data(count):
    products = []
    categories = ["Electronics", "Clothing", "Books", "Home", "Sports", "Food", "Toys"]
    
    for i in range(1, count + 1):
        name = f"Product-{i}"
        category = random.choice(categories)
        
        products.append({
            "id": i,
            "name": name,
            "category": category,
            "price": round(random.uniform(10, 1000), 2),
            "stock": random.randint(0, 100),
            "created_at": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        })
    
    return products

def generate_order_data(count):
    orders = []
    statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    
    for i in range(1, count + 1):
        user_id = random.randint(1, 100)
        order_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
        
        orders.append({
            "id": i,
            "user_id": user_id,
            "status": random.choice(statuses),
            "total": round(random.uniform(20, 500), 2),
            "items": random.randint(1, 10),
            "order_date": order_date.strftime("%Y-%m-%d"),
            "delivery_date": (order_date + datetime.timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d")
        })
    
    return orders

def format_as_json(data, data_type):
    return json.dumps(data, indent=2)

def format_as_sql(data, data_type):
    sql_statements = []
    
    for item in data:
        columns = ", ".join(item.keys())
        placeholders = ", ".join([f"'{str(value)}'" for value in item.values()])
        sql = f"INSERT INTO {data_type} ({columns}) VALUES ({placeholders});"
        sql_statements.append(sql)
    
    return "\n".join(sql_statements)

def format_as_csv(data, data_type):
    if not data:
        return ""
    
    headers = ",".join(data[0].keys())
    rows = [",".join([str(value) for value in item.values()]) for item in data]
    
    return headers + "\n" + "\n".join(rows) 