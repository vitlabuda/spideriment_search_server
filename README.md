# Spideriment Search Server
**Spideriment Search Server** is a proof-of-concept search server for the [Spideriment](https://github.com/vitlabuda/spideriment) web crawler.
It listens on a [MsgESS-wrapped](https://github.com/vitlabuda/msgess-python) Unix socket, accepting search queries from local clients and returning ranked search results.

The server performs the searches in a [Spideriment](https://github.com/vitlabuda/spideriment) web index CSV file.
It should be noted that the whole index is permanently loaded in memory in order to speed up searches, so the server can be very RAM-intensive.



## Usage

### 1. Requirements
   * **Linux**
   * **Python 3.7+**
   
   The program was tested in Python 3.7 (Debian 10) and Python 3.8 (Ubuntu 20.04).


### 2. Change the configuration to fit your needs
   The server's configuration can be changed in the **[Settings.py](src/Settings.py)** file.


### 3. Run the server
   The bash script [run_spideriment_search_server.sh](src/run_spideriment_search_server.sh) prepares the runtime environment and then runs the program:
   ```
   ./run_spideriment_search_server.sh
   ```

   You can also install a [systemd service](src/spideriment_search_server.service) to be able to run the server automatically on startup (on Linux distributions that use systemd).



## Licensing
This project is licensed under the 3-clause BSD license. See the [LICENSE](LICENSE) file for details.

Written by [Vít Labuda](https://vitlabuda.cz/).
