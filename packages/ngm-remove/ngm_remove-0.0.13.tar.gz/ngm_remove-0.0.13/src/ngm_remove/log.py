import syslog


def loginfo(msg: str):
    # Open connection to syslog
    syslog.openlog(
        ident="remove",
        logoption=syslog.LOG_PID | syslog.LOG_CONS,
        facility=syslog.LOG_USER,
    )

    # Log messages
    syslog.syslog(syslog.LOG_INFO, msg)
    # syslog.syslog(syslog.LOG_WARNING, "This is a warning message.")
    # syslog.syslog(syslog.LOG_ERR, "This is an error message.")

    # Close connection to syslog
    syslog.closelog()
