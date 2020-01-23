import google.cloud.logging

client = google.cloud.logging.Client()

# Connects the logger to the root logging handler;
# by default this captures all logs at INFO level and higher
client.setup_logging()
