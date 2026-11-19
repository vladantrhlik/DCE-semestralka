#!/bin/sh
set -eu

ZOO_CONF=/etc/zookeeper/zoo.cfg
ZOO_MY_ID=${ZOO_MY_ID:-1}

case "$ZOO_MY_ID" in
    ''|*[!0-9]*|0)
        echo "ZOO_MY_ID must be a positive integer" >&2
        exit 1
        ;;
esac

cat > "$ZOO_CONF" <<EOF
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/var/lib/zookeeper
clientPort=${ZOO_CLIENT_PORT:-2181}
maxClientCnxns=60
4lw.commands.whitelist=ruok,srvr
EOF

printf '%s\n' "$ZOO_MY_ID" > /var/lib/zookeeper/myid

if [ -n "${ZOO_SERVERS:-}" ]; then
    printf '%s\n' "$ZOO_SERVERS" >> "$ZOO_CONF"
fi

chown zookeeper:zookeeper "$ZOO_CONF" /var/lib/zookeeper/myid
exec su-exec zookeeper /opt/zookeeper/bin/zkServer.sh start-foreground "$ZOO_CONF"
