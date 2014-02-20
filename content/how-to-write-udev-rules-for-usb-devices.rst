How to Write udev Rules for USB Devices
#######################################
:date: 2013-04-13 20:26
:author: Thomas Weininger
:category: Free Software
:tags: Linux, udev, USB
:slug: how-to-write-udev-rules-for-usb-devices

|Udev-tux|\ If you use a custom USB device, for which there isn't a
suitable udev rule installed on your system yet, you might notice that
only the root user has read and write access for it. In order to make it
usable for every user you need to write a new udev rule. Here I show you
an easy way how to do this.

First we have to collect some information about that device. As we have
a USB device in this example, we get some basic information from
``lsusb``. Its output must look something like this:

``Bus 001 Device 003: ID 1111:2222 FooDev``

Now we know where in the Linux filesystem that device has been mounted:

``/dev/bus/usb/001/003``

We can use this path now to ask udev about how this device looks like
for udev:

``udevadm info -a -p $(udevadm info -q path -n /dev/bus/usb/001/003)``

Maybe you have to use ``udevinfo`` instead of ``udevadm info``. The
output should look like this:

.. code:: text

    looking at device '/devices/pci0000:00/0000:00:06.0/usb1/1-2':
        KERNEL=="1-2"
        SUBSYSTEM=="usb"
        DRIVER=="usb"
        ATTR{bDeviceSubClass}=="00"
        ATTR{bDeviceProtocol}=="00"
        ATTR{devpath}=="2"
        ATTR{idVendor}=="1111"
        ATTR{speed}=="12"
        ATTR{bNumInterfaces}==" 1"
        ATTR{bConfigurationValue}=="1"
        ATTR{bMaxPacketSize0}=="64"
        ATTR{busnum}=="1"
        ATTR{devnum}=="3"
        ATTR{configuration}==""
        ATTR{bMaxPower}=="500mA"
        ATTR{authorized}=="1"
        ATTR{bmAttributes}=="80"
        ATTR{bNumConfigurations}=="1"
        ATTR{maxchild}=="0"
        ATTR{bcdDevice}=="0106"
        ATTR{avoid_reset_quirk}=="0"
        ATTR{quirks}=="0x0"
        ATTR{serial}==" 10T7371 9028039"
        ATTR{version}==" 1.10"
        ATTR{urbnum}=="10"
        ATTR{ltm_capable}=="no"
        ATTR{manufacturer}=="Foo Inc"
        ATTR{removable}=="unknown"
        ATTR{idProduct}=="2222"
        ATTR{bDeviceClass}=="00"
        ATTR{product}=="Some FooDev"

With this information we can start writing a new udev rule. We do this
by creating a new file:

``vim /etc/udev/rules.d/10-local.rules``

For instance if we would like to give everyone in the group "users" read
and write access to the device, we put following line in that file:

``SUBSYSTEMS=="usb", ATTRS{product}=="Some FooDev", GROUP="users"``

Please note that it's ATTRS in the rules file, not ATTR.

Now we can test the new rule. For this we need the /devices/... path
from the ``udevadm info`` output from before.

``udevadm test /devices/pci0000:00/0000:00:06.0/usb1/1-2``

Like before, you might have to use ``udevtest`` instead of
``udevadm test``. The output should also contain information about the
permissions for this device:

``[...] handling device node '/dev/bus/usb/001/003', devnum=c189:2, mode=0664, uid=0, gid=100 set permissions /dev/bus/usb/001/003, 020664, uid=0, gid=100 [...]``

gid=100 is the group id of the "users" group. So this is the proof that
it works.

If your rule was not applied although it seems to be correct, chances
are good that it has been overridden by another rule. In that case use
the ":=" operator instead of "=". This tells udev not to override this
property.

.. |Udev-tux| image:: https://upload.wikimedia.org/wikipedia/de/d/da/Udev-tux.png
