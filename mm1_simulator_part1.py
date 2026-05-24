# import random
# import time
# import heapq
#
# # Seed the random number generator with current time to get different results
# random.seed(time.time())
#
# """
# fucntions initializeX - initialize vars
# function ServerSimulation - simple M/M/1/N simulation based on LinkdIn example given with changes for limit of
#                             queue size (N) for ex 1-3, counting wait time as total time (wait + service) and adding the service time
#                             of request that went straight to work in the stats (previously wasn't added). printing os stats
#                             for ex 1 are commented out and are just returned.
# function MultiServerSimulation -
# """
#
# # Events
# ARRIVAL = 1
# DEPARTURE = 2
#
#
# def initializeVars():
#     # State variables
#     current_time = 0.0
#     queue = []
#     server_busy = False
#     event_list = []
#     current_customer_arrival = None
#     return current_time, queue, server_busy, event_list, current_customer_arrival
#
#
# def initializeStats():
#     # Statistics
#     num_in_queue = 0
#     total_wait_time = 0.0 # this includes service time
#     num_customers_served = 0
#     num_customers_dropped = 0
#     return num_in_queue, total_wait_time, num_customers_served,num_customers_dropped
#
#
# def ServerSimulation(sim_num, arrival_rate, service_rate, num_requests, simulation_time):
#     num_in_queue, total_wait_time, num_customers_served,num_customers_dropped = initializeStats()
#     current_time, queue, server_busy, event_list, current_customer_arrival = initializeVars()
#     # Schedule the first arrival
#     heapq.heappush(event_list, (random.expovariate(arrival_rate), ARRIVAL))
#
#     while current_time < simulation_time:
#         event_time, event_type = heapq.heappop(event_list)
#         current_time = event_time
#
#         if event_type == ARRIVAL:
#             if not server_busy:
#                 server_busy = True
#                 current_customer_arrival = current_time
#                 service_time = random.expovariate(service_rate)
#                 heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
#             else:
#                 if not len(queue) == num_requests-1:
#                     queue.append(current_time)
#                 else:
#                     num_customers_dropped += 1
#             next_arrival = current_time + random.expovariate(arrival_rate)
#             heapq.heappush(event_list, (next_arrival, ARRIVAL))
#         elif event_type == DEPARTURE:
#             num_customers_served += 1
#             # Calculate total wait time for customer departing
#             if current_customer_arrival is not None: #UNSURE
#                 wait_time = current_time - current_customer_arrival
#                 total_wait_time += wait_time
#             if queue:
#                 arrival_time = queue.pop(0)
#                 current_customer_arrival = arrival_time
#                 service_time = random.expovariate(service_rate)
#                 heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
#             else: # there are no customers waiting
#                 server_busy = False
#                 current_customer_arrival = None
#
#     # Results
#     # print(f"Simulation number: {sim_num}")
#     # print(f"Number of customers served: {num_customers_served}")
#     # print(f"Average wait time: {total_wait_time / num_customers_served if num_customers_served > 0 else 0}")
#     avg_wait_time = total_wait_time / num_customers_served if num_customers_served > 0 else 0
#     return num_customers_served, num_customers_dropped, avg_wait_time
#
#
# def MultiServerSimulation(queue_capacities, service_rates, routing_probabilities, arrival_rate, simulation_duration)
#
