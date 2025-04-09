##Sepidar Class Documentation##
Overview
The Sepidar class is designed for interacting with the Sepidar search API. It allows users to perform searches and manage search history efficiently.

Example Usage
python
Run
```python
sepidar = Sepidar("Tatlo", page=1)
results = sepidar.search()
print(results)
```
Class Definition

Features
Search Functionality: Perform searches using a specified query and page number.
Dynamic User-Agent: Automatically generates a random User-Agent string for each request.
Search History Management:
Retrieve previous search queries.
Clear search history.
Save search queries to history during searches.
Error Handling
The class handles HTTP errors by checking the response status code and printing an error message if the request fails.
It also catches exceptions related to request failures and prints an appropriate message.
Conclusion
The Sepidar class provides a simple and effective way to interact with the Sepidar search API, making it easy to perform searches and manage search history.