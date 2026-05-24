import random
import time
import heapq
from typing import List, Tuple

# Seed the random number generator with current time to get different results
random.seed(time.time())

"""
fucntions initializeX - initialize vars 
function ServerSimulation - simple M/M/1/N simulation based on LinkdIn example given with changes for limit of 
                            queue size (N) for ex 1-3, counting wait time as total time (wait + service) and adding the service time 
                            of request that went straight to work in the stats (previously wasn't added). printing os stats
                            for ex 1 are commented out and are just returned.
Implementation of multiple server simulation will be done via the following classes:
    -SimulationEvent - representing an event object that is either "ARRIVAL" or "DEPARTURE".
    -Server - representing a server object with the following functions:
        *handle_customer_arrival - 
        *handle_customer_departure - 
        *_start_customer_service
    -MultiServerSimulation
 -                                                
"""

# Events
ARRIVAL = 1
DEPARTURE = 2


def initializeVars():
    # State variables
    current_time = 0.0
    queue = []
    server_busy = False
    event_list = []
    current_customer_arrival = None
    return current_time, queue, server_busy, event_list, current_customer_arrival


def initializeStats():
    # Statistics
    num_in_queue = 0
    total_wait_time = 0.0 # this includes service time
    num_customers_served = 0
    num_customers_dropped = 0
    return num_in_queue, total_wait_time, num_customers_served,num_customers_dropped


# def ServerSimulation(sim_num, arrival_rate, service_rate, num_requests, simulation_time):
#     num_in_queue, total_wait_time, num_customers_served,num_customers_dropped = initializeStats()
#     current_time, queue, server_busy, event_list, current_customer_arrival = initializeVars()
#     # Schedule the first arrival
#     heapq.heappush(event_list, (random.expovariate(arrival_rate), ARRIVAL))
#
#     while current_time < simulation_time:
#         event_time, event_type = heapq.heappop(event_list)
#         if event_time > simulation_time:
#             break
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
#             # Only get new event if it will start within the simulation time
#             if next_arrival <= simulation_time:
#                 heapq.heappush(event_list, (next_arrival, ARRIVAL))
#         elif event_type == DEPARTURE:
#             # Only count event handled if it ends within the simulation time
#             if current_time <= simulation_time:
#                 num_customers_served += 1
#                 # Calculate total wait time for customer departing
#                 if current_customer_arrival is not None: #UNSURE
#                     wait_time = current_time - current_customer_arrival
#                     total_wait_time += wait_time
#                 if queue:
#                     arrival_time = queue.pop(0)
#                     current_customer_arrival = arrival_time
#                     service_time = random.expovariate(service_rate)
#                     # Even if the departure ends after simulation time it will get filtered later and not counted
#                     heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
#                 else: # there are no customers waiting
#                     server_busy = False
#                     current_customer_arrival = None
#
#     # Results
#     # print(f"Simulation number: {sim_num}")
#     # print(f"Number of customers served: {num_customers_served}")
#     # print(f"Average wait time: {total_wait_time / num_customers_served if num_customers_served > 0 else 0}")
#     avg_wait_time = total_wait_time / num_customers_served if num_customers_served > 0 else 0
#     return num_customers_served, num_customers_dropped, avg_wait_time

