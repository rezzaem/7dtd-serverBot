from woocommerce import API

wcapi = API(
    url="http://teamlifo.ir",
    consumer_key="ck_52e407c4f76f5d542f856ddd93d95fd81e51023c",
    consumer_secret="cs_ab6471bfe28c378648b77491374a33c4e2027562",
    version="wc/v3"
)
order_id = 1187
new_status = "completed"

# Prepare the data payload
data = {
    "status": new_status
}

# Update the order status using the API
response = wcapi.put(f"orders/{order_id}", data)

# Print the response
print(response)