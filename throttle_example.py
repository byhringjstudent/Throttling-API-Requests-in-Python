import requests
import time
import json

def throttled_api_call(url, headers, max_requests_per_second, num_requests, output_file):
    """
    Makes an API call with throttling to respect rate limits and saves responses to a JSON file.

    Args:
        url (str): The URL of the API endpoint.
        headers (dict): The headers for the API call, including the authentication token.
        max_requests_per_second (int): The maximum number of requests allowed per second.
        num_requests (int): The number of requests to make before stopping.
        output_file (str): The file path to save the JSON responses.
    """

    min_delay_between_requests = 1 / max_requests_per_second
    responses = []

    for i in range(num_requests):
        try:
            response = requests.get(url, headers=headers)
            print(f"Request {i + 1}: Status Code = {response.status_code}")
            print(f"Response Text: {response.text}")

            if response.status_code == 403:
                reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))  # Fallback to 60 seconds
                wait_time = reset_time - time.time()
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
                time.sleep(wait_time)
                continue

            response.raise_for_status() 
            responses.append(response.json())
            time.sleep(min_delay_between_requests)

        except requests.exceptions.RequestException as e:
            print(f"Error making API call: {e}")
            break

    with open(output_file, 'w') as f:
        json.dump(responses, f, indent=4)

    print(f"Responses saved to {output_file}")


api_url = "https://api.github.com" 
headers = {
    "Authorization": "token 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"
}
throttled_api_call(api_url, headers, 5, 10, 'api_responses.json')  # 5 requests per second, 10 requests total, save to 'api_responses.json'
