# Login Log Analyser

A beginner Python project that counts failed login attempts by IP address and highlights addresses reaching a chosen threshold. It practises CSV reading, dictionaries, validation and command-line arguments.

## Run

Requires Python 3.10 or later, with no extra packages. Open a terminal in this folder:

```sh
python analyser.py sample_logins.csv
python analyser.py sample_logins.csv --threshold 4
```

On Windows, use `py` instead of `python` if needed; on macOS/Linux, try `python3`.

The first command prints:

```text
Login events: 5
Failed logins: 4
IPs with at least 3 failures across the whole file:
192.0.2.10: 3 failures
```

The second command prints `None` in the address list because no address reaches four failures.

## Input and scope

The CSV needs `timestamp`, `ip` and `status` columns. Use ISO timestamps such as `2026-10-01T09:00:00`, valid IPv4/IPv6 addresses and either `success` or `failure`. The program stops with a line number for invalid records. A header-only file is a valid empty log.

The sample is fictional and uses documentation IP addresses. This program reads local files only. Counts cover the whole file, not a rolling time window. A high failure count is a prompt for investigation, not proof of an attack. The program does not block addresses or detect every kind of suspicious activity.

## How it works

1. Read each row using `csv.DictReader`.
2. Validate the timestamp, address and status.
3. Count every event, then count failures in a dictionary keyed by IP.
4. Compare each failure count with the threshold and print matching addresses.

## Try changing it

- Add a success after three failures: should the failure count change?
- Add a summary of successful logins.
- Later, add a time-window filter rather than counting the entire file.

## Development

This initial version was generated with ChatGPT as a beginner learning project. Suggested extensions above are not implemented. Before presenting it, run it, understand each function and make your own improvements.
