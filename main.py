from mm1_simulator import ServerSimulation, MultiServerSimulation
import sys
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt



"""
functions validate_X_X - used to validate values for different variables - used both in ex1-3 
                         but mainly usefule for ex4 
function q1 (commented out) - used for a simple simulation of a M/M/1/N for question 1 with static parameters
function q3 (commented out) - used for statistical graphs based of margin of error of 20 M/M/1/N simultions 
              for different T's - values ranging from 10 to 100 
function q4 - 
"""

CONVERGENCE_ITERATIONS = 20


def validate_positive_integer(value, name, minimum=1):
    if value < minimum:
        raise ValueError(f"The value of {name} must be at least {minimum}.")
    return value


def validate_positive_float(value, name):
    if value <= 0:
        raise ValueError(f"The {name} must be a positive float.")
    return value


def validate_positive_floats(values, name):
    if any(rate <= 0 for rate in values):
        raise ValueError(f"{name} must be positive floats.")
    return values


def validate_non_negative_integers(values, name):
    if any(n < 0 for n in values):
        raise ValueError(f"{name} must consist of non-negative integers.")
    return values


def validate_probabilities(probabilities):
    # Check if sum of probabilities is 1
    if abs(sum(probabilities) - 1.0) > 1e-10:
        raise ValueError("The probabilities must sum to 1.")
    return probabilities


def q1():
    simulation_time = validate_positive_integer(5, "simulation_duration", 1)
    num_requests = validate_positive_integer(1000, "queue_capacity", 1)
    arrival_rate = validate_positive_float(2, "arrival rate")
    service_rate = validate_positive_float(5, "service rate")

    for sim_num in range(1, 6):
        # Execute simulation with parsed parameters
        ServerSimulation(sim_num, arrival_rate, service_rate, num_requests, simulation_time)


def theoretical_values(current_duration, arrival_rate, service_rate):
    """
    Calculate theoretical values for MM1 queue
    """
    rho = arrival_rate / service_rate  # Traffic intensity

    if rho >= 1:
        raise ValueError("System is unstable: arrival rate >= service rate")

    # Average time in system including service
    avg_time_in_system = 1 / (service_rate - arrival_rate)

    # Average number of customers served per unit time using little's law as in q3.3 because system is stable
    customers_served = current_duration * arrival_rate

    return avg_time_in_system, customers_served

#
# def q3():
#     """
#     Analyze simulation convergence by testing different runtime durations
#     Creates plots showing how accuracy improves with longer simulation times
#     """
#
#     # Create figure with two subplots (one above the other)
#     fig, axes = plt.subplots(2, 1)
#
#     # Simulation parameters for convergence testing
#     num_requests = validate_positive_integer(1000, "queue_capacity", 1)
#     arrival_rate = validate_positive_float(2, "arrival rate")
#     service_rate = validate_positive_float(5, "service rate")
#
#     # Data collection arrays
#     simulation_durations = []  # x-axis: different runtime lengths tested
#     time_error_percentages = []  # y-axis: error in system time measurement
#     task_error_percentages = []  # y-axis: error in task count measurement
#
#     for current_duration in range(10, 110, 10):
#         current_duration = validate_positive_integer(current_duration, "simulation_duration", 1)
#         # Record current duration being tested
#         simulation_durations.append(current_duration)
#         theoretical_avgTime, theoretical_customersServed = theoretical_values(current_duration, arrival_rate, service_rate)
#
#         # Reset accumulators for this duration test
#         total_system_time = 0  # sum of all (wait_time + service_time)
#         total_customers_served = 0  # sum of customers served across runs
#
#         # Run multiple simulations at this duration to get reliable averages
#         for sim_num in range(CONVERGENCE_ITERATIONS):
#             # Create and run one simulation
#             customers_served, customers_dropped, average_wait_time = ServerSimulation(sim_num, arrival_rate, service_rate, num_requests, current_duration)
#
#             # Accumulate results across all iterations
#             total_customers_served += customers_served
#             total_system_time += average_wait_time  # total time customer spends in system
#
#         # Calculate error percentages for this duration
#         # DOTO - check if this calculation is correct
#         average_customers_served = total_customers_served / CONVERGENCE_ITERATIONS
#         current_task_error = abs(theoretical_customersServed - average_customers_served) / theoretical_customersServed * 100
#
#         # Time error: how close is observed system time to theoretical expectation
#         average_system_time = total_system_time / CONVERGENCE_ITERATIONS
#         current_time_error = abs(theoretical_avgTime - average_system_time) / theoretical_avgTime * 100
#
#         # Store error percentages for plotting
#         task_error_percentages.append(current_task_error)
#         time_error_percentages.append(current_time_error)
#
#     # Create convergence plots
#     # Top plot: System time error vs simulation duration
#     axes[0].plot(simulation_durations, time_error_percentages)
#     axes[0].set_ylabel("Time Error (%)")
#     axes[0].set_xlabel("Simulation Duration")
#     axes[0].set_title("System Time Error Convergence")
#     axes[0].grid()
#
#     # Bottom plot: Task count error vs simulation duration
#     axes[1].plot(simulation_durations, task_error_percentages)
#     axes[1].set_ylabel("Tasks Served Error (%)")
#     axes[1].set_xlabel("Simulation Duration")
#     axes[1].set_title("Task Count Error Convergence")
#     axes[1].grid()
#
#     # Display the plots
#     plt.tight_layout()  # Adjust spacing between subplots
#     plt.show()
#

def main():
    #q1()
    #q3()
    # Check and parse user input - min 7 for single server
    if len(sys.argv) < 7:
        raise ValueError("Insufficient parameters. Please provide valid parameters.")
    simulation_duration = validate_positive_integer(int(sys.argv[1]), "simulation_duration", 1)
    number_of_servers = validate_positive_integer(int(sys.argv[2]), "number_of_servers", 1)
    routing_probabilities = validate_probabilities([float(x) for x in sys.argv[3:3+number_of_servers]])
    arrival_rate = validate_positive_float(float(sys.argv[3+number_of_servers]), "arrival rate")
    # Server_i capacity is Q_i + 1
    queue_capacities = validate_non_negative_integers([int(x) for x in sys.argv[4+number_of_servers:4+2*number_of_servers]], "queue_capacities")
    service_rates = validate_positive_floats([float(x) for x in sys.argv[4+2*number_of_servers:4+3*number_of_servers]], "service rates")
    if not len(queue_capacities) == len(service_rates) == len(routing_probabilities) == number_of_servers:
        raise ValueError("Size of queue capacities, service rates and routing probabilities don't match up. Please provide valid parameters.")
    # Execute simulation with parsed parameters
    simulation = MultiServerSimulation(queue_capacities, service_rates, routing_probabilities, arrival_rate, simulation_duration)
    simulation.run_complete_simulation()


if __name__ == "__main__":
    main()
