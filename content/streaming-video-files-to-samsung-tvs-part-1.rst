Streaming video files to Samsung TVs (Part 1)
#############################################
:date: 2012-05-12 18:31
:author: Thomas Weininger
:category: Free Software
:tags: DLNA, Linux, NAS, Samsung TV, Serviio
:slug: streaming-video-files-to-samsung-tvs-part-1

|image0|

I have a huge video archive on my NAS and I wanted to be able to stream
the files to my Samsung TV UE40D6300 using its DLNA capability. Because
TVs in general and the DLNA standard especially do not support many
codecs it was clear to me that this goal may not be that easy to
achieve.

I thought transcoding would solve my codec problems, so I installed
`Mediatomb`_ on my NAS. Unfortunately it hasn't. Instead It brought me
some new problems. Suddenly I wasn't able to use the fast-forward
function anymore. Furthermore I didn't like Mediatomb much, as it seems
the developers stopped working on this project. So I searched for
alternatives. `MiniDLNA`_ was a promising candidate, but it didn't
support on-the-fly transcoding like Mediatomb did and I even noticed
that some files that would play fine on my TV without any transcoding
don't work with miniDLNA. It was clear that miniDLNA couldn't offer the
functionality I needed.

For a long time I had no real solution for these issues and so my search
for a better mediaserver continued. Finally I found a new project called
`Serviio`_. It hasn't been released under Open Source license yet, but
it seemed to have (nearly) all the features I was searching for. It
supports transcoding while it is still possible to jump forwards and
backwards in many movies. Using profiles Serviio is able to adjust its
behaviour depending on what client hardware you use. And Serviio even
detects your hardware and sets the matching profile automatically.
That's how software should work wherever possible - without any
intervention of its user. Of course Serviio isn't perfect yet, eg. it
seems to have problems with huge collections, but it's better than
anything I've tried before. I strongly encourage everyone having similar
problems to try Serviio out. It's a great piece of software.

Basically I was happy with my setup. I was able to watch all my movies
from my NAS on my TV. But on-the-fly transcoding has a downside that
still hindered the perfect streaming experience. It wasn't possible to
use fast-forward wherever transcoding was necessary. I had to find out
which codecs and which container formats my Samsung TV is able to play
over DLNA, so I prepared a series of testvideos with different video and
audio codecs and different container formats on my NAS to test it out.

The results of my investigations and my final approach for solving my
streaming issues will be subject of my next posts.

.. _Mediatomb: http://mediatomb.cc/
.. _MiniDLNA: http://sourceforge.net/projects/minidlna/
.. _Serviio: http://www.serviio.org/

.. |image0| image:: http://blog.weinimo.de/wp-content/uploads/2012/05/logo1-300x79.png
   :target: http://blog.weinimo.de/wp-content/uploads/2012/05/logo1.png
