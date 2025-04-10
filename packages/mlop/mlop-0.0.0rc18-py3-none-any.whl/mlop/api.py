import json
import logging
import re
import signal

from .data import Histogram
from .util import clean_dict

STATUS = {
    -1: "RUNNING",
    0: "COMPLETED",
    1: "FAILED",
    signal.SIGINT.value: "TERMINATED",  # "INTERRUPTED",
}

ABBR = {
    "pct": "percentage",
    "net": "network",
    "mem": "memory",
    "recv": "received",
    "bytes_": "bytes/",
}


def make_compat_start_v1(config, settings, info):
    return json.dumps(
        {
            # "runId": settings._op_id,
            "runName": settings._op_name,
            "projectName": settings.project,
            "config": json.dumps(config) if config is not None else None,
            "loggerSettings": json.dumps(clean_dict(settings.to_dict())),
            "systemMetadata": json.dumps(info) if info is not None else None,
        }
    ).encode()


def make_compat_stop_v1(settings, trace=None):
    return json.dumps(
        {
            "runId": settings._op_id,
            "status": STATUS[settings._op_status],
            # "metadata": json.dumps(settings.meta),
            "statusMetadata": json.dumps(trace) if trace is not None else None,
        }
    ).encode()


def make_compat_meta_v1(meta, dtype, settings):
    return json.dumps(
        {
            "runId": settings._op_id,
            # "runName": settings._op_name,
            # "projectName": settings.project,
            "logType": dtype.upper() if dtype != "num" else "METRIC",
            "logName": meta,  # TODO: better aggregate
        }
    ).encode()


def make_compat_monitor_v1(data):
    if not ABBR:
        return data
    pattern = re.compile("|".join(map(re.escape, ABBR.keys())))
    return {pattern.sub(lambda m: ABBR[m.group(0)], k): v for k, v in data.items()}


def make_compat_num_v1(data, timestamp, step):
    line = [
        json.dumps(
            {
                "time": int(timestamp * 1000),  # convert to ms
                "step": int(step),
                "data": data,
            }
        )
    ]
    return ("\n".join(line) + "\n").encode("utf-8")


def make_compat_data_v1(data, timestamp, step):
    lines = []
    for k, dl in data.items():
        for d in dl:
            if isinstance(d, Histogram):
                j = d.to_dict()
                if j["shape"] == "uniform":
                    bins = {
                        "min": min(j["bins"]),
                        "max": max(j["bins"]),
                        "num": len(j["bins"]) - 1,
                    }
                    j["bins"] = bins
                c = json.dumps(j)
            else:
                c = json.dumps(d.to_dict())

            lines.append(
                json.dumps(
                    {
                        "time": int(timestamp * 1000),  # convert to ms
                        "data": c,
                        "dataType": type(d).__name__.upper(),
                        "logName": k,
                        "step": step,
                    }
                )
            )
    return ("\n".join(lines) + "\n").encode("utf-8")


def make_compat_file_v1(file, timestamp, step):
    batch = []
    for k, fl in file.items():
        for f in fl:
            i = {
                "fileName": f"{f._name}{f._ext}",
                "size": f._size,
                "fileType": f._ext[1:],
                "logName": k,
                "step": step,
            }
            batch.append(i)
    return json.dumps({"files": batch}).encode()


def make_compat_storage_v1(f, fl):
    # workaround for lack of file ident on server side
    for i in fl:
        if next(iter(i.keys())) == f"{f._name}{f._ext}":
            return next(iter(i.values()))
    return None


def make_compat_message_v1(level, message, timestamp, step):
    # TODO: server side int log level support
    line = [
        json.dumps(
            {
                "time": int(timestamp * 1000),  # convert to ms
                "message": message,
                "lineNumber": step,
                "logType": logging._levelToName.get(level),
            }
        )
    ]
    return ("\n".join(line) + "\n").encode("utf-8")
