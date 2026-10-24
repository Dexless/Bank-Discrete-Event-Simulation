# Bank Efficiency: Discrete-Event Simulation

This CSCI 154 team project models customer service at a bank using Python. It explores FIFO and priority-based service policies, changes in teller availability, and variations in customer work requirements.

The goal is to investigate how queueing and resource allocation affect waiting time, customer throughput, and teller utilization.

## Project Files

- [`bank_simulation.py`](bank_simulation.py) - Original simulation code, repeated experiments, and console result summaries.
- [Project report](Bank%20Efficiency%20-%20Project%20Report.pdf) - *Who's In Charge?: A Discrete Simulation of Bank Efficiency*, including the team's methodology, recorded results, and discussion.
- [`requirements.txt`](requirements.txt) - Python dependency.

## Tools and Libraries

- Python
- NumPy
- Custom priority queue implemented with a sorted list
- Random sampling and repeated simulation experiments

## Simulation Model

Customers arrive during an eight-hour bank workday. Each request has a service demand measured in work units. Available tellers serve requests at 10 work units per hour.

The FIFO model processes customers in arrival order and assigns each customer to the earliest available teller. The priority variant divides requests into light and heavy queues and processes light requests first.

### Default Code Parameters

| Parameter | Value |
|---|---|
| Customers per day | 160 |
| Workday length | 480 minutes |
| Baseline teller windows | 10 |
| Alternative teller counts | 9 and 11 |
| Teller service rate | 10 work units per hour |
| Customer arrivals | Uniform across the workday |
| Main work-demand sampler | Normal mean 5, standard deviation 0.5, truncated to [5, 15] |
| Repeated runs | 10,000 each for FIFO and priority variants |

## Workflow

1. Generate sorted random arrival times.
2. Sample customer service demands with rejection sampling.
3. Track teller availability using a priority queue of service completion times.
4. Compute each customer's start time, completion time, and waiting time.
5. Count customers whose service completes within the workday.
6. Calculate waiting-time and utilization summaries.
7. Repeat the FIFO and priority experiments and average their metrics.
8. Print additional single-run scenarios for different teller counts and service-demand distributions.

## Scenarios Compared

| Scenario | Purpose |
|---|---|
| FIFO, 10 tellers | Baseline service model |
| Priority, 10 tellers | Explore light-request-first service |
| FIFO, 11 tellers | Explore additional capacity |
| FIFO, 9 tellers | Explore reduced capacity |
| Alternative work-demand distribution | Explore more variable service requirements |

## Evaluation Metrics

- Average waiting time in minutes
- Customers served before closing
- Customers whose service does not finish before closing
- Aggregate teller utilization percentage

In the code, average waiting time includes all scheduled customers, including those finishing after closing. Utilization counts service time only for customers completing before closing, rather than all busy time within the workday.

## Reported Results

The original report records the following results. They are historical report values, not results reproduced from the supplied script for this upload.

| Report scenario | Average wait (min) | Served | Unserved | Utilization |
|---|---:|---:|---:|---:|
| FIFO, 10 windows | 17.49 | 137 | 23 | 92.81% |
| Priority, 10 windows | 30.67 | 129 | 31 | 87.47% |
| FIFO, 11 windows | 5.40 | 146 | 14 | 89.85% |
| FIFO, 9 windows | 43.63 | 125 | 35 | 94.14% |
| Non-uniform arrivals (report label) | 228.09 | 68 | 92 | 88.85% |

The report illustrates how adding or removing teller capacity can affect waiting times and throughput. The supplied code and report describe different configurations in several places, so these values should not be treated as validated outputs of the current script.

## How to Run

1. Clone the repository and enter its directory.
2. Install the dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Run the simulation:

   ```bash
   python bank_simulation.py
   ```

The script runs 10,000 repetitions each for the FIFO and priority cases before printing additional single-run scenarios. For a quick run, lower `num_runs` in the script. Parameters are defined near the bottom of the file.

The original script does not set a random seed, so output varies between runs. For repeatable experiments, set `np.random.seed(...)` before the top-level parameter and simulation block.

## Implementation Notes and Limitations

The source is preserved as supplied for the course project. Important details when interpreting its results:

- **Priority threshold:** light requests are defined as work demand `<= 5`, while the main sampler is truncated to `[5, 15]`. Almost all sampled requests therefore enter the heavy queue, limiting the intended policy comparison.
- **Priority timing:** the priority variant processes the entire light queue before the heavy queue, rather than choosing among customers who have already arrived at each service decision. It also does not reserve a separate teller for light requests as described in the report.
- **Alternative scenario:** the code's "Non-Uniform Case" changes service demand; customer arrivals remain uniform. The report instead discusses non-uniform arrivals.
- **Report parameters:** the report describes work-demand mean 10 and standard deviation 2; the supplied code uses mean 5 and standard deviation 0.5 for its main sampler.
- **Comparison design:** repeated FIFO and priority cases draw separate random inputs. Additional teller-count scenarios are single runs, not the same repeated experiment.
- **Validation:** Python syntax and a small seeded smoke run of both simulation functions were checked. The full 10,000-run experiment and report results were not reproduced for this upload.

## Team Attribution

The accompanying report credits **Jason Avalos, Timothee Tran, Anush Nazaryan, and Margaret Mullooly**. This repository presents the bank simulation portion of that team coursework; it does not assign individual ownership of specific implementation components.
