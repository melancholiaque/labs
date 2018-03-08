# Report

### Summary<br>
Repo contains code of `parallel vs sequental` implementation of certain word count in text corpus.<br>
file `naive.py` contains sequental implementation.<br>
files `server.py` and `client.py` containts parallel implementation, besides `settings.py` aids 
one to conviniently configurate connection or text corpus destination.
<br>

### Test<br>
All tests have been run on 10x copies of "War and Peace" by Leo Tolstoy.<br>
Time for naive implementation was measured trivially, whereas measurement for parallel implementation 
was performed by typing appropriate commands in two separate terminals, then hitting <RET> 
on one contatins server startup + time command, then quickly(**sic!!!**) swapping to second term also hitting <RET>
to spawn all 10 processes necessary. Thus parallel implementation shoul yield even better result if measured properly.<br>
<br>
First run<br>
![first run](https://github.com/melancholiaque/labs/blob/master/parallel/zero-lab/result.png)<br>
Second run<br>
![second run](https://github.com/melancholiaque/labs/blob/master/parallel/zero-lab/result2.png)
