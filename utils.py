import os
import pandas as pd
import time
import multiprocessing as mp
from datetime import datetime
from loguru import logger


def sync_student(upload_page, student_page):
    col_num = len(student_page.get_row(1, include_tailing_empty=False))
    row_num = len(student_page.get_col(1, include_tailing_empty=False))
    data = student_page.get_values((2, 1), (row_num, col_num))
    upload_page.update_values(crange=(2, 1), values=data)


def sync_upload_page(df, file_box):
    df["status"] = "F"
    for student_id in df.index:
        if student_id in file_box.keys():
            df.loc[student_id, ["filename", "last time"]] = (
                file_box[student_id]["filename"],
                datetime.fromtimestamp(os.path.getmtime(file_box[student_id]["path"])) \
                        .strftime("%Y-%m-%d %H:%M:%S"),
            )
    return df


def file_delete(student_file_list, root_path):
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            temp = os.path.join(root, filename)
            if not temp in student_file_list:
                os.system(f"echo 'y' | rm -r {temp}")
                logger.info(f"delete file {temp}")


def file_manage(student_list, root_path):
    # according to student_id classification
    file_box = dict()
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            temp = filename.split("-")
            if len(temp) == 1:
                temp = (temp[0].split(".")[0] + "-1" + temp[0].split(".")[1]).split('-')

            temp[0] = temp[0].upper()
            file_box[temp[0]] = file_box.get(temp[0], {"version": list(), "path": list(), "filename": list()})
            temp[1] = int("".join(filter(str.isdigit, temp[1])))
            file_box[temp[0]]["version"].append(temp[1])
            file_box[temp[0]]["path"].append(os.path.join(root, filename))
            file_box[temp[0]]["filename"].append(filename.split(".zip")[0])

    # each student leaves a file
    for index in file_box.keys():
        # delete student_id when not exist in list
        if not index in student_list:
            del file_box[index]
        # select file max version
        pre = file_box[index]
        latest_index = pre["version"].index(max(pre["version"]))
        pre["version"] = int("".join(map(str, pre["version"][latest_index:latest_index+1])))
        pre["path"] = "".join(pre["path"][latest_index:latest_index+1])
        pre["filename"] = "".join(pre["filename"][latest_index:latest_index+1])
        logger.info(f"student: {index}, max_version: {pre['version']}, path: {pre['path']}, filename: {pre['filename']}")

    # delete unnecessary files
    file_delete([file_box[index]["path"] for index in file_box.keys()], root_path)

    return file_box


def unzip_file(student_id, file_box):
    try:
        server_file_path = f"./data/{file_box[student_id]['filename']}"
        if not os.path.isdir(server_file_path):
            os.system(f"sudo unzip {file_box[student_id]['path']} -d {server_file_path}")
            logger.info(f"success unzip {file_box[student_id]['filename']} file")
        else:
            logger.info(f"{file_box[student_id]['filename']} exist")
    except Exception as e:
        logger.error(e)


def multi_processing(file_box):
    with mp.Pool(8) as pool:
        for student_id in file_box.keys():
            pool.apply_async(
                unzip_file,
                (student_id, file_box, )
            )
        pool.close()
        pool.join()


def routine(upload_page, student_page, upload_root_path):

    sync_student(upload_page, student_page)
    logger.info("updated student ID")

    col_num = len(upload_page.get_row(1, include_tailing_empty=False))
    row_num = len(upload_page.get_col(1, include_tailing_empty=False))
    upload_df = upload_page.get_as_df(index_column=1,
                                      end=(row_num, col_num),
                                      numerize=False,
                                      include_tailing_empty=False)
    logger.info("get upload page")

    file_box = file_manage(list(upload_df.index), upload_root_path)
    logger.debug(file_box)
    upload_df = sync_upload_page(upload_df, file_box)
    logger.info("sync upload_df")

    multi_processing(file_box)
    logger.info("unzip all student file")

    upload_page.set_dataframe(upload_df, start="A2", copy_head=False, copy_index=True, nan='')
    logger.info("update upload page")

    upload_page.update_value("H3", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    logger.info("update time")

    ####################################
    # print upload_df
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(upload_df)

    # os.path.isfile(file_path)
    # os.system(f"sudo cp /data/dsai1092/upload/{student_id}.zip /home/netdb/dsai-server/data/{student_id}.zip")
    # logger.info(f"cp {student_id} file")
    # os.system(f"sudo unzip ./data/{student_id}.zip -d ./data/{student_id}/")
    # logger.info(f"unzip {student_id} file")
    # os.system(f"sudo rm ./data/{student_id}.zip")