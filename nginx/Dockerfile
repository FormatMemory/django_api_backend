from nginx:1.15.10-alpine
MAINTAINER FormatMemory <davidthinkleding@gmail.com>

ENV TZ=${TIME_ZONE}

# Copy custom configuration file from the current directory
COPY nginx.conf /etc/nginx/nginx.conf

# RUN adduser -D user
# RUN mkdir -p /media
# RUN mkdir -p /static
# RUN chown -R user:user /static/
# RUN chown -R user:user /media/
# RUN chmod -R 755 /static/
# RUN chmod -R 755 /media/
# USER user