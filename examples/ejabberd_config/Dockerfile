FROM ejabberd/ecs:20.04

COPY ejabberd.yml conf/ejabberd.yml
COPY entrypoint.sh /home/ejabberd/bin/entrypoint.sh

ENTRYPOINT ["/home/ejabberd/bin/entrypoint.sh"]