def ServerSimulation(sim_num, arrival_rate, service_rate, num_requests, simulation_time):
    num_in_queue, total_wait_time, num_customers_served,num_customers_dropped = initializeStats()
    current_time, queue, server_busy, event_list, current_customer_arrival = initializeVars()
    # Schedule the first arrival
    heapq.heappush(event_list, (random.expovariate(arrival_rate), ARRIVAL))

    while current_time < simulation_time:
        event_time, event_type = heapq.heappop(event_list)
        current_time = event_time

        if event_type == ARRIVAL:
            if not server_busy:
                server_busy = True
                current_customer_arrival = current_time
                service_time = random.expovariate(service_rate)
                heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
            else:
                if not len(queue) == num_requests-1:
                    queue.append(current_time)
                else:
                    num_customers_dropped += 1
            next_arrival = current_time + random.expovariate(arrival_rate)
            heapq.heappush(event_list, (next_arrival, ARRIVAL))
        elif event_type == DEPARTURE:
            # Only count the events that end within the scope of the simulation - also add their wait time (wait + service)
            if current_time <= simulation_time:
                num_customers_served += 1
                # Calculate total wait time for customer departing
                if current_customer_arrival is not None: #UNSURE
                    wait_time = current_time - current_customer_arrival
                    total_wait_time += wait_time
            if queue:
                arrival_time = queue.pop(0)
                current_customer_arrival = arrival_time
                service_time = random.expovariate(service_rate)
                heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
            else: # there are no customers waiting
                server_busy = False
                current_customer_arrival = None

    # Results
    # print(f"Simulation number: {sim_num}")
    # print(f"Number of customers served: {num_customers_served}")
    # print(f"Average wait time: {total_wait_time / num_customers_served if num_customers_served > 0 else 0}")
    avg_wait_time = total_wait_time / num_customers_served if num_customers_served > 0 else 0
    return num_customers_served, num_customers_dropped, avg_wait_time


class SimulationEvent:
    """Event in discrete simulation with timing and customer data"""
    def __init__(self, scheduled_time, event_type, server_id=None, customer_arrival_time=0.0, service_duration=0.0):
        self.scheduled_time = scheduled_time
        self.event_type = event_type
        self.server_id = server_id
        self.customer_arrival_time = customer_arrival_time
        self.service_duration = service_duration

    def __lt__(self, other):
        return self.scheduled_time < other.scheduled_time

class Server:
    """Individual server with queueing and performance tracking"""
    def __init__(self, service_rate, queue_capacity, simulation_manager: 'MultiServerSimulation', server_id):
        self.service_rate = service_rate
        self.queue_capacity = queue_capacity
        self.simulation_manager = simulation_manager
        self.server_id = server_id

        # Server state
        self.waiting_customers = []  # Waiting customers (arrival times)
        self.is_serving_customer = False

        # Performance metrics
        self.customers_served = 0
        self.customers_dropped = 0
        self.total_wait_time = 0.0
        self.total_service_time = 0.0

    def handle_customer_arrival(self, arrival_event: SimulationEvent):
        """Process new customer - serve, queue, or drop based on server state"""
        if not self.is_serving_customer:
            self._start_customer_service(arrival_event.scheduled_time, arrival_event.customer_arrival_time)
        elif len(self.waiting_customers) < self.queue_capacity:
            self.waiting_customers.append(arrival_event.customer_arrival_time)
        else:
            self.customers_dropped += 1

    def handle_customer_departure(self, departure_event):
        """Process service completion and statistics update"""
        # CHECK THIS!! - CHANGED TO DISREGARD REQUESTS FINISHED AFTER SIMULATION TIME
        if departure_event.scheduled_time <= self.simulation_manager.simulation_duration:
            # Update performance counters
            self.customers_served += 1
            self.total_service_time += departure_event.service_duration

            # Calculate wait time: total_system_time - service_time
            event_system_time = departure_event.scheduled_time - departure_event.customer_arrival_time
            waiting_time = event_system_time - departure_event.service_duration
            self.total_wait_time += waiting_time

            # Update network's latest completion time
            if departure_event.scheduled_time > self.simulation_manager.simulation_end_time:
                self.simulation_manager.simulation_end_time = departure_event.scheduled_time

        # Handle next waiting customer or become idle
        if self.waiting_customers:
            next_customer_arrival = self.waiting_customers.pop(0)  # FIFO service
            # # Only schedule if arrives during simulation scope
            # if next_customer_arrival <= self.simulation_manager -
            # causes problems due to empty queue
            self._start_customer_service(departure_event.scheduled_time, next_customer_arrival)
        else:
            self.is_serving_customer = False

    def _start_customer_service(self, service_start_time, customer_arrival_time):
        """Begin serving customer and schedule their departure"""
        self.is_serving_customer = True
        service_duration = random.expovariate(self.service_rate)
        departure_time = service_start_time + service_duration
        # Create and schedule departure event
        departure_event = SimulationEvent(
            scheduled_time=departure_time,
            event_type=DEPARTURE,
            server_id=self.server_id,
            customer_arrival_time=customer_arrival_time,
            service_duration=service_duration
        )
        # Events ending after simulation scope will be filtered out in the handle_departure
        heapq.heappush(self.simulation_manager.events_queue, departure_event)


