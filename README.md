# FCFS CPU Scheduling Simulator

A Python 3 Tkinter desktop application implementing non-preemptive First Come, First Served CPU scheduling.

## Requirements
- Python 3 with Tkinter (included with most Windows Python installations)
- No third-party Python packages

## Run
Open a terminal in this folder and run:

```bash
python fcfs_simulator.py
```

On systems using `python3`, use `python3 fcfs_simulator.py`.

## Usage
1. The app opens with four sample processes and computed results.
2. Enter a unique process ID, non-negative integer arrival time, and positive integer burst time; click **Add process**.
3. Select a process row to load its values for **Update selected** or **Delete selected**.
4. Click **Run FCFS** to calculate and display the Gantt chart, CT, TAT, WT, and averages.
5. **Clear all** removes all processes; **Load sample** restores the demonstration data.

## Algorithm
Processes are sorted by arrival time, preserving insertion order for ties. Each starts at `max(current_time, arrival_time)` and runs to completion. CPU idle intervals are explicitly displayed.

- CT = start + BT
- TAT = CT - AT
- WT = TAT - BT
- Average WT = sum(WT) / number of processes
- Average TAT = sum(TAT) / number of processes

## Sample results
| Process | AT | BT | Start | CT | TAT | WT |
|---|---:|---:|---:|---:|---:|---:|
| P1 | 0 | 5 | 0 | 5 | 5 | 0 |
| P2 | 1 | 3 | 5 | 8 | 7 | 4 |
| P3 | 2 | 8 | 8 | 16 | 14 | 6 |
| P4 | 3 | 2 | 16 | 18 | 15 | 13 |

Average WT: 5.75; average TAT: 10.25.

## Tests
```bash
python -m unittest -v test_fcfs.py
```

## Suggested demonstration
1. Define FCFS as non-preemptive, arrival-order scheduling.
2. Show the four sample processes and click **Run FCFS**.
3. Explain the Gantt chart and how CT, TAT, WT are computed.
4. Add P5 with AT=22 and BT=2, then run again. The chart should show CPU IDLE from 18 to 22.
5. Demonstrate input validation by attempting a negative arrival time or zero burst time.
6. Mention the convoy effect: short processes can wait behind long processes.
