#!/usr/bin/env python3
import requests
import socket


class AwsHostInfoService(object):
    @staticmethod
    def get_ip():
        try:
            print("AWSHostInfoService.get_ip()")
            # Step 1: Get the metadata token
            token_response = requests.put(
                "http://169.254.169.254/latest/api/token",
                headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}, timeout=5
            )
            token_response.raise_for_status()
            print("token", token_response)
            token = token_response.text.strip()  # Ensure token is a proper string
            if not token:
                print("token not found")
                raise ValueError("No token received from metadata service.")

            # Step 2: Use the token to get the IP address
            ip_response = requests.get(
                "http://169.254.169.254/latest/meta-data/local-ipv4",
                headers={"X-aws-ec2-metadata-token": token}, timeout=5
            )
            ip_response.raise_for_status()
            print("ip_response", ip_response)
            print("IP : ", ip_response.text)
            return ip_response.text

        except requests.RequestException as req_err:
            print(f"Error retrieving IP from metadata service: {req_err}")
            return None
        except ValueError as val_err:
            print("Value error metadata service", val_err)
            return None


class LocalHostInfoService(object):
    @staticmethod
    def get_ip():
        print("LocalHostInfoService.get_ip()")
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip


class DockerHostInfoService(object):
    @staticmethod
    def get_ip():
        print("DockerHostInfoService.get_ip()")
        return "host.docker.internal"


class LoopBackHostInfoService(object):
    @staticmethod
    def get_ip():
        print("LoopBackHostInfoService.get_ip()")
        return "127.0.0.1"


print(LocalHostInfoService.get_ip())
