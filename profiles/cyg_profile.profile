desc:
    Enable function entry and exit tracepoints for a -finstrument-functions compiled application
ust:
    - lttng_ust_cyg_profile*
    - lttng_ust_statedump*
preload:
    - liblttng-ust-cyg-profile.so
