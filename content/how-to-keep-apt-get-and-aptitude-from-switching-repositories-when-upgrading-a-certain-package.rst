How to keep apt-get and aptitude from switching repositories when upgrading a certain package
#############################################################################################
:date: 2012-05-17 18:30
:author: Thomas Weininger
:category: Free Software
:tags: APT, Debian, Linux
:slug: how-to-keep-apt-get-and-aptitude-from-switching-repositories-when-upgrading-a-certain-package

Today, after the usual

.. code:: text

    apt-get update; apt-get upgrade

procedure on my Debian box, I noticed that FFMPEG wasn't working as
expected anymore. It happend that the upgrade installed a new version of
FFMPEG from the official Debian repositories, while I had used the
deb-multimedia.org repository for this package before. The official
Debian package lacks support for libfaac. However, I had to switch back
to the old package. Here is how I've done this.

APT allows to set priorities for certain repositories and packages.
Debian calls this feature "APT pinning".Â All I had to do was to set the
priority for the FFMPEG related packages from deb-multimedia.org to
values >1000 to make apt always install FFMPEG from there. To do this,
just create a new file inÂ /etc/apt/preferences.d. I called that file
deb-multimedia. Here are the contents of the new file:

.. code:: text

    Package: ffmpeg
    Pin: origin www.debian-multimedia.org
    Pin-Priority: 1001

Basically it says: "Use the www.debian-multimedia.org repository for the
ffmpeg package no matter what.". Debian plans to replace ffmpeg with
libav in future releases, so I additionally made APT never ever install
libav by creating another file inÂ /etc/apt/preferences.d:

.. code:: text

    Package: libav-tools
    Pin: origin ""
    Pin-Priority: -1

Pin-Priority: -1 tells APT to never install that package. After these
few steps it is possible to switch to the old repository by simple
reinstalling the packages. Great work Debian, thank you for this!
