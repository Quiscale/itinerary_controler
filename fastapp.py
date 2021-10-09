"""
Start this file by using `python -m uvicorn fastapp:app --no-use-colors`
"""
# #############################################################################
# Imports
# #############################################################################

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database as db
from typing import Dict

# #############################################################################
# Attributes
# #############################################################################

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=False,
                   allow_methods=["*"],
                   allow_headers=["*"])


# #############################################################################
# Paths
# #############################################################################

@app.get("/origin")
def f_origin():
    """

    :return:
    """
    with db.connect() as base:
        ans = {}

        a0 = base.origin_get("A0")[0]
        r50 = base.origin_get("R50")[0]
        ans = {
            "A0": [a0[1], a0[2]],
            "R50": [r50[1], r50[2]],
            "code": 200
        }

        return ans


@app.get("/origin/{position}")
def f_origin_pos(position: str, x: int = None, y: int = None):
    """

    :param position:
    :param x:
    :param y:
    :return:
    """
    with db.connect() as base:
        ans = {}

        if x is None or y is None:
            pos = base.origin_get(position)[0]
            ans = {
                pos[0]: [pos[1], pos[2]],
                "code": 200
            }
        else:
            base.origin_set(position, x, y)
            ans["code"] = 200

        return ans


@app.get("/category")
def f_category(add: str = None, remove: int = None) -> Dict:
    """
    Access for the control of categories

    :param add: The category to create
    :param remove: The category to remove
    :return: The list of categories
    """
    with db.connect() as base:
        ans = {}

        if add is not None:
            base.category_add(add)
            ans["added"] = add

        if remove is not None:
            base.category_remove(remove)
            ans["removed"] = remove

        rows = base.category_list()
        if len(rows) > 0:
            ans["code"] = 200
            ans["categories"] = [{"id": row[0], "name": row[1], "color": row[2]} for row in rows]
        else:
            ans["code"] = 204

        return ans


@app.get("/point/get")
def f_point_get(point: str = None, category: int = None):
    """

    :param point:
    :param category:
    :return:
    """
    with db.connect() as base:
        ans = {}
        rows = []

        if point is not None:
            rows = base.point_get(point)
        elif category is not None:
            rows = base.point_get_category(category)
        else:
            rows = base.point_get_all()

        if point is not None:
            ans["code"] = 200
            ans["point"] = {
                "id": rows[0][0],
                "category": rows[0][1],
                "x": rows[0][2],
                "y": rows[0][3]
            }
        else:
            ans["code"] = 200
            ans["points"] = [{
                "id": row[0],
                "category": row[1],
                "x": row[2],
                "y": row[3]
            } for row in rows]
            if category is not None:
                ans["category"] = {
                    "id": category,
                    "name": base.category_get(category)[0][1]
                }

        return ans


@app.get("/point/set")
def f_point_set(id: str, category: int, x: float, y: float):
    """
    Ajoute un point ou le modifie s' il existe déjà

    :param id: Point's id
    :param category: Point's category
    :param x: Y position
    :param y: X position
    :return: 200 if point updated, 201 if created
    """
    with db.connect() as base:
        ans = {}

        rows = base.point_get(id)
        if len(rows) > 0:
            base.point_update(id, category, x, y)
            ans["code"] = 200
        else:
            base.point_add(id, category, x, y)
            ans["code"] = 201

        return ans

    return {"code": 412}


@app.get("/point/remove")
def f_point_remove(id: str):
    """

    :param id:
    :return:
    """
    with db.connect() as base:
        ans = {}

        base.point_remove(id)
        ans["code"] = 200

        return ans


@app.get("/path")
def f_path(add: str = None, remove: int = None) -> Dict:
    """

    :param add:
    :param remove:
    :return:
    """
    with db.connect() as base:
        ans = {}

        if add is not None:
            base.path_add(add)
            ans["added"] = add

        if remove is not None:
            base.path_remove(remove)
            ans["removed"] = remove

        rows = base.path_list()
        if len(rows) > 0:
            ans["code"] = 200
            ans["paths"] = [{"id": row[0], "name": row[1]} for row in rows]
        else:
            ans["code"] = 204

        return ans


