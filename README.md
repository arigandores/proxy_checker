# Project Explanation: Proxy Checker

This project is designed to read lists of proxies, test their viability, and save the ones that successfully connect.

## How It Works

The project operates in three main stages:

1.  **Proxy Parsing**:
    *   The `ProxyParser` class located in `core/ProxyParser.py` is responsible for reading proxy lists from text files.
    *   It contains methods to parse different types of proxies:
        *   HTTP proxies from `proxies/http.txt`
        *   SOCKS4 proxies from `proxies/socks4.txt`
        *   SOCKS5 proxies from `proxies/socks5.txt`
    *   Each proxy string (expected to be in `ip:port` format) is transformed into a dictionary format that the `requests` library can use (e.g., `{'http': 'http://proxy_ip:port', 'https': 'https://proxy_ip:port'}` for HTTP proxies, and similarly for SOCKS proxies using `socks5h://` or `socks4a://` schemes).
    *   The `read_proxies()` method in `ProxyParser` consolidates all successfully parsed proxies from these files into a single `queue.Queue` object. If a proxy file is missing or empty, it's skipped.

2.  **Proxy Checking**:
    *   The main script, `main.py`, orchestrates the proxy validation process.
    *   It initializes a `requests.Session` for making HTTP requests.
    *   It retrieves the queue of proxy dictionaries from `ProxyParser().read_proxies().queue`.
    *   The core checking logic is in the `check_proxy(proxy)` function:
        *   This function attempts to make a GET request to `http://httpbin.org/anything` using the provided proxy dictionary. `httpbin.org/anything` is a service that echoes back information about the request, making it a good target for testing connectivity.
        *   If the request is successful (i.e., no exceptions occur), the function returns the original proxy dictionary.
        *   If any `requests.exceptions.ProxyError` or other connection-related exceptions occur, indicating the proxy is not working or is unreachable, the function returns `False`.
    *   To speed up the checking process, a `concurrent.futures.ThreadPoolExecutor` with a maximum of 300 worker threads is used. The `executor.map(check_proxy, proxies)` call applies the `check_proxy` function concurrently to all proxies in the queue.

3.  **Preparing and Saving Good Proxies**:
    *   After the concurrent checking is complete, the `prepare_good_proxies(results)` function in `main.py` processes the outcomes.
    *   It iterates through the list of results returned by the `ThreadPoolExecutor`. If a result is not `False` (meaning the proxy test was successful), it extracts the proxy address string (e.g., `proxy_ip:port`) from the dictionary's `'https'` key by stripping the scheme part (like `https://`).
    *   The `ResultsWriter` class in `core/ResultsWriter.py` is responsible for saving these validated proxy addresses.
        *   When an instance of `ResultsWriter` is created, it automatically creates a new directory inside the `results/` folder. This new directory is named with the current date and time (e.g., `results/[DD.MM.YYYY]_[HH.MM.SS]/`) to keep results from different runs separate.
        *   An empty file named `good.txt` is created within this timestamped directory.
    *   The `main.py` script then iterates through the list of good proxy strings obtained from `prepare_good_proxies` and calls `results_writer.write_to_file(good_proxy)` for each one, appending each good proxy to `good.txt` on a new line.

**In summary:** The script automates the task of sifting through lists of potentially unreliable proxies, testing each one for actual internet connectivity, and then compiling a clean list of working proxies into a timestamped output file.

## How to Run

1.  **Prerequisites**:
    *   Ensure you have Python 3 installed.
    *   Install the necessary library using pip:
        ```bash
        pip install requests
        ```
        (Alternatively, you can install from `requirements.txt`: `pip install -r requirements.txt`)

2.  **Prepare Proxy Lists**:
    *   Populate the files in the `proxies/` directory with your proxy lists:
        *   `proxies/http.txt` for HTTP proxies (one `ip:port` per line).
        *   `proxies/socks4.txt` for SOCKS4 proxies (one `ip:port` per line).
        *   `proxies/socks5.txt` for SOCKS5 proxies (one `ip:port` per line).
    *   If you don't have one type of proxy, you can leave the corresponding file empty or delete it (the script handles missing files).

3.  **Execute the Script**:
    *   Run the main script from the project's root directory:
        ```bash
        python main.py
        ```

## Expected Output

*   The script will not produce much console output while running, as it focuses on processing.
*   Upon completion, a new directory will be created under the `results/` folder. The name of this directory will be the date and time of the run (e.g., `results/[28.07.2024]_[10.30.55]/`).
*   Inside this timestamped directory, a file named `good.txt` will contain all the proxies that were successfully validated. Each working proxy (`ip:port`) will be listed on a new line.
*   If no proxies from your lists are working, `good.txt` will be empty.
