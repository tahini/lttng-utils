# lttng-utils
This repository contains helper scripts to record traces with LTTng for many common use cases.

### Install

To install the helper script and profiles, run the setup script

```
$ sudo python3 setup.py install
```

### Usage

To simply record a trace with common kernel events that can then be analyzed with most of the analyses in [lttng-analyses](https://github.com/lttng/lttng-analyses) or opened in [Trace Compass](http://tracecompass.org). Tracing can be stopped by pressing ctrl-c.

```
$ lttng-record-trace
```

To trace a specific application, just add the application to trace to the arguments of the commands, for example, to trace only the *ls -alt* command

```
$ lttng-record-trace ls -alt
```

More options are available for tracing. See the helper

```
$ lttng-record-trace --help
```