@app.get("/path/{path}")
def f_path_point(path: int, add: str = None, add_after: str = None, remove: str = None):
    """

    :param path: Path to interact with
    :param add: Point to add to the path
    :param add_after: Point before the Point to add
    :param remove: Point to remove
    :return:
    """
    with db.connect() as base:
        ans = {}

        if add is None and remove is None:
            path, points = base.path_get(path)

            ans["path"] = {
                "id": path[0][0],
                "name": path[0][1]
            }
            ans["points"] = {}
            for point, next, minutes in points:
                point = base.point_get(point)[0]
                ans["points"][point[0]] = {
                    "next": next,
                    "minutes": minutes,
                    "category": point[1],
                    "x": point[2],
                    "y": point[3]
                }

        if add is not None:
            base.path_point_add(id_path=path, id_point=add, id_previous=add_after)
        if remove is not None:
            base.path_point_remove(path, remove)

        ans["code"] = 200
        return ans


@app.get("/path/{path}/{point}")
def f_path_time(path: int, point: str, minutes: int = None):
    """

    :param path:
    :param point:
    :param minutes:
    :return:
    """
    with db.connect() as base:
        ans = {}

        if minutes is not None:
            base.path_point_set_time(path, point, minutes)

        point = base.path_point_get(path, point)[0]

        ans["point"] = {
            "path": point[1],
            "id": point[2],
            "next": point[3],
            "minutes": point[4]
        }
        ans["code"] = 200

        return ans


@app.get("/vehicle")
def f_vehicle(add_id: str = None, add_type: str = None, add_point: str = None, remove: int = None, path: int = None) -> Dict:
    """

    :param add_id:
    :param add_type:
    :param remove:
    :param point:
    :return:
    """
    with db.connect() as base:
        ans = {}

        if add_id is not None:
            if add_type is not None and add_point is not None:
                base.vehicle_add(add_id, add_type, add_point)
                ans["added"] = add_id
            else:
                ans["error"] = "add_type and add_point must be set if add_id is"

        if remove is not None:
            base.vehicle_remove(remove)
            ans["removed"] = remove

        rows = []
        if path is None:
            rows = base.vehicle_list()
        else:
            rows = base.vehicle_by_path(path)

        if len(rows) > 0:
            ans["code"] = 200
            ans["vehicles"] = {}
            for row in rows:
                ans["vehicles"][row[0]] = {
                    "type": row[1], "path": row[2], "point": row[3],
                    "hour_start": row[4], "hour_end": row[5],
                    "mallette": row[6], "kanban": row[7], "consommable": row[8]
                }
        else:
            ans["code"] = 204

        return ans


@app.get("/vehicle/{id}")
def f_vehicle_by_id(id: int, point: str = None, path: str = None):
    """

    :param id:
    :param point:
    :param path:
    :return:
    """
    with db.connect() as base:
        ans = {}

        if point is not None:
            base.vehicle_set_pos(id, point)
        if path is not None:
            base.vehicle_set_path(id, path)

        vehicles = base.vehicle_get(id)
        if len(vehicles) > 0:
            vehicle = vehicles[0]
            ans["vehicle"] = {
                "id": vehicle[0], "type": vehicle[1], "path": vehicle[2], "point": vehicle[3],
                "hour_start": vehicle[4], "hour_end": vehicle[5],
                "mallette": vehicle[6], "kanban": vehicle[7], "consommable": vehicle[8]
            }
            ans["code"] = 200
        else:
            ans["code"] = 400
            ans["message"] = "Id not found"

        return ans


@app.get("/vehicle/{id}/start")
def f_vehicle_start(id: int, hour_start: str, hour_end: str):
    """

    :param id:
    :param hour_start:
    :param hour_end:
    :return:
    """
    with db.connect() as base:
        ans = {}

        base.vehicle_set_hours(id, hour_start, hour_end)

        ans["code"] = 200

        return ans


@app.get("/vehicle/{id}/fill")
def f_vehicle_fill(id: int, mallette: int, kanban: int, consommable: int):
    """

    :param id:
    :param mallette:
    :param kanban:
    :param consommable:
    :return:
    """
    with db.connect() as base:
        ans = {}

        base.vehicle_set_fill(id, mallette, kanban, consommable)

        ans["code"] = 200

        return ans

if __name__ == "__main__":
    #print(f_path_time(path=13, point='MK_A3', minutes=3))
    print(f_path(remove=13))
