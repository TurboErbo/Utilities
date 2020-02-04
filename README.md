# Utilities
Useful little programs to help get you through the day.

1. file_split.py
Splits a large file into parts. 
Partial files are created in the same directory as the original file, with ".partN" appended to the file name.
The default chunk size is 100MB.
Usage: python file_split.py filename [chunk_size] [max_parts]

2. shadowsocks_helper.py
Automates changing the Elastic IP address of my AWS shadowsocks server (after it gets blocked by the Great Firewall of China).
Error handling very rudimentary.
The script will also update the saved server IP in shadowsocks client's config file. To-do: restart the client program after writing to the file.
