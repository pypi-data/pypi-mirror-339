import requests
import os
import json


SBS_TYPE_SINGLE = "single"
SBS_TYPE_DOUBLE = "sbs"


def create(
    name,
    first,
    second="",
    address="localhost:80",
    sorry_words=["я не могу", "извините"],
    type=SBS_TYPE_DOUBLE,
):
    """Create SBS"""
    if not "name" in first:
        print("Please, provide model names.")
        return
    if not "data" in first:
        print("Please, provide paths to the files with data.")
        return
    if not os.path.isfile(first["data"]):
        print(f"{first['data']} does not exist")
        return

    if type == SBS_TYPE_DOUBLE:
        if not "name" in second:
            print("Please, provide model names.")
            return
        if not "data" in second:
            print("Please, provide paths to the files with data.")
            return
        if not os.path.isfile(first["data"]):
            print(f"{second['data']} does not exist")
            return

    if not name:
        print("Please, provide name of the test.")
        return

    print("Validating data...")

    with open(first["data"], "r", encoding="utf-8") as file1:
        content1 = json.load(file1)

    meta_1_provided = False
    meta_2_provided = False
    raw_1_provided = False

    if "meta" in first and os.path.isfile(first["meta"]):
        meta_1_provided = True
        with open(first["meta"], "r", encoding="utf-8") as file1_meta:
            meta1 = json.load(file1_meta)
            rb_meta1 = json.dumps(meta1).encode("utf-8")

    if "raw" in first and os.path.isfile(first["raw"]):
        raw_1_provided = True
        with open(first["raw"], "r", encoding="utf-8") as file1_raw:
            raw1 = json.load(file1_raw)
            rb_raw1 = json.dumps(raw1).encode("utf-8")

    extra_data = {}

    if type == SBS_TYPE_DOUBLE:
        with open(second["data"], "r", encoding="utf-8") as file2:
            content2 = json.load(file2)

        err = validate(content1, content2)
        if err:
            print(err)
            return

        extra_data = {
            "sorry_1": get_sorry(content1, sorry_words),
            "sorry_2": get_sorry(content2, sorry_words),
            "avg_len_1": avg_len(content1),
            "avg_len_2": avg_len(content2),
        }

        if "meta" in second and os.path.isfile(second["meta"]):
            meta_2_provided = True
            # rb_meta2 = json.dumps(["{}"] * len(content2)).encode("utf-8")
            with open(second["meta"], "r", encoding="utf-8") as file2_meta:
                meta2 = json.load(file2_meta)
                rb_meta2 = json.dumps(meta2).encode("utf-8")

    print(f"Uploading data to {address}...")

    if type == SBS_TYPE_SINGLE:
        with open(first["data"], "rb") as file_1:
            data = {
                "name": name,
                "model_1": first["name"],
                "filename_1": os.path.basename(first["data"]),
                "extra_data": json.dumps(extra_data),
                "type": type,
            }
            files = {first["data"]: file_1}
            if meta_1_provided:
                data["filename_meta_1"] = os.path.basename(first["meta"])
                files[data["filename_meta_1"]] = rb_meta1
            if raw_1_provided:
                data["filename_raw_1"] = os.path.basename(first["raw"])
                files[data["filename_raw_1"]] = rb_raw1
            response = requests.post(
                f"http://{address}/sbs/create",
                data=data,
                files=files,
            )
    elif type == SBS_TYPE_DOUBLE:
        with open(first["data"], "rb") as file_1:
            with open(second["data"], "rb") as file_2:
                data = {
                    "name": name,
                    "model_1": first["name"],
                    "model_2": second["name"],
                    "filename_1": os.path.basename(first["data"]),
                    "filename_2": os.path.basename(second["data"]),
                    "extra_data": json.dumps(extra_data),
                    "type": type,
                }
                files = {first["data"]: file_1, second["data"]: file_2}
                if meta_1_provided:
                    data["filename_meta_1"] = os.path.basename(first["meta"])
                    files[data["filename_meta_1"]] = rb_meta1
                if meta_2_provided:
                    data["filename_meta_2"] = os.path.basename(second["meta"])
                    files[data["filename_meta_2"]] = rb_meta2
                response = requests.post(
                    f"http://{address}/sbs/create",
                    data=data,
                    files=files,
                )
    else:
        print("Provided type is not supported.")
        return

    try:
        res = json.loads(response.content.decode("utf-8"))
    except Exception as e:
        print("Exception occured:", str(e))
        return

    sbs_id = res["id"]

    # print(f"Done.\n\nSBS run: http://{address}/sbs/run/{sbs_id}")
    # print(f"SBS progress: http://{address}/sbs/show/{sbs_id}")

    print(f"Done.\n\nSBS run: http://{address}/data/check/{sbs_id}")
    print(f"SBS progress: http://{address}/data/show/{sbs_id}")

    return res


def avg_len(content):
    """Calculate avg lenght"""
    return round(sum(len(x[1]) for x in content) / len(content))


def info(sbs_guid, address="localhost:80"):
    """Get SBS status"""
    response = requests.get(f"http://{address}/sbs/info/{sbs_guid}")
    res = json.loads(response.content.decode("utf-8"))
    return res


def get_actions(sbs_guid, address="localhost:80"):
    """Get SBS actions history"""
    response = requests.get(f"http://{address}/sbs/history/actions/{sbs_guid}")
    res = json.loads(response.content.decode("utf-8"))
    return res


def get_comments(sbs_guid, address="localhost:80"):
    """Get SBS comments history"""
    response = requests.get(f"http://{address}/sbs/history/comments/{sbs_guid}")
    res = json.loads(response.content.decode("utf-8"))
    return res


def debug_update_db(sbs_guid, address="localhost:80"):
    """Patch SBS DB schema to the latest version"""
    response = requests.get(f"http://{address}/sbs/debug/patch/{sbs_guid}")
    return response.status_code


def debug_set_answer_counter(sbs_guid, task_id, count, address="localhost:80"):
    """Drop answer counter"""
    response = requests.get(
        f"http://{address}/sbs/debug/counter/answer/set/{sbs_guid}/{task_id}/{count}"
    )
    return response.status_code


def debug_update_sbs_state(sbs_guid, state_id, address="localhost:80"):
    """Update SBS state"""
    response = requests.get(
        f"http://{address}/sbs/debug/state/set/{sbs_guid}/{state_id}"
    )
    return response.status_code


def validate(content1, content2):
    """Validate content"""
    len1, len2 = len(content1), len(content2)
    if len1 != len2:
        return f"Provided files contain different amount of items: {len1} and {len2}."
    return ""


def get_sorry(content, sorry_words):
    """Calculate censored answers"""
    c = 0
    for x in content:
        for sorry in sorry_words:
            if sorry.lower() in x[1].lower():
                c += 1
    return c
