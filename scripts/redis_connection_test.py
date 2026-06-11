import redis

# Use your connection URL (including the /0 database index)
redis_url = "redis://localhost:6379/0"

try:
    # Connect using the URL
    client = redis.from_url(redis_url)
    
    # Send a ping command to Redis
    response = client.ping()
    
    if response:
        print("✅ Success! Connected to Redis successfully.")
except redis.exceptions.ConnectionError as e:
    print("❌ Connection Failed! Could not connect to Redis.")
    print(f"Error details: {e}")