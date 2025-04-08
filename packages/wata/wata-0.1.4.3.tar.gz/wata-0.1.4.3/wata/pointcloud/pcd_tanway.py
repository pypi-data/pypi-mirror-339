from wata.pointcloud.utils import utils
from numpy import ndarray
import numpy as np
from pathlib import Path
from typing import Union
from wata.display.utils.utils import wataprint
import json

class PointCloudTanway:

    @staticmethod
    def saveTanwayRoadPCDBinaryCompressed(points: ndarray, save_path):
        '''
        **功能描述**: 保存 BinaryCompressed pcd格式的点云,仅支持tanway 路端的数据
        
        Args:
            points: numpy格式的点云  
            save_path: pcd格式的点云文件保存的路径

        Returns:
            无  
        '''
        fields = ['x', 'y', 'z', 'intensity', 'channel', 'angle', 'echo', 'mirror', 'block', 't_sec', 't_usec', 'lidar_id']
        npdtype = ['f32', 'f32', 'f32', 'f32', 'i32','f32', 'i32', 'i32', 'i32', 'u32', 'u32', 'i32']

        utils.save_pcd(points, save_path=save_path, fields=fields, npdtype=npdtype, type='binary_compressed')


    @staticmethod
    def get_anno_from_tanway_json(json_data):
        boxes = []
        class_list = []
        for agent in json_data:
            boxes.append(
                [agent["position3d"]["x"], agent["position3d"]["y"], agent["position3d"]["z"], agent["size3d"]["x"],
                 agent["size3d"]["y"], agent["size3d"]["z"], agent["heading"]])
            class_list.append(agent["type"])
        return np.array(boxes), class_list
    

    @staticmethod
    def det_to_tanway_json(label):
        tanway_label = []
        for i in range(len(label["bbox"])):
            agent_dict = {}

            agent_dict["type"] = None if label["classname"][i] is None else "TYPE_"+label["classname"][i]

            agent_dict["position3d"] = {}
            agent_dict["position3d"]["x"] = label["bbox"][i][0]
            agent_dict["position3d"]["y"] = label["bbox"][i][1]
            agent_dict["position3d"]["z"] = label["bbox"][i][2]
            agent_dict["size3d"] = {}
            agent_dict["size3d"]["x"] = label["bbox"][i][3]
            agent_dict["size3d"]["y"] = label["bbox"][i][4]
            agent_dict["size3d"]["z"] = label["bbox"][i][5]
            agent_dict["heading"] = label["bbox"][i][6]
            agent_dict["pitch"] = 0

            if "numPoints"  in label:
                for k, numP in enumerate(label["numpoints"][i]):
                    agent_dict[f"numPoints{k}"] = numP[k]

            if "id" in label:
                agent_dict["ID"] = label["id"][i]

            agent_dict["tag"] = {}
            if "confidence" in label:
                agent_dict["tag"]["confidence"] = str(int(label["confidence"][i]))
            if "movement_state" in label:
                agent_dict["tag"]["movement_state"] = str(int(label["movement_state"][i]))

            tanway_label.append(agent_dict)

        return tanway_label

    @staticmethod
    def get_anno_from_beisai_json(label_path):

        classmap = {
            'Car': 'Car',
            'Van': 'Van',
            'Bus': 'Bus',
            'Truck': 'Truck',
            'Semitrailer': 'Semitrailer',
            'Special_vehicles': 'Special_vehicles',
            'Cycle': 'Cycle',
            'Tricyclist': 'Tricyclist',
            'Pedestrian': 'Pedestrian',
            'Vichcle': 'Car',
            'Animal': 'Animal',
            None: None
        }

        with open(label_path, 'r', encoding='UTF-8') as f:
            beisai_data = json.loads(f.read())

        bbox = []
        classname = []
        confidence_list = []
        movement_state_list = []
        id_list = []
        link_id_list = []

        for i, agent in enumerate(beisai_data[0]["objects"]):
            obj_type = None
            confidence = 3
            movement_state = 0
            link_id = None
            obj_id = None

            contour = agent["contour"]
            bbox.append([contour['center3D']['x'],
                        contour['center3D']['y'],
                        contour['center3D']['z'],
                        contour['size3D']['x'],
                        contour['size3D']['y'],
                        contour['size3D']['z'],
                        contour['rotation3D']['z']])
            assert "classValues" in agent, "classValues not in " + label_path

            for c_v in agent["classValues"]:
                if c_v["name"] == "label" or c_v["name"] in classmap:
                    obj_type = c_v["value"]
                if "name" in c_v and c_v["name"] == "confidence":
                    confidence = c_v["value"]
                if "name" in c_v and c_v["name"] == "movement_state":
                    movement_state = c_v["value"]
                if "name" in c_v and (c_v["name"] == "link_id" or c_v["name"] == "link_ID"):
                    link_id = int(c_v["value"])
                if "name" in c_v and c_v["name"] == "ID":
                    obj_id = int(c_v["value"])

            if obj_type is None and link_id is not None:
                obj_type = "Semitrailer"

            if obj_type is None:
                wataprint(f"⚠️ {label_path} 中的第{i}个框中无类别信息,请检查!", type="r")

            if obj_type is not None and obj_type not in classmap:
                wataprint(f"Error: {obj_type} not in classmap in {label_path}!", type="r")
                classname.append(obj_type)
            else:
                classname.append(classmap[obj_type])

            confidence_list.append(confidence)
            movement_state_list.append(movement_state)
            id_list.append(obj_id)
            link_id_list.append(link_id)

        assert len(bbox) == len(classname) == len(confidence_list) == len(movement_state_list) == len(id_list) == len(link_id_list)
        output = {
            "bbox": bbox,
            "classname": classname,
            "confidence": confidence_list,
            "movement_state": movement_state_list,
            "id": id_list,
            "link_id": link_id_list,
            }

        return output
