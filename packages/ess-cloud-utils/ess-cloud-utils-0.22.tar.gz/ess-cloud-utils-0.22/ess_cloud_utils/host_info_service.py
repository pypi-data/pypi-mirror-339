#!/usr/bin/env python3
import requests
import socket


class AwsHostInfoService(object):
    @staticmethod
    def get_ip():
        try:
            # Step 1: Get the metadata token
            token_response = requests.put(
                "http://169.254.169.254/latest/api/token",
                headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
                timeout=2
            )
            token_response.raise_for_status()
            token = token_response.text
            print("Token : ", token)

            # Step 2: Use the token to get the IP address
            ip_response = requests.get(
                "http://169.254.169.254/latest/meta-data/local-ipv4",
                headers={"X-aws-ec2-metadata-token": token},
                timeout=2
            )
            ip_response.raise_for_status()
            print("IP : ", ip_response.text)
            return ip_response.text

        except requests.RequestException as e:
            print(f"Error retrieving IP from metadata service: {e}")
            return None


class LocalHostInfoService(object):
    @staticmethod
    def get_ip():
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip


class DockerHostInfoService(object):
    @staticmethod
    def get_ip():
        return "host.docker.internal"


class LoopBackHostInfoService(object):
    @staticmethod
    def get_ip():
        return "127.0.0.1"


print(LocalHostInfoService.get_ip())
