#!/usr/bin/env python3
""" Py script that provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_logs = client.logs.nginx

    print(nginx_logs.count_documents({}), "logs")
    print("Methods:")
    print("\tmethod GET:", nginx_logs.count_documents({"method": "GET"}))
    print("\tmethod POST:", nginx_logs.count_documents({"method": "POST"}))
    print("\tmethod PUT:", nginx_logs.count_documents({"method": "PUT"}))
    print("\tmethod PATCH:", nginx_logs.count_documents({"method": "PATCH"}))
    print("\tmethod DELETE:", nginx_logs.count_documents({"method": "DELETE"}))
    print(nginx_logs.count_documents({"method": "GET", "path": "/status"}),
          "status check")

    print('IPs:')
    pipe = [
            {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
    ]
    popular = list(nginx_logs.aggregate(pipe))
    for ip in popular:
        print('\t{}: {}'.format(ip['_id'], ip['count']))
