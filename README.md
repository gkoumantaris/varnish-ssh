Pack-Varnish-SSH

Configuration pack for varnish hosts based on ssh checks

This pack monitors varnish servers and displays data in webui.
I am only collecting these data:
client_conn- Client connections accepted (per second)
client_drop- Dropped client requests
client_req - Client requests received
cache_hit - Cache hits
cache_miss - Cache misses 
backend_conn - Backend connections success 
backend_unhealthy - Unhealthy backend
backend_busy - Busy backend
backend_fail - Backend connection Failures
fetch_failed - Fetch failed
n_object - Number of cached objects
n_wrk - N worker threads
n_wrk_failed -  N worker threads failed 
n_lru_nuked - Objects thrown out to make room for others

Future work :
* will add flags to be able to set the varnishstat options in the host file
* will set alerts 
