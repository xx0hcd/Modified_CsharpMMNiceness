# Modified_CsharpMMNiceness
modified https://github.com/fullmetalcache/CsharpMMNiceness to support msf5 options.

Great code by fullmetalcache. I added options to use msf5 encrypt and use custom SSL certs in https payloads.

example:
python mod_nice.py -a x64 -P https -l 127.0.0.1 -p 443 -e aes256 -k test123 -ssl msfkey.pem -s