class MultiServerSimulation:
    """Multi-server network simulation with customer routing"""
    def __init__(self, queue_capacities, service_rates, routing_probabilities, arrival_rate, simulation_duration):

        # Network configuration
        self.arrival_rate = arrival_rate
        self.simulation_duration = simulation_duration
        self.routing_probabilities = routing_probabilities

        # Simulation state
        self.events_queue = []
        self.simulation_end_time = 0.0

        # Create server nodes
        self.servers = []
        self.servers = [Server(service_rates[i], queue_capacities[i], self, i) for i in range(len(queue_capacities))]

    def run_complete_simulation(self) -> Tuple[int, int, float, float, float]:
        """Execute full simulation: generate arrivals, process events, return metrics"""
        self._pre_generate_all_arrivals()
        self._process_events_chronologically()
        return self._calculate_final_statistics()

    def _pre_generate_all_arrivals(self):
        """Generate all customer arrivals before simulation starts"""
        current_time = 0.0
        while current_time < self.simulation_duration:
            # Generate inter-arrival time (exponentially distributed)
            inter_arrival_time = random.expovariate(self.arrival_rate)
            current_time += inter_arrival_time
            # Create arrival event
            arrival_event = SimulationEvent(
                scheduled_time=current_time,
                event_type=ARRIVAL,
                customer_arrival_time=current_time
            )
            heapq.heappush(self.events_queue, arrival_event)

    def _process_events_chronologically(self):
        """Process all events in time order until queue empty"""
        while self.events_queue:
            current_event = heapq.heappop(self.events_queue)

            # Skip events beyond simulation time - thanks to the pre_generate function shouldn't be events of the sort
            if current_event.scheduled_time > self.simulation_duration:
                continue

            # Route new arrivals to servers
            if current_event.event_type == ARRIVAL:
                '''
                Creates server ID's based on number of servers, uses probabilities as weights to add advantage to 
                chose a server, return a single element list of the chosen server and extracts it using [0]
                '''
                chosen_server_id = random.choices(range(len(self.servers)), weights=self.routing_probabilities, k=1)[0]
                current_event.server_id = chosen_server_id
                self.servers[chosen_server_id].handle_customer_arrival(current_event)

            # Process departures
            elif current_event.event_type == DEPARTURE:
                self.servers[current_event.server_id].handle_customer_departure(current_event)

    def _calculate_final_statistics(self) -> Tuple[int, int, float, float, float]:
        """Aggregate server statistics and compute network-wide averages"""
        # Sum across all servers
        total_customers_served = sum(server.customers_served for server in self.servers)
        total_customers_dropped = sum(server.customers_dropped for server in self.servers)
        total_wait_time = sum(server.total_wait_time for server in self.servers)
        total_service_time = sum(server.total_service_time for server in self.servers)

        # Calculate averages
        if total_customers_served > 0:
            average_wait_time = abs(total_wait_time / total_customers_served)
            average_service_time = abs(total_service_time / total_customers_served)
        else:
            average_wait_time = average_service_time = 0.0

        # Print results in original format
        print(f"\n{total_customers_served} {total_customers_dropped} {self.simulation_end_time:.4f} "
              f"{average_wait_time:.4f} {average_service_time:.4f}\n")

        return (total_customers_served, total_customers_dropped,
                average_wait_time, average_service_time, self.simulation_end_time)

