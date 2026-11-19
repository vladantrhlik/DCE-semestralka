FROM alpine:3.21

ARG ZOOKEEPER_VERSION=3.9.3

RUN apk add --no-cache bash openjdk17-jre-headless su-exec wget \
    && addgroup -S zookeeper \
    && adduser -S -G zookeeper zookeeper \
    && mkdir -p /opt/zookeeper /etc/zookeeper /var/lib/zookeeper \
    && wget -q "https://archive.apache.org/dist/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz" -O /tmp/zookeeper.tar.gz \
    && tar -xzf /tmp/zookeeper.tar.gz --strip-components=1 -C /opt/zookeeper \
    && rm /tmp/zookeeper.tar.gz \
    && chown -R zookeeper:zookeeper /opt/zookeeper /etc/zookeeper /var/lib/zookeeper

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 2181 2888 3888
VOLUME ["/var/lib/zookeeper"]
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
