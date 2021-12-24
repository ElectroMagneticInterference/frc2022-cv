import cv2

import src.daemon
import pathlib
import src.logic as logic

from inspect import getmembers, isfunction
from json import load as jsload


def pint(*args):
    ram_check.freeze()
    print(*args)
    ram_check.unfreeze()


def init_directories(settings):
    output_dir = pathlib.Path(settings["image_out_dir"])

    # clear output directory
    [x.unlink() if x.is_file() else x.rmdir() for x in output_dir.glob("*")]

    return [
        cv2.imread(str(x))
        for x in [x for x in pathlib.Path(settings["image_in_dir"]).glob("*.*")]
    ], output_dir


def iteration(step, images):
    # didn't enumerate because I need the image to change in the array.
    for j in range(len(images)):

        if step.get("branch"):
            break

        method = logic_methods.get(step["method"])

        if not method:
            ram_check.end()
            raise Exception("Method not found! `" + step["method"] + "`")

        return method(images[j], step)


def run():

    images, output_dir = init_directories

    for i, step in enumerate(settings["steps"]):

        pint(f"\r{i}: {step}")

        iteration(step, images)

        if step.get("display"):
            for j, image in enumerate(images):
                cv2.imshow(f"Image {j} : Step {i}", image)

            if not step.get("noWait"):
                cv2.waitKey()

        if step.get("save"):
            for j, image in enumerate(images):
                cv2.imwrite(str(output_dir.joinpath(f"Image {j} Step {i}.png")), image)

        if step.get("removeWindows"):
            cv2.destroyAllWindows()


ram_check = src.daemon.ram_check()


settings = jsload(open("settings.json"))

logic_methods = dict(getmembers(logic, isfunction))

run()

ram_check.end()
cv2.destroyAllWindows()
