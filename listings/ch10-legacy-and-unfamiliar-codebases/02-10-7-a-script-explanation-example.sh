find /var/app/logs -name '*.log' -mtime +7 -print0 \
  | xargs -0 -r gzip -9              # compress logs older than 7 days
find /var/app/logs -name '*.gz' -mtime +90 -delete   # delete after 90 days
[ -s /var/run/app.pid ] && kill -HUP "$(cat /var/run/app.pid)"
# send SIGHUP so the app reopens its log files; skipped if no pid file
