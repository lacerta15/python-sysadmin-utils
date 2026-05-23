#!/usr/bin/env python3
"""Cloudera Manager API client utilities."""
import requests
import json
import os

class ClouderaClient:
    def __init__(self, host, user="admin", password="admin", version="v51"):
        self.base = f"http://{host}:7180/api/{version}"
        self.auth = (user, password)
        self.headers = {"Content-Type": "application/json"}

    def get(self, path):
        r = requests.get(f"{self.base}{path}", auth=self.auth, verify=False)
        r.raise_for_status()
        return r.json()

    def post(self, path, data=None):
        r = requests.post(f"{self.base}{path}", auth=self.auth,
                         json=data, headers=self.headers, verify=False)
        r.raise_for_status()
        return r.json()

    def list_clusters(self):
        return self.get("/clusters")["items"]

    def cluster_services(self, cluster):
        return self.get(f"/clusters/{cluster}/services")["items"]

    def restart_service(self, cluster, service):
        return self.post(f"/clusters/{cluster}/services/{service}/commands/restart")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("host")
    p.add_argument("--user",     default="admin")
    p.add_argument("--password", default="admin")
    args = p.parse_args()

    cm = ClouderaClient(args.host, args.user, args.password)
    clusters = cm.list_clusters()
    for c in clusters:
        print(f"Cluster: {c['name']} ({c['clusterType']})")
        for svc in cm.cluster_services(c['name']):
            print(f"  {svc['name']:30s} {svc['serviceState']}")
