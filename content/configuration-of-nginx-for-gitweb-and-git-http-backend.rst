NGINX Configuration for Gitweb and git-http-backend
###################################################
:date: 2012-12-15 13:55
:author: Thomas Weininger
:category: Free Software
:tags: Development, Git, Linux
:slug: configuration-of-nginx-for-gitweb-and-git-http-backend

Gitweb is a nice web interface for Git repositories. For instance go
to \ http://git.kernel.org/ to see how it looks like. I find it useful
especially when I'm using the machine of somebody else and need to check out
some files from one of my own repositories. git-http-backend allows me
to clone git repositories over HTTPS so I don't have to use SSH.

First you have to prepare your repositories on your server for accessing
them via HTTPS. I would recommend to create an extra user "git" for it.
In this example I put my repositories to /home/git/repositories.
Basically you can put them where you want.

.. code:: sh

    useradd -m git
    su git
    git clone --bare /old/repo.git /home/git/repositories/repo.git
    cd /home/git/repositories/repo.git
    sudo chmod -R g+ws .    # Setting necessary rights for pushing to the repository.
    sudo chgrp -R git .

Now configure your repositories:

.. code:: sh

    git --bare update-server-info
    cp hooks/post-update.sample hooks/post-update
    chmod a+x hooks/post-update

This generates all the information that is necessary to share the
repository using a webserver like NGINX.

I found a nice tutorial about how to set up NGINX for gitweb and
git-http-backend `here`_. It almost worked out-of-the-box for me. I just
had to add following lines to fix some errors I got when I tried to work
with git-http-backend.

.. code:: text

    fastcgi_param GIT_HTTP_EXPORT_ALL "";
    fastcgi_param REMOTE_USER $remote_user;

Furthermore, I have added the auth\_basic lines to restrict the access to
my repositories. The configuration shown below has been tested with
Ubuntu 12.04.

But first make sure you have all required packages installed:

.. code:: text

    (sudo) apt-get install git gitweb fcgiwrap

Here is my NGINX configuration file for Gitweb and git-http-backend. It
allows access only using HTTPS and asks for authentication both for the
web interface and for cloning the repositories. It works basically like
the .htaccess authentication mechanism from Apache.

.. code:: text

    server {
        listen      80;
        server_name git.weinimo.de;
        access_log /var/log/nginx/git.weinimo.de.access.log;
        rewrite     ^   https://$server_name$request_uri? permanent;
    }

    # HTTPS server
    #
    server {
        listen       443;
        server_name  git.weinimo.de;
        root /usr/share/gitweb;
        access_log /var/log/nginx/git.weinimo.de.access.log;

        ssl                  on;
        ssl_certificate      /etc/ssl/certs/certforyoursite.crt;
        ssl_certificate_key  /etc/ssl/private/sitekey.pem;
        ssl_session_timeout 5m;
        ssl_protocols        TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers          HIGH:!ADH:!MD5;
        ssl_prefer_server_ciphers on;

        auth_basic           "RESTRICTED ACCESS";
        auth_basic_user_file /etc/nginx/access_list;

        # static repo files for cloning over https
        location ~ ^.*\.git/objects/([0-9a-f]+/[0-9a-f]+|pack/pack-[0-9a-f]+.(pack|idx))$ {
            root /home/git/repositories/;
        }

        # requests that need to go to git-http-backend
        location ~ ^.*\.git/(HEAD|info/refs|objects/info/.*|git-(upload|receive)-pack)$ {
            root /home/git/repositories;

            fastcgi_pass unix:/var/run/fcgiwrap.socket;
            fastcgi_param SCRIPT_FILENAME   /usr/lib/git-core/git-http-backend;
            fastcgi_param PATH_INFO         $uri;
            fastcgi_param GIT_PROJECT_ROOT  /home/git/repositories;
            fastcgi_param GIT_HTTP_EXPORT_ALL "";
            fastcgi_param REMOTE_USER $remote_user;
            include fastcgi_params;
        }

        # send anything else to gitweb if it's not a real file
        try_files $uri @gitweb;
        location @gitweb {
            fastcgi_pass unix:/var/run/fcgiwrap.socket;
            fastcgi_param SCRIPT_FILENAME   /usr/share/gitweb/gitweb.cgi;
            fastcgi_param PATH_INFO         $uri;
            fastcgi_param GITWEB_CONFIG     /etc/gitweb.conf;
            include fastcgi_params;
       }
    }


| **Update1:** I had to add the line fastcgi\_param REMOTE\_USER
| $remote\_user; to the NGINX configuration to fix the 403 errors I got
| when trying to push changes to the server. This is necessary because I
| use HTTP authentification. I also added some commands for preparing the
| repositories for git-http-backend.

| **Update2:** Added a section for setting up the repository file modes
| to prevent the "remote: error: insufficient permission for adding an
| object to repository database ./objects" error when trying to push to
| the repository.

| **Update3:** Disabled SSL and enabled TLS1.1 and TLS1.2 support.
| Thanks for your comment itefixnet.

.. _here: http://eatabrick.org/20120126_gitweb_nginx.html
