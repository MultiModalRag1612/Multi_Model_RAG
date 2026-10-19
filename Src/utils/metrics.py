from fastapi import FastAPI,Request,Response
# generate_latest ==> return the last statistics prometheus calculate (CONTENT_TYPE_LATEST)
from prometheus_client import Histogram,Counter,generate_latest,CONTENT_TYPE_LATEST
import time
from starlette.middleware.base import BaseHTTPMiddleware

#define metrics
#premotheus to collect data and grafana to visualize it 
#counter to count number of call end_point , method , post get , status ==> ['method','endpoint','status']
request_count = Counter('http_request_total','Total HTTP Requests',['method','endpoint','status'])
request_latency = Histogram('http_request_duration_seconds','HTTP Request Latency',['method','endpoint'])

class prometheusmiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        start_time = time.time()
        response = await call_next(request)
        
        #record metrics after reauest is processed

        duration = time.time()-start_time
        # get name of endpoint  /   ex/process{id}
        endpoint = request.url.path

        request_latency.labels(method=request.method , endpoint=endpoint).observe(duration)
        request_count.labels(method=request.method , endpoint=endpoint , status = response.status_code).inc()

        return response

def setup_metrics(app:FastAPI):

    # add prometheus middleware
    app.add_middleware(prometheusmiddleware)

    # include_in_schema = False  ==> dont appear in docs for security reason
    @app.get("/metrics",include_in_schema=False)
    def metrics():
        return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)